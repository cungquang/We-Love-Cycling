import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy.stats import gaussian_kde
import scikit_posthocs as sp
import seaborn as sns
import sys
import os

sns.set(style="ticks", color_codes=True)

def get_file(dir):
    file_name = []
    file_list =  os.listdir(in_dir)

    for i in range(len(file_list)):
        file_list[i] = in_dir + '/' + file_list[i]

    return file_list

# create one dataframe for all cycles of one individual
def get_data(list_file):
    li = []

    # for each .csv file (a cycle) in a directory
    for f in list_file:
    	data = pd.read_csv(f)
    	li.append(data)

    df = pd.concat(li, axis=0, ignore_index=True)
    return df


def main(in_dir):

	list_file = get_file(in_dir)
	data = get_data(list_file)

	#Pre clean - remove outlier for v_index:
	v_outlier = data['v_index'].between(1, 2, inclusive = True)
	subdata = data[v_outlier]
	subdata = subdata[subdata['avg_alt'] < 2500]


	#use <subdata> after this point
	#generate summary
	cyclist = subdata['cyclist_id'].unique()
	
	per_cyclist = subdata.groupby(['cyclist_id']).agg(days = ('file_name','count'), longest_time = ('total_time_sec', 'max'),
		shortest_time = ('total_time_sec', 'min'), avg_time = ('total_time_sec', 'mean'), longest_distance = ('total_dist_km', 'max'),
		shortest_distance = ('total_dist_km', 'min'), avg_distance = ('total_dist_km', 'mean'),max_v_index = ('v_index', 'max'),
		min_v_index = ('v_index', 'min'), avg_v_index = ('v_index', 'mean'), highest_alt = ('avg_alt', 'max'),
		lowest_alt_meters = ('avg_alt', 'min'), avg_alt_meters = ('avg_alt', 'mean'),max_s_index = ('s_index', 'max'),
		min_s_index = ('s_index', 'min'), avg_s_index = ('s_index', 'mean'))
	per_cyclist = np.round(per_cyclist, 2)
	
	#print(per_cyclist)

	subdata['velocity'] = np.divide(subdata['total_dist_km'], (subdata['total_time_sec']/3600))

	#calculate the density point:
	x = subdata['v_index'].to_numpy()
	y = subdata['velocity'].to_numpy()
	xy = np.vstack([x,y])
	z = gaussian_kde(xy)(xy)
	idx = z.argsort()
	x, y, z = x[idx], y[idx], z[idx]

	fig, ax = plt.subplots()
	density = ax.scatter(x, y, c=z, s=50, cmap=plt.cm.jet)
	plt.xlabel('v_index')
	plt.ylabel('performance (km/hr)')
	plt.colorbar(density)
	#plt.show()
	fig.savefig('Images/Density')

	#pair plot variable:
	sns_pair = sns.pairplot(subdata,height=2.5, vars = ['v_index', 's_index', 'total_time_sec', 'total_dist_km','avg_power','avg_alt'])
	sns_pair.savefig('Images/pairplot.png')


	#There are not normally distribute, however this is sufficient large dataset >1000 sample - it is okay to apply anova:
	#ANOVA analysis:
	anova = stats.f_oneway(subdata['v_index'], subdata['s_index'], subdata['total_time_sec'], subdata['total_dist_km'],
		subdata['avg_alt'])
	print("Anova testing:")
	print(anova)
	
	#melt the data for post_hoc test:
	melt_table = subdata.melt(value_vars = ['v_index', 's_index', 'total_time_sec', 'total_dist_km','avg_power','avg_alt'])

	#POST_HOC Pairwise_turkeyhsd analysis:
	turkey = pairwise_tukeyhsd(melt_table['value'], melt_table['variable'], alpha = 0.05)
	print("Post_hoc Pairwise_tukeyhsd:")
	print(turkey)


	#KRUSKAL analysis:
	kruskal = stats.kruskal(subdata['v_index'], subdata['s_index'], subdata['total_time_sec'], subdata['total_dist_km'],
		subdata['avg_alt'])
	print("Kruskal testing:")
	print(kruskal)

	#POST_HOC Dunn analysis:
	dunn = sp.posthoc_dunn(a = melt_table, val_col = 'value', group_col = 'variable', p_adjust = 'bonferroni')
	print("Post_hoc Dunn analysis:")
	print(dunn)




if __name__ == "__main__":
    in_dir = sys.argv[1]
    main(in_dir)

