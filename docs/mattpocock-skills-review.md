# Upstream skills review

Reviewed 2026-10-04. The five adaptations below are now implemented in repository source.
The local baseline was commit `5d2fda7`. The upstream snapshot is
[`24fe0ef7737efae15c87225755e9f6f5965e4888`](https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/README.md). Recommendations below distinguish useful techniques
from upstream workflow policy. Installed skill copies and agent configuration have not been changed.

## Recommendation

The accepted scope updates three existing skills and adds two explicit-request
workflows, architecture-review and retro. The active inventory now has eleven
packages. The broader upstream collection and workflow router remain deferred.

| Order | Upstream source | Destination | Adaptation and acceptance |
| --- | --- | --- | --- |
| 1 | [codebase-design][design], [alternative designs][alternatives] | `skills/api-and-interface-design` | Evaluate the complexity callers must learn, including ordering, errors, and configuration. Compare materially different contracts when a real tradeoff exists. A worked example must identify what complexity moves behind the interface and what remains with callers. Routine changes must not require multiple agents. |
| 2 | [tdd][tdd] | `skills/test-strategy` | Require expected results independent of the implementation. Prove a regression test fails for the reported behavior and passes after correction. Prefer one behavior at a time when test-first development fits. Preserve the existing exceptions for docs, existing proof, and unclear reproduction. |
| 3 | [diagnosing-bugs][debug] | `skills/debugging-and-error-recovery` | Make the feedback command detect the user's actual symptom. Capture the environment and reproduction rate for intermittent failures. For hard cases, use falsifiable hypotheses and remove temporary instrumentation. Evaluate with a wrong-symptom repro and an intermittent failure; avoid fixed hypothesis counts or a ban on reading code before a repro exists. |
| 4 | [architecture review][architecture] | `skills/architecture-review` | Explicit request only. Review the named area or demonstrated change hot spots. Return a short ranked list of concrete friction, owner, interface change, and proof required. Accept a result with no useful refactor. Scope exploration to the delegated owner repository. |
| 5 | [retro][retro] | `skills/retro` | Explicit session review only. Convert corrections into owner-assigned prevention using architecture, checks, skills/rules, then human review. Reuse existing checks before inventing new ones. Each finding needs a failure mode, strongest practical prevention, acceptance evidence, and remaining gap. |

Both new packages use `agents/openai.yaml` with
`policy.allow_implicit_invocation: false`. They are registered in `curation.toml`.
Upstream frontmatter keys were adapted to the local name/description contract.
The retrospective retains the upstream name `retro`, as requested.

## Ownership boundaries

| Owner | Owns | Effect of the adoption |
| --- | --- | --- |
| `skills` | Portable workflow procedure, triggers, references, and inseparable small helpers | Own the three procedural upgrades and any new reusable review skills. Keep each independently usable. |
| `agent-config` | Shared working defaults, authorization, delegation discipline, communication, and configuration deployment | Existing defaults already cover these needs. Avoid adding the upstream skill catalog or its full writing guide to the baseline. Change a baseline rule only for a demonstrated cross-task gap. |
| `compute` | Owner discovery, bounded assignments, dependency coordination, and acceptance | Invoke the selected workflow and pass owner references. Retain coordination results and links to owner evidence. Delegate implementation context to the owner. |
| Implementation repository | Domain vocabulary, ADRs, production interfaces, lint rules, tests, and runtime proof | Implement and enforce the accepted design here. Preserve language, unit, hardware, and release constraints. |

An architecture review of a Rust crate belongs with that crate. A review of
coordination contracts belongs in compute. A portable retrospective procedure
belongs in skills; the resulting prevention check belongs with the behavior it
protects. The lead retains integration and acceptance.

Compute's specific registry, private inventory, and deployment details must not
be copied into this public skills repository. Use generic examples in portable
skills. Repository boundaries are authoritative even when an abstraction could
combine behavior across them.

## Techniques to borrow selectively

- [Domain modeling][domain]: use concrete counterexamples to clarify overloaded
  terms. Keep vocabulary and consequential design decisions with their owner.
  Follow the owner's document layout. Do not restore the retired
  `documentation-and-adrs` skill merely to prescribe a glossary filename.
- [Task decomposition][tickets]: make tasks independently verifiable and record
  real blockers. Preserve expand/migrate/contract sequencing for broad changes.
  Compute can use this in assignments; a new tracker or per-ticket file hierarchy
  is not required. Publishing tasks remains separately authorized.
- [Handoff][handoff]: reference existing artifacts instead of repeating them.
  Compute already has a handoff contract. Select temporary or durable storage
  based on the purpose, and include current authority and remaining evidence.
- [Code review][review]: distinguish fulfillment of the requested behavior from
  compliance with owner standards. Keep evidence for both, but let the lead
  combine, deduplicate, and prioritize actionable findings. Use independent
  reviewers only when expected value exceeds their coordination cost.
- [Writing for agents][writing]: keep instructions concise and load supporting
  references only when relevant. Preserve familiar project terminology. Its
  broad claims about model attention are design hypotheses, not verified local
  performance results.

These are candidate techniques, not instructions to execute the upstream skills.
The existing baseline already covers much of this material.

## Do not port unchanged

