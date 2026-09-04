import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import PPS_SIGNALS, pps_header, pps_schema, signal_pin_defs
from helpers.schema import validate_harness_schema


CONNECTIONS = [
    ConnectionDef("VCC", label="VCC", loc="top"),
    ConnectionDef("PPS", label="PPS", loc="top"),
    ConnectionDef("GND", label="GND", loc="bottom"),
]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=10)
    left_pins = signal_pin_defs(PPS_SIGNALS, side="right")
    right_pins = signal_pin_defs(PPS_SIGNALS, side="left")
    validate_harness_schema("GPSDO", left_pins, "TIMEBASE", right_pins, CONNECTIONS, pps_schema())
    with d:
        gpsdo = pps_header("GPSDO", side="right")
        timebase = pps_header("TIMEBASE", at=(8, 0), side="left")
        connect_by_signal(gpsdo, timebase, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("pps_sync.svg")
