import time
starttime = time.time()

# importing sys
import sys
# from matplotlib.cbook import dedent  

# adding smurfpytest.0 to the system path
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Processing_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Migration_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Stacking_Scripts')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Plotting_Scripts')
sys.path.insert(0, '/Users/r03sb21/TauP-2.5.0/bin')
sys.path.insert(0, '/Users/r03sb21/Documents/smurfpy/Tools')
  
# importing functions
import download_data_per_station
import cut_out_raw_data
import rotate_data_NE_RT
import add_travel_times
import plot_events_epicentral_distance
# import plot_data_preRF_perstation
import compute_receiver_functions
import auto_select_receiver_functions
import plot_data_selection
import plot_data_perstation
import plot_data_perstation_baz
import RFsPerStation
import manualremoval

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
    print('Usage:                 cd /Volumes/GoogleDrive/My\ Drive/SMURFPy')
    print('                       python3 /Users/r03sb21/Documents/smurfpy/Oneshot_Scripts/1_receiver_function_generation.py MetMalaysia 110 122 0 12 /Users/r03sb21/Documents/smurfpy/MetMalaysiaRaw /Users/r03sb21/Documents/smurfpy/MY_sabah.turfpy 30 90 2018-01-01 2019-01-01')
    print('-----------------------------------------------------------------------------------------------------------------------')
    print('\n')
    sys.exit()

# Initial options
Data = str(sys.argv[1])
lonmin = int(sys.argv[2]) 
lonmax = int(sys.argv[3]) 
latmin = int(sys.argv[4]) 
latmax = int(sys.argv[5])
path2archive=str(sys.argv[6])
input_file=str(sys.argv[7])
min_epi=int(sys.argv[8]) 
max_epi=int(sys.argv[9])
dates=str(sys.argv[10])
datef=str(sys.argv[11])

#----------------------- Processing SCRIPTS --------------------------

Filters = ['jgf1']#['tff4']#,'jgf1']#'tff4', 'tff5'] #'jgf3', 'jgf2','tff1', 'tff2', 'tff3', 
Models = ['prem']#,'ak135']
Noise = ['Alistair']#,'Sanne','Sophia']


### Processing ###
# download_data_per_station.download_data(Data, dates, datef, lonmin, lonmax, latmin, latmax)
# # Description: select and download appropriate events and stations based on user inputs  
# # Inputs: search area lat/lon, start and end times (in function), epicentral dist of ev/station, event magnitude range, trace length, data filter band, station networks to search, dataclient  
# # Outputs: python stream objects in PICKLE format with a dictionary of header info for each event. Saves to ../Data/NT.STA/Originals/  
# # Usage: >> python3 1_download_data_per_station.py  

# cut_out_raw_data.Get_archive_data(path2archive, input_file, Data, 1, 100)
print('cut_out_raw_data')
# Description: DATA DOWNLOAD FOR RF ANALYSIS from turfpy
# # This script selects appropriate events and extracts times from archive of continuous data set up in SDS format
# # Event catalogue is downloaded from the IRIS server
# # Inputs: - path2archive = path to raw data directory
# #         - ut_file = txt file listing stations in format:
# #                                                         net|sta|lat|lon|el|loc|start_date|end_date
# #                                                         KO|SILT|41.153|29.643|100.0|Sile-ISTANBUL|2007-08-01T00:00:00|2015-01-01T00:00:00Z
# # Outputs: - python stream objects in PICKLE format with a dictionary of header info for each event

# rotate_data_NE_RT.rotate_data_NE_RT(Data)
print('rotate_data_NE_RT')	  	
# # # Description: Preprocessing for RF calculation: merges truncations, trims, donsamples, rotates components Z-R-T, renoisefilters based on BAZ and EPI-DIST.  
# # # Inputs: Data directory (usually ../Data/)  
# # # Outputs: python stream objects in PICKLE format with a dictionary of header info for each event in a new folder leaving a copy of the unprocessed original data for future use  
# # # Usage: >> python3 2_rotate_data_NE_RT.py  

