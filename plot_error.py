import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd

# Influence of sigma on one agent 
adress = "MABS_data\model_stats_02_02_2023 16_43_41.xlsx" # 1 agent ?


data = pd.read_excel(adress, sheet_name="Model")
data = data[data["Step"]>450].groupby("Debate")["Sigma", "Truth Deviation"].mean()
print(data)

data.plot.scatter("Sigma", "Truth Deviation", marker="+", color="orange")
p_data=data.groupby("Sigma")["Truth Deviation"].mean()
print(p_data)
plt.scatter(p_data.index, p_data.values)

plt.xlabel("$\sigma$")
plt.ylabel("Truth Devation $TD$")
plt.show()

# influence of P ER on a community of agents 

adress = "MABS_data\merged_10_agents_p_er_500_steps.xlsx" #merged 10 agents, p_er vary

data = pd.read_excel(adress, sheet_name="Model")
data = data[data["Step"]>450].groupby("Debate")["P ER", "Truth Deviation"].mean()
print(data)

data.plot.scatter("P ER", "Truth Deviation", marker="+", color="orange")
p_data=data.groupby("P ER")["Truth Deviation"].mean()
print(p_data)
plt.scatter(p_data.index, p_data.values)

plt.xlabel("$p_{ER}$")
plt.ylabel("Truth Devation $TD$")
plt.show()