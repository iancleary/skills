---
name: source-driven-development
description: "Ground implementation decisions in primary sources before coding. Use when a task depends on framework, library, API, CLI, protocol, or vendor behavior that may be version-sensitive, current, subtle, or easy to misremember; prefer local source and official docs over summaries."
---

# Source-Driven Development

Use primary sources to make external behavior explicit before changing code.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Identify the claim that must be true for the change to be correct.
2. Read the most authoritative source available:
   - local source, generated types, schemas, tests, and lockfiles
   - official documentation or release notes
   - upstream source when docs are unclear
3. Record the version, commit, package, API date, or doc date when it matters.
4. Implement only the behavior that is supported by the evidence.
5. If the source is missing or ambiguous, state the uncertainty and keep the change reversible.

## Routing

- Use `openai-docs` for OpenAI API, model, ChatGPT, or Codex product questions.
- Use repo-local docs and source first when working inside a checked-out project.
- Use web search only when the dependency contract is not available locally or could have changed.

## Output

Include:

- source consulted
- decision it supports
- assumptions still unverified
- tests or checks that prove the local behavior

## Checks

- Do not cite blog posts or AI summaries as authority when official docs or source are available.
- Do not keep implementation details that were added only to satisfy an unverified assumption.
