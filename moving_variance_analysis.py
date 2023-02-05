import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



## Analysis : computing the variance of the opinion of each agent for a window of 20 steps
#(not optimized)


#data = pd.read_excel("20 agents_pER=0_1500_steps_model_stats_06_09_2022 11_08_13.xlsx",sheet_name = "Agents")
#data = pd.read_excel("20_agents_500_steps_model_stats_05_09_2022 15_45_18.xlsx",sheet_name = "Agents")
#data = pd.read_excel("model_stats_06_09_2022 14_59_11.xlsx",sheet_name = "Agents")
adress = "MABS_data\model_stats_05_02_2023 11_14_44.xlsx"
data = pd.read_excel(adress, sheet_name = "Agents")


##### plotting the rolling std for one agent for one debate :

#opinion_data1 = data[(data["Debate"] == 0) & (data["AgentID"] == 0)]["Opinion"]
# opinion_data2 = data[(data["Debate"] == 2) & (data["AgentID"] == 0)]["Opinion"]
# opinion_data3 = data[(data["Debate"] == 3) & (data["AgentID"] == 0)]["Opinion"]

# mv1 = opinion_data1.rolling(window=20).std()

# print(mv1)
# mv1.plot()

# mv2 = opinion_data2.rolling(window=20).std()
# mv2.plot()

# mv3 = opinion_data3.rolling(window=20).std()
# mv3.plot()


#####  Averaging for all agents of one debate 

fig, ax = plt.subplots()

def show_moving_variance(data,debate_index, threshold):
    data_debate = data[data["Debate"] == debate_index]
    pivot = pd.pivot_table(data_debate, values='Opinion', index='Step', columns='AgentID')
    mv = pivot.rolling(20).std()
    mv['mean'] = mv.mean(axis=1)

    mv['mean'].plot()
    mv['threshold'] = threshold
    mv['threshold'].plot()

    return mv
 

def compute_stability(data, debate_index, threshold, nb_steps):
    """This function returns the step at which a debate has reached stability, ie when the average moving variance has been lower than threshold for nb_steps steps. Returns False when the 
     stability has not beed reached. """
    
    data_debate = data[data["Debate"] == debate_index]
    pivot = pd.pivot_table(data_debate, values='Opinion', index='Step', columns='AgentID')
    mv = pivot.rolling(20).std()

    mv['mean'] = mv.mean(axis=1)
    #mv['threshold'] = 0.001
    mv['below_threshold'] = mv['mean'].values<threshold


    count=0
    for s, val in mv['below_threshold'].iteritems():
        if val:
            count += 1
        else: 
            count = 0
        if count >= nb_steps: 
            return s
    return False

# def compute_stability_for_df(df):
#     list_stability_steps=[]
#     for debate_index in df["Debate"].values:
#         data_debate = data[data["Debate"] == debate_index]
#         pivot = pd.pivot_table(data_debate, values='Opinion', index='Step', columns='AgentID')
#         mv = pivot.rolling(20).std()

#         mv['mean'] = mv.mean(axis=1)
#         #mv['threshold'] = 0.001
#         mv['below_threshold'] = mv['mean'].values<0.005
#         count=0
#         for s, val in mv['below_threshold'].iteritems():
#             if val:
#                 count += 1
#             else: 
#                 count = 0
#             if count >= 50: 
#                 list_stability_steps += [s]
#             else:
#                 list_stability_steps += [False]
#     return list_stability_steps


    
threshold = 0.005
nb_steps = 50

# compute stability for each debate in the data 

    
g_dict= dict()
for p_er in data["P ER"].unique():
    print(p_er)

    per_data = data[data["P ER"]==p_er]

    stab_list = []
    for debate_id in per_data["Debate"].unique():
        deb_data=per_data[per_data["Debate"]==debate_id]
        res = compute_stability(deb_data, debate_id, threshold, nb_steps)
        #print("Step where stability is reached", res)
        #show_moving_variance(data,i, threshold)

        stab_list += [res]
    g_dict[p_er]=stab_list


print(g_dict)
dt = pd.DataFrame(g_dict)
dt.to_csv("mv_data_5_agents_stability" +".csv")

# ax.legend(["MV", str(threshold)])

# plt.show()
