import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import ETHERNET_T568B_SIGNALS, ethernet_rj45, ethernet_schema, ethernet_variant_schema, signal_pin_defs
from helpers.schema import BusParticipant, validate_bus_schema, validate_harness_schema


CONNECTIONS = [
    ConnectionDef("TX+", label="TX+", loc="top"),
    ConnectionDef("TX-", label="TX-", loc="top"),
    ConnectionDef("RX+", label="RX+", loc="top"),
    ConnectionDef("BI1+", label="BI1+", loc="top"),
    ConnectionDef("BI1-", label="BI1-", loc="bottom"),
    ConnectionDef("RX-", label="RX-", loc="bottom"),
    ConnectionDef("BI2+", label="BI2+", loc="bottom"),
    ConnectionDef("BI2-", label="BI2-", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=9)
    left_pins = signal_pin_defs(ETHERNET_T568B_SIGNALS, side="right")
    right_pins = signal_pin_defs(ETHERNET_T568B_SIGNALS, side="left")
    validate_bus_schema(
        [
            BusParticipant(
                label="PSE",
                role="pse",
                pins=tuple(left_pins),
                shield_policy="chassis",
                poe_policy="pse_alt_a",
            ),
            BusParticipant(
                label="PD",
                role="pd",
                pins=tuple(right_pins),
                shield_policy="chassis",
                poe_policy="pd_alt_a",
            ),
        ],
        ethernet_variant_schema(shielded=True, poe_mode="alt_a"),
    )
    validate_harness_schema("PSE", left_pins, "PD", right_pins, CONNECTIONS, ethernet_schema())
    with d:
        pse = ethernet_rj45("PSE", side="right")
        pd = ethernet_rj45("PD", at=(10, 0), side="left")
        connect_by_signal(pse, pd, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("ethernet_poe_link.svg")
