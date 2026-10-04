---
name: retro
description: "Review an explicitly selected session or body of work and turn recurring agent corrections into owner-assigned prevention with acceptance evidence."
---

# Retro

Use for an explicit retrospective request. Default to the current conversation
when the user does not name another session. Use the supplied artifacts and
relevant repository evidence; avoid sweeping private logs or unrelated projects.

## Find the preventable failure

Identify the correction, failed attempt, or repeated manual work and its concrete
cost. Distinguish observed behavior from inference. Check the owner's current
instructions and check commands before recommending a new safeguard.

A check that exists but was skipped, unwired, or broken is a different problem
from a missing check. Tie each check to the claimed outcome: installation,
readiness, and acceptance can be distinct states. Preserve truthful intermediate
states rather than inventing a stronger success condition for every command.
Distinguish an immediate repair from protection against recurrence. Ignore speculative improvements with no demonstrated need.

Consider unclear ownership, navigation, stale duplicated state, ambiguous
interfaces, weak feedback, excessive context, and instructions that add no useful
behavior. These are investigation prompts, not a mandatory checklist of findings.

## Choose prevention in order

1. Eliminate the invalid choice through ownership, architecture, an interface,
   a type, or a data structure.
2. Otherwise enforce the invariant with a deterministic check at its owner.
   Wire it into the normal gate and CI where present. Prove the original failure
   is rejected and valid behavior passes.
3. Use a concise skill or rule for judgment that cannot reasonably be encoded.
   Explain why a stronger mechanism is impractical.
4. Retain human review for residual judgment and required authorization.
   Repeated manual detection is a remaining gap, not permanent prevention.

Place the procedure with its workflow owner and the check with the behavior it
protects. Shared agent defaults belong in their baseline owner. A coordinator
retains assignments, dependencies, and acceptance references; it does not collect
all owner implementations or duplicate their runbooks.

## Output and closure

Rank findings by recurrence, consequence, and cost of prevention. For each, state
the observed failure, owner, strongest practical intervention, existing protection,
acceptance evidence, and any dependency or authority still needed. A smaller or
empty backlog is valid when the current controls address the evidence.

Propose tasks locally unless tracker publication is explicitly authorized. A
retrospective does not by itself authorize deployment, configuration installation,
remote writes, or implementation of every recommendation.

When implementation is authorized, close each item with the revision, maintained
check or interface, results, and remaining limits. Refresh the nearest owner record
and remove stale competing guidance. Do not add a scheduled audit without a
recurring need and authorization.

Adapted from Matt Pocock's retrospective workflow, with the local prevention
hierarchy and ownership model. See [third-party notices](THIRD_PARTY_NOTICES.md)
for pinned sources and MIT notice.
