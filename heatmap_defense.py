import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import glob

path = r'./data_defense_targeted_home' # use your path
patience_thresh = [50, 100, 500, 1000]
patience_thresh.reverse()
patience_refill = [1, 10, 100, 1000]
patience_refill.reverse()
all_files = glob.glob(path + "/*.csv")
print(len(all_files))

width = len(patience_thresh)
height = len(patience_refill)

spec_data = np.zeros((width,height,4))
temp_data = np.zeros((4))

for i, e in enumerate(patience_thresh):
    for j, m in enumerate(patience_refill):

        count = 0

        for file in all_files:
            if ("del_incr-"+str(m)) in file:
                if ("del_max-"+str(e)) in file:
                    dt = np.array(pd.read_csv(file, header=None))
                    modified_data = dt[-1]
                    modified_data = (modified_data)/(1-0.05)
                    temp_data = np.add(temp_data, modified_data)
                    count = count + 1
                    # break

        temp_data = temp_data / count

        spec_data[(width-1)-i,(height-1)-j] = temp_data
        temp_data = np.zeros((4))
        count = 0
    

# #heatmap axis
x = np.array(patience_thresh)
# y = [str(n) for n in range(1,11)]
y = np.array(patience_refill)

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
    if(i%2==0):
        df[i] = df[i].rename_axis("Maximum Patience Threshold")
    if(i>1):
        df[i] = df[i].rename_axis("Patience Refill Steps", axis=1)
    color = color_blue if i<2 else color_green
    plot = sns.heatmap(df[i], vmin=cbar_mins[i], vmax=cbar_maxs[i], ax=ax, xticklabels = y, yticklabels = x, cmap=color, cbar=True)#not(i%2==0))
    # plt.xticks(rotation = 45)

plot.figure.savefig("final_heatmaps/heatmap_defense_targeted_home.png")
