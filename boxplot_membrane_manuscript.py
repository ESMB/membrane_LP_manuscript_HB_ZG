import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load locs into a dataframe
path = r"/Users/user3/Documents/membrane_manuscript_data/reorg_data/combined_locs_data/"
file = "combined_cell_level_data_v2.csv"

os.chdir(path)
locs = pd.read_table(file, sep=",")
df = pd.DataFrame(data=locs)

sns.boxplot(data=df, x='Target', y='ratio')
sns.stripplot(data=df, x='Target', y='ratio', color='black')
plt.show()