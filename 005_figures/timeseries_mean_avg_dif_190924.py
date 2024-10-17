"""This file is to plot the netcdf data as timeseries. To do this the data is average over all grid cells for a given time step. 
Author: Luca Boestfleisch 
Last updated: 22.02.24"""

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


start_day_CMIP5 = 4 * 365 + 1 + 1
end_day_obs = 16435 - (9 * 365 + 2)
print('start step for the CMIP5 data', start_day_CMIP5) 
print('end step for the observational data', end_day_obs)


'''explanation about the timesteps
the CMIP5 dataset ranges from 1966 (incl) to 2005 (incl), however, the observational dataset only ranges from 1970 (incl) - 2014 (incl)
So want the data for the overlap: 1970 - 2005
leap years in that range: 1968 & 2008, 2012 
=> hence the start point for the CMIP5 data is 4 years in (incl 1 leap year), I also added 1 more day because the calculated day is the last dat in 1969, the next day is the first day in 1970
 and the observational data end point is the total length - 9 years in which there are 2 leap years '''


file_path_RACMO = 'C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/spei_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc' #######  ADAPT THIS 
# C:\03_Capstone\Data\Python_NetCDF_join\Output\run3_140324_CURRENT
# C:\03_Capstone\Data\Future\ssp585\02_run2_160324
data_RACMO = nc.Dataset(file_path_RACMO, 'r')  
variable = "spei" #####  ADAPT THIS 
units = "??" #######   ADAPT THIS
latitude = data_RACMO.variables['rlat'][:]
longitude = data_RACMO.variables['rlon'][:]
time_model = data_RACMO.variables['time'][:] 
variable_to_average_RACMO = data_RACMO.variables[variable][start_day_CMIP5:14610, :, :] 



file_path_HIRHAM = "C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5/r12i1p1_v1/output/spei_CMIP5_EUR-11_DMI_ICHEC-EC-EARTH_historical_HIRHAM5_r12i1p1_v1_day.nc"
data_HIRHAM = nc.Dataset(file_path_HIRHAM, 'r')  
variable_to_average_HIRHAM = data_HIRHAM.variables[variable][start_day_CMIP5:14610, :, :] 

file_path_CCLM = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output/spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc"
data_CCLM = nc.Dataset(file_path_CCLM, 'r')
variable_to_average_CCLM = data_CCLM.variables[variable][start_day_CMIP5:14610, :, :]

file_path_pentad = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output/pentads_spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc"
data_pentad = nc.Dataset(file_path_pentad, 'r')
variable_to_average_pentad = data_pentad.variables['pentad_avg'][:, :, :] #length of pentad time 2629
time_pentad = data_pentad['pentad'][:]

# file_path_obs  ="C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_1970-2014.nc"
file_path_obs  ="C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/one_grid_cell_obs_spei_1970-2014.nc"
data_obs = nc.Dataset(file_path_obs, 'r')
variable_to_average_onegrid = data_obs.variables[variable]
print(f"data obs shape: {variable_to_average_onegrid.shape}")
# variable_to_average_obs = data_obs.variables[variable][0:end_day_obs, :, :] 
# variable_to_average_obs = data_obs.variables[variable][:, :, :] #no time restriction 
# time_obs = data_obs.variables['time'][:]
time_obs = data_obs.variables['time']
print(time_obs.shape)


"Calculating the mean for each time step over lat and lon"
# average_values_RACMO = np.nanmean(variable_to_average_RACMO, axis=(1, 2))
# min_values_RACMO = np.nanmin(variable_to_average_RACMO, axis=(1, 2))

# average_values_HIRHAM = np.nanmean(variable_to_average_HIRHAM, axis=(1, 2))
# min_values_HIRHAM = np.nanmin(variable_to_average_HIRHAM, axis=(1, 2))

# average_values_CCLM = np.nanmean(variable_to_average_CCLM, axis=(1,2))
# min_values_CCLM = np.nanmin(variable_to_average_CCLM, axis=(1,2))

# average_values_pentad = np.nanmean(variable_to_average_pentad, axis=(1,2))
# min_values_pentad = np.nanmin(variable_to_average_pentad, axis=(1,2))

# average_values_obs = np.nanmean(variable_to_average_obs, axis=(1,2))
# min_values_obs = np.nanmin(variable_to_average_obs, axis=(1,2))

