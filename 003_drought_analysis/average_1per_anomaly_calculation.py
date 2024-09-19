"""
purpose: calculate the climate average and top 1% for given time periods and calculate the anomalies to the avg/per1% SPEI of a reference dataset 

This file consists of 3 parts 
    1) calculation of mean SPEI over time 
    2) calculating the top 1% SPEI over time 
    3) Calculating anomalies 
Author: Luca Boestfleisch 
file last updated on: 14.03.2024
"""
import xarray as xr 
from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import griddata

"define the lon/lat min & max below "
'CMIP6'
# lon_max = 4323286.0
# lon_min =  4028021.5  
# lat_max = 3023612.5
# lat_min = 2641848.5
# lon_length = 59 #10 #59
# lon_length_model = (lon_max-lon_min)//50000*2
# lon_length_obs = (lon_max-lon_min)//5000
# print(f"lon length model: {lon_length_model}")
# print(f"lon length obs: {lon_length_obs}")
# lat_length = 77 #7 #77
# lat_length_model = (lat_max- lat_min)//50000
# lat_length_obs = (lat_max - lat_min)//5000 +1 
# print(f"lat length model: {lat_length_model}")
# print(f"lat length obs: {lat_length_obs}")


"CMIP5"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0
lon_length = 63
lat_length = 128

######################################################################################
""" to calculate the mean spei over the entire timeperiod """

file_path = 'C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/spei_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc' #adapt 
data = Dataset(file_path, 'r')
Array2 = np.zeros((lon_length, lat_length), dtype=np.float32)
average_spei = np.zeros((lon_length, lat_length))

"define below the start and end year number: only applies if it is daily data"
'based on a year basis'
# start_year = 0  #adapt
# start_day = start_year *365  
# print(start_day)
# end_year = 1  #adapt
# end_day = end_year*365
# print(end_year)

"based on the entire dataset"
start_day = 0
end_day = 14610

for j in range(lon_length): 
    for i in range(lat_length):
        spei_var = data.variables['spei'][start_day:end_day, j, i] #adapt the variable name if necessary 

        # average_spei[i,j] = sum(spei_var)/all_days
        average_spei[j, i] = np.nanmean(spei_var)

    print(f"lon: {j}, lat: {i}")

output_file = 'C:/03_Capstone/a_publishing/data/complete_CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/spei_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc' #adapt

var = "spei_avg" 
with Dataset(output_file, 'w', format='NETCDF4') as ds:
    lon = ds.createDimension('rlon', lon_length)  
    lat = ds.createDimension('rlat', lat_length)  

    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)

    value[:, :] = average_spei


#############################################
"""
Calculating the trend over time
trend = average top 1% of spei
# # """
# file_path = '' #adapt
# data = Dataset(file_path, 'r')
# start_year = 0 #adapt
# start_month = start_year *31
# start_day = start_year * 365 
# print(start_month)
# end_year = 1 #adapt 
# end_month = end_year*31
# end_day = end_year * 365
# print(end_month)
# percentile_spei = np.zeros((lon_length, lat_length))


# for j in range(lon_length): 
#     for i in range(lat_length):
#         spei_var = data.variables['predicted_spei'][start_day:end_day, j, i]  #adapt 

#         percentile_spei[j, i] = np.nanpercentile(spei_var, 1)

#     print(f"lon: {j}, lat: {i}")

# output_file = ''#adapt
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
variable = "spei_avg"

# his_path = ""     #adapt
# his_file = Dataset(his_path, 'r')        
# var_model = his_file.variables[variable][:]
# lon_model = his_file.variables['lon'][:]
# lat_model = his_file.variables['lat'][:]

# avg_path = ""       #adapt
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


# output_file = ''#adapt
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



