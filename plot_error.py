import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd


ft_size = 15 # fotn size for axis labels

# Influence of sigma on one agent 
adress = "MABS_data\model_stats_02_02_2023 16_43_41_error_1_agent.xlsx" # 1 agent ?


# data = pd.read_excel(adress, sheet_name="Model")
# data = data[data["Step"]==499].groupby("Debate")["Sigma", "Truth Deviation"].mean()
# print(data)

# data.plot.scatter("Sigma", "Truth Deviation", marker="+", color="orange")
# p_data=data.groupby("Sigma")["Truth Deviation"].mean()
# print(p_data)
# plt.scatter(p_data.index, p_data.values)
# plt.plot(p_data.index, p_data.values)

# plt.xlabel("Experimental Accuracy $\sigma$", fontsize=ft_size)
# plt.ylabel("Truth Devation $TD$", fontsize=ft_size)
# plt.xticks(fontsize = ft_size)
# plt.yticks(fontsize = ft_size)
# plt.show()

# influence of P ER on a community of agents 

adress = "MABS_data\merged_10_agents_p_er_500_steps.xlsx" #merged 10 agents, p_er vary

data = pd.read_excel(adress, sheet_name="Model")
print(data.columns)

# truth deviation
data_grouped = data[data["Step"]==499].groupby("Debate")["P ER", "Truth Deviation", "Collective Error"].mean()
print(data_grouped)

#data_grouped.plot.scatter("P ER", "Truth Deviation", marker="+", color="orange")
av_data=data_grouped.groupby("P ER")["Truth Deviation", "Collective Error"].mean()
print(av_data)
plt.scatter(av_data.index, av_data["Truth Deviation"].values)
plt.plot(av_data.index, av_data["Truth Deviation"].values)

# global error

#data_grouped.plot.scatter("P ER", "Collective Error", marker="+", color="purple")
g_data=data_grouped.groupby("P ER")["Collective Error"].mean()
print(g_data)
plt.scatter(g_data.index, g_data.values)
plt.plot(g_data.index, g_data.values)


plt.xlabel("$p_{ER}$", fontsize = ft_size)
plt.ylabel("Truth Devation $TD$", fontsize=ft_size)
plt.xticks(fontsize = ft_size)
plt.yticks(fontsize = ft_size)
plt.show()