---
name: herdr-coordinator
description: "Use when asked to complete a task with Herdr, coordinate Herdr workers or panes, delegate work inside a Herdr session, or run a multi-agent Herdr workflow with integration and verification."
---

# Herdr Coordinator

Use Herdr as the work coordinator, not as a message relay for the user.

## Workflow

1. Restate the task outcome and constraints before delegation.
   - Identify deliverables, repositories, writable surfaces, external actions, secrets, and any user-specified model or effort requirements.
   - Do not push, publish, deploy, touch production, or send sensitive information externally unless the user explicitly authorized that action.
   - Done when the task contract and authorization boundary are clear.

2. Inspect the current Herdr server and session.
   - Check which workers, panes, models, and working directories are already available.
   - Reuse existing workers when their context and checkout are appropriate.
   - Treat local and remote machines as visible coordination targets only when the current Herdr session exposes them; do not assume a CLI command can dispatch across machines unless the active Herdr surface proves it.
   - Done when every usable worker and checkout is accounted for.

3. Split work only where pieces can move independently.
   - Use one worker when one worker can complete the task cleanly.
   - Use research or review workers for read-only work.
   - Give concurrent writers separate Git worktrees so no two writers modify the same checkout.
   - Done when each worker has one clear outcome and no overlapping write ownership.

4. Assign each worker a complete contract.
   - Include working directory, necessary context, deliverable, allowed changes, forbidden changes, verification method, model, and effort.
   - Ask workers to return a short report with result, commit or artifact location, verification results, and unresolved issues.
   - Tell workers not to dump full logs into the main conversation.
   - Done when every worker can proceed without the user carrying context between panes.

5. Coordinate through Herdr until the reports are actionable.
   - Wait for worker results, read each report, and follow up directly when a report is incomplete, contradicted, or unverified.
   - Resolve factual disagreements with tests, source reads, screenshots, or other inspectable evidence.
   - Decide judgment calls yourself when evidence is sufficient.
   - Done when all accepted worker outputs have evidence attached.

6. Verify before accepting work.
   - Inspect the relevant diff, screenshot, generated artifact, or command output yourself.
   - Do not accept a completion message alone as verification.
   - When independent review is needed, use a worker with a different model that did not implement the change and give it a specific commit, diff, or artifact version to inspect.
   - Done when accepted work has been checked against the actual artifact.

7. Integrate in one place.
   - Bring accepted changes into one checkout for the final state.
   - Preserve the user's existing work and any undelivered artifacts.
   - Rerun the project's actual checks from the integration checkout.
   - Done when the integrated state is coherent and verified.

8. Release or preserve resources intentionally.
   - Close panes, stop processes, and remove temporary worktrees when they are no longer needed.
   - Preserve retained worktrees, panes, or artifacts that still contain useful undelivered work, and report them explicitly.
   - Done when there are no forgotten task resources.

## Output

Finish with:

- what was completed
- verification evidence
- anything unresolved or unverified
- panes, workers, worktrees, or artifacts still retained

## Checks

- Do not ask the user to relay messages between Herdr panes.
- Do not split work for ceremony when one worker is enough.
- Do not allow two writers to share a Git checkout.
- Do not leak secrets, credentials, or private context into worker prompts beyond what the task requires.
