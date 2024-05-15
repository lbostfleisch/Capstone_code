"""
10.05.24
figure 4B: probability distribution 

steps to consider: 
1) split the dataset up into days 
2) plot the pdf of that year 
3) add the colors at a gradual change 
"""
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Times New Roman'


input_file_ssp126 = "C:/03_Capstone/Data/Future/ssp126/run1_200324/ssp126_spei_2015-2100_obsgevpara.nc"
input_ssp126 = Dataset(input_file_ssp126, 'r')
var = 'spei'
lon = input_ssp126['lon'][:]
lat = input_ssp126['lat'][:]
time = input_ssp126['time'][:]




# 2016 is a leap year 

colors = [((i+0.01) / 86, 0.1, 0) for i in range(86)]  # Ranging from dark red to bright red
custom_red_cmap = LinearSegmentedColormap.from_list('custom_red_r', colors)

color_2015 = 'green'

minvalue = -6
maxvalue = 6

for year in range (2015, 2100+1, 1):
    a = year -2015
    color_index = a
    if a == 0: 
        start_day = 0 
        end_day = 364 

        data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
        data_without_nan = data[~np.isnan(data)]
        mu, sigma = norm.fit(data_without_nan)  # Fit data to a normal distribution
       
        x = np.linspace(np.min(data_without_nan), np.max(data_without_nan), 1000)
        pdf = norm.pdf(x, mu, sigma)
        plt.plot(x, pdf, color=color_2015, lw=10)

    elif ((a + 1)%4) == 0:  #+1 because 2016 is a leap year 
        end_day += 366
        start_day = end_day - 365
        data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
        data_without_nan = data[~np.isnan(data)]
        mu, sigma = norm.fit(data_without_nan)  # Fit data to a normal distribution
     
        x = np.linspace(np.min(data_without_nan), np.max(data_without_nan), 1000)
        pdf = norm.pdf(x, mu, sigma)
        plt.plot(x, pdf, color=custom_red_cmap((year - 2015) / (2100 - 2015)), lw=2, alpha=a/86)
    else: 
        end_day += 365 
        start_day = end_day - 364
        data = input_ssp126.variables[var][start_day:end_day, :, :].flatten()
        data_without_nan = data[~np.isnan(data)]
        mu, sigma = norm.fit(data_without_nan)  # Fit data to a normal distribution
        x = np.linspace(np.min(data_without_nan), np.max(data_without_nan), 1000)
        pdf = norm.pdf(x, mu, sigma)
        plt.plot(x, pdf, color=custom_red_cmap((year - 2015) / (2100 - 2015)), lw=2, alpha=a/86)


plt.xlabel("SPEI Value")
plt.ylabel("Probability Density")
plt.xlim(minvalue, maxvalue)
plt.show()

