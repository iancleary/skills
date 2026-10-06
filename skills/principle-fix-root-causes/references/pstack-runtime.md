# Pstack trial runtime contract

Read this before the upstream procedure. These local adaptations govern all
steps, references, playbooks, and delegated work in this trial.

- Apply a skill when explicitly requested or called by an explicitly selected
  pstack workflow. Installation does not activate poteto-mode globally. The
  setup skill remains normally discoverable, matching upstream.
- Preserve the user's scope and existing authorization rules. A playbook does
  not authorize messages, issue creation, PR writes, pushes, merges, deployment,
  deletion, or unrelated fixes. Prepare authorized local work before asking for
  missing authorization. Serialize Git mutations and verify each completion.
- Translate Cursor Task calls to the runtime's available subagent tools. Inherit
  the session model unless the user has configured supported alternatives.
  Never pass Cursor model slugs to another runtime. State when reviewers share
  a model; do not claim model diversity or cloud isolation. If delegation or
  required isolation is unavailable, report that limitation before substituting
  a sequential review. Give workers scope, ownership, and acceptance evidence.
- The poteto-agent role means a worker must read poteto-mode and this contract.
  Comment Sicko's role text is bundled with no-comments under references. Use
  an available generic role with that brief; do not assume native registration.
- Resolve other skills through the installed catalog. Read sibling files when
  working directly from this repository. Translate /skill-name to the runtime's
  explicit skill invocation. Resolve scripts from their owning skill directory,
  not from a presumed plugins/pstack checkout.
- On Codex, use skill-creator for create-skill. Discover actual verification and
  UI tools instead of assuming cursor-team-kit is installed. If deslop is absent,
  review the diff for unnecessary code manually and identify that substitution.
  Do not claim an unavailable control or live verification step passed.
- Read only task-relevant, accessible history through available runtime tools.
  Do not assume Cursor transcript paths or mine unrelated private conversations.
- Do not create /loop substitutes or recurring jobs unless requested. Cursor
  cloud orchestration and Grok webhook routines require their actual services.
  make-bot-ui is conditional on those services and is not a generic UI generator.
- Keep license notices and comments needed for correctness or public contracts.
  no-comments may propose structural changes but must not remove a necessary
  explanation while leaving its underlying constraint unresolved.
- Bundled scripts are upstream code, not verified cross-runtime integrations.
  Inspect dependencies and side effects before executing them. Follow the
  repository's toolchain. Runtime setup must not install hidden hooks.

## Model configuration on Codex

Use the current session defaults without setup. If the user invokes setup-pstack,
inspect available models, ask for role/budget preferences, and record confirmed
choices in a project-local pstack-models.md. Read that file for later pstack
delegation. Store model and reasoning effort separately. Do not write Cursor
rules or edit global Codex configuration. Do not invent supported model names.
This file is a workflow convention, not automatic runtime configuration.
