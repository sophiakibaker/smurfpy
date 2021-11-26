# common conversion point stacking

# Uses routines from common_converion_point_stack.
# Needs a directory 'CCP_Volumes'

#----------------------------------------------------#
import common_conversion_point_stack as CCP_stack
import glob
import os
import time
import sys
from obspy import read

#----------------------------------------------------#

# Command line help
# if len(sys.argv) != 10 or str(sys.argv[1]).lower() == 'help':
#     print('\n')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print(sys.argv[0])
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('Description:           Wrapper for the function contained within common_conversion_point_stack.py')
#     print('Inputs:                depth conversion, lon/lat box, filter band')
#     print('Outputs:               Common conversion point stack volume (PICKLE)\n')
#     print('Usage:                 >> python3 stack_CCP.py conversion lonmin lonmax latmin latmax rffilter newstack')
#     print('Format                 1,2: [str], 3-6: [float], 7: [str], 8: [float], 9: [bool]')
#     print('Recommended:           >> python3 stack_CCP.py CCP_Global prem -179.0 179.0 -89.0 89.0 jgf1 2.0 True')
#     print('-----------------------------------------------------------------------------------------------------------------------')
#     print('\n')
#     sys.exit()

def stack_CCP(Data, noisefilter, name, conv, lonmin, lonmax, latmin, latmax, rffilter, factor, newstack):
    # Initial options
    name = str(name)
    conversion = str(conv) # conversion use
    lonmin = float(lonmin) 
    lonmax = float(lonmax) 
    latmin = float(latmin) 
    latmax = float(latmax)
    rffilter=str(rffilter)  # RF filter used
    factor = float(factor)  # e.g. 2.0 to double the fresnel zone width
    newstack = bool(str(newstack)) #Starting a new stack (True) or adding data to an old one (False)
    Results = Data+'_Results'

    depmin=60.
    depmax=1300.
    lonrez=(lonmax-lonmin)*2.+1. # every 0.5 degrees
    latrez=(latmax-latmin)*2.+1. # every 0.5 degrees
    deprez=(depmax-depmin)/2. # every 2 km

    script_start = time.time()
    # Make sure a CCP_volumes directory is present
    dirout=Results+'/CCP_volumes/'
    if not os.path.exists(dirout):
        os.makedirs(dirout)

    ## Intialize stack or load latest stack
    CCP= CCP_stack.ccp_volume()#

    if newstack:
        CCP.start_empty_volume(name= name, noisefilter=noisefilter, filter=rffilter, conversion=conversion, factor=factor, lonmin = lonmin, lonmax= lonmax, lonrez=int(lonrez), latmin=latmin, latmax=latmax, latrez=int(latrez),depmin=depmin, depmax=depmax, deprez=int(deprez))
    else:
        CCP.load_latest(name= name,filter=rffilter, conversion=conversion, factor=factor)


    ## Data to add (currently looping through all RFs in station directories, this could be adapted
    stations=glob.glob(Data+ '/*')

    for sta in stations:
        rflist=[]
        if os.path.exists(sta + '/selected_RFs_'+ noisefilter +str(rffilter)+'.dat'):
            station_file = open(sta + '/selected_RFs_'+ noisefilter+str(rffilter)+'.dat','r')
            file_list=station_file.read().strip().split()
            for file in file_list:
                seis=read(file, format='PICKLE')
                if hasattr(seis[0],rffilter):
                    rflist.append(file)
            CCP.addlist(noisefilter,rflist,name=name,filter=rffilter, conversion=conversion, factor=factor)

            print('Finished adding RFs... now cleaning...')
            line=open(Results+'/CCP_volumes/'+name+'_'+ noisefilter +rffilter+'_'+conversion+'_'+str(factor)+'/filenames.dat','r').readlines()
            if len(line)>1:
                rm_file=line[-2].split()[1]
                try:
                    print('deleting '+str(rm_file)+'...')
                    os.remove(rm_file)
                except:
                    print('Failed to delete '+str(rm_file))


    print('CCP stacking for '+str(name)+'_'+ noisefilter +str(rffilter)+'_'+str(conversion)+'_'+str(factor)+' is COMPLETE!!!')
    print('It took', time.time()-script_start, 'seconds.')
