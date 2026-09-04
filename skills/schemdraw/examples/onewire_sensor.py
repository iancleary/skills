import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import ONEWIRE_SIGNALS, onewire_header, onewire_schema, signal_pin_defs
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("DQ", label="DQ", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(ONEWIRE_SIGNALS, side="right")
    right_pins = signal_pin_defs(ONEWIRE_SIGNALS, side="left")
    validate_harness_schema("HOST", left_pins, "1WIRE DEV", right_pins, CONNECTIONS, onewire_schema())
    with d:
        host = onewire_header("HOST", side="right")
        device = onewire_header("1WIRE DEV", at=(7, 0), side="left")
        connect_by_signal(host, device, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("onewire_sensor.svg")
