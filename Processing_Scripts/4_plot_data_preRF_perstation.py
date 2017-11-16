#####RAW SEISMOGRAM PLOTTING SCRIPT FOR RF ANALYSIS#################

# This script plots ZRT seismogram components with predicted arrival times after initial processing and before RF creation 

##################################################################

import obspy
from obspy import read
from obspy.core import Stream
from obspy.core import trace
import matplotlib.pyplot as plt
import os.path
import time
import glob
import shutil
import numpy as np
from obspy import UTCDateTime
import subprocess
from obspy.taup.taup import getTravelTimes
from obspy.taup import TauPyModel

direc = 'DataRF'


stadirs = glob.glob(direc+'/*')


for stadir in stadirs:


    # loop through events
    stalist=glob.glob(stadir+'/*.PICKLE')

    c=0
    # Loop through data
    if(len(stalist)>0):
        for i in range(len(stalist)): #range(cat.count()):

                seis=read(stalist[i],format='PICKLE')

                #extract epi dist of event/station from header info
                distdg=seis[0].stats['dist']

                #----------------PLOT VERTICAL--------------------------------
                #1 of 3 subplots (grid 1 row 3 columns)
                plt.subplot(1,3,1)
                vertical = seis.select(channel='BHZ')[0] #extract V from stream
                vertical.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
                
                plt.plot(vertical.times(), vertical.data/np.max(vertical.data)+np.round(distdg),'k')#plot normalised data as black line

                #Plot predicted travel times as coloured points (add more phases as wanted)
                plt.plot(seis[0].stats.traveltimes['P'],np.round(distdg),'.b')
                plt.plot(seis[0].stats.traveltimes['S'],np.round(distdg),'.g')
               
                #lable plot
                plt.title('Vertial')   
                plt.ylabel('Epi dist (degrees)') 
                plt.xlabel('Time from Origin (sec)') 


                #----------------PLOT RADIAL--------------------------------
                #2 of 3 subplots
                plt.subplot(1,3,2)
                radial = seis.select(channel='BHR')[0]

                radial.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
 
                plt.plot(radial.times(), radial.data/np.max(radial.data)+np.round(distdg),'k')

                      
                plt.plot(seis[0].stats.traveltimes['P'],np.round(distdg),'.b')
                plt.plot(seis[0].stats.traveltimes['P410s'],np.round(distdg),'.b')
                plt.plot(seis[0].stats.traveltimes['P660s'],np.round(distdg),'.b')
                plt.plot(seis[0].stats.traveltimes['S'],np.round(distdg),'.g')
                
                plt.title('Radial')    
                plt.xlabel('Time from Origin (sec)') 

                #----------------PLOT TRANSVERSE--------------------------------
                #3 of 3 subplots                
                plt.subplot(1,3,3)
                transverse = seis.select(channel='BHT')[0]
                transverse.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
  
                plt.plot(transverse.times(), transverse.data/np.max(transverse.data)+np.round(distdg),'k')  
                plt.plot(seis[0].stats.traveltimes['P'],np.round(distdg),'.b')
                plt.plot(seis[0].stats.traveltimes['S'],np.round(distdg),'.g') 
                plt.title('Transverse') 
                plt.xlabel('Time from Origin (sec)')     
      
        plt.show()