# plot_events_epicentral_distance.plot_quakes(Data)
# print('plot_events_epicentral_distance')

for Model in Models:

        print('\n'+Model+'\n')

        # add_travel_times.add_travel_times(Data, Model, ['P', 'S', 'P660s', 'P410s'])
        print('add_travel_times')
        # Description: compute predicted travel-times for user defined phases based on TauP, predicted times are added to waveform header information (python dictionary)  
        # Inputs: Data directory (usually ../Data/), 1D velocity model, phases to compute TTs for  
        # Outputs: Overwrites files from above with new dictionary (seis[0].stats.traveltimes)  
        # Usage: >> python3 3_add_travel_times.py P S P660s P410s

        # plot_data_preRF_perstation.plot_data_preRF_perstation(Data)   
        # print('plot_data_preRF') 
        # # Description: [OPTIONAL] plot Z-R-T seismogram components with predicted arrival times after initial processing, before RF creation  
        # # Inputs: Data directory (usually ../Data/), station directory  
        # # Outputs: On-screen plotting  
        # # Usage: >> python3 4_plot_data_preRF_perstation.py  


        for filt in Filters:

                print('\n'+filt+'\n')

                # compute_receiver_functions.compute_R_F(Data, filt) 
                print('compute_R_F')
                # # # Description:  
                # # # Inputs: Data directory (usually ../Data/), horizontal component (usually radial), filter band, decon algorithm (usually iterative decon - default)  
                # # # Outputs: Adds computed RF to pre-existing PICKLE waveform file  
                # # # Usage: >> python3 5_compute_receiver_functions.py jgf1      

                for noisefilter in Noise:
                        # auto_select_receiver_functions.auto_select_RF(Data, noisefilter, filt)  
                        print('auto_select_R_F '+ noisefilter)
                        
                        
                # # # # Description: Removes low quality ones based on set criteria:   
                # #         # 1. Minimum percentage of radial compoment to be fit (after reconvolving the RF with the vertical component (fitmin)  
                # #         # 2. Peak amplitude max threshold before main P-wave arrival (noisebefore)  
                # #         # 3. Peak amplitude max threshold after main P-wave arrival (noiseafter)  
                # #         # 4. Peak amplitude min threshold after main P-wave arrival (minamp)  
                # # # Inputs: Data directory (usually ../Data/), horizontal component (usually radial), filter band, SNR calculation type, fitmin, noisebefore, noiseafter, minamp  
                # # # Outputs: Two ".dat" files specific to the chosen filter band recording the good RF files and the good RF file SNR ratios (V & R components)  
                # # # Usage: >> python3 6_auto_select_receiver_functions.py jgf1  

                        # plot_data_selection.plot_data_selection(Data, noisefilter, filt)
                        # print('plot_data_selection')
                # #         # # # Description: [OPTIONAL] Plots the perstation distribution of "Acceptable - Green" and "Removed - red" events as a funciton of EQ magnitude and epicentral   distance.  
                # #         # # # Inputs: Data directory (usually ../Data/)  
                # #         # # # Outputs: On-screen plotting  
                # #         # # # Usage: >> python3 7_plot_data_selection.py jgf1  

                # #         # quit() 

                        # plot_data_perstation.plot_data_perstation(Data, noisefilter, Model, filt)
                        print('plot_data_perstation')
                        # plot_data_perstation_baz.plot_data_perstation(Data, noisefilter, Model, filt)
                        print('plot_data_perstation_baz')
                        
                #         # # # Description: [OPTIONAL] Plots V,R,RF as a function of time and epicentral distance.  
                #         # # # Inputs: Data directory (usually ../Data/), horizontal component (usually radial), filter band  
                #         # # # Outputs: On-screen plotting  
                #         # # # Usage: python3 8_plot_data_perstation.py jgf1  

                        print("Ready for manual QC.")

                        manualremoval.manualremoval_perstation(Data, noisefilter, Model, filt)
                        print('manualremoval_perstation')

print('RF generation and selection for '+str(Filters+Models+Noise)+' took' + str(time.time()-starttime) + 'seconds.')
                    