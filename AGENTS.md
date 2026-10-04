# AGENTS.md

Guidance for agents working in `iancleary/skills`.

## Purpose

This repo distributes portable agent skills and small plugins that make those
skills enforceable. It is not the implementation home for a general-purpose CLI.

Use this repo to preserve reusable workflow instructions. A skill or plugin can
include a small executable helper when the helper is inseparable from that
workflow and has no useful standalone command surface. General-purpose tools,
release machinery, and their implementation docs belong in their owning repos.

## Before Editing

- check `git status --short`
- read the skill you plan to change
- read `docs/release.md` before cutting or changing releases
- keep the change scoped to the requested skill or repo-level doc
- verify whether the behavior belongs here or in the owning tools repo
- when retiring or moving a skill, preserve the installed capability or document the accepted break

## Skill Rules

- each skill lives under `skills/<skill-name>/`
- skill names use lowercase letters, digits, and hyphens
- `SKILL.md` frontmatter must contain only `name` and `description`
- frontmatter `name` must match the folder name
- the `description` must say when the skill should be used
- keep the skill body concise and procedural
- prefer command contracts, decision rules, and verification checks over generic advice
- do not add scripts, references, or assets unless the skill or plugin actually needs them
- keep automatic triggers narrow; explicit-request workflows may set
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml`
- when retiring a skill, remove active references and document installed-copy
  migration; baseline routing managed in another repo must be updated there

For retired skills and preserved baseline guidance, see
[`docs/skill-retirement.md`](docs/skill-retirement.md).

## Repository Docs

- `README.md` explains the repo to humans
- `install.md` is the prompt-style installer contract for agents
- `AGENTS.md` tells coding agents how to maintain this repo
- `CLAUDE.md` gives Claude-compatible entry guidance and should stay aligned with this file

Avoid duplicating full skill content in repo-level docs. Link to the owning skill instead.

## Validation

Run `just check` after package, plugin, or curation changes. The aggregate gate
validates every active package against `curation.toml`, rejects retired or moved
names and duplicates, and runs negative fixtures and plugin tests. The release
contract invokes the same gate. Change curation policy deliberately when adding
or moving a package. See `docs/curation.md`.

Repository Python tasks use `uv run --no-project --managed-python --python 3.11 python`.
Do not replace managed execution with ambient `python3`. Preserve positional
argument forwarding through `"$@"` in task recipes.

## Releases

Use the repo-local release runner:

```sh
uv run --no-project --managed-python --python 3.11 scripts/release.py check --json
uv run --no-project --managed-python --python 3.11 scripts/release.py plan --json
uv run --no-project --managed-python --python 3.11 scripts/release.py run --dry-run --version YYYY.MM.DD.XX --expected-head COMMIT --expected-config SHA256 --json
uv run --no-project --managed-python --python 3.11 scripts/release.py run --apply --version YYYY.MM.DD.XX --expected-head COMMIT --expected-config SHA256 --json
```

For ordinary release requests, use `release-runner` from `iancleary/release-skills` and the checked-in contract. Use `create-release-process` for maintenance. Versions use UTC `YYYY.MM.DD.XX`, where `XX` starts at `0` each day. Read `docs/release.md` for version selection and runner provenance.

## Safety

- do not commit secrets or account-specific setup
- do not move private notes into public skills
- do not add external writes to a skill unless the workflow requires them and the user must explicitly request them
- do not make skills depend on hidden local paths unless the path is part of the documented local environment

## Writing Style

Write for future agents. Be direct, specific, and compact.

Prefer:

- "Use `api-and-interface-design` before changing a stable CLI contract."
- "Use the owning tools repo for a reusable executable command."

Avoid:

- broad philosophy without a command or decision rule
- transcript summaries
- aspirational behavior documented as if it already exists
