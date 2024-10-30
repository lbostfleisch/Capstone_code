"""
File for converting the CMIP5 rotated coordinate system into the LCC Europe EPSG3034 projection 
Date created: 09.10.24
working with the following link: https://gis.stackexchange.com/questions/10808/manually-transforming-rotated-lat-lon-to-regular-lat-lon 
"""
import os
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

file_name = "pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc"
file_path = os.path.join("C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/", file_name)
data = Dataset(file_path, 'r')
var = 'pr'

rlon_file = data.variables['rlon'][:]
rlat_file = data.variables['rlat'][:]
time_file = data.variables['time'][:]
var_file = data.variables[var][:]


"CMIP 5"
lat_min, lat_max = -6.0, 8.0
lon_min, lon_max = -8.0, -1.0
lon_length = 63
lat_length = 128

print(f"rotated lat 0: {rlat_file[0]}")
print(f"rotated lat max: {rlat_file[len(rlat_file)-1]}")
print(f"rotated lon 0: {rlon_file[0]}")
print(f"rotated lon max: {rlon_file[len(rlon_file)-1]}")

lat0 = 198 #rotated pole from https://cordex.org/domains/cordex-region-euro-cordex/
lon0 = 39.25 #rotated pole from https://cordex.org/domains/cordex-region-euro-cordex/
theta = -(90 + lat0) #formula from https://gis.stackexchange.com/questions/10808/manually-transforming-rotated-lat-lon-to-regular-lat-lon 
#added
Nx = 106 #added # Number of columns (longitude direction)
Ny = 103 #added 
# theta = -(90 + lon0)
print(f"rotation around y axis: {theta}")
phi = -lon0 #formula from https://gis.stackexchange.com/questions/10808/manually-transforming-rotated-lat-lon-to-regular-lat-lon 
#added 
# phi = -lat0
print(f"rotation around z axis: {phi}")

"converting to radians (x,y,z)"
theta_rad = np.radians(theta)
phi_rad = np.radians(phi)

def spherical_to_cartesian(rlon, rlat):
    rlon_rad = np.radians(rlon)
    rlat_rad = np.radians(rlat)

    x_r = np.cos(rlon_rad) * np.cos(rlat_rad)
    y_r = np.sin(rlon_rad) * np.cos(rlat_rad)
    z_r = np.sin(rlon_rad)

    return x_r, y_r, z_r

def rotate_coords(x_r, y_r, z_r): 
    x = (np.cos(theta_rad) * np.cos(phi_rad) * x_r +
         np.sin(phi_rad) * y_r +
         np.sin(theta_rad) * np.cos(phi_rad) * z_r)

    y = (-np.cos(theta_rad) * np.sin(phi_rad) * x_r +
         np.cos(phi_rad) * y_r -
         np.sin(theta_rad) * np.sin(phi_rad) * z_r)

    z = (-np.sin(theta_rad) * x_r + np.cos(theta_rad) * z_r)
    
    return x, y, z


def cartesian_to_spherical(x, y, z): 
    lat = np.arcsin(z)
    lon = np.arctan2(y, x)

    lat_deg = np.degrees(lat)
    lon_deg = np.degrees(lon)
    #added
    # if lon_deg < 0:
    #     lon_deg += 360

    return lat_deg, lon_deg


#continue here with the last steps of bringing it all together 
def rotated_to_geographic(rlon, rlat): 
    x_r, y_r, z_r = spherical_to_cartesian(rlon, rlat)

    x, y, z = rotate_coords(x_r, y_r, z_r)

    lat_deg, lon_deg = cartesian_to_spherical(x, y, z)

    return lon_deg, lat_deg

geo_lon = np.empty_like(rlon_file)
geo_lat = np.empty_like(rlat_file) 

print(f"rlon file shape: {rlon_file.shape[0]}")
print(f"rlat file shape: {rlat_file.shape[0]}")
print(rlat_file.shape[0])
print(rlon_file.shape[0])

