import schemdraw
import schemdraw.elements as elm


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.2, fontsize=11)
    with d:
        controller = elm.Ic(
            pins=[
                elm.IcPin(name="TXD", pin="1", side="right", anchorname="TXD"),
                elm.IcPin(name="RXD", pin="2", side="right", anchorname="RXD"),
                elm.IcPin(name="GND", pin="3", side="right", anchorname="GND"),
                elm.IcPin(name="V+", pin="4", side="right", anchorname="VP"),
            ],
            label="Controller",
        )

        connector = elm.Ic(
            pins=[
                elm.IcPin(name="TX", pin="A", side="left", anchorname="TX"),
                elm.IcPin(name="RX", pin="B", side="left", anchorname="RX"),
                elm.IcPin(name="GND", pin="C", side="left", anchorname="GND"),
                elm.IcPin(name="12V", pin="D", side="left", anchorname="VP"),
            ],
            label="J1",
        ).at((8, 0))

        elm.Line().at(controller.TXD).to(connector.TX).label("TX", loc="top")
        elm.Line().at(controller.RXD).to(connector.RX).label("RX", loc="top")
        elm.Line().at(controller.GND).to(connector.GND).label("GND", loc="bottom")
        elm.Line().at(controller.VP).to(connector.VP).label("12V", loc="bottom")
    return d


if __name__ == "__main__":
    build().save("icd_connector.svg")
