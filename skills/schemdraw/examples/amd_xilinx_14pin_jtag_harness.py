import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import (
    AMD_XILINX_14PIN_JTAG_PIN_MAP,
    amd_xilinx_14pin_jtag_header,
    amd_xilinx_14pin_jtag_link_schema,
    pin_map_pin_defs,
)
from helpers.schema import validate_harness_schema


CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for _, signal in AMD_XILINX_14PIN_JTAG_PIN_MAP]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.9, fontsize=8)
    left_pins = pin_map_pin_defs(AMD_XILINX_14PIN_JTAG_PIN_MAP, odd_side="right", even_side="left")
    right_pins = pin_map_pin_defs(AMD_XILINX_14PIN_JTAG_PIN_MAP, odd_side="left", even_side="right")
    validate_harness_schema(
        "CABLE",
        left_pins,
        "TARGET HDR",
        right_pins,
        CONNECTIONS,
        amd_xilinx_14pin_jtag_link_schema(),
    )
    with d:
        cable = amd_xilinx_14pin_jtag_header("CABLE", at=(0, 0))
        target = amd_xilinx_14pin_jtag_header("TARGET HDR", at=(11, 0))
        connect_by_signal(cable, target, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("amd_xilinx_14pin_jtag_harness.svg")
