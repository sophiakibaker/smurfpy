# DATA DOWNLOAD FOR RF ANALYSIS#################
# This script selects appropriate events and extracts times from archive of continuous data set up in SDS format
# Event catalogue is downloaded from the IRIS server
#requires input file of the format:
#net|sta|lat|lon|el|loc|start_date|end_date
#KO|SILT|41.153|29.643|100.0|Sile-ISTANBUL|2007-08-01T00:00:00|2015-01-01T00:00:00Z
# Inputs: -input file
#         -location of Data Archive
#         -start and end lines of input file
#         -epicentral dist of ev/station
#         -event magnitude range
#         -trace lenth
#         -data filter band

#will track cut events even if they are later removed from the "Originals folder"
#so you can run again if your archive is updated and it will only cut out new data

# Outputs: -python stream objects in PICKLE format with a dictionary of
# header info for each event

# NOTE: Recommended to run in yearly blocks max 3 in parrallel, otherwise
# the event catalogs get so big that the connection with IRIS times out.
# Also note that it is important to check IRIS stations and pick out
# relevant networks otherwise programs wastes a lot of time look in single
# compinent or infra sound only networks. Makes folder 'Data' one level up from 
# current working directory program will be run in - the structure will be
# used in all foloowing scripts


# Usage is: python download_data_per_station.py
# Or usage is: python download_data_per_station.py '2015-01-01' '2016-01-01', when sys.argv is used to pass start and end time as command line arguments
#


import obspy
from obspy.clients.fdsn import Client as IRISClient
from obspy import UTCDateTime
from obspy import read_inventory, Trace
#import matplotlib.pyplot as plt
import os.path
import time
import obspy.geodetics.base
import numpy as np
import obspy.geodetics
import sys
import dateutil.parser
import glob
import pickle 
import fnmatch

