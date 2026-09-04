from __future__ import annotations

import argparse
import ast
import importlib
import json
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import schemdraw
import schemdraw.elements as elm


MODULE_ALIASES = {
    "elm": "schemdraw.elements",
    "elements": "schemdraw.elements",
    "intcircuits": "schemdraw.elements.intcircuits",
    "flow": "schemdraw.flow",
    "logic": "schemdraw.logic",
    "dsp": "schemdraw.dsp",
    "timing": "schemdraw.logic.timing",
    "bitfield": "schemdraw.logic.bitfield",
    "pictorial": "schemdraw.pictorial",
}

STYLE_METHODS = {
    "color",
    "fill",
    "linewidth",
    "linestyle",
}

LABEL_KWARGS = {
    "loc",
    "ofst",
    "rotate",
    "font",
    "fontsize",
    "color",
    "halign",
    "valign",
}


@dataclass
class BackendStmt:
    backend: str


@dataclass
class ThemeStmt:
    name: str


@dataclass
class ConfigStmt:
    values: dict[str, Any]


@dataclass
class ElementStmt:
    name: str | None
    element: str
    attrs: dict[str, Any]


Statement = BackendStmt | ThemeStmt | ConfigStmt | ElementStmt


def parse_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "none":
        return None
    if raw.startswith(("(", "[", "{", "'", '"')) or raw.replace(".", "", 1).replace("-", "", 1).isdigit():
        try:
            return ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            pass
    return raw


def split_key_value(token: str) -> tuple[str, Any]:
    if "=" not in token:
        raise ValueError(f"expected key=value token, got: {token}")
    key, raw = token.split("=", 1)
    return key, parse_value(raw)


def parse_line(line: str, line_number: int) -> Statement | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    parts = shlex.split(stripped, comments=True, posix=True)
    if not parts:
        return None

    head = parts[0]
    if head == "use":
        if len(parts) != 2:
            raise ValueError(f"line {line_number}: use expects one backend name")
        return BackendStmt(parts[1])
    if head == "theme":
        if len(parts) != 2:
            raise ValueError(f"line {line_number}: theme expects one theme name")
        return ThemeStmt(parts[1])
    if head == "config":
        values = dict(split_key_value(token) for token in parts[1:])
        return ConfigStmt(values)

    name: str | None = None
    index = 0
    if head == "let":
        if len(parts) < 4 or parts[2] != "=":
            raise ValueError(f"line {line_number}: let statements must look like 'let NAME = Element ...'")
        name = parts[1]
        index = 3

    element = parts[index]
    attrs = dict(split_key_value(token) for token in parts[index + 1 :])
    return ElementStmt(name=name, element=element, attrs=attrs)


def parse_sdl(text: str) -> list[Statement]:
    statements: list[Statement] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        stmt = parse_line(line, line_number)
        if stmt is not None:
            statements.append(stmt)
    return statements


def resolve_element_class(name: str) -> type[Any]:
    if "." not in name:
        return getattr(elm, name)

    module_alias, class_name = name.split(".", 1)
    module_name = MODULE_ALIASES.get(module_alias, f"schemdraw.{module_alias}")
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def resolve_ref(value: Any, env: dict[str, Any]) -> Any:
    if isinstance(value, str) and "." in value:
        object_name, anchor_name = value.split(".", 1)
        if object_name in env:
            return getattr(env[object_name], anchor_name)
    return value


def apply_direction(obj: Any, direction: str, length: Any | None) -> Any:
    method = getattr(obj, direction)
    return method(length) if length is not None else method()