# for i in range(rlon_file.shape[0]):
#     for j in range(rlat_file.shape[1]):
#         geo_lon[i, j], geo_lat[i, j] = rotated_to_geographic(rlon_file[i, j], rlat_file[i, j], theta_rad, phi_rad)
all_days = 14610
# Array_r = np.zeros((all_days, lon_length, lat_length), dtype=np.float32)  


"actual"
# for i in range(rlon_file.shape[0]):
#     for j in range(rlat_file.shape[0]):
#         for t in range(len(time_file)):
#             geo_lon[i], geo_lat[j] = rotated_to_geographic(rlon_file[i], rlat_file[j])
#             # Array_r[t, j, i] = geo_lon[i], geo_lat[j]
#     print(f"lat: {j}, lon: {i}, time: {t}")

"test without time => apparently can also use this one: why not having to loop over time?"
for i in range(rlon_file.shape[0]):
    for j in range(rlat_file.shape[0]):
        geo_lon[i], geo_lat[j] = rotated_to_geographic(rlon_file[i], rlat_file[j])
        # Array_r[t, j, i] = geo_lon[i], geo_lat[j]
    print(f"lat: {j}, lon: {i}")

# for i in range(Ny):
#     for j in range(Nx):
#         geo_lon[i], geo_lat[j] = rotated_to_geographic(rlon_file[i], rlat_file[j])
#         # print(f"Converted: Rlon={rlon_file[i]}, Rlat={rlat_file[j]} => Geo Lon={geo_lon[i]}, Geo Lat={geo_lat[j]}")


output_nc_file = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/rotated_files/231024_reprojection_pr_original_theta_phi.nc'
new_dataset = Dataset(output_nc_file, 'w', format='NETCDF4')

# Define dimensions (assuming the same dimensions as in the original file)
time_dim = new_dataset.createDimension('time', len(time_file))
lat_dim = new_dataset.createDimension('lat', geo_lat.shape[0])
lon_dim = new_dataset.createDimension('lon', geo_lon.shape[0])

# Create new variables for geographic coordinates
time_var = new_dataset.createVariable('time', np.float64, ('time',))
# lat_var = new_dataset.createVariable('lat', np.float64, ('lat',))
# lon_var = new_dataset.createVariable('lon', np.float64, ('lon',))
# geographic_lon_var = new_dataset.createVariable('lon', 'f4', ('lon', 'lat')) #took this out because it should not include lat 
geographic_lon_var = new_dataset.createVariable('lon', 'f4', ('lon',))  
geographic_lat_var = new_dataset.createVariable('lat', 'f4', ('lat'))
# geographic_lat_var = new_dataset.createVariable('lat', 'f4', ('lon', 'lat'))
# data_var_new = new_dataset.createVariable(var, np.float64, ('time', 'lon', 'lat'))  
data_var_new = new_dataset.createVariable(var, np.float64, ('time', 'lat', 'lon'))  # lon and lat ordered the other way 


# Assign the projected geographic coordinates to the new variables
time_var[:] = time_file
print(geographic_lat_var.shape)
print(geo_lon.shape)

geographic_lon_var[:] = geo_lon
geographic_lat_var[:] = geo_lat
data_var_new[:, :, :] = var_file 

# lons[:] = np.linspace(lon_min, lon_max, lon_length)
# lats[:] = np.linspace(lat_min, lat_max,lat_length)

# new_dataset.close()
print(f"New NetCDF file created: {output_nc_file}")


"""plotting """

# Create a figure
time_step = 0
data_at_time = data[time_step, :, :]  # Slicing the data for the first time step

# Plotting the data (e.g., using contour or pcolormesh)
plt.figure(figsize=(10, 6))
plt.contourf(geographic_lon_var, geographic_lat_var, data_at_time, cmap='viridis')
plt.colorbar(label='Data Value')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
# plt.title(f'Data at Time = {time[time_step]}')

# Show the plot
plt.show()

