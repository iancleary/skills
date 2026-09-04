import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import I2C_SIGNALS, i2c_header, i2c_multidrop_schema, signal_pin_defs
from helpers.schema import BusParticipant, validate_bus_schema


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

    controller_pins = signal_pin_defs(I2C_SIGNALS, side="right")
    sensor_pins = signal_pin_defs(I2C_SIGNALS, side="left")
    eeprom_pins = signal_pin_defs(I2C_SIGNALS, side="left")
    validate_bus_schema(
        [
            BusParticipant(
                label="MCU",
                role="controller",
                pins=tuple(controller_pins),
                pullup_policy="present",
            ),
            BusParticipant(
                label="SENSOR",
                role="target",
                pins=tuple(sensor_pins),
                pullup_policy="absent",
            ),
            BusParticipant(
                label="EEPROM",
                role="target",
                pins=tuple(eeprom_pins),
                pullup_policy="absent",
            ),
        ],
        i2c_multidrop_schema(),
    )

    with d:
        mcu = i2c_header("MCU", side="right")
        sensor = i2c_header("SENSOR", at=(8, 2), side="left")
        eeprom = i2c_header("EEPROM", at=(8, -2), side="left")
        connect_by_signal(mcu, sensor, CONNECTIONS)
        connect_by_signal(mcu, eeprom, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("i2c_multidrop.svg")
