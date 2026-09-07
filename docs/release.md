# Release Process

This repository uses UTC CalVer `YYYY.MM.DD.XX`, with a daily serial starting
at zero. Tags remain the version source.

`release.toml` uses the tag-only template from `iancleary/release-skills`
v0.2.0. `scripts/release.py` is an unchanged copy of its bundled runner.
`scripts/release_policy.py` owns version inference and the requirement for a
clean main checkout matching origin/main.

Use `create-release-process` for maintenance and `release-runner` for execution.
The commands need no globally installed skills.

```sh
uv run scripts/release.py check --json
uv run scripts/release.py plan --json
uv run scripts/release.py run --dry-run --version YYYY.MM.DD.XX --json
uv run scripts/release.py run --apply --version YYYY.MM.DD.XX --json
```

Fetch origin tags before planning a real release. Plan uses local tags and the
current UTC date. Pass its next_version as the exact --version to dry-run and
apply. Do not use SemVer --bump here.

Check runs whitespace checks and plugin unit tests. Dry-run additionally
requires a clean main checkout matching the remote main branch and an available
tag. Apply requires explicit publication authorization. It creates an annotated
tag, pushes the tag, then creates the GitHub release. GitHub generates notes
unless --notes-file supplies a file inside the repository. If publication fails
after the tag push, repair the partial release explicitly; reruns reject the tag.

The previous scripts/cut_release.py remains available during this testing pass.
It uses commit-log notes and creates the tag through GitHub as its final action.
Do not alternate runners during a partial release.

Verify the contract without publishing:

```sh
uv run --python 3.11 python -B scripts/test_release_contract.py
```

This test uses a temporary checkout and local bare remote. It verifies CalVer
planning, checks, dry-run, unchanged tags and worktree, and branch rejection.

For runner updates, copy from an explicit release-skills release, update the
provenance in release.toml, inspect the diff, and rerun the consumer test.
Keep repository policy in release_policy.py.
