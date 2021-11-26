import time
starttime = time.time()

# importing sys and os
import sys
import os
# from matplotlib.cbook import dedent  

# adding smurfpytest.0 to the system path
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Processing_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Migration_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Stacking_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Plotting_Scripts')
sys.path.insert(0, '/Users/r03sb21/TauP-2.5.0/bin')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Tools')
  
# importing functions
import RFsPerStation
import calculate_pierce_points
import convert_to_depth_obspy
import epicentral_distance_stack
import baz_distance_stack
import depth_stack
import slowness_stack
import depth_slowness_stack
import stack_CCP
import plot_map_pierce_points
import plot_map_stations_pierce_points
import plot_CCP

# Command line help
if len(sys.argv) != 12 or str(sys.argv[1]) == 'help':
    print('\n')
    print('-----------------------------------------------------------------------------------------------------------------------')
    print(sys.argv[0])
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('Description:           Run smurfpy for every filter')
    print('Inputs:                data directory, lonmin, lonmax, latmin, latmax, binsize, smoothing, min_epi, max_epi, dates, datef')
    print('Outputs:               epicentral distance, depth and slowness stacks; piercing point plots for P410s and P660s;')
    print('                       CCP stacks; for filters jgf1,2,3 and tff1,2,3,4,5\n')
    print('Usage:                 export PATH="/Users/r03sb21/TauP-2.5.0/bin:$PATH"')
    print('Usage:                 python3 smurfpy-oneshot-commandlineinput.py MetMalaysia 110 120 0 10 3 True 30 90 2018-01-01 2019-01-01')
    print('Usage:                 cd /Volumes/GoogleDrive/My\ Drive/SMURFPy ')
    print('                       export PATH="/Users/r03sb21/TauP-2.5.0/bin:$PATH"')
    print('                       python3 /Users/r03sb21/Documents/smurfpy/Oneshot_Scripts/2_stacking_and_plotting.py MetMalaysia 110 122 0 12 3 True 30 90 2018-01-01 2019-01-01')
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('\n')
    sys.exit()

# Initial options
Data = str(sys.argv[1])
lonmin = int(sys.argv[2]) 
lonmax = int(sys.argv[3]) 
latmin = int(sys.argv[4]) 
latmax = int(sys.argv[5])
bin_size=int(sys.argv[6])
smoothing=bool(sys.argv[7])
min_epi=int(sys.argv[8]) 
max_epi=int(sys.argv[9])
dates=str(sys.argv[10])
datef=str(sys.argv[11])

# bin_size=5
# smoothing=False
# lonmin, lonmax, latmin, latmax, min_epi, max_epi = -179, 179, -89, 89, 30, 90

#----------------------- Processing SCRIPTS --------------------------

Filters = ['jgf1']#,'jgf1']#'tff4', 'tff5'] #'jgf3', 'jgf2','tff1', 'tff2', 'tff3', 
Models = ['prem']#,'ak135']
Noise = ['Alistair']#,'Sanne', 'Sophia'] 




