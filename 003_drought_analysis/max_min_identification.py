"""
Purpose: identifying the maximum/minimum/average value thorughout a study area 
    for files with and without a time dimension 

Author: Luca Boestfleisch 
Date: 16.05.24

"""

from netCDF4 import Dataset
import numpy as np


analysis_file = "" #adapt 
data = Dataset(analysis_file, 'r')

var = "dr_freq" #adapt 

time = data.variables["time"][:] #uncomment if there is not a time dimension 
lon = data.variables["lon"][:]
lat = data.variables['lat'][:]

max = 0

"depending on the type of input data, uncomment some sections below"
"with time dimension"
for t in range(len(time)): 
    for j in range(len(lon)):
        for i in range(len(lat)): 
            data_input = data.variables[var][t, j, i]
            if data_input > max: 
                max = data_input
            else: 
                continue 
        # print(max)
    print("time:", t)

Array = np.zeros((len(lon), len(lat)), dtype=np.float32)

"without time dim"
for j in range(len(lon)):
    for i in range(len(lat)):
        data_input = data.variables[var][j, i]
        if data_input > max: 
            max = data_input
        else: 
            continue 
    print("latitude:", i)

print("The maximum", var, "in this period is:", max)


"mean avg days"
duration = []
for j in range(len(lon)):
    for i in range(len(lat)):
        data_input = data.variables[var][j, i]
        duration.append(data_input)
    print("latitude:", i)

mean = np.nanmean(duration)
print("Mean of avg drought days:", mean)
