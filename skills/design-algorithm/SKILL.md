---
name: design-algorithm
description: Reduce unresolved feature or workflow scope by questioning requirements, deleting unnecessary work, and deciding whether automation is justified. Use when the user is still deciding what should exist or requests a design reduction pass. Do not use for implementation within an agreed contract.
---

# Design Algorithm

Start from the user's proposed job and constraints. Apply this sequence to the
unresolved scope:

1. Question requirements. Identify the owner and the concrete job each requirement
   serves. Challenge inherited rules and hypothetical future needs.
2. Delete unnecessary parts or processes before improving them. Look for
   duplicated policy, unused output, and interface growth justified only by analogy.
3. Simplify what remains into the smallest useful contract.
4. Identify a speed improvement only after the work itself is necessary.
5. Automate stable, repeated work when its benefit exceeds the maintenance cost.

Report the surviving contract, proposed omissions, and the reason to automate or
defer automation. A recommendation to do nothing is valid. Do not invent a deletion
or automation step just to fill out the sequence.
