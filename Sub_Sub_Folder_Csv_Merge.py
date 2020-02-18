# data merging for multiple scans of each samples located in a directory

# Importing libraries and modules

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import glob, configparser


config = configparser.ConfigParser()
config.read('specx.conf')
method = config.get('method','input')

def csvmerge(csv_path):
	route = csv_path
	sub_dirs = [os.path.join(route, dir) for dir in os.listdir(route) if os.path.isdir(os.path.join(route, dir))]

	for dir in sub_dirs:
		#print(dir)
		# list that will store the names of all CSV in subdirectory 
		csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]

		# merging all CSV side by side based on same wavelength and reference values
		temp = pd.DataFrame()
		for filename in csv_files:
			df = pd.read_csv(filename, skiprows=range(0,29)).drop(columns=['Absorbance (AU)'])
			if temp.empty == True:
				temp = temp.append(df)
			else:
				temp = temp.merge(df, on=['Wavelength (nm)', 'Reference Signal (unitless)'], how='left')
		#print(temp)

		
		R = temp.iloc[:, 1].values
		#print(R)
		S = temp.iloc[:,2:].values.mean(axis=1)
		#print(S)
		W = temp.iloc[:,0].values
		A = np.log10(R/S)	
		temp['Absorbance'] = A
		temp = temp.fillna(0)
		#print(temp)

		# Storing values to seperate CSV files
		if method == 'paddy':
			temp.to_csv(route + '/{}.csv'.format(os.path.basename(dir)[0:]+route[41:56]), index=False)
		elif method == 'normal':
			temp.to_csv(route + '/{}.csv'.format(os.path.basename(dir)[0:]), index=False)
		

	# Joining CSV files to create dataset

	csv_files = [os.path.join(route, csv) for csv in os.listdir(route) if os.path.isfile(os.path.join(route, csv)) and csv.endswith('.csv')]

	new_df = pd.DataFrame()
	for filename in csv_files:
		String_Split = route.split('\\')
		temp = []
		df = pd.read_csv(filename)
		param = os.path.basename(filename).rstrip('.csv')
		P_1 = String_Split[-1]
		temp.append(P_1)
		temp.append(param)
		temp.extend(df['Wavelength (nm)'])
		temp.extend(df['Absorbance'])
		temp_df = pd.DataFrame([temp])
		new_df = new_df.append(temp_df, sort = False)


	# Storing dataset into excel workbook
	new_df.to_excel(route+'/{}.xlsx'.format(P_1), index=False)

	#print(Sub_Dirs)
	return [route+'/{}.xlsx'.format(P_1)]

if method == 'normal':
	Route_1 = r'C:\\Users\Shuvashri\Downloads\drive-download-20200212T043636Z-001\\'

if method == 'paddy':
	Route_1 = r'C:\\Users\Shuvashri\Downloads\PADDY\PADDY\direct refrence\\'


item = os.listdir(Route_1)
for i in item:
	csvmerge(Route_1+i)
All_Excel = pd.DataFrame()

for root, dirs, files in os.walk(Route_1, topdown=True):
	for i in glob.glob(root+'/*.xlsx'):
		All_Excel = All_Excel.append(pd.read_excel(i))
		#print(All_Excel)
	
		#print(All_Excel)

All_Excel.to_csv(Route_1+'/Final.csv', index=False)