from __future__ import annotations

from helpers.connectors import header_1x, header_2x, rj45_t568b, rj45_t568b_schema
from helpers.pinmap import PinDef, endpoint
from helpers.schema import BusSchema, EndpointSchema, HarnessSchema


def signal_pin_defs(signals: tuple[str, ...], *, side: str = "left") -> list[PinDef]:
    return [PinDef(signal, str(index + 1), side=side) for index, signal in enumerate(signals)]


def pin_map_pin_defs(
    pin_map: tuple[tuple[str, str], ...],
    *,
    odd_side: str = "left",
    even_side: str = "right",
) -> list[PinDef]:
    pins: list[PinDef] = []
    for pin, signal in pin_map:
        pin_number = int(str(pin))
        side = odd_side if pin_number % 2 else even_side
        pins.append(PinDef(signal, str(pin), side=side))
    return pins


def pin_map_endpoint(
    label: str,
    pin_map: tuple[tuple[str, str], ...],
    *,
    at: tuple[float, float] | None = None,
    odd_side: str = "left",
    even_side: str = "right",
):
    return endpoint(label, pin_map_pin_defs(pin_map, odd_side=odd_side, even_side=even_side), at=at)


def exact_endpoint_schema(family: str, signals: tuple[str, ...]) -> EndpointSchema:
    return EndpointSchema(
        family=family,
        pin_count=len(signals),
        exact_signals=signals,
    )


def pin_map_endpoint_schema(family: str, pin_map: tuple[tuple[str, str], ...]) -> EndpointSchema:
    return EndpointSchema(
        family=family,
        pin_count=len(pin_map),
        pin_map=pin_map,
    )


def pin_map_passthrough_schema(name: str, family: str, pin_map: tuple[tuple[str, str], ...]) -> HarnessSchema:
    endpoint_schema = pin_map_endpoint_schema(family, pin_map)
    return HarnessSchema(
        name=name,
        left=endpoint_schema,
        right=endpoint_schema,
        required_connections=tuple((signal, signal) for _, signal in pin_map),
    )


def passthrough_schema(name: str, family: str, signals: tuple[str, ...]) -> HarnessSchema:
    endpoint_schema = exact_endpoint_schema(family, signals)
    return HarnessSchema(
        name=name,
        left=endpoint_schema,
        right=endpoint_schema,
        required_connections=tuple((signal, signal) for signal in signals),
    )


def swd_signals(*, include_reset: bool = True, include_swo: bool = False) -> tuple[str, ...]:
    signals = ["VTREF", "SWDIO", "SWCLK"]
    if include_swo:
        signals.append("SWO")
    if include_reset:
        signals.append("NRST")
    signals.append("GND")
    return tuple(signals)


def swd_header(
    label: str,
    *,
    at: tuple[float, float] | None = None,
    side: str = "left",
    include_reset: bool = True,
    include_swo: bool = False,
):
    return header_1x(label, list(swd_signals(include_reset=include_reset, include_swo=include_swo)), at=at, side=side)


def swd_schema(*, include_reset: bool = True, include_swo: bool = False) -> HarnessSchema:
    signals = swd_signals(include_reset=include_reset, include_swo=include_swo)
    return passthrough_schema("SWD programming link", "SWD header", signals)


ARM_20PIN_SWD_PIN_MAP = (
    ("1", "VTREF"),
    ("2", "VSUPPLY"),
    ("3", "NC_TRST"),
    ("4", "GND"),
    ("5", "NC_TDI"),
    ("6", "GND"),
    ("7", "SWDIO"),
    ("8", "GND"),
    ("9", "SWCLK"),
    ("10", "GND"),
    ("11", "NC_RTCK"),
    ("12", "GND"),
    ("13", "SWO"),
    ("14", "RESERVED"),
    ("15", "NRESET"),
    ("16", "RESERVED"),
    ("17", "NC"),
    ("18", "RESERVED"),
    ("19", "P5V_TARGET"),
    ("20", "RESERVED"),
)


def arm_20pin_swd_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, ARM_20PIN_SWD_PIN_MAP, at=at)


