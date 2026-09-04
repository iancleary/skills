import schemdraw
import schemdraw.elements as elm


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=13)
    with d:
        elm.Resistor().label("100KΩ")
        elm.Capacitor().down().label("0.1μF", loc="bottom")
        elm.Line().left()
        elm.Ground()
        elm.SourceV().up().label("10V")
    return d


if __name__ == "__main__":
    build().save("basic_rc.svg")