def Get_archive_data(path2archive, input_file, output_directory, start_line,end_line):
    #input_file='/Users/jjenkins/WORK/RF/RF_SCRIPTS/STATION_list.txt'
    #start_line=1
    #end_line=1

    mapdatafile = []
    
    #build list of stations to cut from input file
    inventory={}
    text_file = open(input_file, "r")
    lines = text_file.readlines()
    i=0
    for line in lines:
        i=i+1
        if (i >= start_line) and (i <= end_line):
            #print(line.split('|'))
            nw=line.split('|')[0]
            sta=line.split('|')[1]
            la=line.split('|')[2]
            lo=line.split('|')[3]
            el=line.split('|')[4]
            beg=line.split('|')[6]
            end=line.split('|')[7]
            try:
                inventory[nw][sta]= {'start_date': beg, 'end_date': end, 'latitude': float(la), 'longitude':float(lo), 'elev':float(el)}
            except:      
                inventory[nw]={}
                inventory[nw][sta]= {'start_date': beg, 'end_date': end, 'latitude': float(la), 'longitude':float(lo), 'elev':float(el)}
        
    
    # load IRIS client
    irisclient = IRISClient("IRIS")

    # #Where to extract data from
    # path2archive='/Users/r03sb21/Documents/smurfpy/MetMalaysia'

    # event parameters
    radmin = 30  # Minimum radius for teleseismic earthquakes
    radmax = 90  # Maximum radius (further distances interact with the core-mantle boundary
    minmag = 5.5  # Minumum magnitude of quake
    maxmag = 8.0  # Maximum magnitude of quake
    lengthoftrace = 30. * 60.  # 30 min

    # define a filter band to prevent amplifying noise during the deconvolution
    # not being used, as responses are not being removed
    fl1 = 0.005
    fl2 = 0.01
    fl3 = 2.
    fl4 = 20.


    count = 0
    stacount = 0   
    for nw in inventory:
        for sta in inventory[nw]:
            stacount=stacount+1
            starttime=inventory[nw][sta]['start_date']
            endtime=inventory[nw][sta]['end_date']
        
            name = nw + '.' + sta
            print(sta)

            # Make directories for data
            direc = output_directory + '/' + name
            if not os.path.exists(direc):
                os.makedirs(direc)
            direc = direc + '/Originals'
            if not os.path.exists(direc):
                os.makedirs(direc)
                    

            
            # Find events
            print(sta, nw)
            mintime = inventory[nw][sta]['start_date']
            if mintime < starttime:
                mintime = starttime
            maxtime = inventory[nw][sta]['end_date']
            if maxtime > endtime:
                maxtime = endtime
            print (mintime, maxtime)    
            # Find all suitable events
            cat = irisclient.get_events(
                latitude=inventory[nw][sta]['latitude'],
                longitude=inventory[nw][sta]['longitude'],
                minradius=radmin,
                maxradius=radmax,
                starttime=mintime,
                endtime=maxtime,
                minmagnitude=minmag)
            print(len(cat))

            
            #check what files have already been downloaded
            data_file=direc+'/downloaded_data.pkl'
            if (os.path.isfile(data_file)):
                with open(data_file,'rb') as rfp:
                    data_list = pickle.load(rfp)
            else:
                data_list=[]
                

            
            for ev in cat:
                evtime = ev.origins[0].time
                evmag = ev.magnitudes[0].mag

                #check that you haven't already got this file
                if len(data_list)>0:
                    pattern = str(str(ev.origins[0].time)[:-7]) + '*.PICKLE'
                    matching = fnmatch.filter(data_list, pattern)
                    print(matching)
                
                    if len(matching)>0:
                        print ('You have already downloaded this file')
                        continue

                        
                # find file in ARCHIVE
                dt=dateutil.parser.parse(str(evtime))
                tt = dt.timetuple()
                julday='{:03d}'.format(tt.tm_yday)
                year='{:04d}'.format(dt.year)
                
                
                #find file and cut out
                files2grab=glob.glob(path2archive+'/'+year+'/'+nw+'/'+sta+'/*/'+nw+'.'+sta+'.*'+year+'.'+julday)
                if len(files2grab) ==0:
                    print('no data coverage for event ',evtime)
                    continue
                if len(files2grab) <3:
                    print('missing components ',evtime)
                    continue
                seis=obspy.Stream()
                try:
                    for comp in files2grab:
                        print(comp)
                        st_cur=obspy.read(comp)
                        st_cur.merge(method=0, fill_value='interpolate')
                        seis.append(st_cur[0])
                    
                    seis.trim(evtime, evtime +lengthoftrace) 
                except:
                    print('error occurred for evtime')
                    continue

                if len(seis) > 1:
                    evtlatitude = ev.origins[0]['latitude']
                    evtlongitude = ev.origins[0]['longitude']
                    try:
                        evtdepth = ev.origins[0]['depth'] / 1.e3  # convert to km from m
                    except:
                        print('failed to get true depth')
                        evtdepth = 30.  # This is a bit of a hack, might need better solution

                    # compute distances azimuth and backazimuth
                    distm, az, baz = obspy.geodetics.base.gps2dist_azimuth(
                        evtlatitude, evtlongitude, inventory[nw][sta]['latitude'], inventory[nw][sta]['longitude'])
                    distdg = distm / (6371.e3 * np.pi / 180.)

                    # remove station instrument response. + Output seismograms
                    # in displacement and filter with corner frequences fl2,
                    # fl3
                    #try:
                    #    seis.remove_response(
                    #        output='DISP', pre_filt=[fl1, fl2, fl3, fl4])
                    #except:
                    #    print('failed to remove response')


                    # Put in various event and station characteristics into the
                    # 'stats'-dictionairy
                    seis[0].stats['evla'] = evtlatitude
                    seis[0].stats['evlo'] = evtlongitude
                    seis[0].stats['evdp'] = evtdepth
                    seis[0].stats['stla'] = inventory[nw][sta]['latitude']
                    seis[0].stats['stlo'] = inventory[nw][sta]['longitude']
                    seis[0].stats['dist'] = distdg
                    seis[0].stats['az'] = az
                    seis[0].stats['baz'] = baz
                    seis[0].stats['station'] = sta
                    seis[0].stats['network'] = nw
                    seis[0].stats['event'] = ev
                    seis[0].stats['stel'] = el
                    seis[0].stats['mag'] = evmag

                    #get orientation
                    t = UTCDateTime(evtime) 
                    for cha in range(len(seis)):
                        # location = seis[cha].stats['location']
                        # channel = seis[cha].stats['channel']
                        identifiers = glob.glob(nw+'.'+sta+'.*'+year+'.'+julday)             #MY.KKM..BHN.D.2018.241         
                        for identifier in identifiers:    
                            print(identifier)
                            orientation = read_inventory().get_orientation(str(identifier), t)
                            print(orientation)

                            seis[cha].stats['orientation'] = orientation['azimuth']
                            seis[cha].stats['dip'] = orientation['dip']
                            # Add the station elevation to the vertical component
                            if cha == 0:
                                inv = inventory.select(network=str(nw), station=str(sta))
                                stel=inv.get_coordinates(identifier,t)['elevation']/1000 # stel in kilometers, positive is upward topography.
                                seis[cha].stats['stel'] = stel

                    # Write out to file
                    filename = direc + '/' + \
                        str(seis[0].stats.starttime) + '.PICKLE'
                    print('writing to ', filename)
                    count = count + 1
                    print(count)
                    seis.write(filename, format='PICKLE')

                    mapdatafile.append([seis[0].stats['evlo'], seis[0].stats['evla'], seis[0].stats['evdp'], seis[0].stats['mag']])

        data_file=direc+'/downloaded_data.pkl'
        if (os.path.isfile(data_file)):
            print('appending to pre-exisiting datafile')
            with open(data_file,'rb') as rfp:
                data = list(pickle.load(rfp) )
                data.extend(os.listdir(direc))
                new_datalist=set(data)                
            with open(data_file,'wb') as wfp:
                pickle.dump(new_datalist, wfp)
                
        else:
            print('creating new data file')
            with open(data_file,'wb') as wfp:
                pickle.dump(os.listdir(direc), wfp)


    np.savetxt("/Users/r03sb21/Documents/smurfpy/mapdatafile_"+data+".txt", mapdatafile)
    print(str(count),'Seismograms found for ',str(stacount), ' stations')
    

# Get_archive_data('/Users/r03sb21/Documents/smurfpy/MetMalaysia/MY_sabah.turfpy',2,24)
#     #input_file='/Users/jjenkins/WORK/RF/RF_SCRIPTS/STATION_list.txt'
#     #start_line=1
#     #end_line=16