def arm_20pin_swd_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("ARM 20-pin SWD", ARM_20PIN_SWD_PIN_MAP)


def jtag_signals(*, include_trst: bool = False, include_srst: bool = False) -> tuple[str, ...]:
    signals = ["VTREF", "TMS", "TCK", "TDI", "TDO"]
    if include_trst:
        signals.append("TRST_N")
    if include_srst:
        signals.append("SRST_N")
    signals.append("GND")
    return tuple(signals)


def jtag_header(
    label: str,
    *,
    at: tuple[float, float] | None = None,
    side: str = "left",
    include_trst: bool = False,
    include_srst: bool = False,
):
    return header_1x(label, list(jtag_signals(include_trst=include_trst, include_srst=include_srst)), at=at, side=side)


def jtag_schema(*, include_trst: bool = False, include_srst: bool = False) -> HarnessSchema:
    signals = jtag_signals(include_trst=include_trst, include_srst=include_srst)
    return passthrough_schema("JTAG programming link", "JTAG header", signals)


ARM_20PIN_JTAG_PIN_MAP = (
    ("1", "VTREF"),
    ("2", "NC"),
    ("3", "NTRST"),
    ("4", "GND"),
    ("5", "TDI"),
    ("6", "GND"),
    ("7", "TMS"),
    ("8", "GND"),
    ("9", "TCK"),
    ("10", "GND"),
    ("11", "RTCK"),
    ("12", "GND"),
    ("13", "TDO"),
    ("14", "RESERVED"),
    ("15", "NRESET"),
    ("16", "RESERVED"),
    ("17", "DBGRQ"),
    ("18", "RESERVED"),
    ("19", "P5V_TARGET"),
    ("20", "RESERVED"),
)


def arm_20pin_jtag_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, ARM_20PIN_JTAG_PIN_MAP, at=at)


def arm_20pin_jtag_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("ARM 20-pin JTAG", ARM_20PIN_JTAG_PIN_MAP)


CORTEX_9PIN_SWD_PIN_MAP = (
    ("1", "VTREF"),
    ("2", "SWDIO_TMS"),
    ("3", "GND"),
    ("4", "SWCLK_TCK"),
    ("5", "GND"),
    ("6", "SWO_TDO"),
    ("8", "NC_TDI"),
    ("9", "NC_TRST"),
    ("10", "NRESET"),
)


def cortex_9pin_swd_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, CORTEX_9PIN_SWD_PIN_MAP, at=at)


def cortex_9pin_swd_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("Cortex 9-pin SWD/JTAG", CORTEX_9PIN_SWD_PIN_MAP)


MSP430_FET_14PIN_PIN_MAP = (
    ("1", "TDO_TDI"),
    ("2", "VCC_TOOL"),
    ("3", "TDI_VPP"),
    ("4", "VCC_TARGET"),
    ("5", "TMS"),
    ("6", "NC"),
    ("7", "TCK"),
    ("8", "TEST_VPP"),
    ("9", "GND"),
    ("10", "AUX_CTS_SCL"),
    ("11", "RST"),
    ("12", "AUX_TXD_SDA"),
    ("13", "AUX_RTS"),
    ("14", "AUX_RXD_SIMO"),
)


def msp430_fet_14pin_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, MSP430_FET_14PIN_PIN_MAP, at=at)


def msp430_fet_14pin_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("TI MSP430 14-pin FET", MSP430_FET_14PIN_PIN_MAP)


def msp430_fet_14pin_link_schema() -> HarnessSchema:
    return pin_map_passthrough_schema("TI MSP430 14-pin FET link", "TI MSP430 14-pin FET", MSP430_FET_14PIN_PIN_MAP)


AMD_XILINX_14PIN_JTAG_PIN_MAP = (
    ("1", "GND1"),
    ("2", "VREF"),
    ("3", "GND3"),
    ("4", "TMS"),
    ("5", "GND5"),
    ("6", "TCK"),
    ("7", "GND7"),
    ("8", "TDO"),
    ("9", "GND9"),
    ("10", "TDI"),
    ("11", "GND11"),
    ("12", "NC"),
    ("13", "PGND"),
    ("14", "SRST"),
)


