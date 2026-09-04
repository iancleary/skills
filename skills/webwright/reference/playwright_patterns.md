# Playwright Patterns

These are the canonical patterns for Webwright-style runs. Execute them through
`uvx`, one command at a time, then observe the output before continuing.

## Browser Launch Skeleton

Use Playwright Firefox by default. Some sites reject Playwright Chromium due to
TLS or HTTP/2 fingerprinting, while Firefox loads the same pages cleanly.

```bash
uvx --with playwright python - <<'PY'
import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright

WORKSPACE = Path(os.environ.get("WORKSPACE_DIR", "."))
SCREENSHOTS = WORKSPACE / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()

        await page.goto("<START_URL>", wait_until="domcontentloaded")
        await page.screenshot(path=str(SCREENSHOTS / "explore_1_start.png"))

        print("URL:", page.url)
        print("TITLE:", await page.title())

        snapshot = await page.locator("body").aria_snapshot()
        print("ARIA:", snapshot)

        await browser.close()

asyncio.run(main())
PY
```

Rules:

- run scratch scripts and final scripts with `uvx --with playwright python`
- always set `viewport={"width": 1280, "height": 1800}`
- never call `page.screenshot(full_page=True)`
- each Playwright run is fresh: navigate from the start URL, reapply filters,
  and reconstruct state in code

## Target Elements With Role And Name

```python
await page.get_by_role("button", name="Filters").click()
await asyncio.sleep(1)

panel = page.get_by_role("button", name="Filters").first.locator("..")
print(await panel.aria_snapshot())

await page.get_by_role("checkbox", name="BMW").check()
await asyncio.sleep(1)
```

If a selected state becomes hidden after a drawer or dropdown closes, reopen it
before capturing the verification screenshot.

## Prefer Interactive Form Filling

When a task requires locations, dates, filters, query strings, or similar input,
drive the on-page form interactively instead of constructing a deep-link URL.
Deep links are brittle across locale, A/B bucket, signed-in state, and parser
changes.

Interactive filling is the primary path in final scripts. If you use a deep
link as a shortcut, verify the visible form state afterward and fall back to
interactive filling when any field is empty or wrong.

```python
form_state = await page.locator("input[aria-label]").evaluate_all(
    "els => els.map(e => ({label: e.getAttribute('aria-label'), "
    "value: e.value, hidden: e.offsetParent === null}))"
)

if not form_is_fully_populated(form_state, expected):
    await fill_form_interactively(page, expected)
```

Guidelines:

- use `get_by_role` and `aria-label` selectors instead of brittle CSS classes
- type the value, wait for the suggestion listbox, then click the option whose
  text contains the canonical token
- for paired fields in one modal, open the modal once and use keyboard
  navigation between fields when needed
- after filling, click the explicit submit control rather than relying on
  auto-submit
- re-read form state and assert each critical point before extracting results

## Final-Script Instrumentation

`final_runs/run_<id>/final_script.py` must:

- write screenshots to
  `final_runs/run_<id>/screenshots/final_execution_<step>_<action>.png`
- reset and append to `final_runs/run_<id>/final_script_log.txt`
- print the final datum at the end of the log

```python
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

RUN_DIR = Path(__file__).parent
SCREENSHOTS = RUN_DIR / "screenshots"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)
LOG = RUN_DIR / "final_script_log.txt"
LOG.write_text("")

def log(step: int, msg: str) -> None:
    line = f"step {step} action: {msg}\n"
    with LOG.open("a") as handle:
        handle.write(line)
    print(line, end="")

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()

        await page.goto("<START_URL>", wait_until="domcontentloaded")
        await page.screenshot(
            path=str(SCREENSHOTS / "final_execution_1_open_start_page.png")
        )
        log(1, "open start page")

        final_value = "<extracted price / code / winner>"
        with LOG.open("a") as handle:
            handle.write(f"\nFINAL_RESPONSE: {final_value}\n")

        await browser.close()

asyncio.run(main())
```

## Inspection Commands

```bash
uvx --with playwright python final_runs/run_<id>/final_script.py
ls -R final_runs/run_<id>
cat final_runs/run_<id>/final_script_log.txt
sed -n '1,220p' final_runs/run_<id>/final_script.py
```

For visual checks, inspect individual PNG files inside
`final_runs/run_<id>/screenshots/` with the available image-reading tool.
