# Workflow

Use this loop for requested browser automation artifacts. Scale evidence to the
task while preserving a rerunnable script and a verified result.

## Plan and explore

Identify each requested constraint and final datum. For complex tasks, record a
checklist in `plan.md`; a short task can use the response or script assertions.
Keep numeric, date, quantity, and unit requirements exact.

Discover stable selectors with scratch Playwright scripts. Inspect relevant
labels, URLs, and ARIA state. Save screenshots when visual state is needed to
verify a requirement. Expand hidden panels before concluding that a control is
unavailable. Use dedicated filter and sort controls when the site provides them.

## Author and execute

Create `final_script.py` in the task workspace. Document starting state,
dependencies, and any authorized login prerequisites. Capture the final result
and enough assertions, logs, or screenshots to verify the constraints. A
screenshot for every action is unnecessary.

Run the script from its documented starting state:

```bash
uvx --with playwright python final_script.py
```

Keep current evidence distinguishable from failed attempts. Separate run folders
are useful for complex retries but are optional for simple tasks. Before a rerun,
check whether earlier actions changed external state; do not repeat a mutation
merely to obtain cleaner evidence.

## Verify and report

Verify each requested constraint against the extracted result, assertions, logs,
or inspected screenshots. Confirm hidden selections through visible summaries or
by reopening their controls. An empty result is valid when the required filters
were applied correctly.

Fix ambiguous or failed checks and rerun when useful and safe. If a blocker
remains, report the observed failure and unverified requirements. Do not claim
success from a script that has only been written.

Deliver the result, script path, rerun command, and relevant evidence paths.
