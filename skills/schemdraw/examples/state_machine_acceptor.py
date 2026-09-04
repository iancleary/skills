import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=12, unit=1)
    with d:
        elm.Arrow().length(1)
        s1 = flow.StateEnd().anchor("W").label("$S_1$")
        elm.Arc2(arrow="<-").at(s1.NE).label("0")
        s2 = flow.State().anchor("NW").label("$S_2$")
        elm.Arc2(arrow="<-").at(s2.SW).to(s1.SE).label("0")
        elm.ArcLoop(arrow="<-").at(s2.NE).to(s2.E).label("1")
        elm.ArcLoop(arrow="<-").at(s1.NW).to(s1.N).label("1")
    return d


if __name__ == "__main__":
    build().save("state_machine_acceptor.svg")
