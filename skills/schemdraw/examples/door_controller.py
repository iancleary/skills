import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=12)
    delta = 4
    with d:
        c4 = flow.Circle(r=1).label("4\nopening")
        c1 = flow.Circle(r=1).at((delta, delta)).label("1\nopened")
        c2 = flow.Circle(r=1).at((2 * delta, 0)).label("2\nclosing")
        c3 = flow.Circle(r=1).at((delta, -delta)).label("3\nclosed")
        elm.Arc2(arrow="->", k=0.3).at(c4.NNE).to(c1.WSW).label("sensor\nopened")
        elm.Arc2(arrow="->", k=0.3).at(c1.ESE).to(c2.NNW).label("close")
        elm.Arc2(arrow="->", k=0.3).at(c2.SSW).to(c3.ENE).label("sensor\nclosed")
        elm.Arc2(arrow="->", k=0.3).at(c3.WNW).to(c4.SSE).label("open")
        elm.Arc2(arrow="<-", k=0.3).at(c4.ENE).to(c2.WNW).label("open")
        elm.Arc2(arrow="<-", k=0.3).at(c2.WSW).to(c4.ESE).label("close")
    return d


if __name__ == "__main__":
    build().save("door_controller.svg")
