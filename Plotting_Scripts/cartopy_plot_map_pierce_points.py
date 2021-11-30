###########################
# Plot map with piercepoints
############################

#----------------------------------------#
import sys
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
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

    m = plt.axes(projection=ccrs.Mercator())

    m.add_feature(cfeature.COASTLINE)
    m.add_feature(cfeature.LAND, color="lightgrey", alpha=0.5)
    m.add_feature(cfeature.BORDERS, linestyle="--")
    m.add_feature(cfeature.OCEAN, color="skyblue", alpha=0.4)

    gl = m.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlines = False
    gl.ylines = False
    # adjust tick locations to requirements
    gl.xlocator = mticker.FixedLocator([lonmin,(lonmin+lonmax)/2,lonmax])
    gl.ylocator = mticker.FixedLocator([latmin,(latmin+latmax)/2,latmax])

    # plot pierce points
    print(lonpp, latpp)
    x1, y1 = lonpp, latpp
    m.scatter(x1, y1, s=30, marker='o', color='k', alpha=.3, transform=ccrs.PlateCarree())

    plt.title('Pierce points for ' + phase + ' at ' + depth + ' km depth')
    plt.savefig(Results+'/Pierce_points_' + phase + '_' + depth+'_'+noise+filt+'_cartopy.png')
    # plt.savefig('Pierce_points_' + phase + '_' + depth+'.pdf')
    # plt.show()
