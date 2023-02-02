
from networkx.algorithms.shortest_paths.weighted import multi_source_dijkstra_path_length
from information_diffusion_model import InformationDiffusion

import random
import pandas as pd 
import numpy as np
from datetime import datetime
import time
import networkx as nx
from islands import SII
import matplotlib.pyplot as plt




if __name__ == '__main__':

    start = time.process_time()

    number_of_runs = 1

    param_dict = dict()
    param_dict['number_of_s_agents'] = 20
    param_dict['step_count'] = 600
    param_dict['sigma'] = 0.15 #accuracy ?

    # Connection parameters
    # communication mode can be either network, public or dynamical-network 
    param_dict['communication_mode'] = 'network'

    # p accept is the parameter controlling the public mode of communication
    param_dict['p_accept'] = 0.85

    # epsilon is the threshold for the bounded confidence in the dynamical-network mode
    param_dict['epsilon'] = 0.05

    # -- Creating the Network of Agents 

    #if param_dict['communication_mode'] == 'network':

        # 1 - Erdos Renyi Graphs
        # p = 0.7 #probability that an agent is connected to another (for Erdos Renyi graphs)
        # param_dict['graph'] = nx.fast_gnp_random_graph(param_dict['number_of_s_agents'], p)

        # 2 - Classical Graphs
        # cycle, wheel and complete :
        #classical_graphs = { 'Cycle' : nx.cycle_graph(param_dict['number_of_s_agents']), 'Wheel' : nx.wheel_graph(param_dict['number_of_s_agents']), 
                            #'Complete' : nx.complete_graph(param_dict['number_of_s_agents']) }

        # Cliques - Barbell Graphs
        #param_dict['graph'] = nx.barbell_graph(param_dict['number_of_s_agents']//2,0)

        # Simple Interconnected Islands
        # param_dict['nb_islands'] = 2
        # param_dict['size_island'] = param_dict['number_of_s_agents']//param_dict['nb_islands']
        # param_dict['p_in'] = 0.95
        # param_dict['nb_inter'] = 1
        # param_dict['graph'] = SII(param_dict['nb_islands'],param_dict['size_island'], param_dict['p_in'],param_dict['nb_inter']) # creating graph here or in the loop ? 


    # Displaying the social network of the agents

    plot_network = False

    if plot_network and param_dict['communication_mode']=='network' or param_dict['communication_mode']=='dynamical-network':
        nx.draw_networkx(param_dict['graph'], pos= nx.spring_layout(param_dict['graph']))
        plt.show()
    

    result_list = []
    mean_result_list = []

    debate_id = 0
    for N in [20]:
        for p_er in [0.1]:
        #param_dict['p_accept'] = p_accept
            for i in range(number_of_runs):
                #p = random.random()
                param_dict['world_value'] = random.random()
                param_dict['number_of_s_agents'] = N
                param_dict['graph'] = nx.fast_gnp_random_graph(param_dict['number_of_s_agents'], p_er)

            
                model = InformationDiffusion(param_dict, lightmode=True)
                model.run_model()
                model_stats = model.datacollector.get_model_vars_dataframe()
                agent_stats =  model.datacollector.get_agent_vars_dataframe()

                model_stats['Debate'] = debate_id
                agent_stats['Debate'] = debate_id
                model_stats['Issue Strength'] = param_dict['world_value']
                agent_stats['Issue Strength'] = param_dict['world_value']

                #model_stats['P accept'] = agent_stats['P accept'] = p_accept
                #model_stats['Graph'] = agent_stats['Graph'] = name
                #model_stats['P Erdos Renyi'] = agent_stats['P Erdos Renyi'] = p

                result_list += [(model_stats, agent_stats)]

                debate_id +=1

        
    # concatenating the dataframes
    result_model = pd.concat([m for (m,a) in result_list])
    result_agents = pd.concat([a for (m,a) in result_list])

    result_agents = pd.DataFrame(result_agents.to_records())

    dt_string = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    name = 'model_stats_' + dt_string + '.xlsx'
    writer = pd.ExcelWriter(name, engine='xlsxwriter')

    result_model.to_excel(writer, sheet_name='Model')
    result_agents.to_excel(writer, sheet_name='Agents')

    writer.save()

    print(time.process_time() - start, "seconds")

    # Plotting the final social graph

    if plot_network and param_dict['communication_mode']=='dynamical-network':
        nx.draw_networkx(model.network, pos= nx.spring_layout(model.network))
        plt.show()
    


    # ------------ Opinion Graph

    """We plot the opinions of the agent of one debate across time."""

    plot = False

    if plot:

        debate_id = 0
        data_adress = name

        debate_data = pd.read_excel(data_adress, sheet_name="Agents")
        debate_data = debate_data[debate_data["Debate"]==debate_id]
        issue_strength = debate_data["Issue Strength"][0]

        print(debate_data)
        debate_data = debate_data[["Step", "AgentID", "Opinion"]]

        tcd = pd.pivot_table(debate_data, values = "Opinion", index ="Step", columns ="AgentID")
        print(tcd)
        print(tcd.index)

        # defining colors for the chart

        # 4 communities of 5 agents 
        # red_range = [(255/255,(200 -x*50)/255, (200-x*50)/255) for x in range(5)] 
        # green_range = [((200-x*50)/255, 255/255, (200-x*50)/255) for x in range(5)]
        # blue_range = [((200-x*50)/255, (200-x*50)/255, 255/255) for x in range(5)]
        # purple_range = [(255/255, (200-x*50)/255, 255/255) for x in range(5)]
        
        # my_colors = red_range + green_range +blue_range + purple_range

        # 2 communities of 15 agents
        red_range = [(1, 0.9 - x*0.05, 0.9 - x*0.05 ) for x in range(15)]
        red_range.reverse()
        blue_range = [(0.9 - x*0.05 , 0.9 - x*0.05,1) for x in range(15)] 
        my_colors = red_range + blue_range



        tcd.plot( ylabel = "Agent opinions", color =my_colors),
        plt.plot(tcd.index, [issue_strength for i in tcd.index], color='black', linewidth=2, linestyle = "dashed")
        plt.plot(tcd.index, [0 for i in tcd.index], color='black', linewidth=1)
        plt.plot(tcd.index, [1 for i in tcd.index], color='black', linewidth=1)
        plt.show()


        

























                # seed += 1

            #results = pd.DataFrame(result_list)
            #results.to_excel(writer, sheet_name = str(p_favor))

            #print(results.mean())
            #writer.save()    

            #open text file
            # text_file = open("data.txt", "a")
            # text_file.write(str(results.mean())+ "\n")
            # text_file.close()

            #mean_result_list += [results.mean()]
            #result_list = []
    
    #mean_results = pd.DataFrame(mean_result_list)
    #mean_results.to_excel("mean_results_" + dt_string + ".xlsx")



        
        # print(results)
        # print("Average on ", number_of_runs, "runs : ", round(sum(results)/len(results), 4))
        
            
        




