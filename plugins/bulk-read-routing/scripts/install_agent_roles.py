#!/usr/bin/env python3
"""Install configured bulk-read agent roles into the personal Codex layer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "agent-roles.json"
DEFAULT_OUTPUT_DIR = Path.home() / ".codex" / "agents"
NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")
REASONING_EFFORTS = {"minimal", "low", "medium", "high", "xhigh", "max", "ultra"}
SERVICE_TIERS = {"default", "fast"}
INSTRUCTIONS = """Stay in read-only exploration mode.
Answer only the delegated question.
Use targeted searches and bounded reads.
Return concise findings with file and line references.
Do not edit files or make product, security, or privacy decisions.
"""


def load_roles(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read role config {path}: {error}") from error
    roles = data.get("roles") if isinstance(data, dict) else None
    if not isinstance(roles, list) or not roles:
        raise ValueError("role config must contain a non-empty roles array")
    return roles


def required_string(role: dict[str, Any], key: str) -> str:
    value = role.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"role field {key} must be a non-empty string")
    return value


def render_role(role: dict[str, Any]) -> tuple[str, str]:
    name = required_string(role, "name")
    description = required_string(role, "description")
    model = required_string(role, "model")
    effort = required_string(role, "modelReasoningEffort")
    service_tier = required_string(role, "serviceTier")
    if not NAME_RE.fullmatch(name):
        raise ValueError(f"invalid role name: {name}")
    if effort not in REASONING_EFFORTS:
        raise ValueError(f"unsupported reasoning effort for {name}: {effort}")
    if service_tier not in SERVICE_TIERS:
        raise ValueError(f"unsupported service tier for {name}: {service_tier}")

    lines = [
        f"name = {json.dumps(name)}",
        f"description = {json.dumps(description)}",
        f"model = {json.dumps(model)}",
        f"model_reasoning_effort = {json.dumps(effort)}",
    ]
    if service_tier == "fast":
        lines.append('service_tier = "fast"')
    lines.extend(
        [
            'sandbox_mode = "read-only"',
            'developer_instructions = """',
            INSTRUCTIONS.rstrip(),
            '"""',
            "",
        ]
    )
    return name, "\n".join(lines)


def install(config: Path, output_dir: Path, force: bool) -> list[Path]:
    rendered = [render_role(role) for role in load_roles(config)]
    output_dir.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for name, content in rendered:
        target = output_dir / f"{name}.toml"
        if target.exists() and target.read_text(encoding="utf-8") != content and not force:
            raise ValueError(f"refusing to overwrite different agent role: {target}")
        target.write_text(content, encoding="utf-8")
        installed.append(target)
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        installed = install(args.config, args.output_dir, args.force)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    for path in installed:
        print(f"installed agent role: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
