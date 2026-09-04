---
name: git-forge-body-file
description: Use when creating or updating issue bodies, pull request bodies, or substantial Markdown comments on GitHub or Gitea. Detect the Git remote host, use `gh` for GitHub and `tea` for a configured Gitea server, and keep substantial body content in a reviewed local file before submission.
---

# Hosted Git Body File

Use a file-backed workflow for substantial Markdown sent to GitHub or Gitea.

## Select The CLI

Inspect the repository remote before composing the command:

```sh
git remote get-url origin
```

- Use `gh` when the remote host is `github.com`.
- Use `tea` when the remote host is a Gitea server configured in `tea`; pass `--remote origin` when repository discovery needs to be explicit.
- Do not treat every non-GitHub remote as Gitea. If the host is not recognizable, inspect the configured remotes and logins or ask which service owns it.
- Verify authentication with the selected CLI before treating an auth failure as authoritative.

## Working Rules

- Write substantial Markdown to a deterministic file under `/tmp` with `apply_patch`.
- Inspect the file before sending it.
- Keep short, low-risk one-line bodies inline.
- Avoid heredocs and directly embedding multiline Markdown in shell commands.
- When `tea` lacks file input, use the documented quoted `$(cat /tmp/file.md)` fallback; shell output is passed as one argument and is not evaluated again as shell syntax.
- Prefer the hosting CLI's native file or stdin option when available.

## GitHub

Use `--body-file` for substantial bodies:

```sh
gh issue create --title "..." --body-file /tmp/issue.md
gh issue edit 123 --body-file /tmp/issue.md
gh pr create --title "..." --body-file /tmp/pr.md
gh pr edit 456 --body-file /tmp/pr.md
gh pr comment 456 --body-file /tmp/comment.md
```

## Gitea

Current `tea` releases use `--description` for issue and pull-request bodies rather than a body-file flag. Author and inspect the file first, then pass its contents as one quoted argument:

```sh
tea issues create --remote origin --title "..." --description "$(cat /tmp/issue.md)"
tea issues edit --remote origin --description "$(cat /tmp/issue.md)" 123
tea pulls create --remote origin --title "..." --description "$(cat /tmp/pr.md)"
tea pulls edit --remote origin --description "$(cat /tmp/pr.md)" 456
tea comments add --remote origin 456 "$(cat /tmp/comment.md)"
```

For comment editing, prefer the supported stdin path:

```sh
tea comments edit --remote origin 789 < /tmp/comment.md
```

Check the relevant `tea ... --help` before relying on a newer file-input flag. If the installed version adds one, prefer it over command substitution.

## Expected Outcome

- substantial Markdown remains file-backed and reviewable before submission
- GitHub remotes use `gh`; configured Gitea remotes use `tea`
- the selected command preserves real newlines and literal Markdown
- unknown hosting services are not guessed from a non-GitHub URL

## Checks

- verify the remote host and selected CLI
- verify the body file contents before submission
- verify the created or updated issue, pull request, or comment afterward
