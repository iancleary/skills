# Schemdraw Reference

This file condenses the official Schemdraw usage docs into the parts Codex needs most often.

Primary sources:

- Getting started: <https://schemdraw.readthedocs.io/en/stable/usage/start.html>
- Placement: <https://schemdraw.readthedocs.io/en/stable/usage/placement.html>
- Labels: <https://schemdraw.readthedocs.io/en/stable/usage/labels.html>
- Styling: <https://schemdraw.readthedocs.io/en/stable/usage/styles.html>
- Backends: <https://schemdraw.readthedocs.io/en/stable/usage/backends.html>

## Core Pattern

Default imports:

```python
import schemdraw
import schemdraw.elements as elm
```

Basic structure:

```python
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

with schemdraw.Drawing() as d:
    elm.Resistor().label('100KΩ')
    elm.Capacitor().down().label('0.1μF', loc='bottom')
    elm.Line().left()
    elm.Ground()
    elm.SourceV().up().label('10V')

d.save('circuit.svg')
```

Key documented behaviors:

- A `Drawing` keeps a current position and direction.
- New elements start where the previous element ended unless you change placement.
- Direction methods such as `.up()`, `.down()`, `.left()`, and `.right()` also set the direction for following elements.
- `.theta(angle)` sets an arbitrary angle in degrees.

## Placement

Anchors:

- placed elements expose anchors as attributes, for example `Q.base`, `Q.collector`, `R.start`, `R.end`, and `R.center`
- anchors are available after the element has been placed in the drawing

Common placement methods:

- `.at(anchor_or_point)`: place an element at a specific anchor or coordinate
- `.anchor(name)`: align a named anchor of the new element to the current position
- `.hold()`: place without moving the drawing cursor
- `.drop(name)`: leave the cursor at a specific anchor after placing the element
- `Drawing.hold()`: temporarily save and restore drawing state
- `Drawing.move(dx=..., dy=...)` and `Drawing.move_from(point, dx=..., dy=...)`: explicit cursor moves

Two-terminal methods:

- `.length(n)`: exact length
- `.up(n)`, `.down(n)`, `.left(n)`, `.right(n)`: direction plus optional length
- `.to(anchor_or_point)`: exact endpoint
- `.tox(anchor_or_point)`: extend horizontally to a target x-coordinate
- `.toy(anchor_or_point)`: extend vertically to a target y-coordinate
- `.endpoints(a, b)`: explicit start and end points
- `.shift(value)`: shift the element off center between endpoints

Orientation methods:

- `.flip()`: flip the symbol orientation
- `.reverse()`: reverse directional symbols like diodes

Connections:

- use `elm.Line()` for simple connections
- use `elm.Wire(shape)` for routed connections
- documented wire shapes: `-`, `-|`, `|-`, `n`, `c`, `z`, `N`
- arrow strings may use `<`, `>`, `|`, and `o`
- two-terminal elements support `.dot()` and `.idot()` for connection dots

## Labels

Labels are added with `.label(...)`.

Important documented options:

- `loc='top'|'bottom'|'left'|'right'|<anchor>`
- `rotate=True` to follow the element angle
- `rotate=<degrees>` for explicit rotation
- `ofst=<float>` or `ofst=(x, y)` for offsets
- `color=...`
- `font=...`
- `fontsize=...`

Text rules:

- UTF-8 symbols such as `μ` and `Ω` are allowed if the font supports them
- LaTeX-style math can be used inside `$...$`
- labels stay horizontal by default

Useful annotation elements documented on the labels page:

- `elm.Label()`
- `elm.CurrentLabel()`
- `elm.CurrentLabelInline()`
- `elm.LoopArrow()`
- `elm.ZLabel()`
- `elm.Annotate()`
- `elm.Encircle()`
- `elm.EncircleBox()`

## Styling

Styling can be applied at three levels:

- global: `schemdraw.config(...)`
- per drawing: `d.config(...)`
- per element: chained methods such as `.color(...)`

Common style controls:

- `color`
- `fill`
- `linewidth`
- `linestyle`
- `font`
- `fontsize`
- `bgcolor`
- `unit` for the default two-terminal length at the drawing level

Documented hierarchy, highest priority first:

1. chained setter methods after instantiation
2. constructor keyword arguments
3. `Element.defaults` values set by the user
4. element-definition overrides
5. `Drawing.config`
6. `schemdraw.config`

Themes:

- `schemdraw.theme('default')`
- documented examples also include `dark`, `monokai`, `gruvboxd`, `gruvboxl`, and others

SVG-only styling features:

- `gradient_fill(...)`
- extra SVG defs through `Drawing.add_svgdef(...)`

## Backends

Schemdraw supports two documented backends:

- `svg`
- `matplotlib`

Default guidance for this skill:

- prefer `svg`
- switch to Matplotlib only when you explicitly need Matplotlib customization or non-SVG output flow

Use SVG globally:

```python
schemdraw.use('svg')
```

Or per drawing:

```python
with schemdraw.Drawing(canvas='svg') as d:
    ...
```

Important SVG settings:

- `schemdraw.svgconfig.text = 'text'` for searchable text
- `schemdraw.svgconfig.text = 'path'` for path-rendered text
- `schemdraw.svgconfig.svg2 = False` for better SVG 1.x compatibility
- `schemdraw.svgconfig.precision = 2` to control decimal precision

Math behavior:

- the SVG backend has basic math text support by default
- fuller LaTeX math support uses `ziamath` and `latex2mathml`

## Practical Defaults For Codex

Prefer these defaults unless the task says otherwise:

- backend: SVG
- import path: `schemdraw` plus `schemdraw.elements as elm`
- placement: anchors first, coordinates second
- styling: `Drawing.config(...)` for shared defaults, per-element methods for exceptions
- export: `.save('file.svg')`

## Common Examples

Loop closing with `tox`:

```python
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

with schemdraw.Drawing() as d:
    c1 = elm.Capacitor()
    elm.Diode()
    elm.Line().down()
    elm.Line().tox(c1.start)
    elm.Source().up()

d.save('loop.svg')
```

Anchor-based placement:

```python
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

with schemdraw.Drawing() as d:
    op = elm.Opamp()
    elm.Resistor().right().at(op.out).label('Rf')

d.save('opamp.svg')
```

## When To Leave SDL And Use Python

Switch from the local SDL to Python when:

- you need multiple labels on one element
- you need advanced annotations or SVG defs
- you need reusable helpers or loops
- the placement is easier to express with ordinary Python control flow
