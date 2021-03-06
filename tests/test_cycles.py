import pytest

from grandalf import *

@pytest.mark.skipif(not utils.dot._has_ply,reason="requires ply module to parse dot input file")
def test_cycles(sample_cycle):
    g = utils.Dot().read(sample_cycle)[0]
    V = {}
    for k,v in g.nodes.iteritems():
        V[k]=graphs.Vertex(k)
        V[k].view = layouts.VertexViewer(10,10)
    E = []
    for e in g.edges:
        E.append(graphs.Edge(V[e.n1.name],V[e.n2.name]))

    G = graphs.Graph(V.values(),E)
    assert len(G.C)==1
    sg = layouts.SugiyamaLayout(G.C[0])
    gr = sg.g

    r = gr.roots()
    assert len(r)==2
    assert V['A1'] in r
    assert V['A2'] in r

    L = gr.get_scs_with_feedback(r)
    assert len(L)==5
    for s in L:
        if V['A1'] in s:
            assert len(s)==1
        if V['A2'] in s:
            assert len(s)==1
        if V['B1'] in s:
            assert len(s)==1
        if V['B2'] in s:
            assert len(s)==1
        if len(s)>1:
            assert V['C1'] in s
            assert V['C2'] in s
            assert V['D1'] in s
            assert V['D2'] in s
            assert len(s)==4
