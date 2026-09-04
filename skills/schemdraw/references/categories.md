# Schemdraw Category Map

This file keeps the broad Schemdraw element surface local enough that Codex usually does not need the web docs just to choose the right module or family.

For exact installed class names, prefer local introspection over browsing:

```bash
uvx --from ./tool schemdraw-tool list --module elements
uvx --from ./tool schemdraw-tool list --module intcircuits
uvx --from ./tool schemdraw-tool list --module logic
uvx --from ./tool schemdraw-tool list --module dsp
uvx --from ./tool schemdraw-tool list --module flow
uvx --from ./tool schemdraw-tool list --module pictorial
```

## Module Map

- `schemdraw.elements as elm`
  Primary symbolic circuit elements, lines, labels, connectors, compound elements, op-amps, transistors, transformers, and most ordinary schematic work.
- `schemdraw.logic as logic`
  Logic gates, timing diagrams, truth tables, Karnaugh maps, and related digital logic surfaces.
- `schemdraw.dsp as dsp`
  Signal-processing blocks such as amplifiers, mixers, filters, summing nodes, ADC/DAC style blocks, and generic square/circle processing nodes.
- `schemdraw.flow as flow`
  Flowcharts, block diagrams, state-style diagrams, decision blocks, and layout helpers.
- `schemdraw.pictorial as pictorial`
  Picture-style components, breadboards, DIPs, LEDs, resistors, and more realistic bench / build / wiring visuals.
- `elm.ElementImage`
  Image-backed custom elements for imported board photos, front panels, connector art, or ICD/cable-drawing assets.

## Circuit Elements

The official `Circuit Elements` area spans these families.

### Basic Elements

Use `schemdraw.elements` for:

- two-terminal components
- single-terminal symbols
- switches
- audio elements
- label elements
- operational amplifiers
- transistors
- vacuum tubes
- cables
- transformers

Best fit:

- ordinary electrical schematics
- analog front ends
- power and signal path drawings
- cable and connectorized symbolic diagrams

Practical local rule:

- if the component is a normal symbol you would expect in an EE schematic, start in `elm`

### Integrated Circuits

Use `elm.Ic`, `elm.IcPin`, `elm.IcDIP`, `elm.SevenSegment`, and predefined IC classes when you need:

- black-box ICs with named pins
- mux/demux style symbols
- DIP package renderings
- predefined parts such as flip-flops, timers, regulators, and common op-amp layouts

Best fit:

- interface control drawings with named signals per side
- cable endpoint drawings where the connector or module pinout matters
- protocol or bus-facing diagrams with explicit IO naming

Practical local rule:

- if you care about side-specific pins, pin numbers, or named anchors, start with the IC family

### Connectors

Use the connector-oriented classes in `schemdraw.elements` when drawing:

- headers
- D-sub connectors
- multi-line cable breakouts
- data busses
- outlets

Best fit:

- cable drawings
- wiring diagrams
- ICDs
- pinout diagrams

Practical local rule:

- if the diagram centers on termination, mating, pin naming, or breakout structure, inspect connector classes first

### Compound Elements

Use the compound families when the symbol is really a packaged relationship of smaller primitives, such as:

- optocouplers
- relays
- Wheatstone bridges
- rectifiers
- two-port representations

Best fit:

- higher-level analog or electromechanical schematics
- documentation where the compound symbol reads better than decomposing everything manually

### Digital Logic

Use `schemdraw.logic` for:

- gates
- logic parser output
- truth tables
- Karnaugh maps

Best fit:

- boolean-logic explanation diagrams
- gate-level hardware views
- logic teaching or documentation artifacts

Practical local rule:

- if the drawing wants `in1`, `in2`, `out`, truth tables, or timing, switch from `elm` to `logic`

### Timing Diagrams

Use `logic.TimingDiagram` and `logic.bitfield.BitField` with JSON-style inputs.

Best fit:

- protocol timing
- register layout / field diagrams
- ICD timing sections
- digital interface documentation

Local rule:

- do not force timing diagrams into SDL; use the timing JSON path in `references/timing.md`
- start from the bundled timing examples before inventing edge syntax by hand

### Signal Processing

Use `schemdraw.dsp` for:

- signal-flow blocks
- mixers
- amplifiers
- filters
- generic square/circle processing blocks

Best fit:

- DSP pipelines
- controls / comms block diagrams
- algorithm and interface diagrams that are more about transformation than wiring

### Image-based Elements

Use `elm.ElementImage` when:

- you need a real board or device outline not covered by built-in elements
- you want imported PNG or SVG artwork as a schematic element
- the drawing needs custom anchor positions over an external asset

Best fit:

- Arduino or custom PCB board overlays
- ICDs with panel art or connector-face art
- cable drawings that need a recognizable equipment silhouette

### Pictorial Elements

Use `schemdraw.pictorial` for:

- breadboards
- pictorial resistors and capacitors
- LEDs and diodes
- DIP packages
- bench/build views

Best fit:

- assembly instructions
- educational wiring diagrams
- cable/build docs where realistic physical appearance matters more than symbolic abstraction

Important style rule:

- pictorial elements are solid-shape oriented, so `.fill()` usually matters more than `.color()`

### Flowcharts And Diagrams

Use `schemdraw.flow` for:

- flowcharts
- block diagrams
- state-like diagrams
- decision trees
- process diagrams

Best fit:

- control flow
- architecture diagrams
- harness/test workflows
- ICD companion diagrams where process matters more than electrical notation

Practical local rule:

- if the diagram is about decision and process instead of voltage/current/connectivity, move to `flow`
- for state machines, start from `examples/state_machine_acceptor.py` or `examples/door_controller.py`

## Diagram-Type Routing

Use this quick routing rule before coding:

- symbolic electrical schematic: `elm`
- IC / pinout / interface box: `elm` plus IC family
- connector or cable drawing: connectors, IC family, and sometimes pictorial/image elements
- gate-level logic or truth-table work: `logic`
- timing or register layout: `logic` timing / bitfield JSON
- DSP or control block view: `dsp`
- pictorial build or breadboard view: `pictorial`
- process or architecture flow: `flow`
- custom hardware silhouette or board art: `ElementImage`

## ICD / Cable / Harness Guidance

For interface-control drawings, cable drawings, and harness-style docs:

- use IC and connector families for endpoint faces and named pins
- use symbolic `elm.Line()` / `elm.Wire()` paths when the drawing is primarily logical connectivity
- use `pictorial` or `ElementImage` when the physical form matters
- prefer Python over SDL once you need reusable endpoint definitions, repeated breakout patterns, or generated pin maps
- treat timing diagrams as separate JSON-driven figures, not inline hacks inside a schematic DSL