def amd_xilinx_14pin_jtag_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, AMD_XILINX_14PIN_JTAG_PIN_MAP, at=at)


def amd_xilinx_14pin_jtag_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("AMD/Xilinx 14-pin JTAG", AMD_XILINX_14PIN_JTAG_PIN_MAP)


def amd_xilinx_14pin_jtag_link_schema() -> HarnessSchema:
    return pin_map_passthrough_schema(
        "AMD/Xilinx 14-pin JTAG link",
        "AMD/Xilinx 14-pin JTAG",
        AMD_XILINX_14PIN_JTAG_PIN_MAP,
    )


INTEL_FPGA_10PIN_JTAG_PIN_MAP = (
    ("1", "TCK"),
    ("2", "GND2"),
    ("3", "TDO"),
    ("4", "VCC_TARGET"),
    ("5", "TMS"),
    ("6", "PROC_RST"),
    ("7", "NC7"),
    ("8", "NC8"),
    ("9", "TDI"),
    ("10", "GND10"),
)


def intel_fpga_10pin_jtag_header(label: str, *, at: tuple[float, float] | None = None):
    return pin_map_endpoint(label, INTEL_FPGA_10PIN_JTAG_PIN_MAP, at=at)


def intel_fpga_10pin_jtag_schema() -> EndpointSchema:
    return pin_map_endpoint_schema("Intel FPGA Download Cable II 10-pin JTAG", INTEL_FPGA_10PIN_JTAG_PIN_MAP)


def intel_fpga_10pin_jtag_link_schema() -> HarnessSchema:
    return pin_map_passthrough_schema(
        "Intel FPGA Download Cable II 10-pin JTAG link",
        "Intel FPGA Download Cable II 10-pin JTAG",
        INTEL_FPGA_10PIN_JTAG_PIN_MAP,
    )


SPI_SIGNALS = ("VCC", "CS_N", "SCLK", "MOSI", "MISO", "GND")


def spi_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(SPI_SIGNALS), at=at, side=side)


def spi_schema() -> HarnessSchema:
    return passthrough_schema("SPI peripheral link", "SPI header", SPI_SIGNALS)


UART_SIGNALS = ("VCC", "TX", "RX", "GND")


def uart_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(UART_SIGNALS), at=at, side=side)


def uart_schema() -> HarnessSchema:
    return passthrough_schema("UART serial link", "UART header", UART_SIGNALS)


I2C_SIGNALS = ("VCC", "SCL", "SDA", "GND")


def i2c_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(I2C_SIGNALS), at=at, side=side)


def i2c_schema() -> HarnessSchema:
    return passthrough_schema("I2C low-speed link", "I2C header", I2C_SIGNALS)


def i2c_multidrop_schema() -> BusSchema:
    endpoint_schema = exact_endpoint_schema("I2C header", I2C_SIGNALS)
    return BusSchema(
        name="I2C multidrop bus",
        roles={
            "controller": endpoint_schema,
            "target": endpoint_schema,
        },
        min_role_counts={
            "controller": 1,
            "target": 1,
        },
        max_role_counts={
            "controller": 1,
        },
        pullup_values=("present", "absent"),
        required_role_policies={
            "controller": {"pullup_policy": ("present",)},
            "target": {"pullup_policy": ("absent",)},
        },
    )


ONEWIRE_SIGNALS = ("VCC", "DQ", "GND")


def onewire_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(ONEWIRE_SIGNALS), at=at, side=side)


def onewire_schema() -> HarnessSchema:
    return passthrough_schema("1-Wire short-reach link", "1-Wire header", ONEWIRE_SIGNALS)


MDIO_SIGNALS = ("VCC", "MDC", "MDIO", "GND")


def mdio_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(MDIO_SIGNALS), at=at, side=side)


def mdio_schema() -> HarnessSchema:
    return passthrough_schema("MDIO management link", "MDIO header", MDIO_SIGNALS)


