import numpy as np 
import pandas as pd
import sys
import os
import copy
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) 
assert spark.version >= '2.3'

data_schema = types.StructType([
    types.StructField('secs', types.LongType()),
    types.StructField('km', types.FloatType()),
    types.StructField('power', types.FloatType()),
    types.StructField('hr', types.LongType()),
    types.StructField('cad', types.LongType()),
    types.StructField('alt', types.FloatType())
]) 

revised_data_schema = types.StructType([
    types.StructField('empty', types.LongType()),
    types.StructField('secs', types.LongType()),
    types.StructField('km', types.FloatType()),
    types.StructField('power', types.FloatType()),
    types.StructField('hr', types.LongType()),
    types.StructField('cad', types.LongType()),
    types.StructField('alt', types.FloatType())
]) 


def write_data(path, out_directory, data_schema, revised):
	if(revised == 1):
		revised_data = spark.read.csv(path, schema = revised_data_schema)
		data = revised_data.drop('empty')
	else:
		data = spark.read.csv(path, schema = data_schema)
	
	cyclist_id = path.split(sep = '/')[1]
	fname = path.split(sep = '/')[2]

	#include file name to the data frame
	data_1 = data.withColumn('cyclist_id', functions.lit(cyclist_id)).withColumn('file_name', functions.lit(fname)) 

	data_1.write.csv(out_directory + '/' + cyclist_id, mode='append', header = True)


def extract_data(in_directory, out_directory):
	iterate = 0
	dir_list = np.sort(os.listdir(in_directory))

	for fname in dir_list:
		new_fname = in_directory + '/' + fname
		
		for fcsv in os.listdir(new_fname):
			
			#if csv file:
			if fcsv.endswith('.csv'):
				path = new_fname + '/' + fcsv

				if "revised" in fcsv:
					write_data(path, out_directory, revised_data_schema, 1)
				else:
					write_data(path, out_directory, data_schema, 0)



def main(in_directory, out_directory):
	#extract data:
	strava_list = extract_data(in_directory, out_directory)


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)