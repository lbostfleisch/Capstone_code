"""
File to Calculate the Potential Evapotranspiration (ETP) and the Standardized Precipitation Evapotranspiration Index (SPEI)
    Calculating the PET based on temperature as calculated by McCloud 1955: 
    mentioned in paper Xiang et al., 2020
    ETp = 0.254 × 1.07 ^ (1.8Ta)
    Ta = 0.5 (Tmax+Tmin) 
    Tmax is maximum air temperature, ℃
    Tmin is minimum air temperature, ℃
    last updated: 13.03.2024

    Calculation of SPEI based on Wang et al., 2021

Author: Luca Boestfleisch, based on the above ETP calculation and SPEI calculation from Vicente-Serrano et al., 2010, and Wang et al., 2021
Date last updated: 20.03.2024
"""
import numpy as np
from netCDF4 import Dataset
import os
from scipy.stats import genextreme
import matplotlib.pyplot as plt
from spei import __version__


""""
File contents: Calculating the Waterbalance, Accumulated Waterbalance, the GEV-Distribution, and the SPEI values for daily data
STEP: 
0) Importing all the files 
1) Calculating the potential evapotranspiration (ETP) and saving it as the etp file 
2) Calculating the Water Balance Di, save the Di file 
3) Calculating the Accumulated Waterbalance Dk, for a time period k 
4) Calculating & Plotting the GEV distribution parameters, & Calculating the SPEI 

Note: everything that needs to be adapted between runs, is marked with the comment: 'ADAPT HERE'
"""


"STEP 0: Importing all the file paths"
# C:\03_Capstone\a_publishing\data\CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E\v2_r1i1p1\tasmax
tmax_nc_path = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/tasmax/tasmax_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_1965-2005_tempC.nc" #adapt 
tmin_nc_path = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/tasmin/tasmin_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_1965-2005_tempC.nc" #adapt 
precipitation_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/pr/pr_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day_joined_mm.nc" #adapt 
tmax_nc = Dataset(tmax_nc_path, 'r')
tmin_nc = Dataset(tmin_nc_path, 'r')
pr_data = Dataset(precipitation_file, 'r')

lon = tmax_nc.variables['rlon'][:]
lat = tmax_nc.variables['rlat'][:]
time = tmax_nc.variables['time'][:]
min_lon, max_lon, min_lat, max_lat = lon.min(), lon.max(), lat.min(), lat.max()

all_days = 14610
#14610 past CMIP5
#16435 past CMIP6
#31411 future 

"CMIP 6"
# lon_max, lon_min = 4323286.0, 4028021.5
# lat_max, lat_min = 3023612.5, 2641848.5
# lon_length = 10
# lon_length_model = (lon_max-lon_min)//50000*2
# lon_length_obs = (lon_max-lon_min)//5000
# print(f"lon length model: {lon_length_model}")
# print(f"lon length obs: {lon_length_obs}")
# lat_length = 7
# lat_length_model = (lat_max- lat_min)//50000
# lat_length_obs = (lat_max - lat_min)//5000 +1 
# print(f"lat length model: {lat_length_model}")
# print(f"lat length obs: {lat_length_obs}")

"CMIP 5"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0
lon_length = 63
lat_length = 128

# #Setting up array
Array_etp = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
Array_di = np.zeros((all_days, lon_length, lat_length), dtype=np.float32) 
Array_dk = np.zeros((all_days, lon_length, lat_length), dtype=np.float32) 
Array_spei = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)

# #####################################################################################################

"STEP 1: Calculating the ETP"
for t in range(all_days):
    for j in range(lon_length):
        for i in range(lat_length):
            tmax = tmax_nc.variables['tasmax'][t, j, i]
            tmin = tmin_nc.variables['tasmin'][t, j, i]

            # potential evapotransp iration formula McCloud 1955, (Xiang et al., 2020)
            ta = 0.5 * (tmax + tmin) 
            etp = 0.254 * (1.07**(1.8 * ta))
            Array_etp[t, j, i] = etp
    print(f"ETP Time step: {t}/{all_days}")


"""saving the file"""            
output_directory_etp = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/" #adapt 
output_file_etp = "etp_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc" #adapt 
var = "etp" #adapt 


