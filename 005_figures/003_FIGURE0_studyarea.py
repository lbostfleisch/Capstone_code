"""
figure 1 
study area 
"""
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams['font.family'] = 'Times New Roman'

input_file = "C:/03_Capstone/Data/Python_NetCDF_join/DWD CDC/Tmax_nc/Output/max_tasmax_1970-2014_no0.nc"
data = xr.open_dataset(input_file)
variable_name = 'tasmax'

num_rows = 1
num_col = 1  # Change to 1
fig, ax = plt.subplots(num_rows, num_col, figsize=(15, 10))
shapefile_path = 'C:/03_Capstone/Data/Analysis/shapefile_br/br_shapefile_epsg3034.shp'
gdf = gpd.read_file(shapefile_path)

variable = data[variable_name]
minvalues = 30
maxvalues = 40

# Plot shapefile
gdf.plot(ax=ax, facecolor='none', edgecolor='black', zorder=1)

# Plot NetCDF data
variable.plot.imshow(x='lon', y='lat', ax=ax, vmin=minvalues, vmax=maxvalues, cmap="OrRd", zorder=0)

# Colorbar (created only for the NetCDF plot)
sm = plt.cm.ScalarMappable(cmap="OrRd")
sm.set_array([])
sm.set_clim(vmin=minvalues, vmax=maxvalues)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust position as needed
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('Maximum Temperature (C) from 1970-2014', fontname='Times New Roman', fontsize=15)

ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)

# Axis labels
ax.set_xlabel('Longitude', fontname='Times New Roman')
ax.set_ylabel('Latitude', fontname='Times New Roman')


ax.images[-1].colorbar.remove()

plt.tight_layout()
plt.show()
