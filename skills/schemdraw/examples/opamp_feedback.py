import schemdraw
import schemdraw.elements as elm


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(unit=2.5, fontsize=12)
    with d:
        op = elm.Opamp().label("U1")
        elm.Line().left().at(op.in1).length(1.2)
        elm.Resistor().left().label("Rin", loc="top")
        elm.SourceSin().down().label("Vin", loc="bottom")

        elm.Line().right().at(op.out).length(1.2).dot()
        fb = elm.Resistor().up().label("Rf", loc="right")
        elm.Line().left().tox(op.in1)
        elm.Line().down().toy(op.in1)

        elm.Line().left().at(op.in2).length(0.8)
        elm.Ground()
    return d


if __name__ == "__main__":
    build().save("opamp_feedback.svg")
