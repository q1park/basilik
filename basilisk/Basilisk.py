"""
BN module constructs a bayesian network from Node objects.
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from graphviz import dot

class BN(object):
    """
    parameters
    ----------
    ls_nodes : list of nodes

    observations: pandas dataframe
        dataframe, where each column represents a discrete random variable.


    attributes
    ----------
    dict_nodes : dictionary
        key represents node name, value is the corresponding node.

    dict_children : dictionary
        key represents node name, value is a list of its children names.
    """
    
    def __init__(self, ls_nodes):
        self.ls_nodes = ls_nodes  
        self.dict_nodes = self._generate_dict_nodes()  # dict for fast lookup
        self.dict_children = self._generate_dict_children()
        

    def fit(self, observations):
        self.observations = observations
        self._generate_cpt()  # compute cpt for each node - no lazy loading 


    def _generate_cpt(self):
        """iterate through all nodes and compute their respective conditional 
        probability tables.
        """

        for node in self.ls_nodes:
            node.cpt = self._calculate_cpt(node)
        
    def _generate_dict_nodes(self):
        """return a dictionary, where key is node name and value is the 
        corresponding node object."""
        d = {}
        for node in self.ls_nodes:
            d[node.name] = node
        return d
    
    def _generate_dict_children(self):
        """return a dictionary, where key is name of node and value is a
        list of its children."""
        d = {}
        for parent in self.ls_nodes:
            children = []
            
            for child in self.ls_nodes:
                if parent in child.ls_parents:
                    children.append(child.name)
            d[parent.name] = children
        return d
    
    def draw_graph(self, **kwargs):
        graph = nx.DiGraph(self.dict_children)
        layout = graphviz_layout(graph, 'dot')
        nx.draw_networkx(graph, layout = layout, **kwargs)
        plt.axis('off')
        plt.show()
        
    def _calculate_cpt(self, node):
        # find node's parents
        parent = node.ls_parents
        
        # subset its corresponding marginals
        ps = [self.observations[x.name] for x in parent]
        cs = self.observations[node.name]
        
        # finally, crosstab
        # # https://stackoverflow.com/questions/53510319/python-pandas-merging-with-more-than-one-level-overlap-on-a-multi-index-is-not
        return pd.crosstab(ps, cs, normalize = 'index').reset_index()