I want you to install Ian Cleary's portable agent skills. Execute all steps autonomously.

OBJECTIVE: Install the skills from `iancleary/skills` so your agent has Ian's portable workflow instructions available in the requested scope.

DONE WHEN: the skills listing for the selected scope shows representative skills from this repository, such as `design-algorithm`, `api-and-interface-design`, and `debugging-and-error-recovery`.

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

For a repository-local install, run:

```sh
npx skills list
```

For a user-global install, run `npx skills list -g` instead.

Confirm that representative portable workflow skills are listed:

- `design-algorithm`
- `debugging-and-error-recovery`
- `api-and-interface-design`

For an upgrade, read `docs/skill-retirement.md` from this repository. Do not
assume installation removes retired skills. Inspect the selected scope and its
manager before removing stale copies or changing baseline routing instructions.

Restart the agent session if the runtime requires a restart to load newly installed skills.

EXECUTE NOW: Start with Step 0. Mark TODO items complete as you go. Stop when the skills are installed and verified.
