'''
Piercepoints_Calc.py
This script computes predicted pierce points for user defined phases based on TauP.
It loops through all the data, checking whether the pierce points have been calculated,
and if not working them out, writing the data to sperate file and the PICKLE file itself.

depth = Depth of piercepoints
phase = Phase
Filt = Filter

eg. Piercepoints_Calc.py 410 P410s jgf1
'''

# Import all the relevant modules
from obspy import read
import os, sys, glob
import subprocess

# # Command line help
# if len(sys.argv) != 4 or str(depth).lower() == 'help':
#     print('\n')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print(sys.argv[0])
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('Description:           Calculate converted phase pierce points at discontinuity depths')
#     print('Inputs:                Depth of piercepoints, Phase, filter band, 1D velocity model')
#     print('Outputs:               Adds PP for given phase and discont depth to each Pickle file, prints to file')
#     print('                       PP_DEPTHkm_PHASE_FILTER.txt\n')
#     print('Usage:                 python3 calculate_pierce_points.py depth phase filter')
#     print('Format [1]:            depth (km) [int]')
#     print('Format [2]:            seismic phase [str]')
#     print('Options [3]:           jgf1, jgf2, jgf3, tff1, tff2, tff3, tff4 or tff5 [str]')
#     print('Recommended:           python3 calculate_pierce_points.py 410 P410s jgf1')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('\n')
#     sys.exit()

def calculate_pierce_points(Data, noise, Model, depth, phase, Filt):

    mod = Model

    # PREM=True
    # ak135=False
    # if PREM:
    #     mod='prem'
    # elif ak135:
    #     mod='ak135'

    directory = Data+"_Results/"

    # Make and open a data file in the Piercepoints directory for this phase
    # and depth ('w' = writable)
    PP = open(directory+'PP_' + str(depth) + 'km_' + str(phase) + '_' + noise + str(Filt) + '.txt', 'w')

    # quit()

    # Loop through stations
    direc = Data
    stadirs = glob.glob(direc + '/*')
    for stadir in stadirs:
        stalist = []
        if os.path.isfile(stadir + '/selected_RFs_'+ noise+str(Filt)+'.dat'):
            with open(stadir + '/selected_RFs_'+ noise+str(Filt)+'.dat') as a:
                starfs = a.read().splitlines()
                for line in starfs:
                    stalist.append(line)

        # Loop through events
        for s in range(len(stalist)):
            seis = read(stalist[s], format='PICKLE')
            print (stalist[s])

            # Note stats of stream
            EVLA = seis[0].stats['evla']
            EVLO = seis[0].stats['evlo']
            EVDP = seis[0].stats['evdp']
            STLA = seis[0].stats['stla']
            STLO = seis[0].stats['stlo']

            # Check if there's a piercepoints dictionary
            if not hasattr(seis[0].stats, 'piercepoints'):

                # Start a piercepoints dictionary
                seis[0].stats.piercepoints = dict()

            # Set up a variable to check whether the process needs to be done
            runthis = False

            # Check if the dictionary has this phase in
            if not str(phase) in seis[0].stats.piercepoints.keys():
                runthis = True

            # Check whether the dictionary with this phase has this depth in
            if str(phase) in seis[0].stats.piercepoints.keys():
                if not str(depth) in seis[0].stats.piercepoints[phase].keys():
                    runthis = True

            # If the file neither has the phase or depth, run the rest of the
            # script
            if runthis:
                print('runthis is True')
                # Call taup_pierce to get piercepoints
                test = [
                    'taup_pierce -mod ' + str(mod) + ' -h ' + str(
                        EVDP) + ' -ph ' + phase + ' -pierce ' + depth + ' -nodiscon -sta ' + str(
                        STLA) + ' ' + str(
                            STLO) + ' -evt ' + str(
                                EVLA) + ' ' + str(
                                    EVLO)]

                # Run test in terminal
                out = subprocess.check_output(
                    test,
                    shell=True,
                    universal_newlines=True)

                # Split the output into lines
                # t[0] is a description
                # t[1] the downwards pierce and t[2] the upwards pierce (if event depth < PP depth)
                # t[1] the upwards pierce (if event depth > PP depth)
                t = out.split('\n')

                # Split the relevant line into strings
                if EVDP <= float(depth):
                    u = t[2].split()
                else:
                    u = t[1].split()

                # For the string U: PP depth = u[1], lat = u[3], lon = u[4]

                # Make a separate dictionary within piercepoints for each phase
                seis[0].stats.piercepoints[phase] = dict()

                # For each phase, create a dictionary for each depth, writing
                # piercepoint depth/lat/lon info
                seis[0].stats.piercepoints[phase][
                    depth] = [u[1], u[3], u[4]]

                # Write pierce point data to original pickle file
                seis.write(stalist[s], format='PICKLE')

                # Add line to opened output file followed by new line
                PP.write(str(float(u[1])) + ' ' + str(float(u[3])) + ' ' + str(float(u[4])) + '\n')

            else:
                PP.write(seis[0].stats.piercepoints[phase][depth][0] + ' ' + \
                seis[0].stats.piercepoints[phase][depth][1] + ' ' + \
                seis[0].stats.piercepoints[phase][depth][2] + '\n')

    # Close the file you are writing to
    PP.close()
    print ('Finished')
