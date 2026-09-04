# Release Process

`iancleary/skills` uses UTC calendar release versions:

```text
YYYY.MM.DD.XX
```

`XX` starts at `0` for the first release on a UTC day and increments by one for additional releases on the same day.

Examples:

- `2026.09.04.0`
- `2026.09.04.1`
- `2026.09.05.0`

## Runner

Use the checked-in Python runner through `uv`:

```sh
uv run scripts/cut_release.py --dry-run
uv run scripts/cut_release.py
```

Read-only version queries:

```sh
uv run scripts/cut_release.py --print-current-version
uv run scripts/cut_release.py --print-next-version
```

Cut a specific version:

```sh
uv run scripts/cut_release.py --version 2026.09.04.0
```

Use explicit release notes:

```sh
uv run scripts/cut_release.py --notes-file release-notes.md
```

When `--notes-file` is omitted, the runner generates notes from non-merge git commits since the latest calendar release tag.

## Release Gate

Before creating a GitHub release, the runner checks:

- working tree is clean
- current branch is `main`
- `HEAD` matches `origin/main`
- target tag does not already exist
- target GitHub release does not already exist

The runner creates the GitHub release with `gh release create`. The tag and release are created together as the final public action.

## Agent Workflow

For ordinary release requests, use the `cut-release` skill and this runner.

Expected flow:

```sh
git status --short --branch
uv run scripts/cut_release.py --print-next-version
uv run scripts/cut_release.py --dry-run
uv run scripts/cut_release.py
```

Do not reconstruct the release by hand unless repairing a failed or partial release.
