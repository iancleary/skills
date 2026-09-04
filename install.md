I want you to install Ian Cleary's agent skills for Forge. Execute all steps autonomously.

OBJECTIVE: Install Forge, verify it works, and install the skills from `iancleary/skills` so your agent knows when and how to use Forge workflows.

DONE WHEN: `forge version` succeeds, `forge doctor` succeeds or reports only documented non-blocking environment warnings, and `npx skills list` shows the Forge skills installed.

## TODO

- [ ] Check whether Forge is already installed
- [ ] Install or update Forge if needed
- [ ] Verify Forge
- [ ] Install skills
- [ ] Verify skills

## Step 0: Check Forge

Check whether `forge` is available:

```bash
forge version
```

If `forge` is not installed, inspect the `iancleary/forge` repository for the current install instructions before choosing an install method. Prefer the repository's documented installer over guessing.

## Step 1: Verify Forge

Run:

```bash
forge doctor
```

If `forge doctor` reports missing optional integrations, continue only when they are unrelated to the user's requested workflow. Fix required failures before installing skills.

## Step 2: Install Skills

Install the skills from this repository:

```bash
npx skills add iancleary/skills
```

To install globally, use:

```bash
npx skills add iancleary/skills -g
```

## Step 3: Verify Skills

Run:

```bash
npx skills list
```

Confirm that `forge-tools` and `forge-cli` are listed. Restart the agent session if the runtime requires a restart to load newly installed skills.

EXECUTE NOW: Start with Step 0. Mark TODO items complete as you go. Stop when Forge is verified and the skills are installed.
