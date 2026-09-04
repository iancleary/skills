---
name: design-algorithm
description: Apply Forge's design sequence when shaping a feature, reviewing a proposed command or skill surface, deciding whether repeated shell work should become a Forge primitive, or challenging unclear requirements. Use for planning, scope reduction, spec review, workflow design, and CLI contract design. Do not use when the task is already a straightforward implementation inside an agreed contract.
---

# Design Algorithm

Use this skill before adding new CLI surface, workflow policy, or documentation.

Apply this sequence in order and do not skip ahead:

1. Question every requirement.
2. Delete any part or process you can.
3. Simplify and optimize what remains.
4. Accelerate cycle time.
5. Automate last.

## Trigger Check

Use this skill when:

- the user is still deciding what should exist
- the proposed feature or command surface feels too broad
- the same shell shaping keeps recurring and you need to decide whether Forge should absorb it
- a spec, issue, or workflow needs a reduction pass before coding

Do not use this skill when:

- the contract is already clear and the task is just to implement it
- the task is ordinary code editing inside an established surface
- the user asked for data retrieval from an existing Forge CLI and no shaping decision is needed

## Working Rules

- Ask who owns each requirement and which concrete user or agent job it serves.
- Challenge inherited requirements, guessed future scope, and interface growth justified only by analogy.
- Delete repeated shell shaping, duplicated policy, or unnecessary interface parts before improving them.
- Prefer the narrowest stable contract that makes the next decision easier.
- Improve loop speed only after the contract is necessary and clean.
- Automate only when the first four steps are satisfied.

## Expected Output

When you use this skill, produce a compact result that answers:

- what requirement survived questioning
- what was deleted or refused
- what the narrowest remaining contract is
- what acceleration is justified now
- whether automation should happen at all

If the requirement does not survive the first two steps, say so directly instead of inventing implementation work.

## Forge Interpretation

In Forge, this usually means:

- do not add a command, flag, or crate just because a workflow exists
- remove noisy JSON fields agents repeatedly ignore
- avoid duplicating guidance across many skills when one shared rule can carry it
- turn recurring, stable manual shaping into a small primitive only after confirming it should exist

## Suggested Flow

1. Restate the proposed job in one sentence.
2. Name the owner of the requirement if it is knowable.
3. List what can be deleted outright.
4. Describe the smallest remaining contract.
5. Identify the single most useful speed improvement.
6. Decide whether any automation is justified yet.

## Quick Checklist

Before finalizing a design, answer:

- What requirement did you question?
- What did you delete?
- What became simpler?
- What loop became faster?
- Why is automation justified now instead of earlier?

## Inputs

- job-to-be-done + candidate surface

## Output

- smallest surviving contract (or explicit “do nothing”) + justification

## Checks

- refuse scope growth justified only by analogy or hypothetical future needs
