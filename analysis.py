import pandas as pd 


# Computing the number of major and minor opinions.
# This is a temporary analysis file and should not be reused in this state. 

# extracting data
path = "C:/Users/Louise/OneDrive/Bureau/Diffusion of Scientific Information/ModelStats/Agents in Networks\Public Diffusion - model_stats_26_07_2022 10_57_32.xlsx"
data = pd.read_excel(path, sheet_name="Agents")

#only looking at the last step : 
data = data.loc[data['Step'] == 24]
print(data)

# compute the number of agents in each opinion slice for every debate 
total_list = []
major_opinion_list = []
p_list = []

number_of_debates = max(list(data['DebateID']))

for d in range(number_of_debates):

    nb_list = [0 for i in range(20)]
    debate_data = data.loc[data['DebateID'] == d]
    p_list += [debate_data.iloc[-1]['P accept']]
    for a in range(20):
        opinion = debate_data.loc[debate_data['AgentID'] == a]['Opinion'].unique()[0]
        index = int(opinion *20)
        nb_list[index] += 1
    total_list += [nb_list]
    max_nb = max(nb_list)
    new_list = [i/max_nb for i in nb_list]
    number_major_opinions = sum(1 for i in new_list if i >= 1/4)
    major_opinion_list += [number_major_opinions]


total_df = pd.DataFrame.from_records(total_list)
total_df['Major Opinions'] = major_opinion_list
total_df['P accept'] = p_list

writer = pd.ExcelWriter("Opinion analysis - Public Communications.xlsx", engine = 'xlsxwriter')
total_df.to_excel(writer, sheet_name = 'Opinion Analysis')
writer.save()
writer.close()


