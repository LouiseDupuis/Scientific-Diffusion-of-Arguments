import networkx as nx
import random

""" This class implements a generator of Simple Interconnected Islands graphs as described by Samuel Thiriot 
in Small World is Not Enough (2020)"""

class SII(nx.Graph):

    def __init__(self, nb_islands, size_island, p_in, n_inter ):
        super().__init__()
        self.nb_islands = nb_islands
        self.size_islands = size_island
        self.p_in = p_in
        self.n_inter = n_inter
        self.totalsize = nb_islands*size_island

        self.add_nodes_from([a for a in range(self.totalsize)])
        
        # for each island
        for i in range(nb_islands):
            start_island = size_island*i
            end_island = start_island+size_island-1

             # create links with probability p_in

            for k in range(start_island, end_island+1):
                for j in range(k+1, end_island + 1):
                    if random.random() <= self.p_in:
                        self.add_edge(k,j)

            # create n_inter links with other islands 
            if i < nb_islands - 1:
                other_island = i+1
                for n in range(self.n_inter):
                    id_this_island = random.sample([m for m in range(start_island, end_island)],1)[0]
                    id_other_island = random.sample([m for m in range(size_island*other_island, size_island*(other_island) + size_island -1)],1)[0]
                    self.add_edge(id_this_island, id_other_island)
            





