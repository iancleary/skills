---
name: schemdraw
description: Use when the user wants circuit, timing, ICD, cable, or signal/block diagrams rendered with Schemdraw from repo-local Python sources. Prefer this skill for diagram generation and editing workflows, and use `uv` / `uvx` for setup and execution instead of `pip`.
---

# Schemdraw

Use this skill when Codex needs to create or revise a diagram as code, not as hand-drawn SVG edits.

This skill ships a small local `uv` tool, local references, and bundled examples:

- `references/schemdraw.md`: condensed Schemdraw usage guidance from the official docs
- `references/sdl.md`: optional Forge Schemdraw Definition Language (SDL) shorthand for simple symbolic schematics
- `references/categories.md`: local map of the main Schemdraw element families and when to use them
- `references/timing.md`: local timing-diagram and bitfield guidance for JSON-first rendering
- `references/protocols.md`: local protocol-harness patterns for SWD, JTAG, SPI, SpaceWire, Ethernet, and PPS
- `examples/`: repo-installable example sources for common diagram families

## Use This When

- the user wants a circuit, analog, digital, or block schematic generated as code
- the output should be reproducible from repo-local Python sources
- the task maps cleanly onto Schemdraw element placement, labels, styling, and SVG export

## Do Not Use This When

- the user wants freeform illustration rather than schematic notation
- the task is best solved by editing an existing SVG manually
- the task needs a full PCB or EDA workflow rather than diagram rendering

## Install And Run

All setup in this skill uses `uv` and `uvx`, not `pip`.

From this skill directory:

```bash
uv tool install ./tool
```

That installs the `schemdraw-tool` executable persistently.

For one-shot use without installation:

```bash
uvx --from ./tool schemdraw-tool render --input ./example.sdl --output ./example.svg
```

When iterating on the local tool during development, use editable install:

```bash
uv tool install --editable ./tool
```

## Default Workflow

1. Prefer repo-local Python as the source of truth.
2. Read `references/schemdraw.md` for the Schemdraw API patterns you need.
3. If you need category-specific elements, read `references/categories.md`.
4. If the job is a timing diagram or bitfield/register view, read `references/timing.md`.
5. If the job is a protocol, debug/programming header, or serialized harness, read `references/protocols.md`.
6. Start from `examples/` when an existing pattern is close enough to adapt.
7. Use the optional SDL path only for small symbolic schematics that benefit from a shorter text format.
8. Prefer SVG output unless the user explicitly needs another backend path.

## Repo Placement

Choose a path that matches the artifact’s audience:

- `docs/diagrams/` for rendered figures and source files tied to published docs
- `docs/icd/` or `docs/cable/` for interface-control, connector, or cable-drawing content
- `schematics/` for project-owned diagram source files used repeatedly
- `tools/schemdraw/` or `scripts/schemdraw/` for generator-style Python modules

Practical rule:

- if the diagram is a maintained project artifact, keep the Python source near the docs or spec it supports
- if the diagram is generated from reusable helpers or inventories, keep the generator in a tooling directory and emit outputs into `docs/` or another checked-in artifact path

## Bundled Examples

Use the bundled examples as local-first starting points:

