# Removed tool skills

These bundles were removed to keep this repository focused on workflows owned
as part of this curation. The deletion is a scope decision, not a judgment that
the tools are no longer useful. Nine skills remain under `skills/`.

The links below pin the complete bundles to the last retained commit,
`36665b248820a45164fd76b9f29693edac18fa6e`:

| Bundle | What to recover |
| --- | --- |
| [schemdraw](https://github.com/iancleary/skills/tree/36665b248820a45164fd76b9f29693edac18fa6e/skills/schemdraw) | CLI, examples, protocol helpers, references, and skill instructions together. |
| [typst-documents](https://github.com/iancleary/skills/tree/36665b248820a45164fd76b9f29693edac18fa6e/skills/typst-documents) | Document build and visual-review guidance. |
| [webwright](https://github.com/iancleary/skills/tree/36665b248820a45164fd76b9f29693edac18fa6e/skills/webwright) | Adapted browser-automation workflow, references, invocation metadata, and license notice. |
| [chrome-devtools-mcp](https://github.com/iancleary/skills/tree/36665b248820a45164fd76b9f29693edac18fa6e/skills/chrome-devtools-mcp) | Browser debugging and setup guidance. |

To restore one bundle in a clean checkout of this repository, create a branch
and restore its directory from the pinned commit. For example:

```sh
git switch -c restore/schemdraw
git restore --source=36665b248820a45164fd76b9f29693edac18fa6e -- skills/schemdraw
git status --short
```

Use the corresponding directory for another bundle. Inspect the restored files,
retain license notices, and validate the skill before installing or republishing.
Setup commands describe the historical snapshot; verify them before execution.
The recovered bundle can instead become part of a separate tools or templates
repository. Restoring files does not install dependencies or activate a skill.

Existing installed copies are unaffected. Follow the ownership and scope checks
in [the retirement migration guide](skill-retirement.md) to remove those copies
and stale baseline references. The bulk-read live test now generates its own
temporary fixture and no longer requires Schemdraw.
