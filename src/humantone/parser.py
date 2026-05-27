import json
import re
from pathlib import Path
from typing import Any


def _mini_yaml_load(text: str) -> dict[str, Any]:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith('#')]
    out: dict[str, Any] = {}
    rules: list[dict[str, Any]] = []
    out["rules"] = rules
    current = None
    for ln in lines:
        if ln.startswith("name:"):
            out["name"] = ln.split(":", 1)[1].strip()
        elif ln.startswith("rules:"):
            continue
        elif ln.strip().startswith("- rule_id:"):
            rid = ln.split(":", 1)[1].strip()
            current = {"rule_id": rid}
            rules.append(current)
        elif current is not None and ":" in ln:
            key, val = [x.strip() for x in ln.split(":", 1)]
            key = key.lstrip("-").strip()
            if val.startswith("[") and val.endswith("]"):
                current[key] = [v.strip() for v in val[1:-1].split(",") if v.strip()]
            else:
                current[key] = re.sub(r'^"|"$', '', val)
    return out


def _load_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yml", ".yaml"}:
        return _mini_yaml_load(text)
    raise ValueError(f"Unsupported file type: {path}")


def load_rulepack(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    data = _load_data(p)
    if not isinstance(data, dict) or "rules" not in data:
        raise ValueError(f"Invalid rulepack format in {p}")
    for i, rule in enumerate(data["rules"]):
        missing = [k for k in ["rule_id", "pattern", "severity", "domain_applicability", "rewrite_hint"] if k not in rule]
        if missing:
            raise ValueError(f"Rule {i} in {p} missing fields: {missing}")
    return data


def load_rulepacks(directory: str | Path) -> list[dict[str, Any]]:
    d = Path(directory)
    packs = []
    for p in sorted(d.glob("*")):
        if p.suffix.lower() in {".yml", ".yaml", ".json"}:
            packs.append(load_rulepack(p))
    return packs
