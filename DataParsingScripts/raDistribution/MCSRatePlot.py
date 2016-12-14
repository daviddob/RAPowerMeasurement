import json
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import re
from sys import platform as _platform

####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    RA_MCS_FILE = '/media/PowerMeasurementStudy/Results/ra_mcs.json'
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_DIR = 'F:\CSE630\Results'
    RA_MCS_FILE = 'F:\CSE630\Results\/ra_mcs_ds_variable.json'
    SLASH_SEPARATOR = "\/"
####################################################################################################################

raFrequencyFile = open(RA_MCS_FILE)
raFrequencyStr = raFrequencyFile.read()
raFrequencyDict = json.loads(raFrequencyStr)
colors = ['#FF0000','#800000','#FFFF00','#008000','#00FFFF','#0000FF','#000080','#800080']
def label(ax, rects, list):
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width()/2., 1.02*height,'%s' % list[i],ha='center', va='bottom')

for bandwidth in raFrequencyDict:
    print bandwidth
    for location in raFrequencyDict[bandwidth]:
        print location
        i=0
        plt.figure(figsize=(10,6))
        for sourceRate in raFrequencyDict[bandwidth][location]:
            print sourceRate
            mcsindex=0
            xlist = []
            ylist = []
            for mcsfreq in raFrequencyDict[bandwidth][location][sourceRate]:
                xlist.append(mcsindex)
                ylist.append(mcsfreq)
                mcsindex += 1
            print(xlist)
            print(ylist)
            #Plot Here
            ax = plt.subplot(111)
            ax.set_title(location+' '+bandwidth+' VariableCPU DS', y = 1.08)
            xlist = [x+(7*i) for x in xlist]
            w = 1
            ax.bar(xlist, ylist,width=w,color=colors,align='center')
            i+=1
        ax.autoscale(tight=True)
        plt.xticks(np.arange(len(xlist))*7+2,raFrequencyDict[bandwidth][location])
        mcs0 = mpatches.Patch(color='#FF0000', label='MCS0')
        mcs1 = mpatches.Patch(color='#800000', label='MCS1')
        mcs2 = mpatches.Patch(color='#FFFF00', label='MCS2')
        mcs3 = mpatches.Patch(color='#008000', label='MCS3')
        mcs4 = mpatches.Patch(color='#00FFFF', label='MCS4')
        mcs5 = mpatches.Patch(color='#0000FF', label='MCS5')
        mcs6 = mpatches.Patch(color='#000080', label='MCS6')
        mcs7 = mpatches.Patch(color='#800080', label='MCS7')
        
        plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.1,handles=[mcs0,mcs1,mcs2,mcs3,mcs4,mcs5,mcs6,mcs7])
        plt.subplots_adjust(left=0.1, right=0.8, top=0.85, bottom=0.1)
        plt.savefig(BASE_DIR + SLASH_SEPARATOR + 'Plots' + SLASH_SEPARATOR + location + '_' + bandwidth + 'VariableCPU_DS_ra_MCS.png', bbox_inches='tight')
        #plt.show()

	