#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Cut a calendar-versioned GitHub release for iancleary/skills."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
import tempfile
from pathlib import Path


VERSION_RE = re.compile(r"^(?P<year>\d{4})\.(?P<month>\d{2})\.(?P<day>\d{2})\.(?P<serial>\d+)$")
REPO = "iancleary/skills"


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=check, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], check=check)


def gh(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["gh", *args], check=check)


def stdout(args: list[str]) -> str:
    return run(args).stdout.strip()


def git_stdout(args: list[str]) -> str:
    return git(args).stdout.strip()


def valid_version(value: str) -> str:
    if not VERSION_RE.match(value):
        raise argparse.ArgumentTypeError("version must match YYYY.MM.DD.XX")
    return value


def release_versions() -> list[str]:
    tags = git(["tag", "--list", "[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9].*"]).stdout.splitlines()
    return [tag for tag in tags if VERSION_RE.match(tag)]


def sort_key(version: str) -> tuple[int, int, int, int]:
    match = VERSION_RE.match(version)
    if match is None:
        raise ValueError(f"invalid version: {version}")
    return (
        int(match.group("year")),
        int(match.group("month")),
        int(match.group("day")),
        int(match.group("serial")),
    )


def current_version() -> str | None:
    versions = release_versions()
    if not versions:
        return None
    return max(versions, key=sort_key)


def next_version(today: dt.date | None = None) -> str:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    prefix = f"{today.year:04d}.{today.month:02d}.{today.day:02d}."
    serials = [
        sort_key(version)[3]
        for version in release_versions()
        if version.startswith(prefix)
    ]
    serial = max(serials) + 1 if serials else 0
    return f"{prefix}{serial}"


def ensure_clean_tree() -> None:
    dirty = git_stdout(["status", "--porcelain"])
    if dirty:
        raise SystemExit(f"working tree is not clean:\n{dirty}")


def ensure_main_matches_origin() -> None:
    branch = git_stdout(["rev-parse", "--abbrev-ref", "HEAD"])
    if branch != "main":
        raise SystemExit(f"release must run from main, not {branch}")

    git(["fetch", "origin", "main", "--tags"])
    head = git_stdout(["rev-parse", "HEAD"])
    origin = git_stdout(["rev-parse", "origin/main"])
    if head != origin:
        raise SystemExit("HEAD does not match origin/main; push or pull before releasing")


def ensure_tag_available(version: str) -> None:
    tag_check = git(["rev-parse", "--verify", f"refs/tags/{version}"], check=False)
    if tag_check.returncode == 0:
        release_check = gh(["release", "view", version, "--repo", REPO], check=False)
        if release_check.returncode == 0:
            raise SystemExit(f"release {version} already exists")
        raise SystemExit(f"tag {version} already exists but GitHub release is missing; repair manually")

    release_check = gh(["release", "view", version, "--repo", REPO], check=False)
    if release_check.returncode == 0:
        raise SystemExit(f"GitHub release {version} already exists")


def latest_prior_tag(version: str) -> str | None:
    prior = [candidate for candidate in release_versions() if sort_key(candidate) < sort_key(version)]
    if not prior:
        return None
    return max(prior, key=sort_key)


def generated_notes(version: str) -> str:
    prior = latest_prior_tag(version)
    if prior:
        range_spec = f"{prior}..HEAD"
        heading = f"Changes since {prior}"
    else:
        range_spec = "HEAD"
        heading = "Changes"

    log = git(["log", "--no-merges", "--pretty=format:- %s (%h)", range_spec]).stdout.strip()
    if not log:
        log = "- No commits since the previous release."

    return f"# {version}\n\n{heading}:\n\n{log}\n"


def notes_for(version: str, notes_file: Path | None) -> str:
    if notes_file is None:
        return generated_notes(version)
    return notes_file.read_text(encoding="utf-8")


def dry_run(version: str, notes_file: Path | None) -> None:
    print(f"repo: {REPO}")
    print(f"version: {version}")
    print(f"target: {git_stdout(['rev-parse', 'HEAD'])}")
    print(f"current_version: {current_version() or 'none'}")
    print("release_notes:")
    print(notes_for(version, notes_file).rstrip())
    print("would run:")
    print(f"gh release create {version} --repo {REPO} --target HEAD --title 'Release {version}' --notes-file <generated>")


def create_release(version: str, notes_file: Path | None) -> None:
    ensure_clean_tree()
    ensure_main_matches_origin()
    ensure_tag_available(version)

    notes = notes_for(version, notes_file)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(notes)
        temp_notes = Path(handle.name)

    try:
        gh([
            "release",
            "create",
            version,
            "--repo",
            REPO,
            "--target",
            "HEAD",
            "--title",
            f"Release {version}",
            "--notes-file",
            str(temp_notes),
        ])
    finally:
        temp_notes.unlink(missing_ok=True)

    release_url = gh(["release", "view", version, "--repo", REPO, "--json", "url", "--jq", ".url"]).stdout.strip()
    print(f"released {version}: {release_url}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", type=valid_version, help="Release version; defaults to the next UTC YYYY.MM.DD.XX version")
    parser.add_argument("--notes-file", type=Path, help="Markdown release notes file; generated from git log when omitted")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned release without creating it")
    parser.add_argument("--print-current-version", action="store_true", help="Print the latest calendar release tag and exit")
    parser.add_argument("--print-next-version", action="store_true", help="Print the inferred next UTC calendar release and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.print_current_version:
        print(current_version() or "")
        return 0

    if args.print_next_version:
        print(next_version())
        return 0

    version = args.version or next_version()
    if args.dry_run:
        dry_run(version, args.notes_file)
    else:
        create_release(version, args.notes_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
