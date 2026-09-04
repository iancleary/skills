import schemdraw

from helpers.connectors import circular10
from helpers.pinmap import ConnectionDef, PinDef, connect_by_signal
from helpers.protocols import INTEL_FPGA_10PIN_JTAG_PIN_MAP, intel_fpga_10pin_jtag_header, pin_map_pin_defs
from helpers.schema import EndpointSchema, HarnessSchema, validate_harness_schema


CIRCULAR10_SIGNALS = (
    "TCK",
    "GND2",
    "TDO",
    "VCC_TARGET",
    "TMS",
    "PROC_RST",
    "NC7",
    "NC8",
    "TDI",
    "GND10",
)

CONNECTIONS = [ConnectionDef(signal, label=signal, loc="top" if "GND" not in signal else "bottom") for signal in CIRCULAR10_SIGNALS]


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=1.95, fontsize=8)
    left_pins = pin_map_pin_defs(INTEL_FPGA_10PIN_JTAG_PIN_MAP, odd_side="right", even_side="left")
    right_pins = [PinDef(signal, str(index + 1), side="left") for index, signal in enumerate(CIRCULAR10_SIGNALS)]
    schema = HarnessSchema(
        name="Intel FPGA 10-pin to circular 10 adapter",
        left=EndpointSchema(
            family="Intel FPGA Download Cable II 10-pin JTAG",
            pin_count=10,
            pin_map=INTEL_FPGA_10PIN_JTAG_PIN_MAP,
        ),
        right=EndpointSchema(family="Circular 10 service connector", pin_count=10, exact_signals=CIRCULAR10_SIGNALS),
        required_connections=tuple((signal, signal) for signal in CIRCULAR10_SIGNALS),
    )
    validate_harness_schema("DOWNLOAD CABLE", left_pins, "CIRCULAR", right_pins, CONNECTIONS, schema)
    with d:
        cable = intel_fpga_10pin_jtag_header("DOWNLOAD CABLE", at=(0, 0))
        circular = circular10("CIRCULAR", list(CIRCULAR10_SIGNALS), at=(11, 0), side="left")
        connect_by_signal(cable, circular, CONNECTIONS)
    return d


if __name__ == "__main__":
    build().save("intel_fpga_to_circular10_adapter.svg")
