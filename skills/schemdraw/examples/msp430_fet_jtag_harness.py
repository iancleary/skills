import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import MSP430_FET_14PIN_PIN_MAP, msp430_fet_14pin_header, msp430_fet_14pin_link_schema, pin_map_pin_defs
from helpers.schema import validate_harness_schema


CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for _, signal in MSP430_FET_14PIN_PIN_MAP]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.9, fontsize=8)
    left_pins = pin_map_pin_defs(MSP430_FET_14PIN_PIN_MAP, odd_side="right", even_side="left")
    right_pins = pin_map_pin_defs(MSP430_FET_14PIN_PIN_MAP, odd_side="left", even_side="right")
    validate_harness_schema("MSP-FET", left_pins, "TARGET HDR", right_pins, CONNECTIONS, msp430_fet_14pin_link_schema())
    with d:
        pod = msp430_fet_14pin_header("MSP-FET", at=(0, 0))
        target = msp430_fet_14pin_header("TARGET HDR", at=(11, 0))
        connect_by_signal(pod, target, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("msp430_fet_jtag_harness.svg")