RS422_SIGNALS = ("TX_P", "TX_N", "RX_P", "RX_N", "GND", "SHIELD")


def rs422_endpoint(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(RS422_SIGNALS), at=at, side=side)


def rs422_schema() -> HarnessSchema:
    endpoint_schema = exact_endpoint_schema("RS-422 endpoint", RS422_SIGNALS)
    return HarnessSchema(
        name="RS-422 full-duplex link",
        left=endpoint_schema,
        right=endpoint_schema,
        required_connections=(
            ("TX_P", "RX_P"),
            ("TX_N", "RX_N"),
            ("RX_P", "TX_P"),
            ("RX_N", "TX_N"),
            ("GND", "GND"),
            ("SHIELD", "SHIELD"),
        ),
    )


def rs422_policy_schema() -> BusSchema:
    endpoint_schema = exact_endpoint_schema("RS-422 endpoint", RS422_SIGNALS)
    return BusSchema(
        name="RS-422 full-duplex link policy",
        roles={
            "node_a": endpoint_schema,
            "node_b": endpoint_schema,
        },
        min_role_counts={
            "node_a": 1,
            "node_b": 1,
        },
        max_role_counts={
            "node_a": 1,
            "node_b": 1,
        },
        shield_values=("continuous",),
        drain_values=("bonded", "floating"),
        termination_values=("paired_rx",),
        required_role_policies={
            "node_a": {
                "shield_policy": ("continuous",),
                "drain_policy": ("bonded",),
                "termination_policy": ("paired_rx",),
            },
            "node_b": {
                "shield_policy": ("continuous",),
                "drain_policy": ("floating",),
                "termination_policy": ("paired_rx",),
            },
        },
    )


RS485_2W_SIGNALS = ("A", "B", "GND", "SHIELD")


def rs485_2w_endpoint(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(RS485_2W_SIGNALS), at=at, side=side)


def rs485_2w_schema() -> HarnessSchema:
    return passthrough_schema("RS-485 2-wire bus segment", "RS-485 2-wire endpoint", RS485_2W_SIGNALS)


def rs485_multidrop_schema() -> BusSchema:
    endpoint_schema = exact_endpoint_schema("RS-485 2-wire endpoint", RS485_2W_SIGNALS)
    return BusSchema(
        name="RS-485 multidrop bus",
        roles={
            "controller_end": endpoint_schema,
            "far_end": endpoint_schema,
            "drop": endpoint_schema,
        },
        min_role_counts={
            "controller_end": 1,
            "far_end": 1,
        },
        max_role_counts={
            "controller_end": 1,
            "far_end": 1,
        },
        shield_values=("continuous",),
        drain_values=("bonded", "floating", "pass"),
        termination_values=("present", "absent"),
        bias_values=("present", "absent"),
        required_role_policies={
            "controller_end": {
                "shield_policy": ("continuous",),
                "drain_policy": ("bonded",),
                "termination_policy": ("present",),
                "bias_policy": ("present",),
            },
            "far_end": {
                "shield_policy": ("continuous",),
                "drain_policy": ("floating",),
                "termination_policy": ("present",),
                "bias_policy": ("absent",),
            },
            "drop": {
                "shield_policy": ("continuous",),
                "drain_policy": ("pass",),
                "termination_policy": ("absent",),
                "bias_policy": ("absent",),
            },
        },
    )


SPACEWIRE_SIGNALS = (
    "TXD_P",
    "TXD_N",
    "TXS_P",
    "TXS_N",
    "RXD_P",
    "RXD_N",
    "RXS_P",
    "RXS_N",
    "GND",
)


def spacewire_endpoint(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(SPACEWIRE_SIGNALS), at=at, side=side)