| Upstream choice | Local decision |
| --- | --- |
| Mandatory vocabulary that prohibits API, service, or boundary | Keep owner vocabulary and precise familiar terms. |
| [Deepening][deepening] rules that always merge pure computation, delete old unit tests, or require two adapters | Make these case-specific decisions. Preserve engineering boundaries and independent proof, including units and numerical edge cases. |
| TDD requires user confirmation of every test seam and reserves refactoring for review | Preserve existing authorization and the owner's test strategy. Avoid routine approval pauses. |
| Architecture review always generates CDN-backed HTML and launches a grilling session | Use concise findings by default. Add a diagram or interactive view when it improves a decision. |
| `ask-matt`, setup, implement, implement-spec, to-spec, triage, and [wayfinder][wayfinder] as a connected process | Defer this suite. It overlaps compute coordination and introduces tracker/setup dependencies. Assess an individual unmet need before importing a workflow. |
| [Prototype][prototype] and [wizard][wizard] | Defer until repeated need is demonstrated. Owner scripts and existing visualization capabilities may already suffice. Never import secret-capture or external-write behavior as an implicit default. |
| Claude Git hooks and Husky setup | Keep permissions in agent-config and repository checks with owners. These do not enforce cross-agent Git serialization. |
| Generic writing, teaching, research, or ADR skills | Preserve the deliberate retirement decisions; ordinary requests and existing skills cover these cases. |
| TypeScript-specific migrations, course scaffolding, and in-progress packages | Outside this adoption scope. |

The review inventoried all upstream SKILL.md descriptions and read the shortlisted
workflows and relevant references. Deferred suites received a lighter review;
they are not approved for installation or execution.

## Attribution and license handling

The inspected upstream LICENSE is MIT, with copyright 2026 Matt Pocock. Its
notice requires inclusion of the copyright and permission text in copies or
substantial portions. Source links supplement that text; they do not replace it.
See [the pinned upstream license][license] and the retained
[component license notice](../LICENSE.mattpocock).

This repository has no root LICENSE at the reviewed revision. Existing adapted
skills carry their own `THIRD_PARTY_NOTICES.md`, including Addy Osmani notices.
Preserve those notices. Do not infer or change the license of all original work
from one upstream import.

For each actual port:

1. Record the exact upstream commit, source files, destination files, and local
   adaptations in the destination package's `THIRD_PARTY_NOTICES.md`.
2. Retain the full applicable copyright and MIT permission/disclaimer text in
   that package so it travels with a single-skill installation.
3. Add immutable source and LICENSE links to the component license ledger.
4. Inspect nested credits and independently licensed helpers before copying.
   Upstream [PR credits][prcredits] identify an additional Humanlayer source;
   that material needs its own provenance review before adoption.
5. Verify packaged notices and referenced files are present. Run `just check`
   after active package or curation changes. Do not claim that the current
   curation gate automatically verifies license completeness.

The component notice covers this review and all five adapted SKILL.md files.
Each affected package also retains the complete MIT notice and exact source
permalinks. Existing Addy Osmani attribution remains intact. No upstream helper
or runtime hook is imported.

## Implementation and validation

The three existing skills preserve their narrow triggers and prior safeguards.
Architecture review and retro have no required dependency on another skill,
a tracker, private inventory, or a particular model. Existing owner boundaries
and baseline authorization rules remain authoritative.

Run `just check` to validate the eleven-package inventory and existing negative
fixtures. Validate both new skills with the skill-creator validator. Inspect
package notices and pinned source paths. Use bounded behavioral exercises to
review whether the guidance improves decisions without imposing new process on
routine tasks. Record limitations of that review rather than claiming measured
agent-speed improvements.

Validation on 2026-10-04 passed the repository gate, all five skill-creator
validations, source-permalink checks, package MIT notices, and explicit invocation
metadata. Existing Addy Osmani notices were preserved.

Two independent, bounded exercises used supplied hypothetical evidence only.
Architecture review rejected a generic RF conversion API with no demonstrated
caller benefit and retained independent unit/error coverage. Retro reused an
existing readiness verifier instead of proposing another baseline reminder.
Review of that answer exposed a possible conflation of installation and readiness;
the skill now requires checks to match the claimed outcome and preserve truthful
intermediate states. These exercises are qualitative evidence, not measurements
of production reliability or agent speed.

Agent-config and compute need no source changes for these portable workflows.
Installation is a separate action; repository edits do not replace installed copies.

[architecture]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/improve-codebase-architecture/SKILL.md
[design]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/codebase-design/SKILL.md
[alternatives]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/codebase-design/DESIGN-IT-TWICE.md
[deepening]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/codebase-design/DEEPENING.md
[retro]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/retro/SKILL.md
[debug]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/diagnosing-bugs/SKILL.md
[tdd]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/tdd/SKILL.md
[domain]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/domain-modeling/SKILL.md
[handoff]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/productivity/handoff/SKILL.md
[tickets]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/to-tickets/SKILL.md
[wayfinder]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/wayfinder/SKILL.md
[review]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/code-review/SKILL.md
[writing]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/productivity/writing-for-agents/SKILL.md
[prototype]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/prototype/SKILL.md
[wizard]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/wizard/SKILL.md
[prcredits]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/pr/CREDITS.md
[license]: https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/LICENSE
