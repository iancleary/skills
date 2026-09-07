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
DEFAULT_CODEX_CONFIG = Path.home() / ".codex" / "config.toml"
BLOCK_START = "# BEGIN bulk-read-routing agent roles"
BLOCK_END = "# END bulk-read-routing agent roles"
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


def registration_block(rendered: list[tuple[str, str]], roles: list[dict[str, Any]], codex_config: Path, output_dir: Path) -> str:
    lines = [BLOCK_START]
    for (name, _), role in zip(rendered, roles):
        description = required_string(role, "description")
        target = output_dir / f"{name}.toml"
        try:
            config_path = f"./{target.relative_to(codex_config.parent)}"
        except ValueError:
            config_path = str(target)
        lines.extend(
            [
                f"[agents.{name}]",
                f"description = {json.dumps(description)}",
                f"config_file = {json.dumps(config_path)}",
                "",
            ]
        )
    lines.append(BLOCK_END)
    return "\n".join(lines) + "\n"


def updated_registration(codex_config: Path, block: str, role_names: list[str]) -> str:
    existing = codex_config.read_text(encoding="utf-8") if codex_config.exists() else ""
    if BLOCK_START in existing or BLOCK_END in existing:
        if existing.count(BLOCK_START) != 1 or existing.count(BLOCK_END) != 1:
            raise ValueError(f"invalid managed role block in {codex_config}")
        start = existing.index(BLOCK_START)
        end = existing.index(BLOCK_END, start) + len(BLOCK_END)
        updated = existing[:start] + block.rstrip() + existing[end:]
    else:
        for name in role_names:
            if re.search(rf"(?m)^\[agents\.{re.escape(name)}\]\s*$", existing):
                raise ValueError(f"refusing to replace unmanaged agent registration: {name}")
        separator = "" if not existing or existing.endswith("\n\n") else "\n"
        updated = existing + separator + block
    return updated


def install(config: Path, output_dir: Path, codex_config: Path, force: bool) -> list[Path]:
    roles = load_roles(config)
    rendered = [render_role(role) for role in roles]
    for name, content in rendered:
        target = output_dir / f"{name}.toml"
        if target.exists() and target.read_text(encoding="utf-8") != content and not force:
            raise ValueError(f"refusing to overwrite different agent role: {target}")
    block = registration_block(rendered, roles, codex_config, output_dir)
    registration = updated_registration(
        codex_config, block, [name for name, _ in rendered]
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    installed: list[Path] = []
    for name, content in rendered:
        target = output_dir / f"{name}.toml"
        target.write_text(content, encoding="utf-8")
        installed.append(target)
    codex_config.parent.mkdir(parents=True, exist_ok=True)
    codex_config.write_text(registration, encoding="utf-8")
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--codex-config", type=Path, default=DEFAULT_CODEX_CONFIG)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        installed = install(args.config, args.output_dir, args.codex_config, args.force)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    for path in installed:
        print(f"installed agent role: {path}")
    print(f"registered agent roles: {args.codex_config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
