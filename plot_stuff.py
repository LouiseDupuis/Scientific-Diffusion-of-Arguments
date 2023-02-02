import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True # using latex style graphs
import numpy as np
import pandas as pd
### Plot 

adress1 = "mv_data_model_stats_01_02_2023 15_48_13.xlsx.csv"
adress2 = "mv_data_model_stats_01_02_2023 13_49_13.xlsx.csv"

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

mv_data = pd.read_csv(adress1).values.tolist() + pd.read_csv(adress2).values.tolist()
print(mv_data)

i=0
for N in [10,5]:
    for p_er in [0.1, 0.5, 0.9]:
        stability_data[N,p_er] = []
        for d in mv_data[i]:
            if d=='False':
                stability_data[N,p_er] += [650]
            else:
                stability_data[N,p_er] += [int(d)]
        i +=1



#### --------

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

m = 'o' #marker

s1=[]
s2=[]

for (N, p_er), points in stability_data.items():


        xs = [N for i in range(len(points))]
        ys = [p_er for i in range(len(points))]
        za = np.average(points)
        zs = points
        ax.scatter(xs, ys, zs, marker=m)
        ax.scatter(xs, ys, za, marker='^', color='black', linewidth=5)

ax.set_xlabel('$N$')
ax.set_ylabel('$p_{er}$')
ax.set_zlabel('First step of stability $t_s$')


plt.show()

