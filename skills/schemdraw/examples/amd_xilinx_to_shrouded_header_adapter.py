import schemdraw

from helpers.connectors import shrouded_header_2x7
from helpers.pinmap import ConnectionDef, PinDef, connect_by_signal
from helpers.protocols import AMD_XILINX_14PIN_JTAG_PIN_MAP, amd_xilinx_14pin_jtag_header, pin_map_pin_defs
from helpers.schema import EndpointSchema, HarnessSchema, validate_harness_schema


HEADER_LEFT = ["GND1", "GND3", "GND5", "GND7", "GND9", "GND11", "PGND"]
HEADER_RIGHT = ["VREF", "TMS", "TCK", "TDO", "TDI", "NC", "SRST"]
HEADER_SIGNALS = tuple(HEADER_LEFT + HEADER_RIGHT)
CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for signal in HEADER_SIGNALS]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.9, fontsize=8)
    left_pins = pin_map_pin_defs(AMD_XILINX_14PIN_JTAG_PIN_MAP, odd_side="right", even_side="left")
    right_pins = [
        *[PinDef(signal, str(index * 2 + 1), side="left") for index, signal in enumerate(HEADER_LEFT)],
        *[PinDef(signal, str(index * 2 + 2), side="right") for index, signal in enumerate(HEADER_RIGHT)],
    ]
    schema = HarnessSchema(
        name="AMD/Xilinx 14-pin to shrouded 2x7 adapter",
        left=EndpointSchema(family="AMD/Xilinx 14-pin JTAG", pin_count=14, pin_map=AMD_XILINX_14PIN_JTAG_PIN_MAP),
        right=EndpointSchema(family="Shrouded 2x7 service header", pin_count=14, exact_signals=HEADER_SIGNALS),
        required_connections=tuple((signal, signal) for signal in HEADER_SIGNALS),
    )
    validate_harness_schema("CABLE", left_pins, "SERVICE HDR", right_pins, CONNECTIONS, schema)
    with d:
        cable = amd_xilinx_14pin_jtag_header("CABLE", at=(0, 0))
        service = shrouded_header_2x7("SERVICE HDR", HEADER_LEFT, HEADER_RIGHT, at=(12, 0))
        connect_by_signal(cable, service, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("amd_xilinx_to_shrouded_header_adapter.svg")
