from collections import defaultdict

from mesa.time import SimultaneousActivation
from mesa.time import RandomActivation
from networkx import Graph
from mesa.space import NetworkGrid


### NOT USED ANYMORE ??? 

class CustomSimultaneousScheduleActivation(RandomActivation):
    """A scheduler to simulate the simultaneous activation of all the agents.

    This scheduler requires that each agent have two methods: step and advance.
    step() activates the agent and stages any necessary changes, but does not
    apply them yet. advance() then applies the changes.

    """

    def step(self) -> None:
        """ Step all agents, then learn arguments. """
        agent_keys = list(self._agents.keys())

        targets =  []
        for agent_key in agent_keys:
            target = self._agents[agent_key].step()
            # if target is not None:
            #     targets += [(agent_key,target)]
        
        # #then, publishing arguments :
        # new_args = []
        # for agent_key, target in targets:
        #     new_arg,edge = self.model.publish_s_argument(target)
        #     new_args += [(new_arg, edge)]
        #     self._agents[agent_key].learn_arg(new_arg, edge) #every agent learns their own argument
        
        # #then, evaluating other's arguments :
        # for new_arg, edge in new_args:
        #     if edge is not None:
        #         for a_key in agent_keys:
        #             self._agents[a_key].evaluate(new_arg,edge) 

        ## Updating the social network in dynamical-network mode 
        # creating links when the distance is less than epsilon, destroying them otherwise

        if self.model.param_dict['communication_mode']=='dynamical-network':
            new_network = Graph()
            for a in agent_keys:
                for b in agent_keys:
                    if a != b:
                        if abs(self._agents[a].get_opinion() - self._agents[b].get_opinion()) <= self.model.param_dict['epsilon']:
                            new_network.add_edge(a,b)
            self.model.network = new_network
                    

        self.steps += 1
        self.time += 1


class RandomScheduleActivation(RandomActivation):
    """SECOND VERSION A scheduler to simulate the activation of all the agents.

    """

    def step(self) -> None:
        """ Step all agents, then learn arguments. """
        # self.steps += 1
        # self.time += 1
