import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob

path = r'./data_exp-mal_frac-mal_evpr_rate-one_iter' # use your path
evapor_set = [0.0,0.5,1.0,2.0,5.0,10.0,50.0,100.0,500.0,1000.0]
evapor_set = evapor_set[::-1]
all_files = glob.glob(path + "/*_iter-0.csv")

spec_data = np.zeros((10,10,100,4))

for i, e in enumerate(evapor_set):
    for m in range(1,11):
        for file in all_files:
            if ("mal_frac-"+str(("%.6f" % (2**-m)))) in file:
                if ("evpr-"+str(e)) in file:
                    dt = np.array(pd.read_csv(file, header=None))
                    # print(dt.shape)
                    modified_data = dt
                    modified_data = (modified_data)/(1-(2**-m))
                    spec_data[9-i,9-(m-1)] = modified_data
                    break

fig,axn = plt.subplots(10, 10, sharex=True, sharey=True)

for i,ax in enumerate(axn.flat):
    e = int(i/10)
    m = i%10
    data = spec_data[e,m]
    ax.plot(data)
    # ax.set_ylim([0,1.1])

# plt.xlabel('it/erations')
# plt.ylabel('cumulative food count/# of benevolent ants')
# plt.savefig("graphs/graph_all_ants_fraction.png")
plt.savefig("graphs/graph_all_food_collected_per_ant.png")