for Model in Models:
        print('\n'+Model+'\n')

        for filt in Filters:
                print('\n'+filt+'\n') 

                for noisefilter in Noise:

                        # RFsPerStation.rfsperstation(Data, noisefilter, filt)
                        print('RFsPerStation')

                        ### Migration ###
                        # calculate_pierce_points.calculate_pierce_points(Data, noisefilter, Model, '410', 'P410s', filt)
                        print('calculate_pierce_points_410')
                        
                        # calculate_pierce_points.calculate_pierce_points(Data, noisefilter, Model, '660', 'P660s', filt)
                        print('calculate_pierce_points_660')
                         # Description: Calculate converted phase pierce points at discontinuity depths  
                                # Inputs: Depth of piercepoints, Phase, filter band, 1D velocity model  
                                # Outputs: Adds PP for given phase and discont depth to each Pickle file, prints to file PP_'DEPTH'km_'PHASE'_'FILTER'.txt'  
                         # Usage: python3 calculate_pierce_points.py 410 P410s jgf1  

                        # convert_to_depth_obspy.convert_to_depth(Data,noisefilter, Model,filt)
                        print('convert_to_depth')
                         # Description: Convert RF from time to depth using 1D model
                         # Inputs: Filter band, 1D velocity model  
                         # Outputs: Adds dictionary seis[0].conversions['<noisefilterof1Dmodel>'] to each Pickle file  
                         # Usage: python3 convert_to_depth_obspy.py jgf1  

                         ### Stacking ###

                        if epicentral_distance_stack.epicentral_distance_stack(Data, noisefilter, bin_size, smoothing, 410, lonmin, lonmax, latmin, latmax, min_epi, max_epi, filt) == True:
                                print('epicentral_distance_stack')
                                # baz_distance_stack.BAZ_stack(Data, noisefilter, 4*bin_size, smoothing, 410, lonmin, lonmax, latmin, latmax, 0, 360, filt)
                                # Description: Stacks the RFs in bins of back azimuth to show the most prominent features  
                                # Inputs: Data, bin_size, smoothing, depth, lon/lat box, epi_dist_limits, filter band  
                                # Outputs: BAZ stack plot  
                                # Usage: python3 epicentral_distance_stack.py Data 5 410 False -179 179 -89 89 30 90 jgf1  

                                # depth_stack.depth_stack(Data, noisefilter, Model, lonmin, lonmax, latmin, latmax, filt) 
                                print('depth_stack')
                                # # Description: Stacks all the RFs within the bounds for the depth stated producing one trace.  
                                # # Inputs: conversion, lon/lat box, filter band  
                                # # Outputs: Depth stack pickle file and pdf/png  
                                # # Usage: python3 depth_stack.py prem -179 179 -89 89 jgf1  

                                # slowness_stack.slowness_stack(Data, noisefilter, lonmin, lonmax, latmin, latmax, filt)
                                print('slowness_stack')
                                # Description: Plot of slowness against time, using a specfic epicentral reference distance.  
                                # Inputs: lon/lat box, filter band  
                                # Outputs: Slowness stack pickle file and pdf/png  
                                # Usage: python3 slowness_stack.py -179 179 -89 89 jgf1  

                                # num_rfs = slowness_stack.slowness_stack(Data, noisefilter, lonmin, lonmax, latmin, latmax, filt)

                                # depth_slowness_stack.depth_slowness(Data, Model, lonmin, lonmax, latmin, latmax, noisefilter, filt, num_rfs)  
                                # [OPTIONAL] Description: Combines previously calculated depth and slowness stack in one figure.  
                                # (Data,conv,lonmin,lonmax,latmin,latmax,noisefilter,rffilter,num_rfs):
                                # Inputs: Depth and slowness stack pickle files  
                                # Outputs: Combined depth and slowness stack image pdf/png  
                                # Usage: python3 depth_slowness_stack.py prem -179 179 -89 89 jgf1 339  

                                # stack_CCP.stack_CCP(Data, noisefilter, 'CCP_Global', Model, lonmin, lonmax, latmin, latmax, filt, 2.0, True) 
                                # # Description: wrapper for the function contained within common_conversion_point_stack.py  
                                # # Inputs: noisefilter, conversion, lon/lat box, filter band, smoothing factor, newstack  
                                # # Outputs: Common conversion point stack volume (PICKLE)  
                                # # Usage: python3 stack_CCP.py CCP_Global prem -179.0 179.0 -89.0 89.0 jgf1 2.0 True  

                                # ### Plotting ###
                                # plot_map_pierce_points.plot_pierce_points(Data, noisefilter, 410, 'P410s', filt)
                                # plot_map_pierce_points.plot_pierce_points(Data, noisefilter, 660, 'P660s', filt)

                                # plot_map_stations_pierce_points.plot_pierce_points(Data, noisefilter, filt)
                                # # Description: Plots discontinuity depth pierce points  
                                # # Inputs: discontinuity depth, converted phase  
                                # # Outputs: matplotlib plot  
                                # # Usage: python3 plot_map_pierce_points.py 410 P410s jgf1   

                                ccpstyles = ['COV', 'TOPO', 'THICK', 'GETTHICK', 'MOVEOUT', '3DTOPO'] 
                                slices = ['NS', 'EW']
                                latorlon = [118, 6]

                                # for ccpstyle in ccpstyles:
                                #         plot_CCP.plot_CCP(Data, noisefilter, 'CCP_Global',Model, filt, 2.0, 2.0, ccpstyle, 410)
                                #         plot_CCP.plot_CCP(Data, noisefilter, 'CCP_Global',Model, filt, 2.0, 2.0, ccpstyle, 660)
                                
                                plot_CCP.plot_CCP(Data, noisefilter, 'CCP_Global',Model, filt, 2.0, 2.0, '3DMTZ', 410)
                                
                                quit()
                                # for i in range(len(slices)):
                                #         if slices[i] == 'NS':
                                #                 latorlon = [116, 116.5, 117, 119]
                                #         else:
                                #                 latorlon = [6, 4.8]

                                #         for ll in latorlon:
                                #                 plot_CCP.plot_CCP(Data, noisefilter, 'CCP_Global',Model, filt, 2.0, 2.0, slices[i], [ll, 1.5])


                                crosssection = [116, 6.5, 118.75, 4, 1.5, 60] #[116, 8, 120, 3, .75, 60] 

                                # plot_CCP.plot_CCP(Data, noisefilter, 'CCP_Global', Model, filt, 2.0, 2.0, 'XC', crosssection)

                                # Description: Wrapper for the function contained within CCP_plottingroutines.py  
                                # Inputs: noisefilter, conversion, filter band, smoothing factor, mincoverage, plot_type, plot_params (doesn't just have to be depth)
                                # Outputs: Various matplotlib plot windows.  
                                # Usage: python3 plot_CCP.py CCP_Global prem jgf1 2.0 2.0 COV 410  
                                # Usage: python3 plot_CCP.py CCP_Global prem jgf1 2.0 2.0 NS lonorlatseed amp

print('Stacking and plotting for '+str(Filters+Models+Noise)+' took' + str(time.time()-starttime) + 'seconds.')