def apply_element(stmt: ElementStmt, env: dict[str, Any]) -> Any:
    attrs = dict(stmt.attrs)
    label_text = attrs.pop("label", None)
    label_kwargs = {key: attrs.pop(key) for key in list(attrs) if key in LABEL_KWARGS}

    constructor_kwargs: dict[str, Any] = {}
    for key in list(attrs):
        if key in {
            "dir",
            "len",
            "theta",
            "at",
            "to",
            "tox",
            "toy",
            "endpoints",
            "anchor",
            "drop",
            "hold",
            "flip",
            "reverse",
            "shift",
        }:
            continue
        if key in STYLE_METHODS:
            continue
        constructor_kwargs[key] = attrs.pop(key)

    obj = resolve_element_class(stmt.element)(**constructor_kwargs)

    if "at" in attrs:
        obj = obj.at(resolve_ref(attrs.pop("at"), env))
    if "anchor" in attrs:
        obj = obj.anchor(attrs.pop("anchor"))

    direction = attrs.pop("dir", None)
    length = attrs.pop("len", None)
    theta = attrs.pop("theta", None)
    if direction is not None:
        obj = apply_direction(obj, direction, length)
        length = None
    elif theta is not None:
        obj = obj.theta(theta)

    if length is not None and hasattr(obj, "length"):
        obj = obj.length(length)
    if "to" in attrs:
        obj = obj.to(resolve_ref(attrs.pop("to"), env))
    if "tox" in attrs:
        obj = obj.tox(resolve_ref(attrs.pop("tox"), env))
    if "toy" in attrs:
        obj = obj.toy(resolve_ref(attrs.pop("toy"), env))
    if "endpoints" in attrs:
        raw = attrs.pop("endpoints")
        if not isinstance(raw, str) or ";" not in raw:
            raise ValueError("endpoints expects REF1;REF2")
        start_raw, end_raw = raw.split(";", 1)
        obj = obj.endpoints(resolve_ref(parse_value(start_raw), env), resolve_ref(parse_value(end_raw), env))
    if "drop" in attrs:
        obj = obj.drop(attrs.pop("drop"))
    if "shift" in attrs:
        obj = obj.shift(attrs.pop("shift"))
    if attrs.pop("flip", False):
        obj = obj.flip()
    if attrs.pop("reverse", False):
        obj = obj.reverse()
    if attrs.pop("hold", False):
        obj = obj.hold()

    for method_name in STYLE_METHODS:
        if method_name in attrs:
            obj = getattr(obj, method_name)(attrs.pop(method_name))

    if label_text is not None:
        obj = obj.label(label_text, **label_kwargs)

    if attrs:
        unknown = ", ".join(sorted(attrs))
        raise ValueError(f"unsupported SDL keys: {unknown}")

    if stmt.name is not None:
        env[stmt.name] = obj
    return obj


def render_sdl(input_path: Path, output_path: Path) -> None:
    statements = parse_sdl(input_path.read_text())
    env: dict[str, Any] = {}
    backend = "svg"
    drawing_config: dict[str, Any] = {}

    for stmt in statements:
        if isinstance(stmt, BackendStmt):
            backend = stmt.backend
        elif isinstance(stmt, ThemeStmt):
            schemdraw.theme(stmt.name)
        elif isinstance(stmt, ConfigStmt):
            drawing_config.update(stmt.values)

    if backend != "svg":
        raise ValueError("the bundled tool currently supports svg output only")

    schemdraw.use("svg")
    with schemdraw.Drawing() as drawing:
        if drawing_config:
            drawing.config(**drawing_config)
        for stmt in statements:
            if isinstance(stmt, ElementStmt):
                apply_element(stmt, env)
    drawing.save(output_path)


def load_python_drawing(input_path: Path) -> Any:
    namespace: dict[str, Any] = {"__name__": "__schemdraw_tool__", "__file__": str(input_path)}
    code = compile(input_path.read_text(), str(input_path), "exec")
    added_path = False
    input_dir = str(input_path.parent.resolve())
    if input_dir not in sys.path:
        sys.path.insert(0, input_dir)
        added_path = True
    try:
        exec(code, namespace)
    finally:
        if added_path and sys.path and sys.path[0] == input_dir:
            sys.path.pop(0)

    if callable(namespace.get("build")):
        return namespace["build"]()
    for candidate in ("drawing", "d"):
        if candidate in namespace:
            return namespace[candidate]
    raise ValueError("python input must define build(), drawing, or d")


