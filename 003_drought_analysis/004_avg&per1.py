"""
File to calculate the difference between the observational and modelled spei data 
Author: Luca Boestfleisch 
file last updated on: 14.03.2024
"""
import xarray as xr 
from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import griddata

# all_days = 16435 
#31411 future 86 years from 201
# 16435 past 45 years from 1970-2014
# all_years = 45
##################################################
lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5
lon_length = 59 #10 #59
lon_length_model = (lon_max-lon_min)//50000*2
lon_length_obs = (lon_max-lon_min)//5000
print(f"lon length model: {lon_length_model}")
print(f"lon length obs: {lon_length_obs}")
lat_length = 77 #7 #77
lat_length_model = (lat_max- lat_min)//50000
lat_length_obs = (lat_max - lat_min)//5000 +1 
print(f"lat length model: {lat_length_model}")
print(f"lat length obs: {lat_length_obs}")
#################################################

######################################################################################
""" to calculate the mean spei over the entire timeperiod """
file_path = 'C:/03_Capstone/Data/Downscale/his-his/downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc'
data = Dataset(file_path, 'r')
Array2 = np.zeros((lon_length, lat_length), dtype=np.float32)
average_spei = np.zeros((lon_length, lat_length))

"depending strongly if the july or whole year calculation"
start_year = 59  #19,39,59
start_day = start_year *365  #before i had 31 but I think this is worng: only for one month 
print(start_day)
end_year = 59  #19, 39, 59, 85
end_day = end_year*365
print(end_year)

for j in range(lon_length): 
    for i in range(lat_length):
        spei_var = data.variables['predicted_spei'][:, j, i]

        # average_spei[i,j] = sum(spei_var)/all_days
        average_spei[j, i] = np.nanmean(spei_var)

    print(f"lon: {j}, lat: {i}")

