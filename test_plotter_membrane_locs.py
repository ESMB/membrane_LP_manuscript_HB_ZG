import pandas as pd
import os
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load locs into a dataframe
path = r"/Users/user3/Documents/membrane_manuscript_data/reorg_data/fig3_ato3/"
file = "fig3_ato3_test_results.csv"

os.chdir(path)
locs = pd.read_table(file, sep=",")
df = pd.DataFrame(data=locs)

# print(df.shape)
# print(df.head())

images = list(np.unique(df['source']))

for img in images:
    filtered_df = df[df['source'] == img]
    sns.set(rc={'figure.figsize':(4,4)})
    sns.scatterplot(data=filtered_df, x='X', y='Y', hue=df['membrane'], )
    plt.xlim(0,120)
    plt.ylim(0,120)
    plt.gca().invert_yaxis()
    plt.show()