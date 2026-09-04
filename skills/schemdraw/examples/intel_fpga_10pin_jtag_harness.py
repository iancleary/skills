import schemdraw

from helpers.pinmap import ConnectionDef, connect_by_signal
from helpers.protocols import (
    INTEL_FPGA_10PIN_JTAG_PIN_MAP,
    intel_fpga_10pin_jtag_header,
    intel_fpga_10pin_jtag_link_schema,
    pin_map_pin_defs,
)
from helpers.schema import validate_harness_schema


CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for _, signal in INTEL_FPGA_10PIN_JTAG_PIN_MAP]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.0, fontsize=8)
    left_pins = pin_map_pin_defs(INTEL_FPGA_10PIN_JTAG_PIN_MAP, odd_side="right", even_side="left")
    right_pins = pin_map_pin_defs(INTEL_FPGA_10PIN_JTAG_PIN_MAP, odd_side="left", even_side="right")
    validate_harness_schema(
        "DOWNLOAD CABLE",
        left_pins,
        "TARGET HDR",
        right_pins,
        CONNECTIONS,
        intel_fpga_10pin_jtag_link_schema(),
    )
    with d:
        cable = intel_fpga_10pin_jtag_header("DOWNLOAD CABLE", at=(0, 0))
        target = intel_fpga_10pin_jtag_header("TARGET HDR", at=(10, 0))
        connect_by_signal(cable, target, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("intel_fpga_10pin_jtag_harness.svg")
