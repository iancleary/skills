# Protocol Harness Patterns

Use this reference when the drawing is primarily about a protocol or debug/programming interface rather than a generic connector family.

## Local Rule

Define protocol links as:

1. a fixed signal inventory
2. an endpoint family
3. a required mapping set
4. a rendered view

Do not start from hand-drawn connector art when the real job is validating a protocol contract.

## Bundled Protocol Examples

- `examples/swd_programming.py`: 2-wire debug/programming plus reset, reference voltage, and ground
- `examples/jtag_fpga.py`: 4-wire FPGA JTAG plus reference and ground
- `examples/msp430_fet_jtag_harness.py`: exact TI MSP430 14-pin programming-pod harness
- `examples/arm20_swd_header.py`: named ARM 20-pin SWD physical header pattern
- `examples/arm20_jtag_header.py`: named ARM 20-pin JTAG physical header pattern
- `examples/cortex9_swd_header.py`: named Cortex 9-pin SWD/JTAG physical header pattern
- `examples/amd_xilinx_14pin_jtag_harness.py`: exact AMD/Xilinx 14-pin FPGA programming-pod harness
- `examples/intel_fpga_10pin_jtag_harness.py`: exact Intel FPGA Download Cable II 10-pin harness
- `examples/msp430_fet_to_microd15_adapter.py`: mock MSP430 pod to Micro-D service-adapter pattern
- `examples/amd_xilinx_to_shrouded_header_adapter.py`: mock AMD/Xilinx pod to shrouded-header service-adapter pattern
- `examples/intel_fpga_to_circular10_adapter.py`: mock Intel FPGA pod to circular-service adapter pattern
- `examples/spi_peripheral.py`: clock, chip-enable, MOSI, MISO, power, and ground
- `examples/uart_serial.py`: simple UART serial plus power and ground
- `examples/i2c_sensor.py`: short-reach I2C bus pattern
- `examples/i2c_multidrop.py`: controller-plus-multiple-target I2C bus pattern with explicit pull-up ownership
- `examples/onewire_sensor.py`: 1-Wire device link pattern
- `examples/mdio_link.py`: MDIO management link pattern
- `examples/rs422_link.py`: full-duplex differential serial with shield policy
- `examples/rs485_bus.py`: 2-wire differential bus segment with shield policy
- `examples/rs485_multidrop.py`: multidrop RS-485 bus with explicit end/drop roles, bias, and termination policy
- `examples/spacewire_link.py`: bidirectional data/strobe differential pairs and ground
- `examples/ethernet_link.py`: RJ45 T568B logical link
- `examples/ethernet_poe_link.py`: shielded PoE-aware Ethernet logical link
- `examples/pps_sync.py`: PPS timing link plus power and ground

## SWD

Typical logical signals for the local helper path:

- `VTREF`
- `SWDIO`
- `SWCLK`
- optional `SWO`
- optional `NRST`
- `GND`

Primary source used for the local defaults:

- ARM DSTREAM-ST SWD reference material describing `SWDIO` as bidirectional and showing `VTREF`, `SWDIO`, `SWCLK`, optional `SWO`, `nSRST`, and `GND`
- SEGGER 20-pin and 9-pin debug connector knowledge-base pinouts for the named physical header examples

## JTAG

Typical logical signals for the local helper path:

- `VTREF`
- `TMS`
- `TCK`
- `TDI`
- `TDO`
- optional `TRST_N`
- optional `SRST_N`
- `GND`

Primary source used for the local defaults:

- vendor JTAG references describing mandatory `TMS`, `TCK`, `TDI`, and `TDO`, with reset signals varying by target family
- SEGGER 20-pin JTAG connector pinout for the named ARM-standard physical header example

Programming-pod rule:

- when the user names a vendor programming pod or exact FPGA download cable, prefer the named physical-standard examples over the generic `jtag_fpga.py` pattern
- use the generic JTAG example only when the logical bus matters more than the pod/header contract

## TI MSP430 Pod

The local helper includes an exact TI MSP430 14-pin FET header pattern with tool-voltage, target-voltage, JTAG/SBW, reset, and auxiliary UART/SPI/I2C lines called out explicitly.

Use this when:

- the harness is defined against the MSP-FET or compatible 14-pin pod/header
- the cable or target header itself is part of the ICD
- you need the multiplexed auxiliary pins documented rather than collapsed into generic labels

Primary sources used for the local defaults:

- TI debug-probe connector guidance for MSP430 and XDS adapters
- TI MSP430 Hardware Tools User's Guide Table B-47 for the 14-pin target connector

## FPGA Programming Pods

The local helper includes exact programming-pod header patterns for:

- AMD/Xilinx 14-pin JTAG
- Intel FPGA Download Cable II 10-pin JTAG

Use these when:

- the programming cable family itself is known
- the target board is expected to mate to a standard vendor pod/header
- you want to validate exact pin numbering rather than only the logical JTAG subset

Source note:

- the AMD/Xilinx active-signal assignments come from the current 14-pin target-interface guidance; the inactive/ground pin treatment is aligned to older Xilinx 14-pin cable documentation, so the full local pin map is partly an inference from those combined sources
- the Intel 10-pin pin map comes from the Intel FPGA Download Cable II pin table

