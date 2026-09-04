import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import SPACEWIRE_SIGNALS, signal_pin_defs, spacewire_endpoint, spacewire_schema
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("TXD_P", "RXD_P", label="D+", loc="top"),
    ConnectionDef("TXD_N", "RXD_N", label="D-", loc="top"),
    ConnectionDef("TXS_P", "RXS_P", label="S+", loc="top"),
    ConnectionDef("TXS_N", "RXS_N", label="S-", loc="top"),
    ConnectionDef("RXD_P", "TXD_P", label="D+", loc="bottom"),
    ConnectionDef("RXD_N", "TXD_N", label="D-", loc="bottom"),
    ConnectionDef("RXS_P", "TXS_P", label="S+", loc="bottom"),
    ConnectionDef("RXS_N", "TXS_N", label="S-", loc="bottom"),
    ConnectionDef("GND", "GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.8, fontsize=9)
    left_pins = signal_pin_defs(SPACEWIRE_SIGNALS, side="right")
    right_pins = signal_pin_defs(SPACEWIRE_SIGNALS, side="left")
    validate_harness_schema("NODE A", left_pins, "NODE B", right_pins, CONNECTIONS, spacewire_schema())
    with d:
        node_a = spacewire_endpoint("NODE A", side="right")
        node_b = spacewire_endpoint("NODE B", at=(12, 0), side="left")
        connect_by_signal(node_a, node_b, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("spacewire_link.svg")
