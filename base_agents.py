from mesa import Agent
import random
import networkx as nx
from graphs import BipolarGraph

class BaseAgent(Agent):
    """
    An agent participating in an argumentative discussion.
    """

    def __init__(self, unique_id, model, opinion_graph = None ):
        """
        Creates a new agent

        Args:
            opinion_graph : the agent's own set of arguments
        """
        super().__init__(unique_id, model)
        if opinion_graph is not None:
            self.opinion_graph = opinion_graph
        else:
            self.opinion_graph = BipolarGraph()
        self.opinion = None # opinion = value of the issue in the graph 
        self.name = unique_id
        self.state = [] # if not light mode, keeping track of all of the agent's graph during the game

    
    def get_opinion(self):
        self.opinion = self.opinion_graph.euler_semantic(self.opinion_graph.get_issue())
        return self.opinion

        
    # def evaluate(self,new_arg,edge):
    #     #Evaluating and possibly learning a new argument
    #     #For now, 1 chance out of 2
    #     if edge is not None:
    #         if random.random()>0.5:
    #             self.learn_arg(new_arg,edge)
    #     return None

    def learn_arg(self, new_arg, target, type):
        self.opinion_graph.add_argument_and_update_evaluation(new_arg, target, type)
    
  

    def __str__(self) -> str:
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()

        

