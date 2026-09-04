import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import jtag_header, jtag_schema, signal_pin_defs
from helpers.schema import validate_harness_schema

SIGNALS = ("VTREF", "TMS", "TCK", "TDI", "TDO", "GND")

CONNECTIONS = [
    ConnectionDef("VTREF", label="VTREF", loc="top"),
    ConnectionDef("TMS", label="TMS", loc="top"),
    ConnectionDef("TCK", label="TCK", loc="top"),
    ConnectionDef("TDI", label="TDI", loc="top"),
    ConnectionDef("TDO", label="TDO", loc="bottom"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(SIGNALS, side="right")
    right_pins = signal_pin_defs(SIGNALS, side="left")
    validate_harness_schema("JTAG", left_pins, "FPGA", right_pins, CONNECTIONS, jtag_schema())
    with d:
        probe = jtag_header("JTAG", side="right")
        fpga = jtag_header("FPGA", at=(10, 0), side="left")
        connect_by_signal(probe, fpga, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("jtag_fpga.svg")
