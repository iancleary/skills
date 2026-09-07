# Release Process

This repository uses UTC CalVer `YYYY.MM.DD.XX`, with a daily serial starting
at zero. Tags remain the version source.

`release.toml` uses the tag-only template from `iancleary/release-skills`.
Its runner_source table pins the exact source commit and SHA-256 included in
`release-skills v1.0.0`. `scripts/release.py` is an unchanged copy of that
release's bundled runner.
`scripts/release_policy.py` owns version inference and the requirement for a
clean main checkout matching origin/main.

Use `create-release-process` for maintenance and `release-runner` for execution.
The commands need no globally installed skills.

```sh
uv run scripts/release.py check --json
uv run scripts/release.py plan --json
uv run scripts/release.py run --dry-run --version YYYY.MM.DD.XX --expected-head COMMIT --expected-config SHA256 --json
uv run scripts/release.py run --apply --version YYYY.MM.DD.XX --expected-head COMMIT --expected-config SHA256 --json
```

Fetch origin tags before planning a real release. Plan uses local tags and the
current UTC date. Pass its version, target_commit, and config_sha256 as the
exact --version, --expected-head and --expected-config to dry-run and apply.
Do not use SemVer --bump here. Explicit versions are validated for the required
format, real calendar date and canonical daily serial before execution.

Plan describes intent and reports ready=null. Check runs the checks declared in
TOML: a clean main checkout matching origin/main, whitespace validation and
plugin tests. Run enforces those same checks through prepared-v1 before tagging;
there is no separate duplicate check list. Dry-run also checks tag availability.
Apply requires explicit publication authorization. It creates an annotated
tag, pushes the tag, then creates the GitHub release. GitHub generates notes
unless --notes-file supplies a file inside the repository. If publication fails
after the tag push, use the explicit recovery procedure below.

The old cut_release.py implementation has been removed. Git history retains it.
The shared runner is the only publication entrypoint.

For a failed GitHub publication with an existing remote tag, inspect its commit
and rerun with --resume, the original --version and --expected-head TAG_COMMIT.
Dry-run first, then explicitly apply. Resume verifies the tag, reruns checks and
completes publication without moving tags. An already published release is a
no-op. Missing or conflicting remote tags require manual inspection.

Verify the contract without publishing:

```sh
uv run --python 3.11 python -B scripts/test_release_contract.py
```

This test uses a temporary checkout and local bare remote. It verifies CalVer
format/date validation, serial rollover, planning, enforced checks, guarded
dry-run, unchanged tags and worktree, and branch rejection.

For runner updates, copy from an explicit release-skills release, update the
provenance in release.toml, inspect the diff, and rerun the consumer test.
Each config load checks the runner checksum, so changing only the vendored
script fails verification. The checksum detects drift; it is not a signature.
Keep repository policy in release_policy.py.
