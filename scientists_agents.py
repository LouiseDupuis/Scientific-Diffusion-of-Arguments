from curses import reset_shell_mode
from mesa import Agent
from base_agents import BaseAgent
import random
import networkx as nx
from scipy import stats
import numpy as np
import math 

class ScientistAgent(BaseAgent):
    """
    A scientist agent researching and publishing results.
    """

    def __init__(self, unique_id, model, opinion_graph=None, gamma = 8, p_accept = 0.8, sigma = 0.2):
        """
        Creates a new agent

        Args:
            opinion_graph : the agent's own set of arguments
            productivity : the chance that an agent has at producing an argument at all (otherwise, too many arguments when the graph is very small)
            gamma : the parameter for the logistic function 
        """


        super().__init__(unique_id, model, opinion_graph)
        self.gamma = gamma
        self.p_accept = p_accept
        self.sigma = sigma
    

    def generate_counterargument(self):
        """ The function which generates arguments from the agent. 
        NOT USED ANYMORE
        """
        #determine if the agent can find something: 
        if random.random() < self.productivity :

            impact_dict = self.model.check_impact()
            opinion = self.get_opinion(self.model.semantic)
            current_value = self.model.get_current_scientific_value()
            node_weight_dict = dict()
        
            #height = self.model.public_scientific_graph.get_height()
            for node, new_value in impact_dict.items():
                
                #distance_to_issue = self.model.public_scientific_graph.get_path_length(node)
                
                if abs(self.model.ground_truth - new_value) <= abs(self.model.ground_truth - current_value):
                    weight = self.model.alpha
                    
                else:
                    weight = 1 - self.model.alpha
                    
                if abs(opinion - new_value) <= abs(opinion - current_value):
                    weight *= self.model.beta
                    
                else:
                    weight *= 1 - self.model.beta
                    
                node_weight_dict[node] = weight 
                #node_weight_dict[node] = weight * (1+distance_to_issue)/(height +1)

            sum_weights = sum(list(node_weight_dict.values()))
            sum_weights_logistic = sum([math.exp(self.gamma * w) for w in list(node_weight_dict.values())])
            xk = list(node_weight_dict.keys())
            # proportionnal proba
            pk = [weight/sum_weights for weight in list(node_weight_dict.values())]
            #logistic proba
            p2k = [math.exp(self.gamma * weight)/sum_weights_logistic for weight in list(node_weight_dict.values())]


            distrib = stats.rv_discrete(name='distribution', values=(xk, p2k))
            d =distrib.rvs(size=1)

            return d[0]
           
        else:
            return None

    
    def generate_argument(self):

        #-1----------choosing one argument to investigate

        arg = self.opinion_graph.select_random_node()
        # select a connected node
        world_value = self.model.public_scientific_graph.nodes[arg]["wv"]
        agent_value = self.opinion_graph.euler_semantic(arg) 

        #-2---------- performing the experiment 
        #--a----------first part : support or attack
        rng = np.random.default_rng()
        res1 = rng.normal(world_value,self.sigma)
        if res1>agent_value:
            type = "support"
        else:
            type = "attack"
        
        if type == "support":
            res2 = rng.normal(world_value,self.sigma)
        elif type =="attack":
            res2 = rng.normal(1- world_value,self.sigma)
        
        # only results between 0 and 1 included 
        if res2 < 0:
            res2 = 0
        if res2 > 1:
            res2 = 1
        

        # if (max(world_value - self.interval_size,0) <= res <= min(world_value + self.interval_size,1)):
        #     return arg, res, "support"
        # else:
        #     return arg, res, "attack"

        return arg, res2, type
    

    def step(self):
        investigated_arg, res, type = self.generate_argument()

        #---------------- publishing the argument
        new_arg= self.model.publish_s_argument(investigated_arg, res, type)
        self.learn_arg(new_arg, investigated_arg, type) #each agent learns their own result

        if self.model.param_dict['communication_mode'] in ['network','mixed']:
        #----------------- neighbors of the agent add the argument 
            neighbors = [self.model.schedule.agents[id] for id in self.model.network.neighbors(self.unique_id)]
            for n in neighbors:
                n.learn_arg(new_arg, investigated_arg, type)
                # adding a random subset of their AG 

        if self.model.param_dict['communication_mode'] in ['public','mixed']:
        #-------------------- every agent evaluates the argument
        #NOTE : what happens for the agents who learn it twice ?
            agent_keys = list(self.model.schedule._agents.keys())
            for a_key in agent_keys:
                if a_key != self.unique_id :
                    self.model.schedule._agents[a_key].evaluate(new_arg, investigated_arg, type) 
        return None


    def evaluate(self,new_arg,target, type):
        #Evaluating and possibly learning a new argument
        # if edge is not None:
        #     value_without_arg = self.model.semantic.get_argument_effect_delete(new_arg, self.model.public_scientific_graph)
        #     opinion = self.get_opinion(self.model.semantic)
        #     current_value = self.model.get_current_scientific_value()

        #     value_drawn = random.random()

        #     if abs(opinion - value_without_arg) <= abs(opinion - current_value) and value_drawn <= self.p_favor: # if the argument favors 
        #         self.learn_arg(new_arg,edge)
        #     if abs(opinion - value_without_arg) > abs(opinion - current_value) and value_drawn <= self.p_against: # if the argument is against
        #         self.learn_arg(new_arg,edge)

        if random.random() <= self.p_accept:
            self.learn_arg(new_arg, target, type)
        return None

    