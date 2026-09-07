---
name: thinking-in-the-limit
description: Use when the user explicitly requests thinking-in-the-limit or a first-principles limits analysis of a concrete system. Examine relevant costs, scale, fundamental constraints, and the gap between current capability and an ideal target.
---

# Thinking In The Limit

Use this skill when the user wants a design reviewed from the bottom up: what it is made of, who takes a cut, what happens at scale, what the physical ideal looks like, and what the true limiting factor is.

## Use this when

- the user explicitly invokes this skill or requests a first-principles limits analysis
- there is a concrete product, design, process, or system to evaluate

## Do not use this when

- the task is only a simple bugfix or implementation detail
- the user needs market sizing, legal advice, or accounting precision beyond available evidence
- there is no concrete artifact, system, or process to evaluate

## Core lenses

Select the lenses that help answer the user's question. State which assumptions
and scale measures fit the system; omit irrelevant lenses.

### 1. Cost structure

Ask:

- what do the raw materials cost versus the final delivered price?
- how many suppliers, intermediaries, or toll collectors sit in the chain?
- who adds real transformation and who mainly takes margin?

Use raw-material comparisons for physical products when relevant. For software
or services, examine applicable inputs such as compute, labor, or coordination.
Account for transformation, reliability, distribution, and risk before treating
the difference between input cost and price as waste. Missing cost data is an
uncertainty, not evidence of excess margin.

> This is called the "Idiot Index" by Elon Musk.

### 2. Scale in the limit

Choose plausible scales for the system, such as prototype, expected operation,
and a credible growth case. Units may be devices, requests, users, or team size.
Use one, one thousand, and one million units only when those scales are useful.

At each scale, ask:

- what cost terms dominate?
- what breaks first?
- which steps stop scaling cleanly?
- is the pain a fundamental limit or just a bad current design?

### 3. Best arrangement of atoms

Ask:

- what is the physically or theoretically best target?
- what would the ideal artifact look like if we could arrange the atoms directly for the job?
- which current steps exist only because our tools are crude?

This defines the direction of improvement even if the ideal is moving or unreachable.

### 4. Tool-constrained path

Ask:

- given the tools we actually have, what is the best approximation we can build now?
- which fabrication, software, organizational, or supply-chain tools are the true bottlenecks?
- what would have to change in the tool stack to close the gap to the ideal?

### 5. Impossible frontier

Ask:

- what would it take to make the currently impossible possible?
- which assumptions would have to break?
- what enabling capability, process, or material is missing today?

Treat this as a map of missing prerequisites, not a hand-wave.

## Working rules

- distinguish hard physical limits from temporary workflow or tooling limits
- separate evidence from speculation
- prefer rough but explicit orders of magnitude over vague adjectives
- call out where uncertainty is high instead of pretending precision
- if data is missing, show the exact question that would reduce uncertainty most

## Output contract

Return a compact analysis of the system's job, relevant limits, current
bottlenecks, and changes that could improve performance. Use a scale table only
when comparing scales helps. Distinguish measured facts, estimates, and
hypotheses. Identify the next measurement that would most reduce uncertainty.
Do not force a verdict of fundamental limits versus poor design when evidence
supports a mixture or remains incomplete.

## Tone

Be blunt about waste, but do not confuse today's implementation with the laws of physics.