def render_python(input_path: Path, output_path: Path) -> None:
    drawing = load_python_drawing(input_path)
    if not hasattr(drawing, "save"):
        raise ValueError("python input did not produce a Schemdraw Drawing")
    drawing.save(output_path)


def render_timing_json(input_path: Path, output_path: Path) -> None:
    from schemdraw import logic

    data = json.loads(input_path.read_text())
    schemdraw.use("svg")
    with schemdraw.Drawing() as drawing:
        logic.TimingDiagram(data)
    drawing.save(output_path)


def render_bitfield_json(input_path: Path, output_path: Path) -> None:
    from schemdraw.logic import bitfield

    data = json.loads(input_path.read_text())
    schemdraw.use("svg")
    with schemdraw.Drawing() as drawing:
        bitfield.BitField(data)
    drawing.save(output_path)


def module_name_for(alias: str) -> str:
    return MODULE_ALIASES.get(alias, alias)


def list_module_symbols(alias: str, contains: str | None, output_json: bool) -> str:
    module = importlib.import_module(module_name_for(alias))
    names = sorted(
        name
        for name, value in vars(module).items()
        if not name.startswith("_") and isinstance(value, type)
    )
    if contains:
        lowered = contains.lower()
        names = [name for name in names if lowered in name.lower()]

    if output_json:
        return json.dumps(
            {
                "module": module.__name__,
                "count": len(names),
                "symbols": names,
            },
            separators=(",", ":"),
        )
    return "\n".join(names) + ("\n" if names else "")


def generate_python(statements: list[Statement], output_name: str = "output.svg") -> str:
    module_aliases = {
        stmt.element.split(".", 1)[0]
        for stmt in statements
        if isinstance(stmt, ElementStmt) and "." in stmt.element
    }
    themes = [stmt.name for stmt in statements if isinstance(stmt, ThemeStmt)]
    extra_imports = [
        f"import schemdraw.{alias} as {alias}"
        for alias in sorted(module_aliases)
    ]
    lines = [
        "import schemdraw",
        "import schemdraw.elements as elm",
        *extra_imports,
        "",
        "",
        "def build():",
        "    schemdraw.use('svg')",
        *[f"    schemdraw.theme({theme!r})" for theme in themes],
        "    d = schemdraw.Drawing()",
        "    with d:",
    ]

    for stmt in statements:
        if isinstance(stmt, ConfigStmt):
            kwargs = ", ".join(f"{key}={value!r}" for key, value in stmt.values.items())
            lines.append(f"        d.config({kwargs})")
        elif isinstance(stmt, ElementStmt):
            expr = build_element_expr(stmt)
            if stmt.name:
                lines.append(f"        {stmt.name} = {expr}")
            else:
                lines.append(f"        {expr}")

    lines.extend(
        [
            "    return d",
            "",
            "",
            "def main():",
            "    drawing = build()",
            f"    drawing.save({output_name!r})",
            "",
            "",
            "if __name__ == '__main__':",
            "    main()",
        ]
    )
    return "\n".join(lines) + "\n"


