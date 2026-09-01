#!/usr/bin/env python3
"""Dependency-free data types and analysis helpers for Careful assessments."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable, Sequence


CLASSIFICATIONS = {"Verified", "Inferred", "Assumption", "Unknown"}
EVIDENCE_KINDS = {"path", "command", "test", "fixture", "review", "external"}
ASSESSMENT_STATES = {
    "satisfied",
    "needs-verification",
    "stale",
    "contradiction",
    "user-decision-needed",
    "accepted-risk",
}


@dataclass(frozen=True)
class EvidenceReference:
    kind: str
    ref: str
    observed: str | None = None
    adapter: str | None = None
    source_revision: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class EvidenceRecord:
    id: str
    claim: str
    classification: str
    evidence: list[EvidenceReference] = field(default_factory=list)
    reason: str | None = None
    scope: dict[str, Any] = field(default_factory=dict)
    links: dict[str, Any] = field(default_factory=dict)
    status: str = "current"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence"] = [item.to_dict() for item in self.evidence]
        return result


@dataclass(frozen=True)
class ImpactFinding:
    surface: str
    classification: str
    paths: list[str]
    source: str
    required: bool = False
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AssessmentFinding:
    id: str
    state: str
    material: bool
    summary: str
    consequence: str = ""
    recommended_options: list[str] = field(default_factory=list)
    unblock: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assessment_state_for(
    kind: str = "impact",
    material: bool = False,
    satisfied: bool = False,
    stale: bool = False,
    contradiction: bool = False,
    user_action: bool = False,
) -> str:
    """Select the first applicable state using conservative precedence."""
    del kind
    if satisfied:
        return "satisfied"
    if contradiction:
        return "contradiction"
    if stale:
        return "stale"
    if user_action:
        return "user-decision-needed"
    if material:
        return "needs-verification"
    return "satisfied"


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [item.strip() for item in value[1:-1].split(",") if item.strip()]
    return value.strip('"\'')


def load_project_assessment_config(path: Path) -> dict[str, Any]:
    """Parse the small, documented ``assessment:`` profile subset."""
    result: dict[str, Any] = {
        "ledger": None,
        "fail_on_unknown": False,
        "required_surfaces": [],
        "mappings": [],
        "run_checks": False,
        "checks": [],
        "stale_after_days": 90,
        "state": ".careful/assessment-state.json",
    }
    if not path.exists():
        return result

    in_assessment = False
    active_list: str | None = None
    current_mapping: dict[str, Any] | None = None
    for raw_line in path.read_text().splitlines():
        if raw_line == "assessment:":
            in_assessment = True
            continue
        if in_assessment and raw_line and not raw_line.startswith(" "):
            break
        if not in_assessment or not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        scalar = raw_line.split(":", 1) if raw_line.startswith("  ") else []
        if len(scalar) == 2 and not raw_line.startswith("    "):
            key, value = scalar
            key = key.strip()
            active_list = None
            if key in {"ledger", "fail_on_unknown", "run_checks", "stale_after_days", "state"}:
                result[key] = _parse_scalar(value)
            elif key in {"required_surfaces", "mappings", "checks"}:
                active_list = key
            continue
        if active_list == "required_surfaces" and raw_line.startswith("    - "):
            result["required_surfaces"].append(raw_line[6:].strip())
            continue
        if active_list in {"mappings", "checks"} and raw_line.startswith("    - "):
            current_mapping = {}
            result[active_list].append(current_mapping)
            item = raw_line[6:].strip()
            if ":" in item:
                key, value = item.split(":", 1)
                current_mapping[key.strip()] = _parse_scalar(value)
            continue
        if active_list in {"mappings", "checks"} and raw_line.startswith("      ") and current_mapping is not None:
            if ":" in raw_line:
                key, value = raw_line.strip().split(":", 1)
                current_mapping[key.strip()] = _parse_scalar(value)
    return result


def _record_from_dict(raw: dict[str, Any]) -> EvidenceRecord:
    evidence = [EvidenceReference(**item) for item in raw.get("evidence", [])]
    return EvidenceRecord(
        id=str(raw.get("id", "")),
        claim=str(raw.get("claim", "")),
        classification=str(raw.get("classification", "")),
        evidence=evidence,
        reason=raw.get("reason"),
        scope=raw.get("scope", {}),
        links=raw.get("links", {}),
        status=str(raw.get("status", "current")),
    )


def parse_evidence_ledger(path: Path) -> list[EvidenceRecord]:
    """Parse a JSON ledger; JSON is the dependency-free serialization of the logical record shape."""
    payload = json.loads(path.read_text())
    raw_records = payload.get("records", payload) if isinstance(payload, dict) else payload
    if not isinstance(raw_records, list):
        raise ValueError("ledger must contain a records list")
    return [_record_from_dict(item) for item in raw_records]


def validate_evidence_ledger(root: Path, ledger_path: Path | None = None) -> dict[str, Any]:
    """Validate a project-local evidence ledger without reading private context."""
    config = load_project_assessment_config(root / "careful.project.yaml")
    relative = ledger_path or config.get("ledger")
    if relative is None:
        return {"status": "pass", "records": [], "errors": [], "warnings": ["ledger is not configured"]}
    path = Path(relative)
    if not path.is_absolute():
        path = root / path
    try:
        root_resolved = root.resolve()
        path_resolved = path.resolve(strict=False)
        if root_resolved != path_resolved and root_resolved not in path_resolved.parents:
            return {"status": "fail", "records": [], "errors": ["ledger must remain inside project root"], "warnings": []}
        if ".careful" in path_resolved.relative_to(root_resolved).parts:
            return {"status": "fail", "records": [], "errors": ["ledger must not be under .careful/"], "warnings": []}
        records = parse_evidence_ledger(path)
    except FileNotFoundError:
        return {"status": "fail", "records": [], "errors": [f"missing ledger: {path.relative_to(root)}"], "warnings": []}
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return {"status": "fail", "records": [], "errors": [f"invalid ledger: {exc}"], "warnings": []}

    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        prefix = f"{record.id or '<missing>'}:"
        if not record.id:
            errors.append("<missing>: id is required")
        elif record.id in seen:
            errors.append(f"{prefix} duplicate id")
        seen.add(record.id)
        if not record.claim:
            errors.append(f"{prefix} claim is required")
        if record.classification not in CLASSIFICATIONS:
            errors.append(f"{prefix} unsupported classification: {record.classification}")
        if record.classification in {"Verified", "Inferred"} and not record.evidence:
            errors.append(f"{prefix} evidence is required for {record.classification}")
        if record.classification in {"Assumption", "Unknown"} and not record.reason:
            errors.append(f"{prefix} reason is required for {record.classification}")
        for evidence in record.evidence:
            if evidence.kind not in EVIDENCE_KINDS:
                errors.append(f"{prefix} unsupported evidence kind: {evidence.kind}")
            if not evidence.ref:
                errors.append(f"{prefix} evidence reference is empty or private")
            elif evidence.kind in {"path", "fixture", "test"}:
                reference = (root / evidence.ref).resolve(strict=False)
                if root_resolved != reference and root_resolved not in reference.parents:
                    errors.append(f"{prefix} evidence reference is outside project root")
                elif ".careful" in reference.relative_to(root_resolved).parts:
                    errors.append(f"{prefix} evidence reference is empty or private")
    return {
        "status": "fail" if errors else "pass",
        "records": [record.to_dict() for record in records],
        "errors": sorted(errors),
        "warnings": [],
    }


def collect_changed_paths(root: Path, diff_file: Path | None = None) -> tuple[list[str], list[str]]:
    """Return changed paths and input diagnostics from an explicit diff or Git."""
    if diff_file is not None:
        try:
            paths = [line.strip() for line in diff_file.read_text().splitlines() if line.strip()]
            return sorted(set(paths)), []
        except OSError as exc:
            return [], [f"diff input unavailable: {exc}"]
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"], cwd=root, text=True, capture_output=True, check=False
        )
        if diff.returncode != 0 and "not a git repository" in diff.stderr.lower():
            return [], [f"repository diff unavailable: {diff.stderr.strip()}"]
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=root, text=True, capture_output=True, check=False
        )
        if status.returncode != 0:
            return [], [f"repository diff unavailable: {status.stderr.strip()}"]
    except OSError as exc:
        return [], [f"repository diff unavailable: {exc}"]
    paths = {line.strip() for line in diff.stdout.splitlines() if line.strip()}
    for line in status.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        if path:
            paths.add(path)
    return sorted(paths), []


def _mapping(surface: str, classification: str, paths: Iterable[str], source: str, required: bool, summary: str) -> ImpactFinding:
    return ImpactFinding(surface, classification, sorted(set(paths)), source, required, summary)


def analyze_change_impact(root: Path, changed_paths: Sequence[str]) -> dict[str, Any]:
    """Map changed paths to explainable workflow surfaces."""
    config = load_project_assessment_config(root / "careful.project.yaml")
    findings: list[ImpactFinding] = []
    paths = sorted(set(changed_paths))
    for mapping in config.get("mappings", []):
        pattern = str(mapping.get("pattern", ""))
        surface = str(mapping.get("surface", ""))
        matched = [path for path in paths if pattern and (path == pattern or path.startswith(pattern.rstrip("/") + "/"))]
        if matched and surface:
            findings.append(_mapping(surface, "verified", matched, "careful.project.yaml assessment.mappings", bool(mapping.get("required")), "explicit project mapping"))

    manifest_distributions: list[tuple[str, str]] = []
    manifest = root / "core" / "adapter-manifest.yaml"
    if manifest.exists():
        current_adapter: str | None = None
        for line in manifest.read_text().splitlines():
            if line.startswith("  ") and not line.startswith("    ") and line.endswith(":"):
                current_adapter = line.strip().removesuffix(":")
            elif current_adapter and line.strip().startswith("distribution:"):
                manifest_distributions.append((line.split(":", 1)[1].strip(), current_adapter))
    authority_openspec = "spec_authority: openspec" in (root / "careful.project.yaml").read_text() if (root / "careful.project.yaml").exists() else False
    rules: list[tuple[str, str, str, bool, str, str]] = [
        ("openspec/", "durable-specification", "careful.project.yaml documentation.spec_authority", True, "OpenSpec capability or change may be affected", "verified" if authority_openspec else "inferred"),
        ("docs/superpowers/plans/", "execution-plan", "configured execution-plan convention", False, "execution plan may need linking", "verified"),
        ("fixtures/adopted-project/", "consumer-fixture", "self-hosting fixture convention", True, "consumer evidence may need updating", "verified"),
        ("README.md", "public-documentation", "configured README orientation", True, "public orientation may be affected", "verified"),
        ("docs/", "documentation", "documentation path convention", False, "documentation may be affected", "inferred"),
    ]
    for distribution, adapter in manifest_distributions:
        rules.append((distribution, f"{adapter}-adapter", f"core/adapter-manifest.yaml supported_adapters.{adapter}.distribution", True, f"{adapter} distribution may be affected", "verified"))
    for prefix, surface, source, required, summary, classification in rules:
        matched = [path for path in paths if path == prefix or path.startswith(prefix)]
        if matched:
            findings.append(_mapping(surface, classification, matched, source, required, summary))
    found_surfaces = {finding.surface for finding in findings}
    if paths:
        for surface in config.get("required_surfaces", []):
            surface = str(surface)
            if surface not in found_surfaces:
                findings.append(_mapping(surface, "unknown", [], "careful.project.yaml assessment.required_surfaces", True, "required surface has no detected impact mapping"))
    covered_paths = {path for finding in findings for path in finding.paths}
    unmatched = sorted(set(paths) - covered_paths)
    if unmatched:
        findings.append(_mapping("unknown", "unknown", unmatched, "no reliable mapping", bool(config.get("fail_on_unknown")), "changed content needs owner or project mapping"))

    unique: dict[tuple[str, tuple[str, ...]], ImpactFinding] = {}
    for finding in findings:
        unique[(finding.surface, tuple(finding.paths))] = finding
    result = sorted(unique.values(), key=lambda item: (item.surface, item.paths))
    return {
        "changed_paths": paths,
        "findings": [finding.to_dict() for finding in result],
        "errors": [],
        "warnings": [],
    }


def assess_findings(
    ledger_result: dict[str, Any],
    impact_result: dict[str, Any],
    depth: str,
    config: dict[str, Any] | None = None,
    checks: Sequence[dict[str, Any]] | None = None,
    hygiene: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Turn raw ledger and impact output into workflow actions and user flags."""
    findings: list[AssessmentFinding] = []
    config = config or {}
    cutoff = date.today() - timedelta(days=int(config.get("stale_after_days", 90)))
    claim_revisions: dict[tuple[str, str], set[str]] = {}
    for item in ledger_result.get("records", []):
        key = (str(item.get("claim", "")), json.dumps(item.get("scope", {}), sort_keys=True))
        revisions = {str(ref.get("source_revision")) for ref in item.get("evidence", []) if ref.get("source_revision")}
        if revisions:
            claim_revisions.setdefault(key, set()).update(revisions)
    if ledger_result.get("status") == "fail":
        findings.append(AssessmentFinding("ledger-validation", "needs-verification", True, "Evidence ledger validation failed.", "Consequential claims cannot be trusted.", ["repair the ledger", "remove the configured ledger and continue without it"], "Resolve ledger validation errors.", "evidence-ledger"))
    if impact_result.get("errors"):
        findings.append(AssessmentFinding("impact-input", "user-decision-needed", True, "Impact analysis input is unavailable or degraded.", "The assessment is not exhaustive.", ["provide a reliable diff or host capability", "accept the degraded assessment explicitly"], "Resolve the unavailable impact input.", "change-impact-analysis"))
    for item in ledger_result.get("records", []):
        status = str(item.get("status", "current"))
        classification = str(item.get("classification", "Unknown"))
        observed_dates = []
        for evidence in item.get("evidence", []):
            observed = evidence.get("observed")
            if observed:
                try:
                    observed_dates.append(date.fromisoformat(str(observed)))
                except ValueError:
                    pass
        if observed_dates and min(observed_dates) < cutoff:
            status = "stale"
        key = (str(item.get("claim", "")), json.dumps(item.get("scope", {}), sort_keys=True))
        if len(claim_revisions.get(key, set())) > 1:
            status = "contradiction"
        if status in {"stale", "contradiction", "accepted-risk"}:
            state = status
        elif classification in {"Unknown", "Assumption"}:
            state = "user-decision-needed"
        else:
            state = "satisfied"
        material = state != "satisfied"
        findings.append(AssessmentFinding(
            id=str(item.get("id", "ledger-record")), state=state, material=material,
            summary=str(item.get("claim", "Ledger claim requires assessment.")),
            consequence="Claim evidence is not currently sufficient for reliance." if material else "Evidence is current.",
            recommended_options=["collect current evidence", "accept the residual risk explicitly"] if material else [],
            unblock="Resolve the ledger finding or record an owner-approved residual risk." if material else "",
            source="evidence-ledger",
        ))
    for item in impact_result.get("findings", []):
        surface = str(item["surface"])
        required = bool(item.get("required"))
        unknown = item.get("classification") == "unknown"
        unknown_requires_action = unknown and (required or bool(config.get("fail_on_unknown")))
        material = required or unknown_requires_action
        passed = any(check.get("surface") == surface and check.get("status") == "passed" for check in (checks or []))
        state = "satisfied" if passed else ("user-decision-needed" if unknown_requires_action else ("needs-verification" if material else "satisfied"))
        path_digest = hashlib.sha1("\n".join(item.get("paths", [])).encode()).hexdigest()[:8]
        findings.append(AssessmentFinding(
            id=f"impact:{surface}:{path_digest}", state=state, material=material,
            summary=str(item.get("summary", surface)),
            consequence="Required follow-up is not yet evidenced." if material else "No material follow-up required.",
            recommended_options=["run the affected check", "record an evidence-backed no-impact result"] if material else [],
            unblock="Complete or explicitly resolve the affected surface." if material else "",
            source=str(item.get("source", "impact analysis")),
        ))
    for item in (hygiene or {}).get("findings", []):
        if str(item.get("severity", "minor")) not in {"important", "critical"}:
            continue
        finding_id = f"hygiene:{item.get('category', 'finding')}:{item.get('path', 'unknown')}"
        findings.append(AssessmentFinding(
            id=finding_id, state="needs-verification", material=True,
            summary=f"Structural hygiene finding at {item.get('path', 'unknown')}.",
            consequence=str(item.get("message", "Independent review is required.")),
            recommended_options=["correct the finding", "accept the residual risk explicitly"],
            unblock="Resolve or explicitly review the hygiene finding.", source="codebase-hygiene",
        ))
    if depth == "quick":
        findings = [finding for finding in findings if finding.material]
    flags = prioritize_user_flags(findings)
    states = {finding.state for finding in findings}
    route = "continue"
    if "contradiction" in states or ("needs-verification" in states and depth == "deep"):
        route = "block-until-verified"
    elif states.intersection({"needs-verification", "stale", "user-decision-needed"}):
        route = "escalate-or-verify"
    return {
        "depth": depth,
        "route": route,
        "findings": [finding.to_dict() for finding in findings],
        "user_flags": flags,
        "handoff": [finding.to_dict() for finding in findings if finding.state != "satisfied"],
    }