# dif_obs_racmo = average_values_obs[:] - average_values_RACMO[:]
# mean_dif_obs_racmo = np.mean(dif_obs_racmo)
# print("dif_obs_racmo mean:", mean_dif_obs_racmo)

# dif_obs_hirham = average_values_obs[:] - average_values_HIRHAM[:]
# mean_dif_obs_hirham = np.mean(dif_obs_hirham)
# print("dif_obs_hirham mean:", mean_dif_obs_hirham)

# dif_obs_CCLM = average_values_obs[:] - average_values_CCLM[:]
# mean_dif_obs_CCLM = np.mean(dif_obs_CCLM)
# print("dif_obs_CCLM mean:", mean_dif_obs_CCLM)

"plotting average"
"CMIP5 average values"
# plt.plot(time_model[start_day_CMIP5:14610], average_values_RACMO, label='Mean Value RACMO', color = 'lightblue')
# plt.plot(time_model[start_day_CMIP5:14610], average_values_HIRHAM, label='Mean Value HIRHAM', color = 'orange') 
# plt.plot(time_model[start_day_CMIP5:14610], average_values_CCLM, label='Mean Value CCLM', color = 'purple') 
# plt.plot(time_pentad, average_values_pentad, label='Mean Value CCLM pentad', color = 'purple') 

"observational average values"
# plt.plot(time_obs, average_values_obs, label='Mean Value', color = 'grey') 
plt.plot(time_obs, variable_to_average_onegrid, label='Mean Value', color = 'grey') 

"plotting differences"
# plt.plot(time_obs[0:13148], dif_obs_racmo, label='difference Value racmo', color = 'lightblue')  #13148 is the total amount of overlapping days between the 2 datasets 
# plt.plot(time_obs[0:13148], dif_obs_hirham, label='difference Value hirham', color = 'orange') 
# plt.plot(time_obs[0:13148], dif_obs_CCLM, label='difference Value CCLM', color = 'purple') 


plt.xlabel('Time')
plt.ylabel(f'mean {variable} Value in {units}')
plt.title(f'mean {variable} Value over {len(time_obs)} days')

"adding a trendline"
'UNCOMMENT if wanting to add a trendline to the average data'
# slope_RACMO, intercept_RACMO, _, _, _ = stats.linregress(time_model, average_values_RACMO)
# trend_line_RACMO = slope_RACMO * time_model + intercept_RACMO
# line_RACMO, = plt.plot(time_model, trend_line_RACMO, label='Trend Line', color='darkblue', linestyle='--')

# slope_HIRHAM, intercept_HIRHAM, _, _, _ = stats.linregress(time_model, average_values_HIRHAM)
# trend_line_HIRHAM = slope_HIRHAM * time_model + intercept_HIRHAM
# line_HIRHAM, = plt.plot(time_model, trend_line_HIRHAM, label=f'Slope={slope_HIRHAM:.10f}', color='darkorange', linestyle='--')

# slope_obs, intercept_obs, _, _, _ = stats.linregress(time_obs, average_values_obs)
# trend_line_obs = slope_obs * time_obs + intercept_obs
# line_obs, = plt.plot(time_obs, trend_line_obs, label=f'Slope={slope_obs:.10f}', color='darkorange', linestyle='--')

# custom_labels = [
#     f'RACMO22e',
#     f'HIRHAM5',
#     f'observational'
# ]
# custom_labels = [
#     f'observational '
# ]
# plt.legend([line_RACMO, line_HIRHAM, line_obs], custom_labels)
# plt.legend([line_obs], custom_labels)
plt.legend()
plt.show()

"plotting minimum"
'UNCOMMENT if wanting to plot the minimum spei and not average'
# plt.plot(time_model, min_values_RACMO, label='Min Value of RACMO22', color = 'lightblue') 
# plt.plot(time_model, min_values_HIRHAM, label='Min Value of HIRHAM5', color = 'orange') ### plotting the maximum 
# ### plotting the maximum 
# plt.xlabel('Time')
# plt.ylabel(f'minimum {variable} Value in {units}')
# plt.title(f'minimum {variable} Value over {len(time_model)} days')
# plt.legend()
# plt.show()

# Close the NetCDF file
data_obs.close()
data_HIRHAM.close()
data_RACMO.close()
data_CCLM.close()