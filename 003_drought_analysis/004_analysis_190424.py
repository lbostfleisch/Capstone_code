"""
Drought Analysis
This code analyses the presence of droughts, amount of drought days (duration), 
    amount of drought periods (frequency), their minimum spei value (intensity)

This code defines it all in one code and saves it to one file with several variables 
Author: Luca Boestfleisch 
Last updated on: 19.04.24

"""
from netCDF4 import Dataset
import numpy as np
import os


#defining the extends, and loading files 
lon_max = 4323286.0
lon_min =  4028021.5  
lat_max = 3023612.5
lat_min = 2641848.5
lon_length = 59                                            ####################### ADAPT THIS 
lon_length_model = (lon_max-lon_min)//50000*2
lon_length_obs = (lon_max-lon_min)//5000
print(f"lon length model: {lon_length_model}")  #10
print(f"lon length obs: {lon_length_obs}")  #59
lat_length = 77                                              ####################### ADAPT THIS 
lat_length_model = (lat_max- lat_min)//50000
lat_length_obs = (lat_max - lat_min)//5000 +1 
print(f"lat length model: {lat_length_model}")  #7
print(f"lat length obs: {lat_length_obs}")   #77

spei_path = "C:/03_Capstone/Data/Downscale/ssp126/downscale_ssp126_050524_lr001_bs128_hs300_dp5_epoch200.nc"  
spei_data = Dataset(spei_path, 'r')
spei_var = "predicted_spei"

all_days = 31411                                              ####################### ADAPT THIS 
#16435 past 
#31411 future 

"Defining where the output files should save to"
output_nc_file = "C:/03_Capstone/Data/Downscale/ssp126/downscale_ssp126_060524_lr001_bs128_hs300_dp5_epoch200_analysis.nc"
output_avg_duration_file = "C:/03_Capstone/Data/Downscale/ssp126/downscale_ssp126_060524_lr001_bs128_hs300_dp5_epoch200_duration.nc"


Array1 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
Array2 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
Array3 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
Array4 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
# Array5 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  
# Array6 = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  


# ##########################################
# "running the code"

global_min = float('inf')

for j in range(lon_length): 
    for i in range(lat_length): 
        dr_freq = 0
        grid_min = float('inf')
        tot_amount_days = 0    #ensuring that these are all set new for each grid cell 
        for t in range(all_days): 
            "defining if its a drought event or not"
            spei_input = spei_data.variables[spei_var][t, j, i]
            spei_threshhold = -1     ########## threshhold based on (Zhao et al., 2021) and (Su et al., 2021)
            
            if np.isnan(spei_input): #to not calculate data for cells in which there is no data 
                dr = np.nan
            elif spei_input <= spei_threshhold: 
                dr = 1
            else: 
                dr = 0    
            Array1[t, j, i] = dr

            "Preforming calculations on the data"
            spei_input = spei_data.variables[spei_var][t,j,i]

            "frequency defining the amount of drought events"
            "amount of days, => drought duration => need to change this to the mean"
            "drought intensity => should store the overall worst drought intensity"

            if np.isnan(dr) or np.isnan(spei_input):  # Skip NaN values    #ISSUE 1: ignoring the fields with nan => compiles over the timeperiods 
                # dr_freq = np.nan   
                # grid_min = np.nan
                # tot_amount_days = np.nan
                dr_freq = dr_freq if np.isnan(dr) else 0
                grid_min = grid_min if np.isnan(spei_input) else grid_min
                tot_amount_days = tot_amount_days if np.isnan(dr) else 0

            elif t > 0 and dr == 1 and Array1[t-1, j, i] == 0: 
                dr_freq += 1
                tot_amount_days += 1
            elif t == 0 and dr == 1:  # Handle the first time step
                dr_freq += 1 
                tot_amount_days += 1
            elif dr == 1: 
                tot_amount_days += 1
            else: 
                dr_freq += 0
                tot_amount_days = 0
            
            if spei_input < grid_min: 
                grid_min = spei_input
            
            if spei_input < global_min: 
                global_min = spei_input
            
            
            Array2[t,j,i] = dr_freq
            Array3[t,j,i] = grid_min 
            Array4[t,j,i] = tot_amount_days
    print(f"Longitude: {j}/{lon_length}")

print(f"The most extreme spei value recorded in this time period is: {global_min}")

"To calculate the avg drought duration for each gridcell"

