"""This file is to plot the netcdf data as timeseries. To do this the data is average over all grid cells for a given time step. 
Author: Luca Boestfleisch 
Last updated: 22.02.24"""

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

file_path = 'C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/spei_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc' #######  ADAPT THIS 
# C:\03_Capstone\Data\Python_NetCDF_join\Output\run3_140324_CURRENT
# C:\03_Capstone\Data\Future\ssp585\02_run2_160324
data = nc.Dataset(file_path, 'r')  
variable = "spei" #####  ADAPT THIS 
units = "??" #######   ADAPT THIS
latitude = data.variables['rlat'][:]
longitude = data.variables['rlon'][:]
time_model = data.variables['time'][:]
# CMIP5_startday = 1461-1
# CMIP5_endday = len(time)-1
# CMIP5_length = CMIP5_endday - CMIP5_startday
# # time = data.variables['time'][:]
# print("time length", time.size)

# print(CMIP5_length)
# variable_to_average = data.variables[variable][CMIP5_startday:CMIP5_endday, :, :] 
variable_to_average = data.variables[variable][1462:14610, :, :] 



file_path2 = "C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/output/spei_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5_r12i1p1_v1_day.nc"
data2 = nc.Dataset(file_path2, 'r')  
variable_to_average2 = data2.variables[variable][1462:14610, :, :] 

file_path_obs  ="C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_1970-2014.nc"
data_obs = nc.Dataset(file_path_obs, 'r')
variable_to_average_obs = data_obs.variables[variable][0:13148, :, :] 
time_obs = data_obs.variables['time'][:]
print(time_obs.shape)


"Calculating the mean for each time step over lat and lon"
# variable_to_average = variable_to_average[:, :, CMIP5_startday:CMIP5_endday]
average_values = np.nanmean(variable_to_average, axis=(1, 2))
# # max_values = np.nanmin(variable_to_average, axis=(1, 2))

# # variable_to_average2 = variable_to_average2[:, :, CMIP5_startday:CMIP5_endday]
average_values2 = np.nanmean(variable_to_average2, axis=(1, 2))
# # max_values2 = np.nanmin(variable_to_average2, axis=(1, 2))

average_values_obs = np.nanmean(variable_to_average_obs, axis=(1,2))

dif_obs_racmo = average_values_obs[:] - average_values[:]
mean_dif_obs_racmo = np.mean(dif_obs_racmo)
print("dif_obs_racmo mean:", mean_dif_obs_racmo)
dif_obs_hirham = average_values_obs[:] - average_values2[:]
mean_dif_obs_hirham = np.mean(dif_obs_hirham)
print("dif_obs_hirham mean:", mean_dif_obs_hirham)
"plotting average"
# plt.plot(time, average_values, label='Mean Value', color = 'lightblue') ### plotting the average 
# plt.plot(time, average_values2, label='Mean Value', color = 'orange') ### plotting the average 
# plt.plot(time_obs, average_values_obs, label='Mean Value', color = 'grey') ### plotting the average 
plt.plot(time_obs[0:13148], dif_obs_racmo, label='difference Value racmo', color = 'grey') ### plotting the average 
plt.plot(time_obs[0:13148], dif_obs_hirham, label='difference Value hirham', color = 'green') ### plotting the average 

plt.xlabel('Time')
plt.ylabel(f'mean {variable} Value in {units}')
plt.title(f'mean {variable} Value over {len(time_obs)} days')

"adding a trendline"
# slope1, intercept1, _, _, _ = stats.linregress(time, average_values)
# trend_line = slope1 * time + intercept1
# line1, = plt.plot(time, trend_line, label='Trend Line', color='darkblue', linestyle='--')

# slope2, intercept2, _, _, _ = stats.linregress(time, average_values2)
# trend_line2 = slope2 * time + intercept2
# line2, = plt.plot(time, trend_line2, label=f'Slope={slope2:.10f}', color='darkorange', linestyle='--')

# slope_obs, intercept_obs, _, _, _ = stats.linregress(time, average_values_obs)
# trend_line_obs = slope_obs * time + intercept_obs
# line_obs, = plt.plot(time, trend_line_obs, label=f'Slope={slope_obs:.10f}', color='darkorange', linestyle='--')

# custom_labels = [
#     f'RACMO22e',
#     f'HIRHAM5',
#     f'observational'
# ]
# custom_labels = [
#     f'observational '
# ]
# plt.legend([line1, line2, line_obs], custom_labels)
# plt.legend([line_obs], custom_labels)
plt.legend()
plt.show()

"plotting maximum"
# plt.plot(time, max_values, label='Min Value of RACMO22', color = 'lightblue') 
# plt.plot(time, max_values2, label='Min Value of HIRHAM5', color = 'orange') ### plotting the maximum 
# ### plotting the maximum 
# plt.xlabel('Time')
# plt.ylabel(f'minimum {variable} Value in {units}')
# plt.title(f'minimum {variable} Value over {len(time)} days')
# plt.legend()
# plt.show()

# Close the NetCDF file
data.close()
