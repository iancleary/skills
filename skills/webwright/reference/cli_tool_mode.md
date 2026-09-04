# CLI Tool Mode

Default Webwright runs produce a one-shot `final_script.py` for the literal
values in the user's task. CLI tool mode produces a reusable, parameterized
browser-task CLI that can be rerun later with different argument values.

## When To Use

Use CLI tool mode when:

- the user asks to "parameterize", "make it reusable", "turn this into a CLI",
  "craft a tool", or similar
- the user wants to call the same web workflow later with different values

Otherwise, stay in one-shot mode.

## `plan.md` Parameters

Before writing the script, identify every requirement the user could plausibly
vary and list it in `plan.md` in addition to the normal critical points:

```markdown
# Task
<verbatim task description>

# Parameters
| name    | type | source phrase from task | default | allowed / format |
|---------|------|-------------------------|---------|------------------|
| <arg_a> | str  | "..."                   | "..."   | <format>         |
| <arg_b> | int  | "..."                   | 3       | <range / units>  |

# Critical Points
- [ ] CP1: ...
- [ ] CP2: ...
```

Rules:

- every parameter becomes a function argument
- every parameter becomes an `argparse --flag`
- fixed site details such as start URL, site name, and selector strategy are
  not parameters
- defaults reproduce the original task exactly
- running `uvx --with playwright python final_script.py` with no arguments must
  reproduce the task

## Required Script Shape

`final_script.py` must contain one reusable function named after the task
domain:

```python
def search_<domain>(arg_a: str, arg_b: int) -> dict:
    """Search the target site and return the requested result.

    Args:
        arg_a: What this represents and accepted format.
            Default: "<value>".
        arg_b: What this represents and accepted range or units.
            Default: 3.

    Returns:
        dict with the extracted result and evidence paths.
    """
```

The script must also include an `argparse` CLI under
`if __name__ == "__main__":`. Each function argument has a matching flag with
the same default as the concrete task.

The module must be import-safe:

- no browser launch at import time
- no network call at import time
- no file write at import time

## Action-Log Parameter Echo

The first line written to `final_script_log.txt` after reset must be:

```text
step 0 params: arg_a=<value> arg_b=<value>
```

List every resolved parameter as `name=value` so the verification pass can see
what inputs produced the result.

## Verification

In addition to the default self-verification:

1. Reproduce the original task with no arguments:

   ```bash
   cd final_runs/run_<id> && uvx --with playwright python final_script.py
   ```

2. Run an import-safety smoke test from another directory:

   ```bash
   uvx --with playwright python -c "import importlib.util; \
spec = importlib.util.spec_from_file_location('fs', 'final_runs/run_<id>/final_script.py'); \
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); \
print([n for n in dir(m) if not n.startswith('_')])"
   ```

3. Optionally run the CLI with one alternate argument value when that is
   practical and safe.
4. Show `uvx --with playwright python final_runs/run_<id>/final_script.py
   --help` so the user knows how to call the tool again.

## Completion Gate

Complete CLI tool mode only when all are true:

1. `plan.md` contains `# Parameters` and `# Critical Points`.
2. `final_script.py` defines exactly one reusable function with a Google-style
   `Args:` docstring.
3. Every parameter maps one-to-one to a function argument and an argparse flag.
4. The script is import-safe.
5. `uvx --with playwright python final_script.py` with no arguments reproduces
   the task.
6. Every CP is verified against screenshots or the action log.
7. `step 0 params: ...` is present in `final_script_log.txt`.
8. The user has the final datum and the `--help` output.

If any item is false, diagnose, fix the script without breaking the CLI shape,
rerun in the next run folder, and re-verify.
