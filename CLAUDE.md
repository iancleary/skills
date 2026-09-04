# CLAUDE.md

This repository contains portable agent skills.

Start by reading `AGENTS.md`. Follow it as the primary repo maintenance policy.

## Working Model

Use this repo for instruction surfaces:

- when to use a tool
- which workflow owns a task
- what safety boundary applies
- how to verify completion

Use `iancleary/forge` for executable tooling:

- Rust CLI implementations
- installers and release scripts
- Forge-managed assets
- command specs and implementation docs

This repo is the intended home for portable non-Forge-CLI workflow skills once Forge policy can install and pin it for a machine or repo. Keep Forge-coupled CLI skills in `iancleary/forge`.

Forge-specific skills such as `forge-tools` and `forge-cli` should not live here.

## Editing Skills

When editing a skill:

1. Read the whole `skills/<skill-name>/SKILL.md`.
2. Keep frontmatter to `name` and `description`.
3. Make the description a clear trigger contract.
4. Keep the body short, imperative, and verifiable.
5. Validate the skill before committing.

Use the skill validator available in your environment. For Codex's `skill-creator` skill, that is usually:

```sh
uv run <path-to-skill-creator>/scripts/quick_validate.py skills/<skill-name>
```

For repo docs-only changes, run:

```sh
git diff --check
```

Do not add private memory, account details, or local-only secrets to this public repo.

## Releases

Read `docs/release.md` before cutting a release.

Use:

```sh
uv run scripts/cut_release.py --dry-run
uv run scripts/cut_release.py
```

For ordinary release requests, follow the `cut-release` skill and do not recreate the tag/release flow by hand.
