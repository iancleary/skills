import schemdraw

from helpers.protocols import ARM_20PIN_JTAG_PIN_MAP, arm_20pin_jtag_header
from helpers.schema import validate_endpoint_schema
from helpers.protocols import arm_20pin_jtag_schema, pin_map_pin_defs


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=10)
    validate_endpoint_schema(
        "ARM-20 JTAG",
        pin_map_pin_defs(ARM_20PIN_JTAG_PIN_MAP),
        arm_20pin_jtag_schema(),
    )
    with d:
        arm_20pin_jtag_header("ARM 20-pin JTAG")
    return d


if __name__ == "__main__":
    build().save("arm20_jtag_header.svg")
