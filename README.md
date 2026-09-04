# Ian Cleary's Agent Skills

Portable skills for agent workflows that should survive outside a single repo checkout.

This repository is the instruction layer for Ian Cleary's agent tooling. It tells agents when to reach for a workflow, what command surface owns the work, and how to verify that the work is done.

The companion tools repo is [`iancleary/forge`](https://github.com/iancleary/forge). Use Forge to install, update, verify, and release the underlying toolbelt. Use this repo to install portable skill instructions.

This repo is also the intended migration home for portable non-Forge-CLI skills that were originally bundled in Forge releases. Forge should keep skills that must move with Forge binaries or Forge-managed assets; this repo should own reusable workflow skills that can be installed by policy.

## Install

For an agent-driven install, use [`install.md`](install.md).

To install directly:

```sh
npx skills add iancleary/skills
```

To install globally:

```sh
npx skills add iancleary/skills -g
```

Then verify:

```sh
npx skills list
```

The seed skills are:

- `forge-tools`: route agents to the right Forge workflow or CLI skill
- `forge-cli`: use and troubleshoot the Forge CLI itself

## Repository Shape

```text
install.md
skills/
  forge-tools/
    SKILL.md
    agents/openai.yaml
  forge-cli/
    SKILL.md
    agents/openai.yaml
```

Each skill must include a `SKILL.md` with frontmatter containing only `name` and `description`. The description is the trigger contract; write it carefully.

`agents/openai.yaml` is optional metadata for agent UIs. Keep it aligned with the skill body when a skill changes.

## What Belongs Here

Add a skill when the workflow is reusable, stable enough to document, and useful for future agents to discover automatically.

Good candidates:

- workflow routers
- CLI usage contracts
- command safety and verification rules
- stable installation or recovery playbooks
- recurring agent tasks that should not depend on memory
- portable workflow skills migrated out of Forge once `forge policy` can install and pin this repo

Poor candidates:

- one-off project notes
- private account details
- speculative workflows that have not earned a stable contract
- full tool implementations
- docs that belong in the owning code repo

## Forge Split

Use this split:

- `iancleary/forge`: tools, binaries, release scripts, managed assets, implementation docs
- `iancleary/skills`: portable instructions that teach agents when and how to use those tools

If a change requires executable code, it probably belongs in Forge. If a change teaches agents how to choose or safely use an existing tool, it probably belongs here.

Long term, Forge policy should decide whether a machine installs this repo into the user-global target, a repo-local target, or both.