## Adapter Mockups

The local example set also includes mock service-adapter patterns that terminate the programming-pod standards into more deployment-oriented connector families:

- Micro-D
- keyed shrouded headers
- circular service connectors

Use these when:

- you want a repo-local starting point for an EGSE or field-service adapter
- the target-side connector family is project-specific rather than vendor-defined
- you want the pod standard kept exact while the far-side connector remains an intentional mock or house pattern

Do not treat these adapter examples as formal industry standards. They are illustrative local patterns meant to be replaced or tightened to project-specific connector contracts.

## Named Physical Standards

The local helper layer now includes exact pin-map patterns for:

- ARM 20-pin SWD
- ARM 20-pin JTAG
- Cortex 9-pin SWD/JTAG
- TI MSP430 14-pin FET
- AMD/Xilinx 14-pin JTAG
- Intel FPGA Download Cable II 10-pin JTAG
- DE-9 RS-232
- RJ45 T568B

Use these when:

- the connector itself is part of the interface contract
- pin numbering matters as much as signal naming
- you want schema validation to catch physical pin-map drift, not just logical signal drift

## SPI

Typical logical signals for the local helper path:

- `VCC`
- `CS_N`
- `SCLK`
- `MOSI`
- `MISO`
- `GND`

Use this for:

- microcontroller peripheral links
- sensor/control buses represented as one controller to one device

## UART

The local helper uses:

- `VCC`
- `TX`
- `RX`
- `GND`

Use this for:

- point-to-point serial debug or console links
- simple ICDs where logical serial naming matters more than exact board header layout

## I2C

The local helper uses:

- `VCC`
- `SCL`
- `SDA`
- `GND`

Use this for:

- short-reach controller-to-sensor links
- ICDs where the important contract is that the shared clock/data pair and reference supply are explicit

Design rule:

- the local example models the logical bus segment, not pull-up placement or multi-drop address policy

Multidrop rule:

- use `examples/i2c_multidrop.py` when the important contract is bus ownership, not just one controller-to-one-target wiring segment
- make one controller own pull-ups in the schema instead of leaving pull-up location implicit

## 1-Wire

The local helper uses:

- `VCC`
- `DQ`
- `GND`

Use this for:

- simple low-speed device links
- deterministic interface drawings where a single bidirectional data line matters more than the exact board connector

## MDIO

The local helper uses:

- `VCC`
- `MDC`
- `MDIO`
- `GND`

Use this for:

- MAC-to-PHY management links
- low-distance board or backplane control interfaces

## RS-422

The local helper uses a full-duplex differential model:

- `TX_P`, `TX_N`
- `RX_P`, `RX_N`
- `GND`
- `SHIELD`

Design rule:

- validate the crossover explicitly: local transmit must land on remote receive
- keep shield handling explicit in the contract instead of leaving it to assembly notes
- for the local policy schema, make drain-bond ownership explicit on one end and require paired receiver termination at both nodes

## RS-485

The local helper uses a 2-wire differential model:

- `A`
- `B`
- `GND`
- `SHIELD`

Design rule:

- treat shield policy and reference ground as part of the interface contract
- the bundled example models one validated bus segment, not full multidrop termination policy

Multidrop rule:

- use `examples/rs485_multidrop.py` when you need one biased controller end, one terminated far end, and zero-or-more unterminated drops
- make drain handling explicit as `bonded`, `pass`, or `floating` instead of burying it in cable notes

## SpaceWire

The local helper treats one full-duplex SpaceWire link as:

- transmit data differential pair: `TXD_P`, `TXD_N`
- transmit strobe differential pair: `TXS_P`, `TXS_N`
- receive data differential pair: `RXD_P`, `RXD_N`
- receive strobe differential pair: `RXS_P`, `RXS_N`
- `GND`

Primary source used for the local defaults:

- SpaceWire references describing two differential pairs in each direction, carrying data and strobe, for a total of eight signal wires per bidirectional link

## Ethernet

The local helper uses the existing T568B logical ordering:

- `TX+`
- `TX-`
- `RX+`
- `BI1+`
- `BI1-`
- `RX-`
- `BI2+`
- `BI2-`

Use this when the drawing needs a deterministic logical link or breakout, not a full PHY or magnetics schematic.

Variant rule:

- use the base Ethernet example for unshielded, non-PoE logical links
- use `examples/ethernet_poe_link.py` when shield bonding and PSE/PD role assignment are part of the contract
- model PoE role explicitly in the schema even when the drawing stays at the logical pair level
- the local Ethernet endpoint schema now also enforces exact RJ45 T568B pin numbering, not just pair naming

## PPS

The local helper uses:

- `VCC`
- `PPS`
- `GND`

Use this for:

- timing distribution notes
- simple ICD or synchronization links
- GPSDO / timing-base connections

## Design Rule

For protocol diagrams, the smallest useful contract is:

- protocol signal set is explicit
- optional signals are named as optional
- mapping is schema-checked
- rendering is generated from the validated mapping

If a connector is known but the protocol is not, start from the connector helper.

If the protocol is known but the physical connector may vary, start from the protocol helper.

If the interface is multidrop or policy-heavy, start from the policy-backed example rather than forcing it into a point-to-point harness template.
