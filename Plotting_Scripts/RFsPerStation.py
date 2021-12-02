import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# loop thru stations
#   for a given station save its name and find length of rf .dat file
# plot lengths

def rfsperstation(Data, noisefilter, filt):
    stations = glob.glob(Data + '/*')
    stalist = []
    rfcount =[]
    noevents =[]

    Results = Data+'_Results'

    for station in stations:
        sta = station.replace(Data+'/','')
        sta = sta.replace('MetMalaysia/','')
        sta = sta.replace('nBOSS/','')
        stalist.append(sta)

    stalist = sorted(stalist)

    for station in stations:
        file = station + '/selected_RFs_'+noisefilter+filt+'.dat'
        
        
        if os.path.isfile(file):
            with open(file, 'r') as fp:
                x = len(fp.readlines())
                events = glob.glob(station+'/*/*.PICKLE')
        else: 
            x = 0
            events = glob.glob(station+'/*/*/*.PICKLE')
        rfcount.append(x)

        noevents.append(len(events))

    ax = plt.gca()

    # ax.figure(figsize=(16,4))
    ax.bar(np.arange(len(stalist))*4,rfcount, tick_label=stalist, color='mediumvioletred',alpha=.4, edgecolor='mediumvioletred', label='RFs used', width=2.5)
    ax.bar(np.arange(len(stalist))*4,noevents, tick_label=stalist, color='coral',alpha=.4, edgecolor='coral', label='Events', width = 2.5)
    # plt.yticks(np.arange(0,121, 10))
    ax.set_ylabel('Frequency')
    ax.set_ylim((0,max(noevents)+20))
    ax.set_xticklabels(labels=stalist, rotation = 90)
    
    plt.tight_layout()

    ax.legend(frameon=False)

    plt.savefig(Results+'/selected_RFs_'+noisefilter+filt+'_per_station.png')
    plt.savefig(Results+'/selected_RFs_'+noisefilter+filt+'_per_station.pdf')