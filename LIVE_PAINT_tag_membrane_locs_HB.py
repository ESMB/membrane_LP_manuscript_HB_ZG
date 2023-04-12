from PIL import Image
import numpy as np
import itertools
import pandas as pd
import os
import re

###~ file structure ~###
# path
# │
# └───cell_masks
# │   │
# │   └───target_folder_1
# │       │   file_1_cell.png
# │       │   file_2_cell.png
# │       │   ...
# │
# └───membrane_masks
# │   │
# │   └───target_folder_1
# │       │   file_1_membrane.png
# │       │   file_2_membrane.png
# │       │   ...
# │
# └───target_folder_1
#     │   file_1_results.csv
#     │   file_2_results.csv
#     │   ...


path = ''

target_folder = '/'

cell_files = os.listdir(path+'cell_masks/'+target_folder)
membrane_files = os.listdir(path+'membrane_masks/'+target_folder)

li = []
filename_contains = '.png'

for file in membrane_files:
    if filename_contains in file:

        # open png file with 'membrane' mask and makes an array of all pixel intensities
        im_membrane = Image.open(path+'membrane_masks/'+target_folder+file)
        print("Opening file: " + file)
        pic_membrane = np.array(im_membrane)
        im_membrane.close()

        # open png file with 'cell' mask and makes an array of all pixel intensities
        cell_filename = file[:-13] + "_cell.png"
        im_cell = Image.open(path+'cell_masks/'+target_folder+cell_filename)
        print("Opening file: " + cell_filename)
        pic_cell = np.array(im_cell)
        im_cell.close()

        # creates a list of unique grayscale values that corresponds to cell-id - this is same list for both cell and membrane
        # so only doing this once
        cell_id_list = list(np.unique(pic_membrane))
        cell_id_list.remove(0)
        # print(cell_id_list)

        # creating an empty dictionary to eventually store all the coordinates of pixels in the membrane mask
        membrane_coords = {}
        cell_coords = {}

        # loops through each cell id to extract coordinates of all pixels pertaining to that cell
        # appends to list-of-lists membrane_coords
        for i in cell_id_list:
            membrane_locs = np.where(pic_membrane == i)
            y_mem = membrane_locs[0]
            x_mem = membrane_locs[1]

            np.array((x_mem, y_mem))
            # m_coords is a single list of coords for a single cell
            m_coords = list(zip(x_mem, y_mem))

            # each key is a cell_id containing list of coordinates in dictionary membrane_coords
            membrane_coords[i] = m_coords

            cell_locs = np.where(pic_cell == i)
            y_cell = cell_locs[0]
            x_cell = cell_locs[1]

            np.array((x_cell, y_cell))
            # m_coords is a single list of coords for a single cell
            c_coords = list(zip(x_cell, y_cell))

            # each key is a cell_id containing list of coordinates in dictionary cell_coords
            cell_coords[i] = c_coords


        # separating out keys and values from the dictionary
        key_list_m = list(membrane_coords.keys())
        val_list_m = list(membrane_coords.values())

        key_list_c = list(cell_coords.keys())
        val_list_c = list(cell_coords.values())

        # combines into a single list - would need to remove and change to do each cell separately
        val_list_m = list(itertools.chain.from_iterable(val_list_m))
        val_list_c_temp = list(itertools.chain.from_iterable(val_list_c))

        print("Completed coordinate list construction. Opening csv.")
        #opening csv with peak fit results
        csv_filename = file[4:-13] + '.tif (LSE) SuperRes_15nm_fit_results.csv'
        peakfit_df = pd.read_csv(path + target_folder + csv_filename)

        peakfit_df['ceilX'] = np.ceil(peakfit_df['X'])
        peakfit_df = peakfit_df.astype({'ceilX': 'int'})
        peakfit_df['ceilY'] = np.ceil(peakfit_df['Y'])
        peakfit_df = peakfit_df.astype({'ceilY': 'int'})

        # creating empty lists for df columns
        membrane = []
        cell_id = []

        def get_key(val):
            for key, value in cell_coords.items():
                #print(key, value)
                if val in value:
                    return key
            return 0

        rows = peakfit_df.shape[0]

        source = [file[4:-13]] * rows

        # looping through each row to extract coordinates of each localisation and
        # matching it to membrane mask to check whether membrane or not
        for index, row in peakfit_df.iterrows():
            loc_coords = (peakfit_df['ceilX'][index], peakfit_df['ceilY'][index])
            if loc_coords in val_list_m:
                membrane.append('mem')
            elif loc_coords in val_list_c_temp:
                membrane.append('cel')
            else:
                membrane.append('no')

            cell_id.append(str(get_key(loc_coords))+'_'+file[4:-13])

        peakfit_df['source'] = source

        print("Appended metadata to dataframe.")

        # adding membrane column to dataframe and outputting modified csv
        peakfit_df['membrane'] = membrane
        print("Appended membrane column to dataframe.")
        peakfit_df['cell_id'] = cell_id
        print("Appended cell_id column to dataframe.")

        li.append(peakfit_df)

combined_data = pd.concat(li)
combined_data.to_csv(path + 'combined_locs_data/' + target_folder[:9] + '_results.csv', index=False)