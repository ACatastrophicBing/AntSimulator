import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import glob

path = r'./data_food_home_targeted' # use your path
evapor_set = [0.0,2.0,4.0,6.0,8.0]
evapor_set.reverse()
mal_frac_set = [0.005, 0.01, 0.05, 0.1, 0.5]
mal_frac_set.reverse()
all_files = glob.glob(path + "/*.csv")
print(len(all_files))

width = len(evapor_set)
height = len(mal_frac_set)

spec_data = np.zeros((width,height,4))
temp_data = np.zeros((4))

for i, e in enumerate(evapor_set):
    for j, m in enumerate(mal_frac_set):

        count = 0

        for file in all_files:
            if ("mal_frac_home-"+str(m/2)) in file:
                if ("evpr-"+str(e)) in file:
                    dt = np.array(pd.read_csv(file, header=None))
                    modified_data = dt[-1]
                    modified_data = (modified_data)/(1-m)
                    temp_data = np.add(temp_data, modified_data)
                    count = count + 1
                    # break

        temp_data = temp_data / count

        spec_data[(width-1)-i,(height-1)-j] = temp_data
        temp_data = np.zeros((4))
        count = 0
    

# #heatmap axis
x = np.array(evapor_set)
# y = [str(n) for n in range(1,11)]
y = np.array(mal_frac_set)

x=x[::-1]
y=y[::-1]
color_blue = sns.color_palette("coolwarm_r", as_cmap=True)
color_green = sns.color_palette("coolwarm_r", as_cmap=True)

fig,axn = plt.subplots(2, 2, sharex=False, sharey=False)

df=[]

for i in range(spec_data.shape[-1]):
    df.append(pd.DataFrame(spec_data[:,:,i]))

cbar_mins = [0, 0, 0, 0]
cbar_maxs = [np.amax(spec_data[:,:,0]), np.amax(spec_data[:,:,1]), 1.0, 1.0]

for i,ax in enumerate(axn.flat):
    # if(i%2==0):
    #     df[i] = df[i].rename_axis("Rel Evaporation Multi")
    # if(i>1):
    #     df[i] = df[i].rename_axis("Malicious Ants Fraction", axis=1)
    df[i] = df[i].rename_axis("Rel Evaporation Multi")
    df[i] = df[i].rename_axis("Malicious Ants Fraction", axis=1)
    color = color_blue if i<2 else color_green
    plot = sns.heatmap(df[i], vmin=cbar_mins[i], vmax=cbar_maxs[i], ax=ax, xticklabels = y, yticklabels = x, cmap=color, cbar=True)#not(i%2==0))

plt.rcParams.update({'font.size': 22})
plt.show()
plot.figure.savefig("final_heatmaps/heatmap_targeted_food_home.png")
