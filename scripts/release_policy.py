#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""UTC CalVer queries and repository checks for the portable release runner."""

import argparse
import datetime as dt
import re
import subprocess


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def versions() -> list[tuple[int, int, int, int]]:
    result = []
    for tag in git("tag", "--list").splitlines():
        if re.fullmatch(r"\d{4}\.\d{2}\.\d{2}\.\d+", tag):
            parts = tuple(map(int, tag.split(".")))
            try:
                dt.date(*parts[:3])
            except ValueError:
                continue
            result.append(parts)
    return result


def format_version(value: tuple[int, int, int, int]) -> str:
    year, month, day, serial = value
    return f"{year:04d}.{month:02d}.{day:02d}.{serial}"


def validate_version(value: str) -> None:
    if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}\.(0|[1-9]\d*)", value, re.ASCII):
        raise ValueError("version must use YYYY.MM.DD.XX with a canonical daily serial")
    dt.date(*map(int, value.split(".")[:3]))


def next_version(today: dt.date | None = None) -> str:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    date = (today.year, today.month, today.day)
    serial = max((v[3] for v in versions() if v[:3] == date), default=-1) + 1
    return format_version((*date, serial))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("current", "next", "check", "validate"))
    parser.add_argument("version", nargs="?")
    args = parser.parse_args()
    if args.action == "validate":
        try:
            validate_version(args.version or "")
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        return
    if args.action == "check":
        if git("branch", "--show-current") != "main":
            raise SystemExit("release must run from main")
        if git("status", "--porcelain"):
            raise SystemExit("release requires a clean working tree")
        remote = git("ls-remote", "origin", "refs/heads/main").split()
        if not remote or git("rev-parse", "HEAD") != remote[0]:
            raise SystemExit("HEAD must match origin/main")
        return
    if args.action == "current":
        known = versions()
        print(format_version(max(known)) if known else "")
        return
    print(next_version())


if __name__ == "__main__":
    main()
