import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import I2C_SIGNALS, i2c_header, i2c_multidrop_schema, i2c_schema, signal_pin_defs
from helpers.schema import BusParticipant, validate_bus_schema, validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("SCL", label="SCL", loc="top"),
    ConnectionDef("SDA", label="SDA", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(I2C_SIGNALS, side="right")
    right_pins = signal_pin_defs(I2C_SIGNALS, side="left")
    validate_bus_schema(
        [
            BusParticipant(
                label="MCU",
                role="controller",
                pins=tuple(left_pins),
                pullup_policy="present",
            ),
            BusParticipant(
                label="SENSOR",
                role="target",
                pins=tuple(right_pins),
                pullup_policy="absent",
            ),
        ],
        i2c_multidrop_schema(),
    )
    validate_harness_schema("MCU", left_pins, "SENSOR", right_pins, CONNECTIONS, i2c_schema())
    with d:
        mcu = i2c_header("MCU", side="right")
        sensor = i2c_header("SENSOR", at=(8, 0), side="left")
        connect_by_signal(mcu, sensor, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("i2c_sensor.svg")
