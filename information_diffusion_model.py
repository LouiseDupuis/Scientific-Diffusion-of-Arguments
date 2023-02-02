from copy import Error
from re import S
from scientists_agents import ScientistAgent
from graphs import BipolarGraph
from mesa import Model
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from schedule import CustomSimultaneousScheduleActivation
from datetime import datetime
import pandas as pd
import copy
import shutil
import networkx as nx
import sys 
import copy
import numpy as np

from pathlib import Path



class InformationDiffusion(Model):
    """
    Model implementing the protocol
    """


    description = (
        "A model for simulating information diffusion"
    )

    def __init__(
        self, param_dict, lightmode = True
    ):
        """
        Create a new model with the given parameters.

        Args: num_s_agents = number of scientific agents
              semantic = a GradualSemantic object used to assess the argument's strength
              lightmode = When False, saves all of the information about the debate (useful eg for the visualization)
            
        """
        super().__init__()
        # Set parameters

        self.param_dict = param_dict
        self.num_s_agents = param_dict['number_of_s_agents']
        self.lightmode = lightmode

        if self.param_dict['communication_mode']=='network' or self.param_dict['communication_mode']=='dynamical-network':
            #self.network = NetworkGrid(param_dict['graph'])
            self.network = param_dict['graph']

        self.world_value = param_dict['world_value']
        self.public_scientific_graph = BipolarGraph(self.world_value)
        self.p_accept = param_dict['p_accept']
        self.sigma = param_dict['sigma']
        self.schedule = CustomSimultaneousScheduleActivation(self)
        self.argument_id=0

        self.current_step = 0

        self.time = str(datetime.now()).replace('.', '_').replace(':', '_') # a time marker to help save all relevant informations

        
        # self.scientific_value = self.semantic.get_argument_value(self.public_scientific_graph.get_issue(), self.public_scientific_graph) # the current vlue of the issue in the public board
        #self.state = [self.public_scientific_graph.deep_copy()] # a list keeping track of or all states of the game - in lightmode, only the last state of the game 
        self.strategies = [] # a list keeping track of all of the agent's strategies during the game
        self.opinions = [] # a list keeping track of all of the agent's opinions during the game
        self.agent_argument_set = set() # the set containing all of the arguments known by the agents

    
        if not self.lightmode:
            self.complete_state = []  #saving previous states of the debate

        # Create each agent and their opinion graph

        #Creating scientists
        for i in range(self.num_s_agents):
                
                agent = ScientistAgent(i, model=self,p_accept = self.p_accept, sigma=self.sigma)
                self.schedule.add(agent)
                #self.network.place_agent(agent, i)


        # create the data collector
        self.datacollector = DataCollector(
            model_reporters={"Step":lambda m: m.current_step,
            "Sigma": lambda m : m.sigma,
            "P Accept" : lambda m: m.p_accept,
                "State of the Art": lambda m: m.get_current_scientific_value(),
                            "Nb of Arguments" : lambda m: m.public_scientific_graph.number_of_nodes(),
                            "Collective Error" : lambda m: abs(m.world_value - m.get_current_scientific_value()),
                            "Avg of Agent\'s Opinion" : lambda m: round(np.average(m.get_agents_opinion()),5),
                            "STD of Agent\'s Opinion'" : lambda m: round(np.std(m.get_agents_opinion()),5),
                            "Average of Errors" : lambda m: round(np.average([abs(m.world_value - opinion) for opinion in m.get_agents_opinion()]),5),
                            "Truth Deviation" : lambda m : np.sqrt((1/m.num_s_agents)*np.sum([(m.world_value - opinion)**2 for opinion in m.get_agents_opinion()]))
            
            }, agent_reporters={"Opinion": "opinion"}
        )


    def get_agents_opinion(self):
            agent_opinions = [agent.get_opinion() for agent in self.schedule.agents]
            return agent_opinions

    def get_semantic(self):
        return self.semantic
    
    def get_time(self):
        return self.time

    def get_current_scientific_value(self):
        current_value = self.public_scientific_graph.nodes[self.public_scientific_graph.get_issue()]["evaluation"]
        return current_value
    
    def publish_s_argument(self, target, world_value, type):
        #Publishing a scientific argument
        # target is the argument that the new argument attacks
        #type is the type of the relation : support or attack
         
        if target  != 'NOTHING' :
            self.argument_id +=1
            new_arg = self.argument_id 
            # self.public_scientific_graph.add_node(new_arg, wv=world_value)
            # self.public_scientific_graph.add_relation(new_arg, target, type)
            self.public_scientific_graph.add_argument_and_update_evaluation(new_arg, target, type, wv=world_value)
        return new_arg


    

    def get_merged_value(self, step = 0, beginning = False):
        # A FAIRE : Implémenter pour les trois classes d'agents 
        return None


        
    def step(self, i):

        self.datacollector.collect(self)

        self.current_step = i+1

        if not self.lightmode:
            print("Warning : not in lightmode")
            self.complete_state += [copy.deepcopy(self)]
       
        self.schedule.step()

        ## Updating the social network in dynamical-network mode 
        # creating links when the distance is less than epsilon, destroying them otherwise

        # if self.param_dict['communication_mode']=='dynamical-network':
        #     print("DYNAMICAL NETWORK")
        #     new_network = nx.Graph()
        #     for a in self.schedule.agent_keys:
        #         for b in self.schedule.agent_key:
        #             if abs(self.schedule._agents[a].get_opinion() - self.schedule._agents[b].get_opinion()) <= self.param_dict['epsilon']:
        #                 print("adding edge between :", a,b)
        #                 new_network.add_edge(a,b)
        #     self.network = new_network
        
   

    def run_model(self):

        for i in range(self.param_dict['step_count']):
            self.step(i)

       
            
        
        #print("====================================== Debate Over ============================================")
            
            
        #state_of_the_art = self.public_scientific_graph.euler_semantic(0)
        # print()
        # print("World Value of the Issue :", self.world_value)
        # print("State of the Art :",state_of_the_art)
        # print("Number of arguments :", len(list(self.public_scientific_graph.nodes)))
        # print()

        return None

   