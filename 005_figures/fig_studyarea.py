"""
purpose: code to map the study area, specifically the maximum temperature 
author: Luca Boestfleisch 
"""
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl


mpl.rcParams['font.family'] = 'Times New Roman'

input_file = "" #adapt
data = xr.open_dataset(input_file)
variable_name = 'tasmax' #adapt 

num_rows = 1
num_col = 1  # Change to 1
fig, ax = plt.subplots(num_rows, num_col, figsize=(15, 10))
shapefile_path = '' #adapt 
gdf = gpd.read_file(shapefile_path)

variable = data[variable_name]
'adapt the bars below'
minvalues = 30
maxvalues = 40

"plot the shapefile with the borders of brandenburg"
gdf.plot(ax=ax, facecolor='none', edgecolor='black', zorder=1)

variable.plot.imshow(x='lon', y='lat', ax=ax, vmin=minvalues, vmax=maxvalues, cmap="OrRd", zorder=0)

sm = plt.cm.ScalarMappable(cmap="OrRd")
sm.set_array([])
sm.set_clim(vmin=minvalues, vmax=maxvalues)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  
cbar = plt.colorbar(sm, cax=cbar_ax)
cbar.set_label('Maximum Temperature (C) from 1970-2014', fontname='Times New Roman', fontsize=15)

ax.annotate('', xy=(0.95, 0.95), xycoords='axes fraction', xytext=(0.95, 0.85),
                arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2))
ax.text(0.95, 0.95, 'N', transform=ax.transAxes, ha='center', va='center', fontsize=8,)

ax.set_xlabel('Longitude', fontname='Times New Roman')
ax.set_ylabel('Latitude', fontname='Times New Roman')


ax.images[-1].colorbar.remove()

plt.tight_layout()
plt.show()
