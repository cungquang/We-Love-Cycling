## We Love Cycling
<!-- blank line --> 
This project aims to serve the purposes of completing the required component of CMPT 353. The report.pdf discusses the entirety of the project. 

## Compilation Instructions

#### Libraries Required
* sys
* os
* numpy
* pandas
* matplotlib.pyplot
* seaborn
* scipy.stats
* pyspark.sql

#### Execution
1. Extract raw_data.zip and run strava_write.py on Spark, with arguments: 
	- input directory 
	- output directory
    - Example: spark-submit strava_write.py raw_data data_1

<!-- blank line -->
2. Run strava_var_index.py to calculate statistics:
	- Example: python3 strava_var_index.py data_1 analyze_data/analyze_1

<!-- blank line -->
3. Run elevationGL.py to calculate elevation index.

<!-- blank line -->
4. Run merge.py to combine results from elevationGl.py with strava_var_index.py.

<!-- blank line -->
5. Run strava_analyze.py to perform analysis:
	- Example: python3 strava_analyze <folder - final_data>
