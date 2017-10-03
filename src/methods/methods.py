
import pandas as pd
import numpy as np

def round_res (vals, resolution):
	#assert(isinstance(vals, list)), "Input should be a list"
	vals_rd = [ np.round (value / resolution) for value in vals]
	return vals_rd

def bar_coordinates(hista, threshold, binsa,  resolution, acc,
	TP_COLOUR = '#e03344',FP_COLOUR = '#ef7b28',TN_COLOUR = '#09ef33',FN_COLOUR = '#aabf22'):
	"""
	Based on score histogram data, create data points and coloring schema for flatten histogram 
	data. Dash requires arrays for plots

	"""
	#
	hist_exp1 = []
	bins_exp1 = []
	colors_1 = []
	colors_2 = []
	#Get the counts for each class for each column on the histogram
	target_acc = acc.score.as_matrix()
	#print(target_acc)

	# create this as a percentage
	target_hist = []
	#print(binsa)

	for cnt in range(0,len(target_acc),2):
		target_hist.append( (target_acc[cnt]/ ( target_acc[cnt] + target_acc[cnt+1])))

	#round up values first
	# Generate colors accoriding to target
	cnt = 0
	step =1/len(binsa)

	for value, x in zip(hista,binsa[1:]):
		no_points = int(value //10  +1) * resolution
		y_points = np.arange(0,value,value/no_points)+ 1
		x_points = (x)*np.ones(no_points)
		class_0 =  int(round(no_points*target_hist[cnt]))
		class_1 = no_points - class_0
		# create the colors based on the thresold
		if x >threshold:
			colors1 = [[FP_COLOUR for c in range(class_0)], [TP_COLOUR for c in range(class_1)]]
		else:
			colors1 = [[FN_COLOUR for c in range(class_0)], [TN_COLOUR for c in range(class_1)]]
		#update vars
		cnt = cnt+1
		hist_exp1.append([y for y in y_points])
		bins_exp1.append([x1 for x1 in x_points])
		colors_1.append(colors1)


	# Unnest lists
	hist_exp  = [val for sublist in hist_exp1 for val in sublist]
	bins_exp  = [val for sublist in bins_exp1 for val in sublist]
	colors_exp  = [val for sublist in colors_1 for val in sublist]
	colors_exp  = [val for sublist in colors_exp for val in sublist]



	# COnvert to np arrays for plotting
	bins_exp = np.asarray(bins_exp)
	hist_exp = np.asarray(hist_exp)
	colors_exp = np.asarray(colors_exp)


	return hist_exp, bins_exp, colors_exp


def histogram_data(input_df, threshold, resolution, bins, target_col = 'class', score_col = 'score',
	TP_COLOUR = '#e03344',FP_COLOUR = '#ef7b28',TN_COLOUR = '#09ef33',FN_COLOUR = '#aabf22'):
	df = input_df.copy()
	hista, binsa = np.histogram(df[score_col], bins = bins, range = [0,1])
	df['cat']= pd.cut(df[score_col], binsa)
	acc =  df[['cat',target_col,score_col]].groupby(['cat',target_col]).count()
	acc.fillna(0,inplace=True)
	# Get now the data to plot 
	# -> for a bar of size 2, we want for exampole to create 8 vertical coordinates

	hist_exp, bins_exp, colors_exp= bar_coordinates(hista, threshold, binsa, resolution, acc)

	return hist_exp, bins_exp, colors_exp


def histogram_data_dict(input_df, resolution, bins, target_col = 'class', score_col = 'score',
	TP_COLOUR = '#e03344',FP_COLOUR = '#ef7b28',TN_COLOUR = '#09ef33',FN_COLOUR = '#aabf22'):
	"""
	Receive data frame and based on score and target data, create a dicionarly of flatten histogram 
	for each threshold for plotting purposes

	"""

	df = input_df.copy()
	hista, binsa = np.histogram(df[score_col], bins = bins, range = [0,1])
	# Bin scores according to the histogram data
	df['cat']= pd.cut(df[score_col], binsa)
	# Split histogram data by target column and get the counts for each class for each bin 
	acc =  df[['cat',target_col,score_col]].groupby(['cat',target_col]).count()
	acc.fillna(0,inplace=True)
	# Get now the data to plot 
	# -> for a bar of size 20, we want for exampole to create 8 data points, and the coloring split according 
	#     to the known target value
	hist_dict = dict()
	bins_dict = dict()
	colors_dict = dict()

	for threshold in binsa:
		hist_exp, bins_exp, colors_exp= bar_coordinates(hista, threshold, binsa, resolution, acc)
		hist_dict[threshold] = hist_exp
		bins_dict[threshold] = bins_exp
		colors_dict[threshold] = colors_exp
				


	return hist_dict, bins_dict, colors_dict