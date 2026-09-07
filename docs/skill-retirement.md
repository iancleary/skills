# Retired skills

The operational portfolio contains 13 skills. These five skills no longer ship:

| Retired skill | Replacement |
| --- | --- |
| `code-simplification` | Baseline rules for preserving behavior and keeping edits scoped. |
| `documentation-and-adrs` | Baseline documentation rules and the target repo's document conventions. |
| `git-forge-body-file` | Baseline hosted-Git rules, including the Gitea details below. |
| `source-driven-development` | Baseline evidence rules and product-specific documentation workflows. |
| `learning-systems` | An ordinary learning request with a topic-appropriate study structure. |

No replacement skill is required for each retired skill. Preserve the following
small rules in the baseline's owning source when updating that baseline:

- Before simplification, identify the behavior to preserve and the evidence
  that demonstrates it. Avoid unrelated formatting or interface changes.
- Put durable decisions with meaningful alternatives in an ADR; put small
  behavior changes in the nearest existing documentation. Remove stale rules.
- Verify external behavior against primary evidence and record the relevant
  version or commit when it affects the conclusion. State unverified assumptions.
- Let the subject determine the learning map. Do not force a fixed number of
  foundational propositions or a single decisive falsifier for every claim.

## Hosted Git details

Inspect the remote host before selecting `gh` for GitHub or `tea` for a configured
Gitea server. A non-GitHub host is not sufficient evidence of Gitea.

Author substantial Markdown in a file, inspect it, and use the CLI's file or
stdin option when supported. Preserve real newlines and literal Markdown.

For Gitea, check the installed command's help before choosing the input form.
When `tea` exposes only `--description`, the quoted substitution below passes
the file contents as one argument without evaluating its contents as shell code:

```sh
tea issues create --remote origin --title "Issue title" --description "$(cat /tmp/issue.md)"
```

Prefer a native file or stdin option when available. Verify the resulting body
after submission. Keep these details with the baseline's hosted-Git guidance.

## Migrate existing installations

Repository deletion does not uninstall a skill or change an existing session.

1. List installed skills in the intended scope with the installation manager.
   Check its help for scope and removal options.
2. Identify the five retired names above. Verify each copy's owner and source;
   a same-named skill may be supplied by another installation.
3. If Forge policy owns the installation, update the policy's skill selection
   and baseline source in Forge before applying its normal reviewed update.
   Otherwise remove the verified copies with their installation manager.
4. Remove routing references to retired names from the baseline's owning source.
   Preserve any missing rules from this document; avoid duplicating existing rules.
5. Verify the installed list and baseline diff, then restart the agent session.

This branch changes repository distribution only. It does not change installed
copies, Forge policy, or user-scoped baseline files. Git history retains the
retired skills if a capability needs to be recovered.
