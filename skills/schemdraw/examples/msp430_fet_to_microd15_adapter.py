import schemdraw
import schemdraw.elements as elm

from helpers.connectors import micro_d15
from helpers.pinmap import ConnectionDef, connect_by_signal, signal_anchor_name
from helpers.protocols import MSP430_FET_14PIN_PIN_MAP, msp430_fet_14pin_header, pin_map_pin_defs
from helpers.schema import EndpointSchema, HarnessSchema, validate_harness_schema


MICRO_D15_SIGNALS = (
    "TDO_TDI",
    "VCC_TOOL",
    "TDI_VPP",
    "VCC_TARGET",
    "TMS",
    "NC",
    "TCK",
    "TEST_VPP",
    "GND",
    "AUX_CTS_SCL",
    "RST",
    "AUX_TXD_SDA",
    "AUX_RTS",
    "AUX_RXD_SIMO",
    "NC15",
)

CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for signal in MICRO_D15_SIGNALS if not signal.startswith("NC")]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.85, fontsize=8)
    left_pins = pin_map_pin_defs(MSP430_FET_14PIN_PIN_MAP, odd_side="right", even_side="left")
    right_pins = pin_map_pin_defs(tuple((str(index + 1), signal) for index, signal in enumerate(MICRO_D15_SIGNALS)), odd_side="left", even_side="left")
    schema = HarnessSchema(
        name="MSP430 FET to Micro-D 15 adapter",
        left=EndpointSchema(family="TI MSP430 14-pin FET", pin_count=14, pin_map=MSP430_FET_14PIN_PIN_MAP),
        right=EndpointSchema(family="Micro-D 15 service adapter", pin_count=15, exact_signals=MICRO_D15_SIGNALS),
        required_connections=tuple((signal, signal) for signal in MICRO_D15_SIGNALS if not signal.startswith("NC")),
    )
    validate_harness_schema("MSP-FET", left_pins, "MICRO-D", right_pins, CONNECTIONS, schema)
    with d:
        pod = msp430_fet_14pin_header("MSP-FET", at=(0, 0))
        microd = micro_d15("MICRO-D", list(MICRO_D15_SIGNALS), at=(12, 0), side="left")
        connect_by_signal(pod, microd, CONNECTIONS)
        elm.Line().at(getattr(microd, signal_anchor_name("NC15"))).length(1.0).label("spare", loc="bottom")
    return d


if __name__ == "__main__":
    build().save("msp430_fet_to_microd15_adapter.svg")
