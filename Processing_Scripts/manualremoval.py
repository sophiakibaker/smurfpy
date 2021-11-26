#

from matplotlib import lines
from obspy import read
import matplotlib.pyplot as plt
import time
import glob
import numpy as np
from obspy import UTCDateTime
import sys
import os.path

def manualremoval_perstation(Data, noisefilter, Model, Filt):
# Command line help
    # if len(sys.argv) != 2 or str(sys.argv[1]).lower() == 'help':
    #     print('\n')
    #     print('-----------------------------------------------------------------------------------------------------------------------')
    #     print(sys.argv[0])
    #     print('-----------------------------------------------------------------------------------------------------------------------')
    #     print('Description:           [OPTIONAL] Plots V,R,RF as a function of time and epicentral distance.')
    #     print('Inputs:                Data directory (usually ../Data/), horizontal component (usually radial), filter band')
    #     print('Outputs:               On-screen plotting\n')
    #     print('Usage:                 >> python3 8_plot_data_perstation.py filterband')
    #     print('Options [1]:           jgf1, jgf2, jgf3, tff1, tff2, tff3, tff4 or tff5 [str]')
    #     print('-----------------------------------------------------------------------------------------------------------------------')
    #     print('\n')
    #     sys.exit()

    direc = Data+''
    flag = 'SV'
    filt = str(Filt)
    counter = 0
    goodrflist = []
    stadirs = sorted(glob.glob(direc+'/*'))

    for stadir in stadirs:
        print(stadir, Filt, Model)

# ------------------------------------- BAZ --------------------------------------------- #

        valid = True
        while valid:

            print('BACK-AZIMUTH')

            if os.path.getsize(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat'):
                BAZs = input("Input BAZ of RFs to remove:")
                
                sta = stadir.replace(direc+'/','')
                
                if os.path.isfile(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat'):
                    if BAZs == "all":
                        open(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat', "w").close()
                        open(stadir+'/SNR_selected_RFs_'+noisefilter+Filt+'.dat', "w").close()
                        print('.dat files cleared.')
                        valid = False
                    elif BAZs == "none":
                        print('.dat files unedited.')
                        valid = False
                    else:
                        if ' ' in BAZs:
                            BAZs = BAZs.split(' ')
                        elif ', ' in BAZs:
                            BAZs = BAZs.split(', ')
                        elif '.' in BAZs:
                            BAZs = BAZs.split('.')
                        elif '/' in BAZs:
                            BAZs = BAZs.split('/')
                        elif 'm' in BAZs:
                            BAZs = BAZs.split('m')
                        elif ',' in BAZs:
                            BAZs = BAZs.split(',')
                        else:
                            BAZs = [BAZs,BAZs]

                        with open(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat','r') as f:
                            for line in f:
                                for BAZ in BAZs:
                                    if "_"+BAZ+"_" in line:
                                        line.replace(line + '\n', '')
                                        print('RF at '+BAZ+' degrees removed from .dat files.')
                        with open(stadir+'/SNR_selected_RFs_'+noisefilter+Filt+'.dat','r') as f:
                            for line in f:
                                for BAZ in BAZs:
                                    if "_"+BAZ+"_" in line:
                                        line.replace(line + '\n', '')
                                        print('RF at '+BAZ+' degrees removed from SNR .dat files.')
                                        valid = False
                        
                        goagain = input("Remove more? [Y/N]")
                        if goagain =='Y':
                            valid = True
                        elif goagain =='N':
                            valid = False

            else:
                print('No RFs to inspect.')
                valid = False

# ------------------------------------- ED --------------------------------------------- #

        valid = True
        while valid:

            print('EPICENTRAL DISTANCE')

            if os.path.getsize(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat'):
                EDs = input("Input E.D. of RFs to remove:")

                sta = stadir.replace(direc+'/','')
                
                if os.path.isfile(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat'):
                    if EDs == "all":
                        open(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat', "w").close()
                        open(stadir+'/SNR_selected_RFs_'+noisefilter+Filt+'.dat', "w").close()
                        print('.dat files cleared.')
                        valid = False
                    elif EDs == "none":
                        print('.dat files unedited.')
                        valid = False
                    else:   
                        if ' ' in EDs:
                            EDs = EDs.split(' ')
                        elif ', ' in EDs:
                            EDs = EDs.split(', ')
                        elif ',' in EDs:
                            EDs = EDs.split(',')
                        else:
                            EDs = np.array(EDs)

                        print(EDs)
                
                        with open(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat','r') as f:
                            for line in f:
                                for ED in EDs:
                                    if "_"+ED+"_" in line:
                                        line.replace(line + '\n', '')
                                        print('RF at '+ED+' degrees removed from .dat files.')
                        with open(stadir+'/SNR_selected_RFs_'+noisefilter+Filt+'.dat','r') as f:
                            for line in f:
                                for ED in EDs:
                                    if "_"+ED+"_" in line:
                                        line.replace(line + '\n', '')
                                        print('RF at '+ED+' degrees removed from SNR .dat files.')
                                        valid = False

                        goagain = input("Remove more? [Y/N]")
                        if goagain =='Y':
                            valid = True
                        elif goagain =='N':
                            valid = False

            else:
                print('No RFs to inspect.')
                valid = False
