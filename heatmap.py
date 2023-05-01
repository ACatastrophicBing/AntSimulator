import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import glob

path = r'./data' # use your path
evapor_set = [0.0,2.0,4.0,6.0,8.0]
evapor_set.reverse()
mal_frac_set = [0.005, 0.01, 0.05, 0.1, 0.5]
mal_frac_set.reverse()
all_files = glob.glob(path + "/*.csv")

width = len(evapor_set)
height = len(mal_frac_set)

spec_data = np.zeros((width,height,4))
temp_data = np.zeros((4))

for i, e in enumerate(evapor_set):
    for j, m in enumerate(mal_frac_set):

        count = 0

        for file in all_files:
            if ("mal_frac_home-"+str(m)) in file:
                if ("evpr-"+str(e)) in file:
                    # print("mal_frac_home-"+str(m))
                    # print("evpr-"+str(e))
                    # print(m)
                    dt = np.array(pd.read_csv(file, header=None))
                    modified_data = dt[-1]
                    # print(modified_data[2])
                    modified_data = (modified_data)/(1-m)
                    # print(modified_data[2])
                    temp_data = np.add(temp_data, modified_data)
                    print(temp_data)
                    count = count + 1
                    # break

        temp_data = temp_data / count

        print(count)
        print(temp_data)

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

fig,axn = plt.subplots(2, 2, sharex=True, sharey=True)

df=[]

for i in range(spec_data.shape[-1]):
    df.append(pd.DataFrame(spec_data[:,:,i]))

for i,ax in enumerate(axn.flat):
    if(i%2==0):
        df[i] = df[i].rename_axis("Rel Evaporation Multi")
    if(i>1):
        df[i] = df[i].rename_axis("Malicious Ants Fraction", axis=1)
    color = color_blue if i<2 else color_green
    plot = sns.heatmap(df[i], ax=ax, xticklabels = y, yticklabels = x, cmap=color, cbar=not(i%2==0))
    plt.xticks(rotation = 45)

plot.figure.savefig("graphs/heatmap_all_data.png")
