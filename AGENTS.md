# AGENTS.md

Guidance for agents working in `iancleary/skills`.

## Purpose

This repo is a portable agent-skill distribution repo. It is not the implementation home for Forge or any other CLI.

Use this repo to preserve reusable workflow instructions. Use `iancleary/forge` for executable tools, release machinery, managed Codex assets, and implementation docs.

This repo is the intended migration home for portable non-Forge-CLI skills that do not need to ship inside Forge releases. Do not move a skill here from Forge unless the migration keeps the installed capability surface intact or the user explicitly accepts the break.

## Before Editing

- check `git status --short`
- read the skill you plan to change
- keep the change scoped to the requested skill or repo-level doc
- verify whether the behavior belongs here or in the owning tools repo
- when migrating a skill from Forge, check the Forge docs and release-skill list before removing it from Forge

## Skill Rules

- each skill lives under `skills/<skill-name>/`
- skill names use lowercase letters, digits, and hyphens
- `SKILL.md` frontmatter must contain only `name` and `description`
- frontmatter `name` must match the folder name
- the `description` must say when the skill should be used
- keep the skill body concise and procedural
- prefer command contracts, decision rules, and verification checks over generic advice
- do not add scripts, references, or assets unless the skill actually needs them

## Repository Docs

- `README.md` explains the repo to humans
- `install.md` is the prompt-style installer contract for agents
- `AGENTS.md` tells coding agents how to maintain this repo
- `CLAUDE.md` gives Claude-compatible entry guidance and should stay aligned with this file

Avoid duplicating full skill content in repo-level docs. Link to the owning skill instead.

## Validation

After changing a skill, run the skill validator available in your agent environment. For Codex's `skill-creator` skill, that is usually `quick_validate.py`:

```sh
uv run <path-to-skill-creator>/scripts/quick_validate.py skills/<skill-name>
```

For docs-only changes, run:

```sh
git diff --check
```

Before pushing, inspect the diff and make sure repo-level docs still describe the current tree.

## Safety

- do not commit secrets or account-specific setup
- do not move private notes into public skills
- do not add external writes to a skill unless the workflow requires them and the user must explicitly request them
- do not make skills depend on hidden local paths unless the path is part of the documented local environment

## Writing Style

Write for future agents. Be direct, specific, and compact.

Prefer:

- "Run `forge doctor` before using Forge-backed workflows."
- "Use `iancleary/forge` for executable tools."

Avoid:

- broad philosophy without a command or decision rule
- transcript summaries
- aspirational behavior documented as if it already exists
