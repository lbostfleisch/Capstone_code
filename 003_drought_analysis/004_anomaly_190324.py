"""
File to calculate the climate anomalies of the future spei data for the day 25.07 (warmest day on record in GER)
Steps : 
(1) Calculate the avg on the 25.07 in the his modelled dataset 
(2) Calculate the anomaly for the timeperiod 2015-2035, 2035-2055, 2055, 2055-2075, 2075-2100 
Last updated on 19.03.24
Author: Luca Boestfleisch 
"""
import numpy as np
from netCDF4 import Dataset
import os


"Step 1: Calculate the avg of the 25.07 in the past dataset"
# year = 1972
# a = 1970 - year
# print(a)
# calc = (a+2)%4
# print(calc)
# day = 0
# #16435 past 
# #31411 future 
# all_days_past = 16435
# num_years = 45
# num_months = 45*31
# lon_max = 4323286.0
# lon_min =  4028021.5  
# lat_max = 3023612.5
# lat_min = 2641848.5
# lon_length = 10
# lat_length = 7

# spei_file_past = "C:/03_Capstone/Data/Future/historical/run2_140324/spei_july_1970-2014_regrid.nc"#############     ADAPT HERE!!!
# spei_data_past = Dataset(spei_file_past, 'r')
# Array = np.zeros((num_months, lon_length, lat_length), dtype=np.float32) #############     ADAPT HERE (lon/lat if necessray)!! 
# b = 0

# 'for one day'
# # for year in range (1970, 2014+1, 1):
# #     a = 1970 - year
# #     if a == 0: 
# #         day = 205 #although it is the 206th day, python starts counting at 0, so it is the 205th day in python 
# #     elif ((a + 2)%4) == 0:
# #         day += 366
# #     else: 
# #         day += 365
# #     print(f"year: {year}, day of July 25: {day}")    
# #     t = day 
# #     for j in range(lon_length):
# #         for i in range(lat_length):
# #             # print(t)
# #                 spei_var = spei_data_past.variables['spei'][t, j, i]
# #                 Array[b, j, i] = spei_var
# #     b += 1
        
# 'for one month'
# for year in range (1970, 2014+1, 1):
#     a = 1970 - year
#     if a == 0: 
#         day_july1 = 181 #although it is the 206th day, python starts counting at 0, so it is the 205th day in python 
#         day_july31 = 211 #although it is the 212th day, python starts counting at 0, so it is the 211th day in python 
#     elif ((a + 2)%4) == 0:
#         day_july1 += 366
#         day_july31 += 366
#     else: 
#         day_july1 += 365
#         day_july31 += 365
#     print(f"year: {year}, July 01: {day_july1}") 
#     print(f"year: {year}, July 31: {day_july31}")
#     for t in range(all_days_past):
#         if  day_july1 <= t <= day_july31: 
#             for j in range(lon_length):
#                 for i in range(lat_length):
#                     spei_var = spei_data_past.variables['spei'][t, j, i]
#                     Array[b, j, i] = spei_var   
#             b += 1

# output_directory = "C:/03_Capstone/Data/Future/historical/run2_140324" #############     ADAPT HERE!!
# output_file = "spei_july_1970-2014_regrid.nc" #############     ADAPT HERE!!
# var = "spei_split" #############     ADAPT HERE!!

# with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
#     time = ds.createDimension('time', num_months)
#     lon = ds.createDimension('lon', lon_length)  
#     lat = ds.createDimension('lat', lat_length)  

#     times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max,lat_length)
#     times[:] = np.arange(0, num_months, 1)

#     value[:, :, :] = Array


####################################################################################
"calculate the future time periods spei for july for the whole dataset"
#16435 past 
#31411 future 
all_days_past = 16435
all_days_future = 31411
num_months = 86 *31
lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5
# lon_length = 10
# lat_length = 7

# spei_file = "C:/03_Capstone/Data/Future/ssp126/run1_200324/ssp126_spei_2015-2100_obsgevpara.nc"#############     ADAPT HERE!!!
# spei_data_past = Dataset(spei_file, 'r')
# Array = np.zeros((num_months, lon_length, lat_length), dtype=np.float32) #############     ADAPT HERE (lon/lat if necessray)!! 
# b = 0

"for one day"
# for year in range (2015, 2100+1, 1):
#     a = 2015 - year
#     if a == 0: 
#         day = 205 #although it is the 206th day, python starts counting at 0, so it is the 205th day in python 
#     elif ((a + 2)%4) == 0:
#         day += 366
#     else: 
#         day += 365
#     print(f"year: {year}, day of July 25: {day}")    
#     t = day 
#     for j in range(lon_length):
#         for i in range(lat_length):
#             # print(t)
#                 spei_var = spei_data_past.variables['spei'][t, j, i]
#                 Array[b, j, i] = spei_var
#     b += 1

"for one month"
# for year in range (2015, 2100+1, 1):
#     a = 2015 - year
#     if a == 0: 
#         day_july1 = 181 #although it is the 182th day, python starts counting at 0, so it is the 181 day in python 
#         day_july31 = 211 #although it is the 212th day, python starts counting at 0, so it is the 211th day in python 
#     elif ((a + 2)%4) == 0:
#         day_july1 += 366
#         day_july31 += 366
#     else: 
#         day_july1 += 365
#         day_july31 += 365
#     # print(f"year: {year}, day of July 25: {day}")    
#     for t in range(all_days_future):
#         if  day_july1 <= t <= day_july31: 
#             for j in range(lon_length):
#                 for i in range(lat_length):
#                     spei_var = spei_data_past.variables['spei'][t, j, i]
#                     Array[b, j, i] = spei_var   
#             b += 1

# output_directory = "C:/03_Capstone/Data/Future/ssp126/run1_200324/" #############     ADAPT HERE!!
# output_file = "ssp126_spei_july_2015-2100.nc" #############     ADAPT HERE!!
# var = "spei" #############     ADAPT HERE!!

# with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
#     time = ds.createDimension('time', num_months)
#     lon = ds.createDimension('lon', lon_length)  
#     lat = ds.createDimension('lat', lat_length)  

#     times = ds.createVariable('time', 'f4', ('time',))
#     lons = ds.createVariable('lon', 'f4', ('lon',))  
#     lats = ds.createVariable('lat', 'f4', ('lat',)) 
#     value = ds.createVariable(var, 'f4', ('time', 'lon', 'lat'))  

#     value.units = 'Unknown'

#     lons[:] = np.linspace(lon_min, lon_max, lon_length)
#     lats[:] = np.linspace(lat_min, lat_max,lat_length)
#     times[:] = np.arange(0, num_months, 1)

#     value[:, :, :] = Array
