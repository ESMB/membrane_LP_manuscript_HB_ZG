import numpy as np
import itertools

import pandas
import pandas as pd
import os

path = '/Users/user3/Documents/membrane_manuscript_data/reorg_data/combined_locs_data/'

raw_results = os.listdir(path)

li = []
filename_contains = '.csv'

for file in raw_results:
    if filename_contains in file:

        peakfit_df = pd.read_csv(path + file)

        rows = peakfit_df.shape[0]

        target = [file[:9]] * rows
        peakfit_df['target'] = target

        li.append(peakfit_df)

concat_data = pd.concat(li)

target_names = list(np.unique(concat_data['target']))

protein_target = []
cell = []
locs = []
membrane_locs = []

for t in target_names:
    temp_df = concat_data[concat_data['target'] == t]
    cell_ids = list(np.unique(temp_df['cell_id']))

    for id in cell_ids:
        if id[0] != '0':
            temp_cell_df = temp_df[temp_df['cell_id'] == id]

            protein_target.append(t)
            cell.append(id)
            locs.append(temp_cell_df.shape[0])
            membrane_locs.append(temp_cell_df.membrane.value_counts().mem)

combined_data = pd.DataFrame(list(zip(protein_target, cell, locs, membrane_locs)),
                             columns =['Target', 'Cell_ID', 'Locs', 'Membrane_locs'])

combined_data['ratio'] = combined_data['Membrane_locs'] / combined_data['Locs']

combined_data.to_csv(path + 'combined_cell_level_data_v2.csv', index=False)
