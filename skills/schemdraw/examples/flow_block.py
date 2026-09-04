import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


def build():
    schemdraw.use("svg")
    d = schemdraw.Drawing()
    d.config(fontsize=12)
    with d:
        ingest = flow.Box(w=3.2, h=1.2).label("Ingest\nHarness Data")
        normalize = flow.Box(w=3.2, h=1.2).right().label("Normalize\nPins / Nets")
        verify = flow.Decision(w=3.0, h=2.2).right().label("Schema\nValid?")
        publish = flow.Box(w=3.2, h=1.2).right().label("Render ICD /\nCable Drawing")

        elm.Line(arrow="->").at(ingest.E).to(normalize.W)
        elm.Line(arrow="->").at(normalize.E).to(verify.W)
        elm.Line(arrow="->").at(verify.E).to(publish.W).label("yes", loc="top")
        reject = flow.Box(w=2.8, h=1.0).down().at(verify.S).label("Fix Inputs")
        elm.Line(arrow="->").at(verify.S).to(reject.N).label("no", loc="right")
    return d


if __name__ == "__main__":
    build().save("flow_block.svg")