def spacewire_schema() -> HarnessSchema:
    endpoint_schema = exact_endpoint_schema("SpaceWire cable endpoint", SPACEWIRE_SIGNALS)
    return HarnessSchema(
        name="SpaceWire link",
        left=endpoint_schema,
        right=endpoint_schema,
        required_connections=(
            ("TXD_P", "RXD_P"),
            ("TXD_N", "RXD_N"),
            ("TXS_P", "RXS_P"),
            ("TXS_N", "RXS_N"),
            ("RXD_P", "TXD_P"),
            ("RXD_N", "TXD_N"),
            ("RXS_P", "TXS_P"),
            ("RXS_N", "TXS_N"),
            ("GND", "GND"),
        ),
    )


ETHERNET_T568B_SIGNALS = (
    "TX+",
    "TX-",
    "RX+",
    "BI1+",
    "BI1-",
    "RX-",
    "BI2+",
    "BI2-",
)


def ethernet_rj45(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return rj45_t568b(label, at=at, side=side)


def ethernet_schema() -> HarnessSchema:
    endpoint_schema = rj45_t568b_schema()
    return HarnessSchema(
        name="Ethernet T568B link",
        left=endpoint_schema,
        right=endpoint_schema,
        required_connections=tuple((signal, signal) for signal in ETHERNET_T568B_SIGNALS),
    )


def ethernet_variant_schema(*, shielded: bool = False, poe_mode: str = "none") -> BusSchema:
    endpoint_schema = exact_endpoint_schema("RJ45 T568B", ETHERNET_T568B_SIGNALS)
    shield_policy = "chassis" if shielded else "none"
    shield_values = ("none", "chassis")
    poe_values = ("none", "pse_alt_a", "pd_alt_a", "pse_alt_b", "pd_alt_b")

    if poe_mode == "none":
        return BusSchema(
            name="Ethernet link policy",
            roles={
                "left": endpoint_schema,
                "right": endpoint_schema,
            },
            min_role_counts={
                "left": 1,
                "right": 1,
            },
            max_role_counts={
                "left": 1,
                "right": 1,
            },
            shield_values=shield_values,
            poe_values=poe_values,
            required_role_policies={
                "left": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("none",),
                },
                "right": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("none",),
                },
            },
        )

    if poe_mode == "alt_a":
        return BusSchema(
            name="Ethernet PoE Alt-A link policy",
            roles={
                "pse": endpoint_schema,
                "pd": endpoint_schema,
            },
            min_role_counts={
                "pse": 1,
                "pd": 1,
            },
            max_role_counts={
                "pse": 1,
                "pd": 1,
            },
            shield_values=shield_values,
            poe_values=poe_values,
            required_role_policies={
                "pse": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("pse_alt_a",),
                },
                "pd": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("pd_alt_a",),
                },
            },
        )

    if poe_mode == "alt_b":
        return BusSchema(
            name="Ethernet PoE Alt-B link policy",
            roles={
                "pse": endpoint_schema,
                "pd": endpoint_schema,
            },
            min_role_counts={
                "pse": 1,
                "pd": 1,
            },
            max_role_counts={
                "pse": 1,
                "pd": 1,
            },
            shield_values=shield_values,
            poe_values=poe_values,
            required_role_policies={
                "pse": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("pse_alt_b",),
                },
                "pd": {
                    "shield_policy": (shield_policy,),
                    "poe_policy": ("pd_alt_b",),
                },
            },
        )

    raise ValueError(f"unsupported Ethernet PoE mode: {poe_mode}")


PPS_SIGNALS = ("VCC", "PPS", "GND")


def pps_header(label: str, *, at: tuple[float, float] | None = None, side: str = "left"):
    return header_1x(label, list(PPS_SIGNALS), at=at, side=side)


def pps_schema() -> HarnessSchema:
    return passthrough_schema("PPS timing link", "PPS header", PPS_SIGNALS)


def fpga_jtag_2x5(label: str, *, at: tuple[float, float] | None = None):
    return header_2x(
        label,
        ["VTREF", "TMS", "TDI", "TDO", "GND"],
        ["NC", "TCK", "NC", "SRST_N", "GND"],
        at=at,
    )


def generic_endpoint(label: str, signals: tuple[str, ...], *, at: tuple[float, float] | None = None, side: str = "left"):
    pins = signal_pin_defs(signals, side=side)
    return endpoint(label, pins, at=at)
