from __future__ import annotations

import re
from dataclasses import dataclass

import schemdraw.elements as elm


@dataclass(frozen=True)
class PinDef:
    signal: str
    pin: str
    side: str = "right"
    anchor: str | None = None

    def to_ic_pin(self) -> elm.IcPin:
        anchorname = self.anchor or signal_anchor_name(self.signal)
        return elm.IcPin(
            name=self.signal,
            pin=self.pin,
            side=self.side,
            anchorname=anchorname,
        )


@dataclass(frozen=True)
class ConnectionDef:
    left_signal: str
    right_signal: str | None = None
    label: str | None = None
    loc: str = "top"


def signal_anchor_name(signal: str) -> str:
    value = signal.replace("+", "P").replace("-", "N")
    value = re.sub(r"[^0-9A-Za-z_]", "_", value)
    if value and value[0].isdigit():
        value = f"P{value}"
    return value


def validate_pin_defs(pins: list[PinDef]) -> None:
    if not pins:
        raise ValueError("endpoint requires at least one pin")

    pin_names: set[str] = set()
    anchor_names: set[str] = set()
    for pin in pins:
        if pin.pin in pin_names:
            raise ValueError(f"duplicate pin label: {pin.pin}")
        pin_names.add(pin.pin)

        anchor = signal_anchor(pin)
        if anchor in anchor_names:
            raise ValueError(f"duplicate anchor name: {anchor}")
        anchor_names.add(anchor)


def endpoint(label: str, pins: list[PinDef], *, at: tuple[float, float] | None = None) -> elm.Ic:
    validate_pin_defs(pins)
    part = elm.Ic(
        pins=[pin.to_ic_pin() for pin in pins],
        label=label,
    )
    if at is not None:
        part = part.at(at)
    return part


def signal_anchor(pin: PinDef) -> str:
    return pin.anchor or signal_anchor_name(pin.signal)


def connect_by_signal(left: elm.Ic, right: elm.Ic, connections: list[ConnectionDef]) -> None:
    for connection in connections:
        left_anchor = signal_anchor_name(connection.left_signal)
        right_signal = connection.right_signal or connection.left_signal
        right_anchor = signal_anchor_name(right_signal)
        line = elm.Line().at(getattr(left, left_anchor)).to(getattr(right, right_anchor))
        if connection.label:
            line.label(connection.label, loc=connection.loc)
