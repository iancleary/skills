---
name: chrome-devtools-mcp
description: Configure and use Chrome DevTools MCP when a coding task needs a live browser with DevTools-backed inspection, console/network visibility, screenshots, or performance traces. Use this for browser debugging and real page inspection; do not use it when simple HTTP fetches or static docs are enough.
---

# Chrome DevTools MCP

Use this skill when Codex needs a real Chrome session instead of text-only web retrieval.

This skill exists for the Chrome DevTools MCP server published by Chrome DevTools.

## Use this when

- you need to inspect a live web app in Chrome
- you need browser console, network, DOM, screenshot, or performance-trace evidence
- a normal fetch or static HTML read is not enough
- you want DevTools-grade debugging instead of ad hoc browser scripting

## Do not use this when

- the task is simple HTTP retrieval
- static documentation or repository reads answer the question
- the page does not require live browser behavior

## Install for Codex

Prefer the user-scope MCP install with telemetry disabled:

```bash
codex mcp add chrome-devtools -- pnpx chrome-devtools-mcp@latest \
  --no-usage-statistics
```

That keeps Codex on the latest release and disables usage-statistics collection.

## Privacy / telemetry default

When you recommend or configure this MCP server for Codex, include `--no-usage-statistics` by default.

If the user also wants to suppress periodic npm update-check notices from the server, set:

```bash
CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS=1
```

Use that env var only when the user wants the extra quiet/no-check behavior; the required no-telemetry default is `--no-usage-statistics`.

## Requirements

- Node.js 20.19+ or newer maintenance LTS
- Google Chrome or Chrome for Testing
- `pnpx` available on PATH

## First checks after install

1. Confirm the MCP entry exists in Codex.
2. Start or attach to Chrome through the MCP client.
3. Run one small proof task such as opening a page and reading console errors.

If startup fails, check Node version, Chrome availability, and whether another browser process is locking the requested profile or debugging port.

## Typical jobs

- inspect console errors after a frontend change
- watch network requests and response failures
- verify DOM state after an interaction
- capture screenshots during debugging
- record a performance trace to explain slowness
- reproduce flaky browser-only behavior in a deterministic tool surface

## Working rules

- Start with the narrowest read or inspection needed.
- Prefer observation before mutation.
- Use screenshots or traces only when simpler evidence is insufficient.
- Keep the task focused on one browser question at a time.
- Treat browser data as sensitive if the page contains private user information.

## Common flow

1. Confirm the server is configured.
2. Open the target page in Chrome.
3. Reproduce the problem or target interaction.
4. Inspect the smallest useful evidence surface:
   - console
   - network
   - DOM state
   - screenshot
   - performance trace
5. Summarize what the browser proved.
6. Only then decide on the code or config change.

## Output contract

Return:

1. `Setup status`
   - whether Chrome DevTools MCP is configured and ready
2. `Browser evidence`
   - the key console/network/DOM/trace findings
3. `Conclusion`
   - what the browser evidence implies
4. `Next action`
   - the narrowest follow-up debugging or implementation step

## Safety

- Chrome DevTools MCP can expose page contents to the MCP client
- avoid using it against pages with secrets unless the user expects that access
- prefer explicit user-scope installation rather than hidden global changes
