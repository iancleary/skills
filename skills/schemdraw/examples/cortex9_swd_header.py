import schemdraw

from helpers.protocols import CORTEX_9PIN_SWD_PIN_MAP, cortex_9pin_swd_header
from helpers.schema import validate_endpoint_schema
from helpers.protocols import cortex_9pin_swd_schema, pin_map_pin_defs


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=10)
    validate_endpoint_schema(
        "Cortex-9 SWD",
        pin_map_pin_defs(CORTEX_9PIN_SWD_PIN_MAP),
        cortex_9pin_swd_schema(),
    )
    with d:
        cortex_9pin_swd_header("Cortex 9-pin SWD/JTAG")
    return d


if __name__ == "__main__":
    build().save("cortex9_swd_header.svg")
