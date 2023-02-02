
from cmath import exp
import networkx as nx
import random
from networkx.classes.function import set_node_attributes
import copy
import matplotlib.pyplot as plt
import re
from pathlib import Path
import math
import numpy as np
   

def sigmoid(x):
  return 1 / (1 + math.exp(-x))


class BipolarGraph(nx.DiGraph):

    """ A Bipolar graph is characterized by an issue, and two types of edges : defense and attack."""

    def __init__(self, world_value = None, nodes = None):

        super().__init__(nodes)
        
        if world_value is not None:
            self.add_node(0, wv=world_value, evaluation=0.5)
            self.issue = 0
        else:
            self.add_node(0, evaluation=0.5)
            self.issue = 0
        

    def get_issue(self):
        return self.issue

    def get_size(self):
        # getting the size of the graph (including the issue)
        return len(list(self.nodes))


    def issue_is_reachable(self, arg):
        for path in nx.all_simple_paths(self, arg, self.issue):
            return True
        return False


    def add_relation(self, arg1, arg2, type):
        self.add_edge(arg1,arg2,type=type)

    
    def euler_semantic(self, arg):
        # recursive function to compute the degree of acceptability based on the euler semantic 

        attacks = []
        supports = []
        for e in self.in_edges(arg, data=True):
            if e[2]["type"]=="attack":
                attacks += [e[0]]
            else:
                supports +=[e[0]]

        #if arg == self.issue:        
        
            # print("computing euler semantic for", arg)
            # print("attacks : ", attacks)
            # print("supports ; ", supports)
        if len(attacks)==len(supports)==0:
            # print("no attacks or supports")
            return 0.5
        res = (1 - 1/(1+ np.exp(sum([self.euler_semantic(sup) for sup in supports]) - sum([self.euler_semantic(att) for att in attacks])))).real
        # print("result obtained : ", res)
        return res

    def compute_eval(self,arg):
        attacks = []
        supports = []
        for e in self.in_edges(arg, data=True):
            if e[2]["type"]=="attack":
                attacks += [e[0]]
            else:
                supports +=[e[0]]
        if len(attacks)==len(supports)==0:
            return 0.5
        res = (1 - (1-0.5*0.5)/(1+0.5*exp(sum([self.nodes[sup]["evaluation"] for sup in supports]) - sum([self.nodes[att]["evaluation"] for att in attacks])))).real
        return res

    
    def add_argument_and_update_evaluation(self,new_arg,target,type, wv=None):
        
        if wv is not None:
            self.add_node(new_arg, wv=wv, evaluation=0.5)
        else:
            self.add_node(new_arg, evaluation=0.5)
        self.add_relation(new_arg,target,type)
        path = sorted(nx.descendants(self, new_arg), reverse = True)
        
        for node in path:
            eval = self.compute_eval(node)
            if "wv" in self.nodes[node]:
                nx.set_node_attributes(self, {node:{"wv": self.nodes[node]["wv"],"evaluation":eval}})
            else:
                nx.set_node_attributes(self, {node:{"evaluation":eval}})


    def select_random_node(self):
        #print("Selecting a node amonsgt : ", list(self.nodes))
        return random.choice(list(self.nodes))

    def deep_copy(self):
        # A copy which changes the graph object but keeps the same node objects
        return copy.deepcopy(self)

        








