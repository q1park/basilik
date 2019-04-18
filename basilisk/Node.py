import numpy as np

class Node(object):
    """Nodes represents discrete random variables.
    """
    
    def __init__(self, name, ls_parents=[]):
        self.name = name
        self.ls_parents = ls_parents
        self.cpt = None  # to be generated by BN.model.fit()

    def get_parents(self):
        return self.ls_parents
        
    @property
    def is_marginal(self):
        """a marginal node does not have any parents."""
        return not self.ls_parents
    
    def sample(self, parent_states, num_samples=1):
        """sample from Node, according to (1) the node's conditional probability 
        table and (2) its parents' states. 
        """
        if self.cpt is None:
            raise ValueError('need to fit model with observations.')
        else:
            cpt = self.cpt.copy()  # dataframes are mutable

            # iteratively filter cpt, according to parents' states
            for p_state in parent_states:
                cpt = cpt.query(p_state)

            # drop unnecssary columns, which correspond to parents' columns
            parents_names = list(map(lambda p_node: p_node.name, self.ls_parents))
            for col in parents_names:
                cpt.drop(col, axis=1, inplace=True)

            # we can sample, now we that have states and respective distributions
            states = np.array(cpt.columns)  # possible states
            distribution = np.array(cpt)  # probability distribution of states

            return np.random.choice(a=states, size=num_samples, p=distribution[0])