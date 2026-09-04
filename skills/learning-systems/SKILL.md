---
name: learning-systems
description: Use George Boole's three-prompt framework to map how a subject thinks before deep study by identifying foundations, falsifiers, and logical dependencies. Use this when the user wants to learn a domain quickly from first principles rather than collecting disconnected facts; do not use it for simple factual retrieval or short definitions.
---

# Learning Systems

Use this skill before diving into course material, textbooks, or long explainers. The goal is to draw the picture of the subject before filling in details.

This skill applies George Boole's three-prompt workflow to any target subject.

## Use this when

- the user wants to learn a new domain, topic, system, field, or course quickly
- the user asks for a first-principles map before deep study
- the user wants to stress-test assumptions in a body of knowledge
- the user wants to know how a subject thinks, not just what facts it contains

## Do not use this when

- the task is simple factual retrieval or a short definition
- the user already knows the structure and only wants detailed examples or exercises
- the subject boundary is too vague to identify five core propositions yet

## Inputs

- Topic or subject area (required)
- Optional scope constraints (time, level, and prerequisite level)

## Prompt chain to execute

The workflow is exactly these three prompts, executed in order, then synthesized into a study map. By the end, the user should have a model of the subject's load-bearing walls rather than a loose summary.

1. Foundations prompt

- Ask for the topic's five core propositions:
  - "What are the 5 foundational propositions of this subject? Not facts, not definitions. The statements that, if true, make everything else in this field follow logically."
- Ensure propositions are concise, testable statements, and clearly central to the topic.

2. Falsifier prompt

- For each proposition, ask:
  - "For each proposition, what is the one piece of evidence that would destroy it? What would have to be true for this framework to be wrong?"
- Capture strongest single falsifier per proposition and why the falsifier is decisive.

3. Dependency prompt

- Ask:
  - "Now show me how these propositions connect to each other. Which ones are assumptions? Which ones are conclusions? Which ones are in tension?"
- Return an explicit map with:
  - Assumptions
  - Derived conclusions
  - Tensions / contradictions
  - Dependency arrows between propositions

## Output contract

1. `Core map`
   - A table with five rows: proposition, reason foundational, best falsifier, and confidence note.
2. `How the subject thinks`
   - A short paragraph explaining the overall logic of the field in plain language.
3. `Dependency model`
   - Textual graph (A -> B) plus bullet classification for each node.
4. `Edge cases to test`
   - 2–4 concrete questions or mini-experiments that would validate the map.
5. `Learning path`
   - 3–6 checkpoints that should be filled after this map is built.

## Safety and style

- Ask for confirmation before changing domain boundaries or adding specialized assumptions not in the user's prompt.
- Keep language precise and conservative where evidence is uncertain.
- Do not present the output as final truth; present it as a working model to improve through study.
