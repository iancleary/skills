# Timing And Bitfield Diagrams

Schemdraw timing diagrams are a separate declarative path from ordinary schematic placement.

Use them for:

- bus/protocol timing
- clock and control sequencing
- ICD timing sections
- register and field-layout diagrams

## Local Commands

Render a timing diagram from WaveJSON-style input:

```bash
uvx --from ./tool schemdraw-tool render --mode timing-json --input ./timing.json --output ./timing.svg
```

Render a bitfield/register diagram:

```bash
uvx --from ./tool schemdraw-tool render --mode bitfield-json --input ./register.json --output ./register.svg
```

Persistent install:

```bash
uv tool install ./tool
schemdraw-tool render --mode timing-json --input ./timing.json --output ./timing.svg
```

## Timing Diagram Model

Schemdraw timing diagrams are driven by a dictionary using the WaveJSON structure used by WaveDrom, with Schemdraw-specific customizations.

At minimum, timing-diagram input usually has:

- `signal`: a list of waves or groups

Optional top-level keys commonly used:

- `edge`
- `config`
- `head`
- `foot`

## Minimal Timing Example

```json
{
  "signal": [
    { "name": "clk", "wave": "P......" },
    { "name": "data", "wave": "x.==.=x", "data": ["head", "body", "tail"] },
    { "name": "ready", "wave": "0..1..0." }
  ],
  "config": { "hscale": 2 }
}
```

## Common Wave Characters

Typical wave strings use one character per period.

Common values documented in Schemdraw / WaveJSON usage:

- `0`: low
- `1`: high
- `.`: repeat previous state
- `p` / `P`: clock pulse forms
- `n` / `N`: inverted clock pulse forms
- `x`: unknown / don’t-care style state
- `=` and numbered data states for bus/data blocks

## Groups

Signals can be nested into labeled groups:

```json
{
  "signal": [
    "Group",
    [
      "Set 1",
      { "name": "A", "wave": "0..1..01." },
      { "name": "B", "wave": "101..0..." }
    ],
    [
      "Set 2",
      { "name": "C", "wave": "0..1..01." },
      { "name": "D", "wave": "101..0..." }
    ]
  ]
}
```

## Nodes And Edges

Use `node` strings inside signals to mark labeled positions and `edge` at top level to annotate relationships between nodes.

Practical rule:

- use nodes when the important part of the diagram is the relationship between events, not just the waveform levels

## Timing Configuration

Useful diagram-level configuration from the docs includes:

- `hscale`: width of one period

Useful keyword-style customization on the Schemdraw element includes:

- `yheight`
- `ygap`
- `risetime`
- `fontsize`
- `datafontsize`
- `nodesize`
- `namecolor`
- `datacolor`
- `nodecolor`
- `gridcolor`

If you need those richer element kwargs, switch to Python so you can instantiate `logic.TimingDiagram(...)` directly.

Useful local examples:

- `examples/timing_sram_rw.json` for extended edge annotations with timing labels
- `examples/timing_jk_flipflop.json` for async transitions and colored outputs
- `examples/timing_bus.json` for a compact bus/tutorial-style pattern

## Bitfield Model

Bitfield/register diagrams use a dictionary with:

- `reg`: list of bit groups
- optional `config`

Each bit-group entry may include:

- `name`
- `bits`
- `attr`
- `type`

## Minimal Bitfield Example

```json
{
  "reg": [
    { "name": "IPO", "bits": 8, "attr": "RO" },
    { "bits": 7 },
    { "name": "BRK", "bits": 5, "attr": "RW", "type": 4 },
    { "name": "CPK", "bits": 2 },
    { "name": "Clear", "bits": 3 },
    { "bits": 8 }
  ]
}
```

## When To Use Python Instead

Switch from JSON rendering to Python when:

- the timing figure must be composed with other schematic elements in one drawing
- you need richer styling than the local JSON path exposes
- you want reusable generators for families of registers or protocol transactions
- you need post-placement composition with other modules
