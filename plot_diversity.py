import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd

#adress1 = "model_stats_02_02_2023 18_31_54.xlsx" #10 agents, 10 debates, 500 steps
#adress = "model_stats_03_02_2023 12_01_25.xlsx" 10 agents, ?? debates, 100 steps
#adress2 = "Output_Data\MABS_data\model_stats_02_02_2023 18_36_59.xlsx" #10 agents, 10 debates, 500 steps
adress = "MABS_data\merged_10_agents_p_er_500_steps.xlsx" #merged 

ft_size = 15 # font size for axis labels

data = pd.read_excel(adress, sheet_name="Model")
print(data)
data = data[data["Step"]==498]
print(data)

data.plot.scatter("P ER", "Opinion Diversity", marker="+", color="orange")
p_data=data.groupby("P ER")["Opinion Diversity"].mean()
print(p_data)
plt.scatter(p_data.index, p_data.values)
plt.plot(p_data.index, p_data.values)

plt.xlabel("$p_{ER}$", font_size=ft_size)
plt.ylabel("Opinion Diversity $ED$", font_size=ft_size)
plt.xticks(fontsize = ft_size)
plt.yticks(fontsize = ft_size)
plt.show()