def prioritize_user_flags(findings: Sequence[AssessmentFinding]) -> list[dict[str, Any]]:
    order = {"contradiction": 0, "user-decision-needed": 1, "stale": 2, "needs-verification": 3, "accepted-risk": 4, "satisfied": 5}
    selected = [
        finding for finding in findings
        if finding.material and finding.state in {"contradiction", "user-decision-needed", "stale", "accepted-risk"}
    ]
    selected.sort(key=lambda finding: (order.get(finding.state, 99), finding.id))
    return [finding.to_dict() for finding in selected]


def run_configured_checks(root: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    """Run explicitly enabled project checks without shell evaluation."""
    if not config.get("run_checks"):
        return []
    results = []
    for item in config.get("checks", []):
        surface = str(item.get("surface", ""))
        command = str(item.get("command", ""))
        if not surface or not command:
            results.append({"surface": surface, "command": command, "status": "invalid"})
            continue
        try:
            completed = subprocess.run(
                shlex.split(command), cwd=root, text=True, capture_output=True, check=False, timeout=120
            )
            results.append({"surface": surface, "command": command, "status": "passed" if completed.returncode == 0 else "failed", "exit_code": completed.returncode, "output": (completed.stdout + completed.stderr)[-4000:]})
        except (OSError, subprocess.SubprocessError) as exc:
            results.append({"surface": surface, "command": command, "status": "unavailable", "output": str(exc)})
    return sorted(results, key=lambda item: (item["surface"], item["command"]))


def run_assessment(root: Path, depth: str, changed_paths: Sequence[str] | None = None) -> dict[str, Any]:
    config = load_project_assessment_config(root / "careful.project.yaml")
    ledger_result = validate_evidence_ledger(root)
    path_errors: list[str] = []
    if changed_paths is not None:
        paths = list(changed_paths)
    else:
        paths, path_errors = collect_changed_paths(root)
    impact_result = analyze_change_impact(root, paths)
    impact_result["errors"].extend(path_errors)
    try:
        from .review_codebase_hygiene import review_codebase_hygiene
    except ImportError:
        from review_codebase_hygiene import review_codebase_hygiene
    hygiene_result = review_codebase_hygiene(root)
    checks = run_configured_checks(root, config)
    result = assess_findings(ledger_result, impact_result, depth, config, checks, hygiene_result)
    result["ledger"] = ledger_result
    result["impact"] = impact_result
    result["hygiene"] = hygiene_result
    result["config"] = config
    result["checks"] = checks
    state_path = Path(str(config.get("state", ".careful/assessment-state.json")))
    if not state_path.is_absolute():
        state_path = root / state_path
    try:
        state_resolved = state_path.resolve(strict=False)
        root_resolved = root.resolve()
        if root_resolved == state_resolved or root_resolved in state_resolved.parents:
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps({"depth": depth, "route": result["route"], "findings": result["findings"], "user_flags": result["user_flags"], "checks": checks}, indent=2, sort_keys=True) + "\n")
        else:
            result.setdefault("warnings", []).append("assessment state path is outside project root and was not written")
    except OSError as exc:
        result.setdefault("warnings", []).append(f"assessment state unavailable: {exc}")
    return result
