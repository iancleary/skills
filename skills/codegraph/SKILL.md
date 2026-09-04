---
name: codegraph
description: Use when a user asks to use CodeGraph, or when semantic code exploration, symbol lookup, call paths, impact analysis, affected-test discovery, or MCP-based local code intelligence would reduce broad grep/read exploration. Prefer CodeGraph before file-by-file search when `.codegraph/` exists; use `forge tool update codegraph` to install or upgrade the standalone CLI.
---

# CodeGraph

Use CodeGraph for local semantic code exploration when a project has a `.codegraph/` index or the user explicitly wants one added.

Start with:

- `codegraph status [path]`
- `codegraph init [path]`
- `codegraph explore "<question>"`
- `codegraph affected <files...>`
- `forge tool update codegraph --dry-run`
- `forge tool update codegraph`

Working rules:

- Prefer the MCP tool `codegraph_explore` when it is available. Treat returned source as already read; do not immediately duplicate the same discovery with grep and file reads.
- If the MCP tool is not available, use the CLI equivalent `codegraph explore "<question>"`.
- Use CodeGraph for structural questions such as "how does X work", "how does X reach Y", "what calls this", "what breaks if this changes", and "which tests are affected".
- Check `codegraph status` before relying on an existing index. If the status reports pending sync for files that matter, read those live files directly or run `codegraph sync` when a manual sync is appropriate.
- Do not run `codegraph init` as a hidden setup step. It creates `.codegraph/`; do it only when the user asks for CodeGraph indexing or when setup is clearly part of the current task.
- Keep `codegraph install` separate from CLI installation. `forge tool update codegraph` installs or upgrades the standalone CLI; `codegraph install` writes agent MCP configuration and should be treated as an explicit config mutation.
- For Codex MCP setup, prefer previewing with `codegraph install --print-config codex` before applying a config write.
- Use `codegraph affected` for test targeting from changed files before guessing a test list manually.
- Fall back to `rg`, file reads, and language-specific tools for unindexed projects, unsupported files, generated artifacts, or when CodeGraph explicitly says to use built-in tools.

## Add CodeGraph To A Repo

When the user asks to add CodeGraph to a repo, keep the three mutation layers separate:

1. CLI availability:

```sh
forge tool update codegraph --dry-run
forge tool update codegraph
```

This installs or upgrades the standalone `codegraph` command. It does not index the repo and does not edit agent config.

2. Agent MCP wiring:

```sh
codegraph install --print-config codex
```

Use the printed config as a preview. Apply `codegraph install` only when the user wants CodeGraph to edit agent configuration. Restart the agent after config changes.

3. Project indexing:

```sh
codegraph status .
codegraph init .
codegraph status .
```

`codegraph init` creates `.codegraph/` and builds the graph. Keep `.codegraph/` local; do not commit the generated SQLite index. If the repo would otherwise track it, add `.codegraph/` to `.gitignore`. Commit `codegraph.json` only when the repo needs shared custom exclusions or file-extension mappings.

After indexing, run one smoke query:

```sh
codegraph explore "What are the main entry points in this project?"
```

## Maintain CodeGraph

Global CLI maintenance:

```sh
forge tool update codegraph --dry-run
forge tool update codegraph
```

Project index maintenance:

```sh
codegraph status .
codegraph sync .
codegraph index . --force
```

Use `status` first. Prefer the auto-sync watcher during normal agent work. Use `sync` when scripting against the index or when the watcher is disabled. Use `index --force` after changing `codegraph.json`, after large branch switches, or when status indicates the graph should be rebuilt.

Cleanup:

```sh
codegraph uninit .
codegraph uninstall
```

`uninit` removes the project index. `uninstall` removes agent wiring and leaves project indexes alone unless removed separately.

## Use CodeGraph

For MCP sessions:

- Use `codegraph_explore` first for architecture, flow, and impact questions.
- Pass `projectPath` when querying an indexed repo that is not the current working directory, or an indexed subproject in a monorepo.
- If the response includes a staleness warning for files that matter, read those live files directly before editing or summarizing.

For CLI fallback:

```sh
codegraph explore "How does auth reach the database?"
codegraph query UserService --kind function --limit 10 --json
codegraph callers UserService.login --limit 20 --json
codegraph callees UserService.login --limit 20 --json
codegraph impact UserService.login --depth 2 --json
codegraph affected --stdin --quiet
```

Use `affected` with changed files before selecting tests:

```sh
git diff --name-only HEAD | codegraph affected --stdin --quiet
```

Do not force CodeGraph into every task. Use normal repo tools for tiny edits, docs-only work, exact text search, unsupported generated files, or unindexed projects.

## Output

- CodeGraph command or MCP tool used
- whether the repo was already indexed or newly initialized
- config/index mutations performed, if any
- any staleness warning that affected the answer
- fallback used when CodeGraph was unavailable or inappropriate

## Checks

- prefer CodeGraph for indexed structural exploration
- do not silently create `.codegraph/`
- do not commit generated `.codegraph/` indexes
- keep agent config writes explicit
- avoid re-grepping CodeGraph results unless freshness or coverage is uncertain

References:

- https://colbymchenry.github.io/codegraph/
- https://github.com/colbymchenry/codegraph
