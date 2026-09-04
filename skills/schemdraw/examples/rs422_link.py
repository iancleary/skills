import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import RS422_SIGNALS, rs422_endpoint, rs422_policy_schema, rs422_schema, signal_pin_defs
from helpers.schema import BusParticipant, validate_bus_schema, validate_harness_schema


CONNECTIONS = [
    ConnectionDef("TX_P", "RX_P", label="TX+", loc="top"),
    ConnectionDef("TX_N", "RX_N", label="TX-", loc="top"),
    ConnectionDef("RX_P", "TX_P", label="RX+", loc="bottom"),
    ConnectionDef("RX_N", "TX_N", label="RX-", loc="bottom"),
    ConnectionDef("GND", "GND", label="GND", loc="bottom"),
    ConnectionDef("SHIELD", "SHIELD", label="SHIELD", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.8, fontsize=9)
    left_pins = signal_pin_defs(RS422_SIGNALS, side="right")
    right_pins = signal_pin_defs(RS422_SIGNALS, side="left")
    validate_bus_schema(
        [
            BusParticipant(
                label="A",
                role="node_a",
                pins=tuple(left_pins),
                shield_policy="continuous",
                drain_policy="bonded",
                termination_policy="paired_rx",
            ),
            BusParticipant(
                label="B",
                role="node_b",
                pins=tuple(right_pins),
                shield_policy="continuous",
                drain_policy="floating",
                termination_policy="paired_rx",
            ),
        ],
        rs422_policy_schema(),
    )
    validate_harness_schema("A", left_pins, "B", right_pins, CONNECTIONS, rs422_schema())
    with d:
        a = rs422_endpoint("A", side="right")
        b = rs422_endpoint("B", at=(10, 0), side="left")
        connect_by_signal(a, b, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("rs422_link.svg")