- `examples/basic_rc.py`: small symbolic schematic
- `examples/opamp_feedback.py`: anchor-based analog block
- `examples/icd_connector.py`: IC / connector / ICD-style drawing
- `examples/harness_bundle.py`: reusable endpoint-definition pattern for harness / cable drawings
- `examples/dsub_breakout.py`: D-sub-to-breakout deterministic connector-family pattern
- `examples/state_machine_acceptor.py`: state-diagram pattern based on flow arcs and loopbacks
- `examples/door_controller.py`: multi-state controller example with curved transitions
- `examples/flow_block.py`: flowchart / block-diagram composition
- `examples/swd_programming.py`: SWD debug/programming harness pattern
- `examples/jtag_fpga.py`: JTAG FPGA/programming harness pattern
- `examples/msp430_fet_jtag_harness.py`: TI MSP430 14-pin programming-pod harness pattern
- `examples/arm20_swd_header.py`: ARM 20-pin SWD physical-header pattern
- `examples/arm20_jtag_header.py`: ARM 20-pin JTAG physical-header pattern
- `examples/cortex9_swd_header.py`: Cortex 9-pin SWD/JTAG physical-header pattern
- `examples/amd_xilinx_14pin_jtag_harness.py`: AMD/Xilinx 14-pin FPGA programming-pod harness pattern
- `examples/intel_fpga_10pin_jtag_harness.py`: Intel FPGA 10-pin download-cable harness pattern
- `examples/msp430_fet_to_microd15_adapter.py`: mock MSP430 pod to Micro-D service-adapter pattern
- `examples/amd_xilinx_to_shrouded_header_adapter.py`: mock AMD/Xilinx pod to shrouded-header adapter pattern
- `examples/intel_fpga_to_circular10_adapter.py`: mock Intel FPGA pod to circular-service adapter pattern
- `examples/spi_peripheral.py`: SPI controller-to-peripheral pattern
- `examples/uart_serial.py`: UART point-to-point serial pattern
- `examples/i2c_sensor.py`: I2C short-reach digital pattern
- `examples/i2c_multidrop.py`: I2C multidrop pattern with explicit pull-up ownership
- `examples/onewire_sensor.py`: 1-Wire short-reach digital pattern
- `examples/mdio_link.py`: MDIO management-link pattern
- `examples/rs422_link.py`: RS-422 full-duplex differential serial pattern
- `examples/rs485_bus.py`: RS-485 2-wire bus-segment pattern
- `examples/rs485_multidrop.py`: RS-485 multidrop bus with explicit end/drop policy
- `examples/spacewire_link.py`: SpaceWire data/strobe full-duplex pattern
- `examples/ethernet_link.py`: Ethernet logical-link pattern
- `examples/ethernet_poe_link.py`: shielded PoE-aware Ethernet logical-link pattern
- `examples/pps_sync.py`: PPS timing-link pattern
- `examples/timing_sram_rw.json`: timing example using extended edge annotations
- `examples/timing_jk_flipflop.json`: timing example using async transitions and colored outputs
- `examples/timing_bus.json`: timing diagram input
- `examples/register_map.json`: bitfield / register-map input
- `examples/helpers/pinmap.py`: shared helpers for endpoint and pin definitions
- `examples/helpers/connectors.py`: standard connector-builder helpers such as D-sub, Micro-D, shrouded headers, circular connectors, terminal blocks, and exact-pin RJ45 T568B
- `examples/helpers/schema.py`: schema validators for endpoint families, required signals, required mappings, and policy-aware bus participants
- `examples/helpers/protocols.py`: protocol-family helpers and schemas for SWD, JTAG, MSP430 pods, FPGA programming pods, SPI, SpaceWire, Ethernet, UART, PPS, multidrop I2C, and multidrop RS-485
- for named debug headers, prefer the pin-map-backed examples over logical-only signal bundles when physical pin numbering matters

Prefer adapting one of these before browsing external docs.

When an exact connector family is already known, prefer the named physical-standard examples over the generic protocol examples.

## Determinism

This wrapper improves determinism by narrowing diagram construction into stable Python helpers instead of free-form drawing logic.

Current deterministic levers:

- frozen `PinDef` / `ConnectionDef` records define endpoint and wire intent explicitly
- endpoint builders validate duplicate pins and duplicate anchor names before drawing
- anchor names are normalized from signal names by one shared function
- connector-family helpers such as D-sub and terminal blocks build from ordered signal lists
- connection helpers route by declared signal mapping rather than ad hoc anchor access spread through the file
- schema validators reject missing required signals, extra unknown signals, duplicate connections, and required-but-unwired mappings before render

What it does not enforce yet:

