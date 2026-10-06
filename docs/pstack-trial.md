# Pstack trial

This trial includes all 51 skills from the snapshot identified in the repository
README. Each package includes its resources, license, and runtime contract.
The machine-readable inventory in [pstack-upstream.json](pstack-upstream.json)
records original file hashes for update and completeness checks.

## Try it

From this checkout, install the local version instead of the unpublished GitHub
branch with `npx skills add . --agent codex`. Choose repository scope for a trial
or add `-g` for an explicitly requested global install. Then run `npx skills list`
(with `-g` for global scope). Existing installations are not changed by this import.

Start a task with `Use poteto-mode to implement <feature and acceptance criteria>`.
Individual skills can also be invoked by name. Keep existing skills available;
select pstack explicitly for trial tasks instead of enabling two competing routers.
Upstream explicit invocation policy is preserved in agents/openai.yaml. Setup
remains discoverable. No baseline instructions, hooks, or model settings change.

## Compatibility

The [runtime contract](../skills/poteto-mode/references/pstack-runtime.md) adapts
delegation, model selection, authorization, history access, and external tools.
Every package contains it so individually installed skills retain the contract.
Cursor agent briefs are bundled as references, not registered globally.
Cursor cloud workflows and Grok webhook routines still require those services.
Bundled Bun and Node helpers retain upstream source; package checks alone do not
prove their integration with Codex. Full behavioral parity is not claimed.

Frontmatter names match directories. Unsupported Cursor metadata is removed.
Setup uses project-local configuration on Codex and retains the upstream Cursor
procedure. Help links point to the pinned upstream guide. Existing authorization
rules take precedence over automatic publication in upstream playbooks.

## Evaluate on real features

Use a bounded feature with observable acceptance criteria. Record architecture
corrections, behavior defects, unnecessary abstractions, and user interventions.
Compare against a similar task using the current workflow. Keep useful skills
based on results. This import makes the complete set available; it does not
establish that every workflow improves feature quality.

Run `just check` before committing package changes. Review upstream updates as
new pinned snapshots and preserve the local runtime contract and invocation policy.

## Local verification

The dotfiles mise configuration supplies Bun 1.4.2. In a temporary copy of the
bundled scripts, `bun install --frozen-lockfile --ignore-scripts` succeeded,
`bun run test` passed all 52 tests, and `bun run typecheck` passed. Repository
`just check` passed for all 62 packages. These results verify the helper tests
and package structure; they do not establish live Cursor or Grok integration.
