import pandas as pd
import numpy as np
import sys
import os

"""
Calculates the Variability Index 
"""

def get_file(in_dir):
    file_name = []
    file_list =  os.listdir(in_dir)

    for i in range(len(file_list)):
        file_list[i] = in_dir + '/' + file_list[i] + '/'

    
    for file in file_list:
        for infile in os.listdir(file):
            if infile.endswith('.csv'): 
                path = file + infile
                file_name.append(file + infile)

    return file_name


# create one dataframe for all cycles of one individual
def get_data(list_file):

    li = []

    # for each .csv file (a cycle) in a directory
    for f in list_file:
        data = pd.read_csv(f)
        data = data.iloc[1: , :]
        li.append(data)

    # concatenate all information from every .csv into one dataframe 
    df = pd.concat(li, axis=0, ignore_index=True)
    return df


# calculates the variability index
def variability_index(df):

    df['rolling_avg'] = df.groupby(['cyclist_id','file_name'])['power'].transform(lambda x: x.rolling(20,1).mean())
    df['rolling_avg_power4'] = df['rolling_avg'] ** 4

    results = df.groupby(['cyclist_id', 'file_name']).agg(total_time_sec = ('secs','last'), total_dist_km = ('km','last'), 
        avg_power = ('power','mean'), avg_alt = ('alt', 'mean'), rolling_avg_power4 = ('rolling_avg_power4','mean')).reset_index(drop = False)
    
    results['normalized_power'] = results['rolling_avg_power4'] ** (1/4)

    #variability index calcations
    results['avg_power'] = np.round(results['avg_power'],3)
    results['avg_alt'] = np.round(results['avg_alt'], 3)
    results['v_index'] = np.round(np.divide(results['normalized_power'],results['avg_power']),3)
    results = results.drop(['normalized_power','rolling_avg_power4'], axis = 1)

    return results


def main(in_dir, out_dir):

    #get list of all the file in the folder:
    list_file = get_file(in_dir)

    #extract the file:
    data = get_data(list_file)      
    final = variability_index(data)
    
    #write the data to .csv file:
    final.to_csv(out_dir + '.csv',index = False)

if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    main(in_dir, out_dir)