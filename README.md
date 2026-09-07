# Ian Cleary's Agent Skills

Portable skills for agent workflows that should survive outside a single repo checkout.

This repository is the portable workflow layer for Ian Cleary's agent tooling.
It tells agents when to reach for a workflow, what command surface owns the
work, and how to verify that the work is done. Small plugins can live here when
they make one workflow enforceable without creating a reusable CLI.

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

From a clone of this repository, the equivalent command is:

```sh
just install-skills
```

Then verify:

```sh
npx skills list
```

## Plugins

The repository also provides Codex plugins for workflows that require lifecycle
hooks. Add its marketplace and install the bulk-read router with:

```sh
codex plugin marketplace add iancleary/skills
codex plugin add bulk-read-routing@iancleary-skills
```

From a clone of this repository, use the idempotent recipe:

```sh
just install-plugin
```

The recipe adds the marketplace when it is missing and refreshes it when it is
already configured before installing the plugin.

Install the supplied personal delegation roles with:

```sh
just install-agent-roles
```

Configure model, `modelReasoningEffort`, and `serviceTier` (`default` or `fast`)
in `plugins/bulk-read-routing/config/agent-roles.json` before installation. The
installer creates `~/.codex/agents/bulk_reader.toml` and
`~/.codex/agents/bulk_reader_fast.toml` and registers both roles in a managed
block in `~/.codex/config.toml`. It leaves `service_tier` unset for the default
role and writes `service_tier = "fast"` for the fast role.

Run the opt-in live delegation smoke test with:

```sh
just test-live-delegation
```

This test consumes model capacity and creates a Codex thread. It passes only
when the hook blocks the read, a collaboration event contains a real receiver
thread for a delegated role, and the parent reports success. The hook recommends
a role, but the driving agent chooses the delegation and fallback path. It can
recover from administrative failures, such as spawn errors and timeouts, and
semantic failures, such as incomplete or incorrect results.

Review and trust the plugin hook with `/hooks` in Codex. The hook blocks
recognizable full-file reads above 350 lines and directs the agent to a bounded
read or subagent summary. Its model-tier policy in
`plugins/bulk-read-routing/config/delegation.json` recommends the stable
`bulk_reader_fast` role more strongly for planner models such as Astra and Sol.
Codex agent configuration owns the model assigned to that role. Set
`BULK_READ_LINE_THRESHOLD` to a positive integer before starting Codex to choose
another threshold.

If a command runs with a tool-specific working directory, use an absolute file
path for an unbounded read. This lets the hook verify the file size before it
allows the command.

## Releases

This repo uses UTC calendar versions in `YYYY.MM.DD.XX` format, with `XX` starting at `0` each day.

Use the checked-in Python runner through `uv`:

```sh
uv run scripts/cut_release.py --dry-run
uv run scripts/cut_release.py
```

See [`docs/release.md`](docs/release.md).

Included skills:

- `api-and-interface-design`
- `chrome-devtools-mcp`
- `code-simplification`
- `codegraph`
- `cut-release`
- `debugging-and-error-recovery`
- `design-algorithm`
- `documentation-and-adrs`
- `git-forge-body-file`
- `learning-systems`
- `librarian`
- `schemdraw`
- `security-and-hardening`
- `source-driven-development`
- `test-strategy`
- `thinking-in-the-limit`
- `typst-documents`
- `webwright`

## Repository Shape

```text
.agents/plugins/marketplace.json
install.md
plugins/
  bulk-read-routing/
    .codex-plugin/plugin.json
    config/agent-roles.json
    config/delegation.json
    hooks/hooks.json
    scripts/pre_tool_use.py
    skills/bulk-read-routing/SKILL.md
skills/
  design-algorithm/
    SKILL.md
  source-driven-development/
    SKILL.md
  ...
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
- small hook-based plugins whose helper is inseparable from the workflow

Poor candidates:

- one-off project notes
- private account details
- speculative workflows that have not earned a stable contract
- full tools or reusable CLIs
- docs that belong in the owning code repo

## Forge Split

Use this split:

- `iancleary/forge`: tools, binaries, release scripts, managed assets, implementation docs
- `iancleary/skills`: portable instructions and small workflow-bound plugins

If executable code has a useful standalone command surface, it belongs in
Forge. If a small helper only enforces one portable workflow, it can remain
beside that skill in this repo.

Long term, Forge policy should decide whether a machine installs this repo into the user-global target, a repo-local target, or both.

Forge-specific skills such as `forge-tools` and `forge-cli` belong only in `iancleary/forge`.
