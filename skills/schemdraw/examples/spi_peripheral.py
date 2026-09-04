import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import SPI_SIGNALS, signal_pin_defs, spi_header, spi_schema
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("CS_N", label="CS_N", loc="top"),
    ConnectionDef("SCLK", label="SCLK", loc="top"),
    ConnectionDef("MOSI", label="MOSI", loc="top"),
    ConnectionDef("MISO", label="MISO", loc="bottom"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(SPI_SIGNALS, side="right")
    right_pins = signal_pin_defs(SPI_SIGNALS, side="left")
    validate_harness_schema("MCU", left_pins, "SENSOR", right_pins, CONNECTIONS, spi_schema())
    with d:
        mcu = spi_header("MCU", side="right")
        sensor = spi_header("SENSOR", at=(10, 0), side="left")
        connect_by_signal(mcu, sensor, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("spi_peripheral.svg")
