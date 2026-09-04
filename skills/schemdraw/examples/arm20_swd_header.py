import schemdraw

from helpers.protocols import ARM_20PIN_SWD_PIN_MAP, arm_20pin_swd_header
from helpers.schema import validate_endpoint_schema
from helpers.protocols import pin_map_pin_defs, arm_20pin_swd_schema


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=10)
    validate_endpoint_schema(
        "ARM-20 SWD",
        pin_map_pin_defs(ARM_20PIN_SWD_PIN_MAP),
        arm_20pin_swd_schema(),
    )
    with d:
        arm_20pin_swd_header("ARM 20-pin SWD")
    return d


if __name__ == "__main__":
    build().save("arm20_swd_header.svg")
