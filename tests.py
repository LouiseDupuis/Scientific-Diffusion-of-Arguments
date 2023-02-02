import math 
from graphs import BipolarGraph


#---------- TEST   -----Euler semantic

# G = BipolarGraph()

# G.add_relation(1,0,"attack")

# print("DA of 1 : ", G.euler_semantic(1))
# print("DA of 0 : ", G.euler_semantic(0))
# print("DA of issue : ", G.euler_semantic(G.get_issue()))

# #---------- TEST   -----Optimized Euler Semantic

# G = BipolarGraph()

# G.add_argument_and_update_evaluation(1,0,"attack")

# print("DA of 1 : ", G.nodes[1]["evaluation"])
# print("DA of 0 : ", G.nodes[0]["evaluation"])
# print("DA of issue : ", G.nodes[G.get_issue()]["evaluation"])


# ------------ TEST - SII Graphs
# from islands import SII
# import networkx as nx
# import matplotlib.pyplot as plt

# sii = SII(3,10,1,0)
# nx.draw_networkx(sii)
# plt.show()



# ---------- TEST - Truth Deviation 
# import numpy as np 

# def truth_deviation(opinions, truth_value):
     
#      return np.sqrt((1/len(opinions))*np.sum([(truth_value - opinion)**2 for opinion in opinions]))

# print(truth_deviation([0.51], 0.5))

# -------- TEST - Gaussian Sampling 
import numpy as np 

truth_value  = 0.8
sigma = 0.15

rng = np.random.default_rng()
for i in range(3):
     print(rng.normal(truth_value,sigma))



