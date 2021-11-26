#

from obspy import read
import matplotlib.pyplot as plt
import time
import glob
import numpy as np
from obspy import UTCDateTime
import sys
import os.path

def plot_data_perstation(Data, noisefilter, Model, Filt):
# Command line help
    # if len(sys.argv) != 2 or str(sys.argv[1]).lower() == 'help':
    #     print('\n')
    #     print('-----------------------------------------------------------------------------------------------------------------------')
    #     print(sys.argv[0])
    #     print('-----------------------------------------------------------------------------------------------------------------------')
    #     print('Description:           [OPTIONAL] Plots V,R,RF as a function of time and back azimuth.')
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
    stadirs = glob.glob(direc+'/*')

    for stadir in stadirs:
        print(stadir)
        
        sta = stadir.replace(direc+'/','')
        
        if os.path.isfile(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat'):
            with open(stadir+'/selected_RFs_'+noisefilter+Filt+'.dat','r') as f:
                goodrfs= f.read().replace('\n', '')

            # loop through events
            stalist=glob.glob(stadir+'/*.PICKLE')
            
            print(stalist)

        else:
            stalist=[]

        

        c=0
        # Loop through data
        if(len(stalist)>0):
            plt.figure()
            for i in range(len(stalist)): #range(cat.count()):
                    # print(stalist[i])
                    seis=read(stalist[i],format='PICKLE')
    
                    bazdg=seis[0].stats['baz']
                    if stalist[i] in goodrfs:
                        good=True
                        print('YAY',seis[0].stats['event'].magnitudes[0].mag)
                    else:
                        good=False
                        print('NO',seis[0].stats['event'].magnitudes[0].mag)

                    if good:

                        counter = counter+1

                        tshift=UTCDateTime(seis[0].stats['starttime'])-seis[0].stats['event'].origins[0].time

                        # plt.figure()

                        #Ptime=Ptime
                        plt.subplot(1,3,1)
                        vertical = seis.select(channel='*HZ')[0]
                        vertical.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
                        windowed=vertical[np.where(vertical.times()>seis[0].stats.traveltimes['P']-100) and np.where(vertical.times()<seis[0].stats.traveltimes['P']+100)]
                        norm=np.max(np.abs(windowed))
                        
                        plt.plot(vertical.times()-seis[0].stats.traveltimes['P'], vertical.data/norm+np.round(bazdg),'k')
                        # else:
                        #     plt.plot(vertical.times()-seis[0].stats.traveltimes['P'], vertical.data/norm+np.round(bazdg),'r')   
            
                        #plt.plot(seis[0].stats.traveltimes['P'],np.round(bazdg),'.b')
                        #plt.plot(seis[0].stats.traveltimes['S'],np.round(bazdg),'.g')
                        plt.xlim([-25,150])
                        plt.ylim([30,92])
                        plt.subplot(1,3,2)
                        radial = seis.select(channel='*HR')[0]

                        radial.filter('bandpass', freqmin=0.01,freqmax=.1, corners=2, zerophase=True)
                        windowed=vertical[np.where(radial.times()>seis[0].stats.traveltimes['P']-100) and np.where(radial.times()<seis[0].stats.traveltimes['P']+100)]
                        norm=np.max(np.abs(windowed))

                        plt.plot(radial.times()-seis[0].stats.traveltimes['P'], radial.data/norm+np.round(bazdg),'k')
                        # else:
                        #     plt.plot(radial.times()-seis[0].stats.traveltimes['P'], radial.data/norm+np.round(bazdg),'r')

                        plt.xlim([-25,150])                  
                        plt.plot(seis[0].stats.traveltimes['P'],np.round(bazdg),'.b')
                        plt.plot(seis[0].stats.traveltimes['S'],np.round(bazdg),'.g')
                        plt.ylim([30,92])
                    
                        plt.subplot(1,3,3)
                        RF=getattr(seis[0],filt)['iterativedeconvolution']
                        time=getattr(seis[0],filt)['time']
                        
                        plt.plot(time, RF/np.max(np.abs(RF))+np.round(bazdg),'k')
                        staname=stalist[i].replace('.PICKLE', '')
                        staname=staname.replace('/', '-')

                        # plt.yticks(np.arange(np.min(RF/np.max(np.abs(RF))+np.round(bazdg)),np.max(RF/np.max(np.abs(RF))+np.round(bazdg)), 15))

                        # with open("goodrflist.txt", "w") as text_file:
                        #     text_file.write(stalist[i])
                        #     text_file.write("\n")
                    # plt.savefig(str(noisefilter) + 'RFs/'+str(staname)+'_'+Filt+'_'+Model+".png")
                        # plt.savefig('SanneRFs/'+str(staname)+'_'+Filt+'_'+Model+"_"+str(counter)+".png")
                        # else:
                        #      plt.plot(time, RF/np.max(np.abs(RF))+np.round(bazdg),'r')  
                    else:
                        print('bad rf: '+str(stalist[i])+' '+Filt+' '+Model)
                        
                        # plt.show()
                    # quit()
                    
                            
                    plt.subplot(1,3,1)
                    plt.title('vertical')
                    plt.ylabel('back azimuth')

                    plt.xlabel('time')
                    plt.subplot(1,3,2)
                    plt.title('radial')
                    plt.ylabel('back azimuth')

                    plt.xlabel('time')
                    plt.subplot(1,3,3)
                    plt.title('receiver functions')
                    plt.ylabel('back azimuth')
                  
                    plt.xlabel('time')
                    plt.tight_layout()
                    plt.legend(title=stadir, loc='best', bbox_to_anchor=(0, -0.59, 0.5, 0.5), frameon=False)
                            #plt.xlim([-150,1000])  
                    
                    plt.savefig(str(noisefilter)+'RFs/'+str(filt)+'/'+str(sta)+'_'+Filt+Model+"_BAZ.png")
#                   print(str(noisefilter)+'RFs/'+str(stadir)+'_'+Filt+Model+".png")







