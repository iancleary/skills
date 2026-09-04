import schemdraw

from helpers.connectors import DE9_RS232_SIGNALS, rs232_breakout_schema, rs232_de9, terminal_block
from helpers.pinmap import ConnectionDef, PinDef, connect_by_signal
from helpers.schema import validate_harness_schema


SIGNALS = list(DE9_RS232_SIGNALS)


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.1, fontsize=10)
    terminal_pins = [PinDef(signal, str(index + 1), side="left") for index, signal in enumerate(SIGNALS)]
    connections = [ConnectionDef(signal, label=signal, loc="top" if signal not in {"GND"} else "bottom") for signal in SIGNALS]
    validate_harness_schema(
        "P1",
        [PinDef(signal, str(index + 1), side="right") for index, signal in enumerate(SIGNALS)],
        "TB1",
        terminal_pins,
        connections,
        rs232_breakout_schema(),
    )
    with d:
        source = rs232_de9("P1", side="right")
        breakout = terminal_block("TB1", SIGNALS, at=(9, 0), side="left")
        connect_by_signal(source, breakout, connections)
    return d


if __name__ == "__main__":
    build().save("dsub_breakout.svg")
