import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd

adress = "model_stats_02_02_2023 16_43_41.xlsx"
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
