
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import pandas as pd

""" This script is used to run additionnal analysis on the data obtained from the model simulation."""


# ------------ Opinion Graph

"""We plot the opinions of the agent of one debate across time."""

debate_id = 0
data_adress = "model_stats_20_01_2023 11_19_36.xlsx"

debate_data = pd.read_excel(data_adress, sheet_name="Agents")
debate_data = debate_data[debate_data["Debate"]==debate_id]
issue_strength = debate_data["Issue Strength"][0]

print(debate_data)
debate_data = debate_data[["Step", "AgentID", "Opinion"]]

tcd = pd.pivot_table(debate_data, values = "Opinion", index ="Step", columns ="AgentID")
print(tcd)
print(tcd.index)

# defining colors for the chart
red_range = [(255/255,(200 -x*50)/255, (200-x*50)/255) for x in range(5)] 
green_range = [((200-x*50)/255, 255/255, (200-x*50)/255) for x in range(5)]
blue_range = [((200-x*50)/255, (200-x*50)/255, 255/255) for x in range(5)]
purple_range = [(255/255, (200-x*50)/255, 255/255) for x in range(5)]
 
my_colors = red_range + green_range +blue_range + purple_range


tcd.plot( ylabel = "Agent opinions", color =my_colors),
plt.plot(tcd.index, [issue_strength for i in tcd.index], color='black', linewidth=2, linestyle = "dashed")
plt.plot(tcd.index, [0 for i in tcd.index], color='black', linewidth=1)
plt.plot(tcd.index, [1 for i in tcd.index], color='black', linewidth=1)
plt.show()


