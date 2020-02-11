# data merging for multiple scans of each samples located in a directory

# Importing libraries and modules

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


route = r'C:\Users\Shuvashri\Downloads\new turmeric scans\new turmeric scans'


sub_dirs = [os.path.join(route, dir) for dir in os.listdir(route) if os.path.isdir(os.path.join(route, dir))]

for dir in sub_dirs:
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
	temp.to_csv(route + '/{}.csv'.format(os.path.basename(dir)[0:]), index=False)

# Joining CSV files to create dataset

csv_files = [os.path.join(route, csv) for csv in os.listdir(route) if os.path.isfile(os.path.join(route, csv)) and csv.endswith('.csv')]

new_df = pd.DataFrame()
for filename in csv_files:
	temp = []
	df = pd.read_csv(filename)
	param = os.path.basename(filename).rstrip('.csv')
	temp.append(param)
	temp.extend(df['Wavelength (nm)'])
	temp.extend(df['Absorbance'])
	temp_df = pd.DataFrame([temp])
	new_df = new_df.append(temp_df, sort = False)


# Storing dataset into excel workbook
new_df.to_excel(route+'/merged_Dataset.xlsx', index=False)




