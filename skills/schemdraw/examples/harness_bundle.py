import schemdraw

from helpers.pinmap import ConnectionDef, PinDef, connect_by_signal, endpoint
from helpers.schema import EndpointSchema, HarnessSchema, validate_harness_schema


CONTROLLER_PINS = [
    PinDef("TXD", "1"),
    PinDef("RXD", "2"),
    PinDef("GND", "3"),
    PinDef("12V", "4", anchor="P12V"),
]

PAYLOAD_PINS = [
    PinDef("TX", "A", side="left"),
    PinDef("RX", "B", side="left"),
    PinDef("GND", "C", side="left"),
    PinDef("12V", "D", side="left", anchor="P12V"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.3, fontsize=11)
    schema = HarnessSchema(
        name="Controller to payload harness",
        left=EndpointSchema(
            family="Controller endpoint",
            pin_count=4,
            exact_signals=("TXD", "RXD", "GND", "12V"),
        ),
        right=EndpointSchema(
            family="Payload endpoint",
            pin_count=4,
            exact_signals=("TX", "RX", "GND", "12V"),
        ),
        required_connections=(
            ("TXD", "TX"),
            ("RXD", "RX"),
            ("GND", "GND"),
            ("12V", "12V"),
        ),
    )
    connections = [
        ConnectionDef("TXD", "TX", label="TX", loc="top"),
        ConnectionDef("RXD", "RX", label="RX", loc="top"),
        ConnectionDef("GND", label="GND", loc="bottom"),
        ConnectionDef("12V", label="12V", loc="bottom"),
    ]
    validate_harness_schema("Controller", CONTROLLER_PINS, "Payload J1", PAYLOAD_PINS, connections, schema)
    with d:
        controller = endpoint("Controller", CONTROLLER_PINS)
        payload = endpoint("Payload J1", PAYLOAD_PINS, at=(8, 0))
        connect_by_signal(controller, payload, connections)
    return d


if __name__ == "__main__":
    build().save("harness_bundle.svg")
