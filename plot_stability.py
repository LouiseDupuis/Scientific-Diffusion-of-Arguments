import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd
### Plot 

adress1 = "MABS_data\mv_data_10_agents_stability.csv" #10 agents
#adress2 = "MABS_data\mv_data_model_stats_01_02_2023 13_49_13.xlsx.csv" # 5 agents
adress2 = "MABS_data\mv_data_5_agents_stability.csv" # 5 agents, 1000 steps
adress3 = "MABS_data\mv_data_20_agents_stability.csv" # 20 agents

stability_data = dict()
# stability_data[0.001,0.9] = [169, 138, 125, 229, 135, 145, 114, 118, 278, 109]
# stability_data[0.001,0.5] = [522, 605, 298, 629, 345, 404, 434, 364, 212, 449]
# stability_data[0.001,0.1] = [137, 84, 187, 132, 154, 323, 171, 130, 157, 80]

# stability_data[0.25,0.9] = [131, 202, 158, 185, 208, 134, 105, 316, 111, 301]
# stability_data[0.25,0.5] = [241, 370, 356, 267, 101, 142, 190, 223, 215, 182]
# stability_data[0.25,0.1] = [119, 115, 111, 169, 338, 122, 644, 140, 332, 156]

# stability_data[0.8,0.9] = [ 206, 273, 181, 173, 302, 251, 226, 345, 219, 328]
# stability_data[0.8,0.5] = [293, 325, 486, 343, 294, 224, 332, 668, 329, 218]
# stability_data[0.8,0.1] = [201, 202, 344, 135, 155, 268, 84, 281, 305, 328]

data1=pd.read_csv(adress1)
data1["N"] = 10


data2=pd.read_csv(adress2)
data2["N"] = 5

data3=pd.read_csv(adress3)
data3["N"] = 20

# data3=pd.read_csv(adress3)
# data3["N"] = 20

stability_data = pd.concat([data1, data2, data3], axis=0,ignore_index=True)
print(stability_data)

# for row in mv_data.items()
#         stability_data[N,p_er] = []
#         for d in mv_data[i]:
#             if d=='False':
#                 stability_data[N,p_er] += [650]
#             else:
#                 stability_data[N,p_er] += [int(d)]
#         i +=1



#### --------

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

m = 'o' #marker

cmap = plt.cm.get_cmap('tab10')
colors = dict([(N,cmap(N*0.05)) for N in stability_data["N"].unique()])

for N in stability_data["N"].unique():
        color = colors[N]
        averages=[]
        for p_er in stability_data.columns[1:-1]:
                points = stability_data[stability_data["N"]==N][str(p_er)].values
                print(points)

                xs = [N for i in range(len(points))]
                ys = [float(p_er) for i in range(len(points))]
                za = np.average(points)
                zs = points
                ax.scatter(xs, ys, zs, marker=m, color=color)
                ax.scatter(xs, ys, za, marker='^', color='black', linewidth=5)
                averages+=[(N,float(p_er),za)]
        ax.plot([N for N,p_er,av in averages], [p_er for N,p_er,av in averages], [av for N,p_er,av in averages], color=color)

ft_size = 15
ax.set_xlabel('$N$')
ax.set_ylabel('$p_{er}$')
ax.set_zlabel('First step of stability $t_s$')
plt.xticks(fontsize = ft_size)
plt.yticks(fontsize = ft_size)
ax.xaxis.label.set_size(ft_size)
ax.yaxis.label.set_size(ft_size)
ax.zaxis.label.set_size(ft_size)

plt.show()