def build_element_expr(stmt: ElementStmt) -> str:
    attrs = dict(stmt.attrs)
    label_text = attrs.pop("label", None)
    label_kwargs = {key: attrs.pop(key) for key in list(attrs) if key in LABEL_KWARGS}

    constructor_kwargs: dict[str, Any] = {}
    for key in list(attrs):
        if key in {
            "dir",
            "len",
            "theta",
            "at",
            "to",
            "tox",
            "toy",
            "endpoints",
            "anchor",
            "drop",
            "hold",
            "flip",
            "reverse",
            "shift",
        }:
            continue
        if key in STYLE_METHODS:
            continue
        constructor_kwargs[key] = attrs.pop(key)

    if "." in stmt.element:
        expr = stmt.element
    else:
        expr = f"elm.{stmt.element}"

    if constructor_kwargs:
        args = ", ".join(f"{key}={value!r}" for key, value in constructor_kwargs.items())
        expr = f"{expr}({args})"
    else:
        expr = f"{expr}()"

    if "at" in attrs:
        expr += f".at({render_ref(attrs.pop('at'))})"
    if "anchor" in attrs:
        expr += f".anchor({attrs.pop('anchor')!r})"

    direction = attrs.pop("dir", None)
    length = attrs.pop("len", None)
    theta = attrs.pop("theta", None)
    if direction is not None:
        if length is None:
            expr += f".{direction}()"
        else:
            expr += f".{direction}({length!r})"
        length = None
    elif theta is not None:
        expr += f".theta({theta!r})"

    if length is not None:
        expr += f".length({length!r})"
    if "to" in attrs:
        expr += f".to({render_ref(attrs.pop('to'))})"
    if "tox" in attrs:
        expr += f".tox({render_ref(attrs.pop('tox'))})"
    if "toy" in attrs:
        expr += f".toy({render_ref(attrs.pop('toy'))})"
    if "endpoints" in attrs:
        raw = attrs.pop("endpoints")
        start_raw, end_raw = str(raw).split(";", 1)
        expr += f".endpoints({render_ref(parse_value(start_raw))}, {render_ref(parse_value(end_raw))})"
    if "drop" in attrs:
        expr += f".drop({attrs.pop('drop')!r})"
    if "shift" in attrs:
        expr += f".shift({attrs.pop('shift')!r})"
    if attrs.pop("flip", False):
        expr += ".flip()"
    if attrs.pop("reverse", False):
        expr += ".reverse()"
    if attrs.pop("hold", False):
        expr += ".hold()"

    for method_name in sorted(STYLE_METHODS):
        if method_name in attrs:
            expr += f".{method_name}({attrs.pop(method_name)!r})"

    if label_text is not None:
        if label_kwargs:
            kwargs = ", ".join(f"{key}={value!r}" for key, value in label_kwargs.items())
            expr += f".label({label_text!r}, {kwargs})"
        else:
            expr += f".label({label_text!r})"

    return expr


def render_ref(value: Any) -> str:
    if isinstance(value, str) and "." in value:
        object_name, anchor_name = value.split(".", 1)
        return f"{object_name}.{anchor_name}"
    return repr(value)


def infer_mode(input_path: Path, explicit_mode: str) -> str:
    if explicit_mode != "auto":
        return explicit_mode
    if input_path.suffix == ".py":
        return "python"
    if input_path.suffix == ".json":
        return "timing-json"
    return "sdl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="schemdraw-tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render = subparsers.add_parser("render")
    render.add_argument("--input", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    render.add_argument(
        "--mode",
        choices=["auto", "python", "sdl", "timing-json", "bitfield-json"],
        default="auto",
    )

    to_python = subparsers.add_parser("to-python")
    to_python.add_argument("--input", required=True, type=Path)
    to_python.add_argument("--output", type=Path)

    list_cmd = subparsers.add_parser("list")
    list_cmd.add_argument("--module", required=True)
    list_cmd.add_argument("--contains")
    list_cmd.add_argument("--json", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "render":
            mode = infer_mode(args.input, args.mode)
            if mode == "python":
                render_python(args.input, args.output)
            elif mode == "timing-json":
                render_timing_json(args.input, args.output)
            elif mode == "bitfield-json":
                render_bitfield_json(args.input, args.output)
            else:
                render_sdl(args.input, args.output)
            return 0

        if args.command == "to-python":
            statements = parse_sdl(args.input.read_text())
            rendered = generate_python(statements)
            if args.output is not None:
                args.output.write_text(rendered)
            else:
                sys.stdout.write(rendered)
            return 0

        if args.command == "list":
            sys.stdout.write(list_module_symbols(args.module, args.contains, args.json))
            return 0
    except Exception as exc:  # pragma: no cover - CLI path
        print(f"schemdraw-tool: {exc}", file=sys.stderr)
        return 1

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
