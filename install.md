I want you to install Ian Cleary's portable agent skills. Execute all steps autonomously.

OBJECTIVE: Install the skills from `iancleary/skills` so your agent has Ian's portable workflow instructions available in the requested scope.

DONE WHEN: `npx skills list` shows representative skills from this repository, such as `design-algorithm`, `source-driven-development`, and `debugging-and-error-recovery`.

## TODO

- [ ] Decide install target
- [ ] Install skills
- [ ] Verify skills

## Step 0: Decide Install Target

Use a local repo install when the skills should apply only to the current repository:

```sh
npx skills add iancleary/skills
```

Use a user-global install when the skills should be available across the machine:

```sh
npx skills add iancleary/skills -g
```

If a machine policy tool such as Forge is available, prefer the policy-managed target rather than guessing.

## Step 1: Install Skills

Run the selected install command from Step 0.

## Step 2: Verify Skills

Run:

```sh
npx skills list
```

Confirm that representative portable workflow skills are listed:

- `design-algorithm`
- `source-driven-development`
- `debugging-and-error-recovery`
- `api-and-interface-design`
- `documentation-and-adrs`

Restart the agent session if the runtime requires a restart to load newly installed skills.

EXECUTE NOW: Start with Step 0. Mark TODO items complete as you go. Stop when the skills are installed and verified.
