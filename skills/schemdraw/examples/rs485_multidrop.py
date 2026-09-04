import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import RS485_2W_SIGNALS, rs485_2w_endpoint, rs485_multidrop_schema, signal_pin_defs
from helpers.schema import BusParticipant, validate_bus_schema


CONNECTIONS = [
    ConnectionDef("A", label="A", loc="top"),
    ConnectionDef("B", label="B", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
    ConnectionDef("SHIELD", label="SHIELD", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=9)

    master_pins = signal_pin_defs(RS485_2W_SIGNALS, side="right")
    drop_pins = signal_pin_defs(RS485_2W_SIGNALS, side="left")
    far_pins = signal_pin_defs(RS485_2W_SIGNALS, side="left")
    validate_bus_schema(
        [
            BusParticipant(
                label="MASTER",
                role="controller_end",
                pins=tuple(master_pins),
                shield_policy="continuous",
                drain_policy="bonded",
                termination_policy="present",
                bias_policy="present",
            ),
            BusParticipant(
                label="DROP",
                role="drop",
                pins=tuple(drop_pins),
                shield_policy="continuous",
                drain_policy="pass",
                termination_policy="absent",
                bias_policy="absent",
            ),
            BusParticipant(
                label="END NODE",
                role="far_end",
                pins=tuple(far_pins),
                shield_policy="continuous",
                drain_policy="floating",
                termination_policy="present",
                bias_policy="absent",
            ),
        ],
        rs485_multidrop_schema(),
    )

    with d:
        master = rs485_2w_endpoint("MASTER", side="right")
        drop = rs485_2w_endpoint("DROP", at=(8, 2), side="left")
        end = rs485_2w_endpoint("END NODE", at=(8, -2), side="left")
        connect_by_signal(master, drop, CONNECTIONS)
        connect_by_signal(master, end, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("rs485_multidrop.svg")
