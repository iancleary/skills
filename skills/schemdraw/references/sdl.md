# Schemdraw Definition Language (SDL)

SDL is a compact, line-oriented shorthand for simple Schemdraw diagrams. It is intentionally smaller than the full Python API and is not the preferred source format when repo-local Python is practical.

Use SDL when the diagram is mostly sequential or anchor-based and a shorter notation genuinely helps. Switch to Python when the schematic becomes procedural or needs advanced features. Use timing JSON rather than SDL for timing diagrams and register/bitfield figures.

## Tool Commands

Render SDL to SVG:

```bash
uvx --from ./tool schemdraw-tool render --input ./circuit.sdl --output ./circuit.svg
```

Translate SDL to Python:

```bash
uvx --from ./tool schemdraw-tool to-python --input ./circuit.sdl --output ./circuit.py
```

Persistent install:

```bash
uv tool install ./tool
schemdraw-tool render --input ./circuit.sdl --output ./circuit.svg
```

List installed classes locally instead of browsing docs:

```bash
schemdraw-tool list --module elements
schemdraw-tool list --module logic
schemdraw-tool list --module flow
```

## File Rules

- one statement per line
- blank lines are ignored
- `#` starts a comment
- values with spaces should be quoted
- tuples should not contain spaces, for example `(0,-2)` or `(-0.6,0.2)`

## Statements

### Backend

```text
use svg
```

Currently, `svg` is the intended default and primary path.

### Theme

```text
theme monokai
```

### Drawing Config

```text
config unit=2.5 fontsize=14 color=navy bgcolor=white
```

Supported config keys are passed directly to `Drawing.config(...)`.

### Element Statement

Unnamed element:

```text
Resistor label="100KΩ"
```

Named element:

```text
let R1 = Resistor label="100KΩ"
```

Named elements can be referenced later through anchors such as `R1.start`, `R1.end`, `Q1.base`, or `OP.out`.

## Element Names

- plain names resolve through `schemdraw.elements`, for example `Resistor`, `Capacitor`, `Line`, `Ground`, `Opamp`
- dotted names are supported for other Schemdraw modules:
  - `flow.Box`
  - `logic.And`
  - `dsp.Amp`

## Supported Element Keys

Constructor kwargs:

- any unknown `key=value` pair is passed to the element constructor
- example: `Capacitor polar=true`

Placement and orientation keys:

- `dir=up|down|left|right`
- `len=<number>`
- `theta=<degrees>`
- `at=<point-or-anchor>`
- `to=<point-or-anchor>`
- `tox=<point-or-anchor>`
- `toy=<point-or-anchor>`
- `endpoints=<point-or-anchor>;<point-or-anchor>`
- `anchor=<anchor-name>`
- `drop=<anchor-name>`
- `hold=true|false`
- `flip=true|false`
- `reverse=true|false`
- `shift=<number>`

Label and style keys:

- `label=<text>`
- `loc=<label-location>`
- `ofst=<float-or-tuple>`
- `rotate=true|false|<degrees>`
- `color=<color>`
- `fill=<color-or-bool>`
- `linewidth=<number>`
- `linestyle=-|--|:|-.`
- `font=<font-name>`
- `fontsize=<number>`

## Value Forms

Booleans:

```text
true
false
```

Numbers:

```text
2
2.5
-0.6
```

Tuples:

```text
(0,0)
(-0.6,0.2)
```

Anchor references:

```text
R1.start
Q1.base
OP.out
```

## Example: Basic RC Supply Loop

```text
use svg
config unit=3 fontsize=14

let R1 = Resistor label="100KΩ"
let C1 = Capacitor dir=down label="0.1μF" loc=bottom
Line dir=left
Ground
SourceV dir=up label="10V"
```

## Example: Anchor Placement

```text
use svg

let OP = Opamp
Resistor dir=right at=OP.out label="Rf"
Line dir=down at=OP.in1
Ground
```

## Example: Closing A Loop

```text
use svg

let C1 = Capacitor
Diode
Line dir=down
Line tox=C1.start
Source dir=up
```

## Practical Guidance

- use `let` whenever a later anchor reference is likely
- prefer `tox` and `toy` over hand-computed coordinates for loop closing
- prefer `anchor=` and `at=` over raw cursor motion
- if you need more than one label or more than one annotation strategy, move to Python