avg_duration = np.zeros((lon_length, lat_length), dtype=np.float32)
flash_drought = np.zeros((lon_length, lat_length), dtype=np.int32)  # Initialize counter

for j in range(lon_length): 
    for i in range(lat_length): 
        durations = []
        current_duration = 0
        for t in range(all_days):
            spei_input = spei_data.variables[spei_var][t, j, i]
            spei_threshhold = -1     ########## threshhold based on (Zhao et al., 2021) and (Su et al., 2021)
            
            if np.isnan(spei_input): #to not calculate data for cells in which there is no data 
                dr = np.nan
            elif spei_input <= spei_threshhold: 
                dr = 1
            else: 
                dr = 0    
            

            if dr == 1:
                current_duration += 1
            elif dr == 0 and current_duration > 0: 
                durations.append(current_duration)
                current_duration = 0
            else: 
                current_duration = 0 
            # print(f"time: {t}, {current_duration}. ")
            # print(f"time: {t}, {durations}. ")
            
        if current_duration >0: #if there is a remaining duration at the end of the loop, we also want to append it 
            durations.append(current_duration)

        flash_drought[j, i] = sum(1 for duration in durations if duration <= 30)
        print(f"lat: {i}, flash drought: {flash_drought[j, i]}")
        if durations:
            avg_duration[j, i] = np.nanmean(durations)
        else:
            avg_duration[j, i] = np.nan    
        print(f"lat: {i}, avg drought duration: {avg_duration[j, i]}")
    print(f"Longitude: {j}/{lon_length}")

print(f"min: {np.nanmin(avg_duration)}")
print(f"max: {np.nanmax(avg_duration)}")

print(f"min: {np.nanmin(flash_drought)}")
print(f"max: {np.nanmax(flash_drought)}")

"Trying to save all the variables in one file"

spei_output_array = spei_data.variables["spei"][:]


"Saving the files " 
with Dataset(output_nc_file, 'w', format='NETCDF4') as ds:
    time = ds.createDimension('time', all_days)
    lon = ds.createDimension('lon', lon_length)  
    lat = ds.createDimension('lat', lat_length)  

    times = ds.createVariable('time', 'f4', ('time',))
    lons = ds.createVariable('lon', 'f4', ('lon',))  
    lats = ds.createVariable('lat', 'f4', ('lat',)) 
    spei = ds.createVariable("spei", 'f4', ('time', 'lon', 'lat'))  
    dr = ds.createVariable("dr", 'f4', ('time', 'lon', 'lat'))  
    dr_freq = ds.createVariable("dr_freq", 'f4', ('time', 'lon', 'lat'))
    grid_min = ds.createVariable("spei_min", 'f4', ('time', 'lon', 'lat'))
    tot_amount_days = ds.createVariable("tot_amount_days", 'f4', ('time', 'lon', 'lat'))

    spei.units = 'Unknown'
    tot_amount_days.units = 'days'

    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    times[:] = np.arange(0, all_days, 1)

    spei[:, :, :] = spei_output_array
    dr[:, :, :] = Array1
    dr_freq[:, :, :] = Array2
    grid_min[:, :, :] = Array3
    tot_amount_days[:, :, :] = Array4

print("The drougth analysis was successfully run and the files are saved!")
print(f"The most extreme spei value recorded in this time period is: {global_min}")

"Saving the avg duration file"
print(f"flash drougth: {flash_drought}")
print(f"avg duration: {avg_duration}")

with Dataset(output_avg_duration_file, 'w', format='NETCDF4') as ds:
    lon = ds.createDimension('lon', lon_length)  
    lat = ds.createDimension('lat', lat_length)  

    lons = ds.createVariable('lon', 'f4', ('lon',))  
    lats = ds.createVariable('lat', 'f4', ('lat',)) 
    avg_dur = ds.createVariable("avg_drought_duration", 'f4', ('lon', 'lat'))  
    flash_dr = ds.createVariable("flash_dr_count", "f4", ('lon', 'lat'))
    avg_dur.units = 'Unknown'
    flash_dr.units = 'Unknown'    
    lons[:] = np.linspace(lon_min, lon_max, lon_length)
    lats[:] = np.linspace(lat_min, lat_max, lat_length)
    avg_dur[:, :] = avg_duration
    flash_dr[:] = flash_drought


print("Average drought duration file saved successfully!")
print(f"The most extreme spei value recorded in this time period is: {global_min}")
