import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import signal_pin_defs, swd_header, swd_schema
from helpers.schema import validate_harness_schema


SIGNALS = ("VTREF", "SWDIO", "SWCLK", "NRST", "GND")
CONNECTIONS = [
    ConnectionDef("VTREF", label="VTREF", loc="top"),
    ConnectionDef("SWDIO", label="SWDIO", loc="top"),
    ConnectionDef("SWCLK", label="SWCLK", loc="top"),
    ConnectionDef("NRST", label="NRST", loc="bottom"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(SIGNALS, side="right")
    right_pins = signal_pin_defs(SIGNALS, side="left")
    validate_harness_schema("DEBUG", left_pins, "MCU", right_pins, CONNECTIONS, swd_schema())
    with d:
        debug = swd_header("DEBUG", side="right")
        mcu = swd_header("MCU", at=(9, 0), side="left")
        connect_by_signal(debug, mcu, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("swd_programming.svg")
