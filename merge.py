import pandas as pd


l = pd.read_csv('transform_data_9.csv')
r = pd.read_csv('data9.csv')

combined = pd.merge(l, r, left_on = ['cyclist_id', 'file_name'], right_on = ['cyclist_id', 'file_name'], how = "inner")
combined = combined.drop(columns ='Unnamed: 0')
combined.to_csv('final_9.csv', index = False)

