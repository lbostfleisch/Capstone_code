"""
File for converting the CMIP5 rotated coordinate system into the LCC Europe EPSG3034 projection 
Date created: 09.10.24
working with the following link: https://gis.stackexchange.com/questions/10808/manually-transforming-rotated-lat-lon-to-regular-lat-lon 
"""
import os
from netCDF4 import Dataset
import numpy as np

file_name = "spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc"
file_path = os.path.join("C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output", file_name)
data = Dataset(file_path, 'r')

rlon_file = data.variables['rlon'][:]
rlat_file = data.variables['rlat'][:]
time_file = data.variables['time'][:]
spei_file = data.variables['spei'][:]


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
print(f"rotation around y axis: {theta}")
phi = -lon0 #formula from https://gis.stackexchange.com/questions/10808/manually-transforming-rotated-lat-lon-to-regular-lat-lon 
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

"order of the files is wrong I believe "
# for t in range(len(time_file)):
#     for i in range(rlon_file.shape[0]):
#         for j in range(rlat_file.shape[0]):
#             geo_lon[i], geo_lat[j] = rotated_to_geographic(rlon_file[i], rlat_file[j])
#             # Array_r[t, j, i] = geo_lon[i], geo_lat[j]
#     print(t)


for i in range(rlon_file.shape[0]):
    for j in range(rlat_file.shape[0]):
        for t in range(len(time_file)):
            geo_lon[i], geo_lat[j] = rotated_to_geographic(rlon_file[i], rlat_file[j])
            # Array_r[t, j, i] = geo_lon[i], geo_lat[j]
    print(f"lat: {j}, lon: {i}, time: {t}")


output_nc_file = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/output/reprojected_WGS_spei_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_1966-2005.nc'
new_dataset = Dataset(output_nc_file, 'w', format='NETCDF4')

# Define dimensions (assuming the same dimensions as in the original file)
time_dim = new_dataset.createDimension('time', len(time_file))
lat_dim = new_dataset.createDimension('lat', geo_lat.shape[0])
lon_dim = new_dataset.createDimension('lon', geo_lon.shape[0])
time_dim = new_dataset.createDimension('time', )
# Create new variables for geographic coordinates
time_var = new_dataset.createVariable('time', np.float64, ('time',))
# lat_var = new_dataset.createVariable('lat', np.float64, ('lat',))
# lon_var = new_dataset.createVariable('lon', np.float64, ('lon',))
geographic_lon_var = new_dataset.createVariable('lon', 'f4', ('lon', 'lat'))
geographic_lat_var = new_dataset.createVariable('lat', 'f4', ('lon', 'lat'))
data_var_new = new_dataset.createVariable('spei', np.float64, ('time', 'lon', 'lat'))  # New variable for data


# Assign the projected geographic coordinates to the new variables
time_var[:] = time_file
geographic_lon_var[:] = geo_lon
geographic_lat_var[:] = geo_lat
data_var_new[:, :, :] = spei_file 

new_dataset.close()
print(f"New NetCDF file created: {output_nc_file}")