output_file = 'C:/03_Capstone/Data/Downscale/his-his/downscale_his_avg_110524.nc'
# output_file_his = "C:/03_Capstone/Data/Future/historical/run2_140324/his_spei_avg_1970-2014.nc"
# output_file_obs = "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_avg_1970-2014.nc"
var = "spei_avg"
with Dataset(output_file, 'w', format='NETCDF4') as ds:
    lon = ds.createDimension('lon', lon_length)  
    lat = ds.createDimension('lat', lat_length)  

    lons = ds.createVariable('lon', 'f4', ('lon',))  
    lats = ds.createVariable('lat', 'f4', ('lat',)) 
    value = ds.createVariable(var, 'f4', ('lon', 'lat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)

    value[:, :] = average_spei


#############################################
"""
Calculating the trend over time
trend = average top 1% of spei
# # """
# file_path = 'C:/03_Capstone/Data/Downscale/his-his/downscale_hismodel_110524_lr001_bs128_hs300_dp5_epoch200.nc'
# data = Dataset(file_path, 'r')
# start_year = 59 #19, 39, 59,
# start_month = start_year *31
# start_day = start_year * 365 
# print(start_month)
# end_year = 59
# end_month = end_year*31
# end_day = end_year * 365
# print(end_month)
# percentile_spei = np.zeros((lon_length, lat_length))


# for j in range(lon_length): 
#     for i in range(lat_length):
#         spei_var = data.variables['predicted_spei'][:, j, i]

#         # average_spei[i,j] = sum(spei_var)/all_days
#         percentile_spei[j, i] = np.nanpercentile(spei_var, 1)

#     print(f"lon: {j}, lat: {i}")

# output_file = 'C:/03_Capstone/Data/Downscale/his-his/downscaled_his_avg_110524.nc'
# # output_file_his = "C:/03_Capstone/Data/Future/historical/run2_140324/his_spei_per1_1970-2014.nc"
# # output_file_obs = "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_per1_1970-2017.nc"
# var = "spei_per1"
# with Dataset(output_file, 'w', format='NETCDF4') as ds:
#     lon = ds.createDimension('lon', lon_length)  
#     lat = ds.createDimension('lat', lat_length)  

#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max, lat_length)

#     value[:, :] = percentile_spei


# print("start day:", start_day)
# print("end day", end_day)

#####################################################################################
"Calculate the anomalies of the avg and per1 files"
# variable = "spei_avg"

# his_path = "C:/03_Capstone/Data/Python_NetCDF_join/Output/run3_140324_CURRENT/obs_spei_avg_1970-2014.nc"     #################   ADAPT THIS!! 
# his_file = Dataset(his_path, 'r')        
# var_model = his_file.variables[variable][:]
# lon_model = his_file.variables['lon'][:]
# lat_model = his_file.variables['lat'][:]

# avg_path = "C:/03_Capstone/Data/Downscale/ssp585/anomaly_mean/ssp585_downscale_avg_2075-2100.nc"       #################   ADAPT THIS!!
# avg_file = Dataset(avg_path, 'r')
# var_obs = avg_file.variables[variable][:]
# lon_obs = avg_file.variables['lon'][:]
# lat_obs = avg_file.variables['lat'][:]

# Array2 = np.zeros((lon_length, lat_length), dtype=np.float32)

# for j in range(lon_length): 
#     for i in range(lat_length):
#         spei_climateavg = his_file.variables[variable][j,i]
#         spei = avg_file.variables[variable][j,i]
#         anomaly = spei -spei_climateavg 
#         Array2[j, i] = anomaly


# output_file = 'C:/03_Capstone/Data/Downscale/ssp585/anomaly_mean/ssp585_downscale_anomaly_avg_2075-2100.nc'
# var = "spei_anomaly"
# with Dataset(output_file, 'w', format='NETCDF4') as ds:
#     lon = ds.createDimension('lon', lon_length)  
#     lat = ds.createDimension('lat', lat_length)  

#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max, lat_length)

#     value[:, :] = Array2



######################################################################
'from calculating the difference to the observed files '

# for t in range(all_days): 
#     var_model_t = var_model[t]
#     var_obs_t = var_obs[t]
#     lon_obs_mesh, lat_obs_mesh = np.meshgrid(lon_obs, lat_obs)
#     lon_model_mesh, lat_model_mesh = np.meshgrid(lon_model, lat_model)
#     var_obs_interp = griddata((lon_obs_mesh.flatten(), lat_obs_mesh.flatten()), var_obs_t.flatten(),
#                               (lon_model_mesh, lat_model_mesh), method='linear')

#     difference = var_model_t - var_obs_interp
#     print(f"Timestep, difference: {t}/{all_days}")
#     Array[t,lon_model, lat_model] = difference


# # grid_x, grid_y = np.meshgrid(lon_obs, lat_obs)
# # lon_model_flat = lon_model.flatten()
# # lat_model_flat = lat_model.flatten()
# # points = np.column_stack((lon_model_flat, lat_model_flat))
# # values = var_obs.flatten()

# # var_low_res_interp = griddata(points, values, (grid_x, grid_y), method='linear')

# # # Calculate the difference between the high resolution and interpolated low resolution data
# # difference = var_model - var_low_res_interp


# ###
# # with Dataset(obs_data_path, "r") as f:
# #     # Crop the data
# #     x_min, x_max = lon_min, lon_max
# #     y_min, y_max = lat_min, lat_max
# #     x_indices = (f.variables['lon'][:] >= x_min) & (f.variables['lon'][:] <= x_max)
# #     y_indices = (f.variables['lat'][:] >= y_min) & (f.variables['lat'][:] <= y_max)
# #     pr_cropped = f.variables[var_obs][x_indices, y_indices]  # Assuming 'pr' is the precipitation variable

# #     # Resample to 5km x 5km resolution
# #     lon_resampled = np.linspace(lon_min, lon_max, lon_length)
# #     lat_resampled = np.linspace(lat_min, lat_max, lat_length)
# #     lon_resampled_2d, lat_resampled_2d = np.meshgrid(lon_resampled, lat_resampled)
# #     pr_resampled = np.empty((pr_cropped.shape[0], lat_length, lon_length))
# #     for i in range(pr_cropped.shape[0]):
# #         pr_resampled[i] = griddata((f.variables['lon'][x_indices], f.variables['lat'][y_indices]),
# #                                     pr_cropped[i], (lon_resampled_2d, lat_resampled_2d), method='linear')






# output_file = "C:/03_Capstone/Data/Analysis/dif_obs-his_1970-2014_180324.nc"    #################   ADAPT THIS!!
# var = "dif"
# dif_spei = np.zeros((lon_length, lat_length))

# with Dataset(output_file, 'w', format='NETCDF4') as ds:
#     lon = ds.createDimension('lon', lon_length)  
#     lat = ds.createDimension('lat', lat_length)  

#     times = ds.createVariable('f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max, lat_length)
#     times[:] = np.arange(0, all_days, 1)

#     value[:, :] = difference


