###########################
# Plot map with piercepoints
############################

#----------------------------------------#
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import scipy
import matplotlib.pyplot as plt
import sys
import pandas as pd
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

def plot_pierce_points(Data, noise, filt):
# Initial options
    rffilter = str(filt)  # RF filter
    Results = Data+'_Results'

    depths = [410, 660]
    colours = ['mediumvioletred','coral']
    shapes = ['o','s']
    plt.figure(figsize=(6, 8))

    piercelist410 = [Results+'/PP_410km_P410s_'+noise+rffilter+'.txt']
    piercelist660 = [Results+'/PP_660km_P660s_'+noise+rffilter+'.txt']

    # Read in pierce points
    lonpp410 = []
    latpp410 = []
    lonpp660 = []
    latpp660 = []

    for filename in piercelist410:
        print(filename)
        rd = open(filename, 'r')

        for line in rd.readlines():
            val = line.split()
            lonpp410.append(float(val[2]))
            latpp410.append(float(val[1]))

        rd.close()

    for filename in piercelist660:
        print(filename)
        rd = open(filename, 'r')

        for line in rd.readlines():
            val = line.split()
            lonpp660.append(float(val[2]))
            latpp660.append(float(val[1]))

        rd.close()

        # Set bounds of map based on piercepoints
    
    lonpp = np.concatenate((np.array(lonpp410), np.array(lonpp660)))
    latpp = np.concatenate((np.array(latpp410), np.array(latpp660)))

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
    gl.xlocator = mticker.FixedLocator([110,115,120])
    gl.ylocator = mticker.FixedLocator([0,5,10])

    # plot pierce points
    x410, y410 = lonpp410, latpp410
    m.scatter(x410, y410, s=30, marker=shapes[0], color=colours[0], alpha=.3, label='P410s',transform=ccrs.PlateCarree())
    x660, y660 = lonpp660, latpp660
    m.scatter(x660, y660, s=30, marker=shapes[1], color=colours[1], alpha=.3, label='P660s',transform=ccrs.PlateCarree())


    data = pd.read_csv('/Users/r03sb21/Documents/smurfpy/MY_BB.lonlat', sep=" ")
    data2 = pd.read_csv('/Users/r03sb21/Documents/smurfpy/new_MY_sabah_sta.lonlat', sep=" ")
    lonMY = np.concatenate((np.array(data['lon']), np.array(data2['lon'])))
    latMY = np.concatenate((np.array(data['lat']), np.array(data2['lat'])))

    x2, y2 = lonMY, latMY
    m.scatter(x2, y2, s=30, marker='v', color='black', alpha=.9, label='MetMalaysia',transform=ccrs.PlateCarree())

    plt.legend(frameon=False, loc = 2)

    plt.title('Pierce points for P410s/P660s at 410/660 km depth')
    plt.savefig(Results+'/Pierce_points_and_stations_'+noise+filt+'cartopy.png')
        # plt.savefig('Pierce_points_' + phase + '_' + depth+'.pdf')
    # plt.show()
