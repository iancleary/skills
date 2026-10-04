"""Validate curated skill packages and ownership without external dependencies."""
from pathlib import Path
import sys
import tomllib
from validate_skill import validate


def check(root):
    with (root / "curation.toml").open("rb") as stream:
        policy = tomllib.load(stream)
    if set(policy) != {"active", "retired", "moved"}:
        raise ValueError("ownership policy requires active, retired, and moved tables")
    if not isinstance(policy["moved"], dict) or policy["moved"] != {
        "cut-release": "iancleary/release-skills",
        "create-release-process": "iancleary/release-skills",
        "release-runner": "iancleary/release-skills",
    }:
        raise ValueError("moved ownership must retain release-skills package owners")
    for field in ["active", "retired"]:
        if not isinstance(policy[field], list) or not all(isinstance(x, str) for x in policy[field]):
            raise ValueError(f"{field} must be an array of strings")
    if len(policy["retired"]) != len(set(policy["retired"])):
        raise ValueError("duplicate retired name")
    if set(policy["retired"]) & set(policy["moved"]):
        raise ValueError("conflicting retired and moved ownership")
    active = policy["active"]
    if len(active) != len(set(active)):
        raise ValueError("duplicate active package")
    forbidden = set(policy["retired"]) | set(policy["moved"])
    if any(Path(path).is_absolute() or ".." in Path(path).parts for path in active):
        raise ValueError("active package paths must stay inside the owner")
    if any(Path(path).name in forbidden for path in active):
        raise ValueError("active policy conflicts with retired or moved ownership")
    names = set()
    discovered = {str(p.parent.relative_to(root)) for p in root.rglob("SKILL.md")
                  if ".git" not in p.parts}
    # Check ownership before inventory so restored packages get a precise error.
    for package in sorted(discovered):
        path = root / package
        validate(path)
        if path.name in forbidden:
            raise ValueError(f"retired or moved package cannot ship here: {path.name}")
        if path.name in names:
            raise ValueError(f"duplicate package name: {path.name}")
        names.add(path.name)
    if discovered != set(active):
        raise ValueError(f"active inventory drift: missing={sorted(set(active)-discovered)}, unexpected={sorted(discovered-set(active))}")
    print(f"curation passed: {len(discovered)} active packages")


if __name__ == "__main__":
    try:
        check(Path(__file__).resolve().parents[1])
    except (ValueError, OSError, KeyError) as exc:
        sys.exit(f"curation failed: {exc}")