- electrical correctness
- project-specific signal schemas
- connector-family standards beyond the helper contracts and schemas you define locally

## ICD / Harness Shaping

For interface-control drawings, cable drawings, and harness work, apply the `design-algorithm` sequence before adding diagram detail:

1. Question every requirement.
2. Delete any part or process you can.
3. Simplify and optimize what remains.
4. Accelerate cycle time.
5. Automate last.

Use that sequence concretely:

- question whether the drawing is actually the source of truth or only a rendered view of a contract that should exist as validated data
- delete duplicated signal lists, manual redraw steps, and ad hoc connector-specific anchor logic
- simplify interfaces into reusable endpoint builders, normalized signal names, and schema-checked mappings
- accelerate the loop for regenerating diagrams after interface changes
- automate only stable parts such as connector families, pin maps, schema checks, and deterministic rendering

Reject these anti-patterns:

- polished drawings backed by ambiguous signal contracts
- ICDs that differ only because each author hand-placed anchors differently
- temporary EGSE or lab adapters that escape the same schema discipline as flight interfaces
- workflow automation that hides unresolved interface ambiguity

Prefer these patterns:

- define the interface as data or validated helper calls first
- render the drawing second
- treat test, ground, and operations harnesses as first-class interfaces
- fail generation when required signals or mappings are incomplete

If you are working inside the Forge repo, see `docs/aerospace-antipatterns.md` for the longer rationale and source-backed aerospace context behind these rules.

## Python Vs SDL

Prefer Python by default.

Prefer SDL only when:

- the drawing is mostly linear or anchor-based
- one label per element is enough
- you want a compact textual spec that can be reviewed quickly

Prefer Python when:

- you need loops, helper functions, or generated structure
- you need multiple labels or richer annotations
- you need direct access to the full Schemdraw API surface
- you need features not covered by the local SDL subset
- you are building interface-control drawings, cable drawings, or other richer harness-style documents where reusable helpers will matter

## Python Rules

- Prefer `schemdraw.use('svg')` unless Matplotlib-specific behavior is required.
- Use `import schemdraw` and `import schemdraw.elements as elm` as the default import pattern.
- Use chained methods such as `.down()`, `.label(...)`, `.at(...)`, `.tox(...)`, and `.color(...)`.
- Use anchors from placed elements, such as `R.start`, `Q.base`, or `OP.out`, instead of hard-coded coordinates when possible.
- Put element-shape parameters in the constructor, but styling in chained methods.

When using the bundled tool to render Python, prefer a file that exposes one of:

- `build() -> schemdraw.Drawing`
- `drawing = <Drawing>`
- `d = <Drawing>`

When you need exact local class names without browsing, use the bundled introspection command:

```bash
uvx --from ./tool schemdraw-tool list --module elements
uvx --from ./tool schemdraw-tool list --module logic
uvx --from ./tool schemdraw-tool list --module intcircuits
```

Minimal project-local render pattern:

```bash
uvx --from ./tool schemdraw-tool render --input ./docs/diagrams/example.py --output ./docs/diagrams/example.svg
```

## SDL Rules

- One statement per line.
- Use `let NAME = Element ...` when later anchor references are needed.
- Use `NAME.anchor` references instead of raw coordinates when practical.
- Keep SDL declarative; if you start fighting the grammar, switch to Python.
- SDL is optional shorthand for schematic-style drawings, not the main path.
- Use timing JSON instead of SDL for timing diagrams.

## Output Contract

Return:

1. the source file you created or edited
2. the render command used
3. the output asset path
4. any known limitation that would justify moving from SDL to Python

## Notes

- Schemdraw’s SVG backend is the default choice here because it avoids a Matplotlib dependency and is faster for ordinary schematic export.
- For searchable SVG text or richer math behavior, read `references/schemdraw.md` before choosing SVG text settings.
- For ICD, cable, and harness-like work, prefer Python modules with reusable endpoint or pin-map helpers over ad hoc one-off diagram files.
