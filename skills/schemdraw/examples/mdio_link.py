import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import MDIO_SIGNALS, mdio_header, mdio_schema, signal_pin_defs
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("MDC", label="MDC", loc="top"),
    ConnectionDef("MDIO", label="MDIO", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(MDIO_SIGNALS, side="right")
    right_pins = signal_pin_defs(MDIO_SIGNALS, side="left")
    validate_harness_schema("MAC", left_pins, "PHY", right_pins, CONNECTIONS, mdio_schema())
    with d:
        mac = mdio_header("MAC", side="right")
        phy = mdio_header("PHY", at=(8, 0), side="left")
        connect_by_signal(mac, phy, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("mdio_link.svg")
