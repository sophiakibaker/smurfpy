###########################
# Plot map with piercepoints
############################

#----------------------------------------#
import sys
import mpl_toolkits
import mpl_toolkits.basemap
from mpl_toolkits.basemap import Basemap
import numpy as np
import scipy
from scipy import interpolate
import matplotlib.pyplot as plt
import subprocess
import glob, sys
#----------------------------------------#

# Command line help
# if len(sys.argv) != 4 or str(sys.argv[1]).lower() == 'help':
#     print('\n')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print(sys.argv[0])
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('Description:           Plots discontinuity depth pierce points')
#     print('Inputs:                discontinuity depth, converted phase, filter band')
#     print('Outputs:               matplotlib plot)\n')
#     print('Usage:                 >> python3 plot_map_pierce_points.py depth phase rffilter')
#     print('Format                 1-3: [str]')
#     print('Recommended:           >> python3 plot_map_pierce_points.py 410 P410s jgf1')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('\n')
#     sys.exit()

def plot_pierce_points(Data, noise, depth, phase, filt):
# Initial options

    Results = Data+'_Results'

    depth = str(depth)   # depth of pierce points to plot
    phase = str(phase)   # phase of pierce points to plot 
    rffilter = str(filt)  # RF filter
    piercelist = [Results+'/PP_'+depth+'km_'+phase+'_'+noise+rffilter+'.txt']

    # Read in pierce points
    lonpp = []
    latpp = []
    print(piercelist)
    for filename in piercelist:
        print(filename)
        rd = open(filename, 'r')

        for line in rd.readlines():
            val = line.split()
            lonpp.append(float(val[2]))
            latpp.append(float(val[1]))

        rd.close()


    plt.figure(figsize=(6, 10))

    # Set bounds of map based on piercepoints
    lonmin = np.min(lonpp) - 2
    lonmax = np.max(lonpp) + 2
    latmin = np.min(latpp) - 2
    latmax = np.max(latpp) + 2

    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # resolution = 'i' means use intermediate resolution coastlines.
    # lon_0, lat_0 are the central longitude and latitude of the projection.
    m = Basemap(
        llcrnrlon=lonmin, llcrnrlat=latmin, urcrnrlon=lonmax, urcrnrlat=latmax,
                resolution='i', projection='merc', lon_0=np.mean((lonmin, lonmax)), lat_0=np.mean((latmin, latmax)))
    m.drawcoastlines()
    m.drawcountries()

    # draw parallels and meridians.
    m.drawparallels(np.arange(-40, 80., 5.), color='gray')
    m.drawmeridians(np.arange(-30., 80., 5.), color='gray')

    # plot pierce points
    print(lonpp, latpp)
    x1, y1 = m(lonpp, latpp)
    m.scatter(x1, y1, s=30, marker='o', color='k', alpha=.3)

    plt.title('Pierce points for ' + phase + ' at ' + depth + ' km depth')
    plt.savefig(Results+'/Pierce_points_' + phase + '_' + depth+'_'+noise+filt+'.png')
    # plt.savefig('Pierce_points_' + phase + '_' + depth+'.pdf')
    # plt.show()
