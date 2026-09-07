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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("current", "next", "check"))
    args = parser.parse_args()
    if args.action == "check":
        if git("branch", "--show-current") != "main":
            raise SystemExit("release must run from main")
        if git("status", "--porcelain"):
            raise SystemExit("release requires a clean working tree")
        remote = git("ls-remote", "origin", "refs/heads/main").split()
        if not remote or git("rev-parse", "HEAD") != remote[0]:
            raise SystemExit("HEAD must match origin/main")
        return
    known = versions()
    if args.action == "current":
        print(format_version(max(known)) if known else "")
        return
    today = dt.datetime.now(dt.timezone.utc).date()
    date = (today.year, today.month, today.day)
    serial = max((v[3] for v in known if v[:3] == date), default=-1) + 1
    print(format_version((*date, serial)))


if __name__ == "__main__":
    main()
