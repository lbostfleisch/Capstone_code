"""
Create file for calculating the highest amount of XX in SSP scenarios 
23.04.2024
"""

from netCDF4 import Dataset
import numpy as np


# analysis_file = "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585/ssp585_drought_analysis_190424.nc"
analysis_file = "C:/03_Capstone/Data/Analysis/01_drought_analysis/ssp585/ssp585_avg_drought_duration_190424.nc"
data = Dataset(analysis_file, 'r')

# var = "dr_freq"
var = "flash_dr_count"
# var = "avg_drought_duration"
# time = data.variables["time"][:]
lon = data.variables["lon"][:]
lat = data.variables['lat'][:]

max = 0
# for t in range(len(time)): 
#     for j in range(len(lon)):
#         for i in range(len(lat)): 
#             data_input = data.variables[var][t, j, i]
#             if data_input > max: 
#                 max = data_input
#             else: 
#                 continue 
#         # print(max)
#     print("time:", t)

# Array = np.zeros((len(lon), len(lat)), dtype=np.float32)

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
# duration = []
# for j in range(len(lon)):
#     for i in range(len(lat)):
#         data_input = data.variables[var][j, i]
#         duration.append(data_input)
#     print("latitude:", i)

# mean = np.nanmean(duration)
# print("Mean of avg drought days:", mean)
