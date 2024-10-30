"""
Rotated coordinates test 23.10.24
website: https://stackoverflow.com/questions/61795766/how-to-manually-reproject-from-a-specific-projection-to-lat-lon 
Variable: lat_vertices, Dimensions: ('rlat', 'rlon', 'vertices'), Shape: (412, 424, 4)
Variable: lon_vertices, Dimensions: ('rlat', 'rlon', 'vertices'), Shape: (412, 424, 4)

"""
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
import xesmf as xe

# Step 1: Define the rotated pole and create the projection
rot_pole_lon = 198.0
rot_pole_lat = 39.25
rotated_pole_proj = ccrs.RotatedPole(pole_longitude=rot_pole_lon, pole_latitude=rot_pole_lat)

# Define the WGS84 projection (PlateCarree is essentially WGS84)
wgs84_proj = ccrs.PlateCarree()

# Step 2: Define the grid in rotated coordinates
Nx, Ny = 106, 103  # Grid size
TLC_lon, TLC_lat = 331.79, 21.67  # Top-left corner in rotated coordinates

# Create arrays for rotated lon/lat
rot_lon_grid = np.linspace(TLC_lon, TLC_lon + Nx - 1, Nx)  # Adjust this to match grid resolution
rot_lat_grid = np.linspace(TLC_lat, TLC_lat - Ny + 1, Ny)  # Adjust accordingly for your grid resolution

# Create a 2D meshgrid of rotated coordinates
rot_lon_mesh, rot_lat_mesh = np.meshgrid(rot_lon_grid, rot_lat_grid)

# Step 3: Convert rotated coordinates to WGS84 (standard lat/lon)
lon_wgs84, lat_wgs84 = rotated_pole_proj.transform_points(wgs84_proj, rot_lon_mesh, rot_lat_mesh)[..., :2].T

# Plot to check the grid in WGS84 coordinates
plt.figure(figsize=(10, 6))
plt.scatter(lon_wgs84, lat_wgs84, s=1, color='blue')
plt.title("Transformed Rotated Grid into WGS84")
plt.xlabel('Longitude (WGS84)')
plt.ylabel('Latitude (WGS84)')
plt.show()


### second part 

# Step 4: Define a regular WGS84 grid (for Europe)
# Define the latitude and longitude bounds for Europe in WGS84
target_lon = np.linspace(-10, 30, 150)  # Longitude bounds for Europe (example)
target_lat = np.linspace(35, 70, 150)   # Latitude bounds for Europe (example)

# Create a meshgrid of the target WGS84 grid
target_lon_mesh, target_lat_mesh = np.meshgrid(target_lon, target_lat)

# Assuming you have data in the original rotated grid (e.g., temperature, precipitation, etc.)
file_path = 'C:/03_Capstone/a_publishing/data/CMIP5_EUR-11_ICHEC-EC-EARTH_CLMcom-CCLM4-8-17/r12i1p1_v1/pr/original_files/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19660101-19701231.nc'  # Replace with your actual file path
ds = xr.open_dataset(file_path)

# Replace 'your_variable_name' with the actual variable name
data = ds['pr']  # Replace 'var' with the actual variable name from the dataset

# Step 5: Use xESMF to regrid the data from the rotated grid to the regular WGS84 grid
# Create an xESMF regridder object
ds_out = xr.Dataset({'lon': (['lon'], target_lon), 'lat': (['lat'], target_lat)})
regridder = xe.Regridder(ds, ds_out, 'bilinear')

# Perform the regridding
regridded_data = regridder(data)

# Step 6: Plot the regridded data
plt.figure(figsize=(10, 6))
plt.contourf(target_lon_mesh, target_lat_mesh, regridded_data, cmap='viridis')
plt.colorbar(label='Data Value')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Regridded Data in WGS84 (European Extent)')
plt.show()
