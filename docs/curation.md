# Package curation

`curation.toml` is the package ownership contract. Active paths include portable
skills and plugin skills. Retired names remain prohibited. Moved names identify
the external owner; this repository cannot ship those packages again.

Run `just check` after a package or policy change. The same command gates
releases through `release.toml`. The validator checks all shipped SKILL.md
packages, frontmatter keys, name and directory agreement, descriptions, duplicate
names, ownership exclusions, and active inventory. Tests reject invalid
frontmatter, restored retired or moved packages, duplicate plugin packages, and
missing active packages. A valid inventory passes.

The frontmatter validator supports this repository's one-line scalar contract.
Use plain descriptions or JSON double-quoted strings. Multiline YAML is outside
this maintained package format. A deliberate ownership change requires an
explicit policy update and review. Fixtures cannot prevent intentional changes
to the policy itself. Installed packages and external owners remain outside this
gate. No CI workflow is present; local and release checks enforce it.