with Dataset(os.path.join(output_directory_etp, output_file_etp), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  
    lat = ds.createDimension('rlat', lat_length)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array_etp

print("ETP file successfully calculated and saved!")

# #####################################################################################################

"STEP 2: Calculating the water balance Di"
pet_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/etp_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc"  #adapt 
pet_data = Dataset(pet_file, 'r')

for t in range(all_days):  
    for j in range(lon_length):
        for i in range(lat_length):
            pr_var = pr_data.variables['pr'][t, j, i] #adapt 
            pet_var = pet_data.variables['etp'][t, j, i] ##adapt 
            
            #Water balance Di
            di= pr_var - pet_var
            Array_di[t, j, i] = di

    print(f"Di, Time step: {t}/{all_days}")

output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/" #adapt 
output_file = "di_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc" #adapt 
var = "di" #adapt 

with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  
    lat = ds.createDimension('rlat', lat_length)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max,lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array_di


# ###################################################################################################################

"STEP 3: Accumulated Waterbalance (Dk) for the time period k"

Di_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/di_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc" #adapt 
Di_data = Dataset(Di_file, 'r')
# print(Di_data.variables['Di'].shape) #for a check, but not necessary 

for t in range(all_days): 
    for j in range(lon_length):
        for i in range(lat_length): 
            if t == 0: 
                Di_var0 = Di_data.variables['di'][t, j, i] 
                Dk = Di_var0
            elif 1 <= t <= 30: 
                k = t
                start_1 = 0
                Di_var1 = Di_data.variables['di'][start_1:k, j, i] 
                Dk = np.sum(Di_var1)
            else: 
                k = 30 #############     ADAPT HERE (if wanting a different k)!!
                start_2 = t-k
                Di_var2 = Di_data.variables['di'][start_2:t+1, j, i]
                Dk = np.sum(Di_var2)
            Array_dk[t, j, i] = Dk
    print(f"Dk, Time step: {t}/{len(time)}")
            
               
output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/" #adapt 
output_file = "dk_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc" #adapt 
var = "dk" #adapt 

"Saving the file "
with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  
    lat = ds.createDimension('rlat', lat_length)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array_dk


#########################################################################################################


"""STEP 4: GEV & OTHER CALCULATIONS

1) Calculating the GEV-probability distribution parameters (shape, location, and scale) from the netcdf data
2) Plotting the GEV in a histogram to visualize the distribution 
3) Having a for-loop to calculate the SPEI according to Wang et al., 2021
4) Plotting the SPEI distribution """

shape_gev_array = np.zeros((all_days, lon_length, lat_length))
loc_gev_array = np.zeros((all_days, lon_length, lat_length))
scale_gev_array = np.zeros((all_days, lon_length, lat_length))         


"SPEI Calculation & saving the data"
C0 = 2.515517 #Do not change these, as these are constants for the spei calculation 
C1 = 0.802853
C2 = 0.010328
d1 = 1.432788
d2 = 0.189269
d3 = 0.001308

Dk_file = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/dk_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc"#adapt
Dk_data = Dataset(Dk_file, 'r')#############     ADAPT HERE!! 

"Uncomment this if wanting to recalculate the shape/loc/scale of gev"
# Dk_variable_data = Dk_data.variables['dk'][:] 
# flattened_data = Dk_variable_data.flatten()
# valid_data = flattened_data[~np.isnan(flattened_data)]
# masked_values = np.ma.masked_invalid(valid_data)
# valid_data_without_mask = masked_values.compressed()
# threshold = np.percentile(valid_data_without_mask, 99.5)#to make sure the distribution fits correctly 
# print(threshold)
# neg_threshold = np.percentile(valid_data_without_mask, 0.5) #to make sure the distribution fits correctly
# print(neg_threshold) 
# # filtered_data = valid_data[valid_data < threshold]
# filtered_data = valid_data[np.logical_and(neg_threshold < valid_data, valid_data < threshold)]

# shape_gev, loc_gev, scale_gev = genextreme.fit(filtered_data)
# print(f"Gev dist calculated for dataset, shape: {shape_gev}, location: {loc_gev}, scale: {scale_gev}")

"Gev parameters calculated by the obs spei "
shape_gev = 0.5251186384248805  #Gev parameters from the observational data 
loc_gev = 12.869076457951188
scale_gev = 64.4255645545341

gev_dist = genextreme(shape_gev, loc=loc_gev, scale=scale_gev)

for t in range(all_days):
    for j in range(lon_length):
        for i in range(lat_length):
            Dk_var = Dk_data.variables['dk'][t, j, i]
            gev_pdf = gev_dist.cdf(Dk_var) #for the second method 
            P = 1 - gev_pdf
            # print(f"P value: {P}")
            if P <= 0.5:
                W = np.sqrt(-2 * np.log(P))
                # print(f"W value: {W}")
                spei1 = W - ((C0 + (C1 * W) + (C2 * (W ** 2))) / 
                        (1 + (d1 * W) + (d2 * (W ** 2)) + (d3 * (W ** 3))))
            else:
                P2 = 1-P
                W = np.sqrt(-2 * np.log(P2))
                # print(f"W value: {W}")
                spei1 = -1*(W - ((C0 + (C1 * W) + (C2 * (W ** 2))) / 
                        (1 + (d1 * W) + (d2 * (W ** 2)) + (d3 * (W ** 3)))))
            
            # print(f"spei1 value: {spei1}")

            Array_spei[t, j, i] = spei1
    print(f"spei, Time step: day {t}")

"Saving the spei data"
output_directory = "C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_KNMI-CNRM-CERFACS-CNRM-CM5_RACMO22E/v2_r1i1p1/output/" #adapt 
output_file = "spei_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_day.nc" #adapt 
var = "spei" #adapt 
with Dataset(os.path.join(output_directory, output_file), 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('rlon', lon_length)  
    lat = ds.createDimension('rlat', lat_length)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('rlon', 'f4', ('rlon',))  
    lats = ds.createVariable('rlat', 'f4', ('rlat',)) 
    value = ds.createVariable(var, 'f4', ('time', 'rlon', 'rlat'))  

    value.units = 'Unknown'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    value[:, :, :] = Array_spei

"To check the coherence of the calculations: (spatially) visually the data and the different trends"
print(f"Gev dist calculated for dataset, shape: {shape_gev}, location: {loc_gev}, scale: {scale_gev}")
print("SPEI calculated and correctly saved!! :) ")
