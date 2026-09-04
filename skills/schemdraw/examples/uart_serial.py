import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import UART_SIGNALS, signal_pin_defs, uart_header, uart_schema
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("TX", label="TX", loc="top"),
    ConnectionDef("RX", label="RX", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(UART_SIGNALS, side="right")
    right_pins = signal_pin_defs(UART_SIGNALS, side="left")
    validate_harness_schema("UART HOST", left_pins, "UART TARGET", right_pins, CONNECTIONS, uart_schema())
    with d:
        host = uart_header("UART HOST", side="right")
        target = uart_header("UART TARGET", at=(8, 0), side="left")
        connect_by_signal(host, target, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("uart_serial.svg")
