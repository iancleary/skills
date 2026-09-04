---
name: thinking-in-the-limit
description: Analyze a design, product, process, or business model by forcing first-principles questions about raw-material cost, supplier layers, scale behavior, physical limits, tool limits, and the gap between current reality and the theoretical best target. Use this when the user needs a deeper systems or design critique, not a surface-level optimization list.
---

# Thinking In The Limit

Use this skill when the user wants a design reviewed from the bottom up: what it is made of, who takes a cut, what happens at scale, what the physical ideal looks like, and what the true limiting factor is.

## Use this when

- the user is evaluating a product, design, process, or manufacturing system
- you need to separate fundamental constraints from accidental implementation choices
- cost structure, scale, or physical feasibility matter
- the user wants a first-principles critique rather than a conventional feature review

## Do not use this when

- the task is only a simple bugfix or implementation detail
- the user needs market sizing, legal advice, or accounting precision beyond available evidence
- there is no concrete artifact, system, or process to evaluate

## Core lenses

Apply these lenses in order.

### 1. Idiot index

Ask:

- what do the raw materials cost versus the final delivered price?
- how many suppliers, intermediaries, or toll collectors sit in the chain?
- who adds real transformation and who mainly takes margin?

The point is not cynicism. The point is to find where cost and complexity enter the system.

### 2. Scale in the limit

Ask the same design question at three scales:

- one unit
- one thousand units
- one million units

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

Return a compact analysis with:

1. `System under review`
   - what is being analyzed and what job it must do
2. `Idiot index`
   - raw-material/core-input cost vs delivered value, key intermediaries, and suspected margin layers
3. `Limit table`
   - one unit / one thousand / one million with dominant constraints at each scale
4. `Ideal target`
   - the theoretical best arrangement or performance target
5. `Current bottlenecks`
   - the real limiting tools, processes, or assumptions
6. `Impossible -> possible`
   - what would have to change to unlock the next regime
7. `Conclusion`
   - whether the problem is fundamentally limited or mainly poorly designed today

## Tone

Be blunt about waste, but do not confuse today's implementation with the laws of physics.
