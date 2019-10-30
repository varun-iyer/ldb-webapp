import networkx as nx
import graphviz as gv
from crossref_commons.retrieval import get_publication_as_json as cr_get_pub
from app.models import Document, reference


class GraphPub(dict):
    """
    Wrapper for dict/JSON that implements a hash function that returns DOI
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash__(self):
        try:
            return self['DOI'].__hash__()
        except KeyError:
            try:
                return self['key'].__hash__()
            except KeyError:
                return self['title'][0].__hash__()

    def __str__(self):
        try:
            return self['title'][0]
        except (KeyError, IndexError):
            try:
                return self['DOI']
            except KeyError:
                return self['key']

    def __repr__(self):
        try:
            return self['DOI']
        except (KeyError, IndexError):
            return self['key']
         
 
def get_pub(doi):
    pub = cr_get_pub(doi)
    return pub


def build_graph(doi, depth=2):
    """
    Returns a graph of the stuff
    """
    graph = nx.DiGraph()
    pub = doi
    if isinstance(pub, str):
        # this is an initial call, get the publication
        pub = GraphPub(get_pub(doi))
    graph.add_node(pub)
    if depth == 0:
        return graph
    else:
        try:
            references = pub['reference']
        except:
            return graph
        for r in references:
            try:
                gr = GraphPub(get_pub(r['DOI']))
            except KeyError:
                gr = GraphPub(r)
            # graph.add_node(gr)
            # graph.add_edge(pub, gr)
            graph.add_edge(pub, gr)
            refgraph = build_graph(gr, depth=depth - 1)
            # graph.add_node(refgraph)
            graph = nx.compose(graph, refgraph)
    return graph
 
def graph_svg(graph):
    '''
    Returns an svg string
    '''
    viz = gv.Digraph(format='svg')
    for node in graph.nodes:
        if 'URL' in graph:
            viz.node(str(node), label='<a href="{}">{}</a>'.format(graph['URL'], str(graph)))
        else:
            viz.node(str(node), label=str(node))
    for f, t in graph.edges:
        viz.edge(str(f), str(t))
    return viz.pipe().decode('utf-8')
