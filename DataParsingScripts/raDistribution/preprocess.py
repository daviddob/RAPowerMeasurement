import json
import matplotlib.pyplot as plt
import numpy as np
import re
from operator import add
from sys import platform as _platform
import matplotlib.patches as mpatches

####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    BASE_DIR = '/media/PowerMeasurementStudy/Results'
    THROUGHPUT_FILE = '/media/PowerMeasurementStudy/Results/throughput.json'
    CPU_FILE = '/media/PowerMeasurementStudy/Results/cpu_result.json'
    POWER_FILE = '/media/PowerMeasurementStudy/Results/power_output.json'
    RA_MCS_FILE = '/media/PowerMeasurementStudy/Results/ra_mcs.json'
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_DIR = 'F:\CSE630\Results'
    THROUGHPUT_FILE = 'F:\CSE630\Results\/throughput.json'
    CPU_FILE = 'F:\CSE630\Results\/final_cpudata.json'
    POWER_FILE = 'F:\CSE630\Results\/final_powerdata.json'
    RA_MCS_FILE = 'F:\CSE630\Results\/ra_mcs.json'
    SLASH_SEPARATOR = "\/"
####################################################################################################################

INF = 999999
colors = ['#FF0000','#800000','#FFFF00','#008000','#00FFFF','#0000FF','#000080','#800080']
mcs0 = mpatches.Patch(color='#FF0000', label='MCS0')
mcs1 = mpatches.Patch(color='#800000', label='MCS1')
mcs2 = mpatches.Patch(color='#FFFF00', label='MCS2')
mcs3 = mpatches.Patch(color='#008000', label='MCS3')
mcs4 = mpatches.Patch(color='#00FFFF', label='MCS4')
mcs5 = mpatches.Patch(color='#0000FF', label='MCS5')
mcs6 = mpatches.Patch(color='#000080', label='MCS6')
mcs7 = mpatches.Patch(color='#800080', label='MCS7')
bee = mpatches.Patch(color='pink', label='BEE')
bth = mpatches.Patch(color='tomato', label='BTH')

energyPerBitDict = {}
averageThroughputDict = {}
energyDict = {}

throughputFile = open(THROUGHPUT_FILE)
throughputStr = throughputFile.read()
throughputDict = json.loads(throughputStr)

cpuFile = open(CPU_FILE)
cpuStr = cpuFile.read()
cpuDict = json.loads(cpuStr)

powerFile = open(POWER_FILE)
powerStr = powerFile.read()
powerDict = json.loads(powerStr)

for freq in throughputDict:
    freqEPBDict = {}
    freqATDict = {}
    freqEnergyDict = {}
    for location in throughputDict[freq].keys():
        locEPBDict = {}
        locATDict = {}
        locEnergyDict = {}
        for mcs in throughputDict[freq][location].keys():
            mcsEPBDict = {}
            mcsATDict = {}
            mcsEnergyDict = {}
            for rate in throughputDict[freq][location][mcs].keys():
                validReadings = 0
                avgPower = 0
                avgBPS = 0
                powerReadings = []
                bpsReadings = []
                rawPowerReadings = []
                for cpuPower, totPower, bps in zip(cpuDict[freq][location][mcs][rate], powerDict[freq][location][mcs][rate], throughputDict[freq][location][mcs][rate]):
                    
                    if bps != 0:
                        # print(cpuPower, totPower, bps)
                        validReadings += 1
                        powerReadings.append((totPower - cpuPower)/bps)
                        bpsReadings.append(bps)
                        rawPowerReadings.append(totPower-cpuPower)
                        avgPower += totPower - cpuPower
                        avgBPS += bps
                if avgBPS == 0:
                    print freq + " " + location + " " + mcs + " " + rate
                mcsEPBDict[rate] = (INF,0) if avgBPS == 0 else (np.mean(powerReadings),np.std(powerReadings))#avgPower / avgBPS
                mcsATDict[rate] = (0,0) if validReadings == 0 else (np.mean(bpsReadings), np.std(bpsReadings))#avgBPS / validReadings
                mcsEnergyDict[rate] = (INF, 0) if avgBPS == 0 else (np.mean(rawPowerReadings), np.std(rawPowerReadings))
            locEPBDict[mcs] = mcsEPBDict
            locATDict[mcs] = mcsATDict
            locEnergyDict[mcs] = mcsEnergyDict
        freqEPBDict[location] = locEPBDict
        freqATDict[location] = locATDict
        freqEnergyDict[location] = locEnergyDict
    energyPerBitDict[freq] = freqEPBDict
    averageThroughputDict[freq] = freqATDict
    energyDict[freq] = freqEnergyDict

with open(BASE_DIR + SLASH_SEPARATOR + "final_energyPerBit.json", 'w') as fp:
    json.dump(energyPerBitDict, fp)
with open(BASE_DIR + SLASH_SEPARATOR + "final_averageThroughput.json", 'w') as fp:
    json.dump(averageThroughputDict, fp)
with open(BASE_DIR + SLASH_SEPARATOR + "final_power.json", 'w') as fp:
    json.dump(energyDict, fp)


def mostEfficientEPB(locationDict):
    result = {}
    for mcs in locationDict.keys():
        if mcs != 'mcsra':
            for rate in locationDict[mcs].keys():
                if rate in result:
                    if locationDict[result[rate]][rate][0] > locationDict[mcs][rate][0]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        if locationDict[result[i]][i][0] == INF:
            resultList.append((i, '',(0,0)))
        else:
            resultList.append((i, result[i][3:],locationDict[result[i]][i]))
    return resultList

def mostEfficientPower(locationDict, pDict):
    result = {}
    for mcs in locationDict.keys():
        if mcs != 'mcsra':
            for rate in locationDict[mcs].keys():
                if rate in result:
                    if locationDict[result[rate]][rate] > locationDict[mcs][rate]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((i, result[i][3:],pDict[result[i]][i]))
    return resultList

def mostEfficientMbps(locationDict, tDict):
    result = {}
    for mcs in locationDict.keys():
        if mcs != 'mcsra':
            for rate in locationDict[mcs].keys():
                if rate in result:
                    if locationDict[result[rate]][rate][0] > locationDict[mcs][rate][0]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((i, result[i][3:],tDict[result[i]][i]))
    return resultList

def highestThroughputEPB(locationDict, tDict):
    result = {}
    for mcs in locationDict.keys():
        if mcs != 'mcsra':
            for rate in locationDict[mcs].keys():
                if rate in result:
                    if tDict[result[rate]][rate][0] < tDict[mcs][rate][0]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        if locationDict[result[i]][i][0] == INF:
            resultList.append((i, '',(0,0)))
        else:
            resultList.append((i, result[i][3:],locationDict[result[i]][i]))
    return resultList

def highestThroughputPower(pDict, tDict):
    result = {}
    for mcs in pDict.keys():
        if mcs != 'mcsra':
            for rate in pDict[mcs].keys():
                if rate in result:
                    if tDict[result[rate]][rate][0] < tDict[mcs][rate][0]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        if pDict[result[i]][i][0] == INF:
            resultList.append((i, '',(0,0)))
        else:
            resultList.append((i, result[i][3:],pDict[result[i]][i]))
    return resultList

def highestThroughputMbps(tDict):
    result = {}
    for mcs in tDict.keys():
        if mcs != 'mcsra':
            for rate in tDict[mcs].keys():
                if rate in result:
                    if tDict[result[rate]][rate][0] < tDict[mcs][rate][0]:
                        result[rate] = mcs
                else:
                    result[rate] = mcs
    resultList = []
    for i in sorted(result, key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((i, result[i][3:],tDict[result[i]][i]))
    return resultList

def rateAdaptationEPB(locationDict):
    resultList = []
    mcs = 'mcsra'
    for rate in sorted(locationDict[mcs].keys(), key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((rate, mcs[3:], locationDict[mcs][rate],0.125))
    return resultList

def rateAdaptationMbps(tDict):
    resultList = []
    mcs = 'mcsra'
    for rate in sorted(tDict[mcs].keys(), key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((rate, mcs[3:], tDict[mcs][rate],0.125))
    print resultList
    print "----------------------------------------------------------------------"
    print tDict
    return resultList

def rateAdaptationPower(pDict):
    resultList = []
    mcs = 'mcsra'
    for rate in sorted(pDict[mcs].keys(), key=(lambda k: int(re.findall('\d+', k)[0]))):
        resultList.append((rate, mcs[3:], pDict[mcs][rate],0.125))
    return resultList

def label(ax, rects, list):
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width()/2., 1.02*height,'%s' % list[i],ha='center', va='bottom')

def energyBarPlot(freq, location, eff, ht, mcsth):
    width = 0.20
    ind = np.arange(len(eff))
    fig, ax = plt.subplots(figsize=(10,6))
    rects1 = ax.bar(ind, list(eff[i][2][0] for i in ind ), width, color='pink', yerr=list(eff[i][2][1] for i in ind ))
    label(ax,rects1,list(eff[j][1] for j in ind))
    rects2 = ax.bar(ind + width, list(ht[i][2][0] for i in ind ), width, color='tomato', yerr=list(ht[i][2][1] for i in ind ))
    label(ax,rects2,list(ht[i][1] for i in ind ))
    #rects3 = ax.bar(ind + 2 * width, list(mcsth[i][2][0] for i in ind ), width, color='plum', yerr=list(mcsth[i][2][1] for i in ind ))
    #label(ax,rects3,list(mcsth[i][1] for i in ind ))
    prevlist=[0,0,0,0,0,0,0,0]
    for z in range(0,8):
        if(z == 7): 
            for i in ind:
                ax.text(i + 2 * width + width/2 + 0.05, mcsth[i][2][0] + 0.5, "ra", ha='center', va='bottom')
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], yerr=list(mcsth[i][2][1] for i in ind ), bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
        else:
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
    ax.set_ylabel('Energy per bit (nJ/bit)')
    ax.set_xlabel('Send Rate (Mbps)')
    ax.set_title(location+' '+freq, y = 1.08)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(list(eff[k][0][:-4] for k in ind))
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.1,handles=[mcs0,mcs1,mcs2,mcs3,mcs4,mcs5,mcs6,mcs7,bee,bth])
    plt.subplots_adjust(left=0.1, right=0.8, top=0.85, bottom=0.1)
    #plt.savefig(BASE_DIR + SLASH_SEPARATOR + 'Plots' + SLASH_SEPARATOR + location + '_' + freq + '_energy.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)

def powerBarPlot(freq, location, eff, ht, mcsth):
    width = 0.20
    ind = np.arange(len(eff))
    fig, ax = plt.subplots(figsize=(10,6))
    rects1 = ax.bar(ind, list(eff[i][2][0] for i in ind ), width, color='pink', yerr=list(eff[i][2][1] for i in ind ))
    label(ax,rects1,list(eff[j][1] for j in ind))
    rects2 = ax.bar(ind + width, list(ht[i][2][0] for i in ind ), width, color='tomato', yerr=list(ht[i][2][1] for i in ind ))
    label(ax,rects2,list(ht[i][1] for i in ind ))
    #rects3 = ax.bar(ind + 2 * width, list(mcsth[i][2][0] for i in ind ), width, color='plum', yerr=list(mcsth[i][2][1] for i in ind ))
    #label(ax,rects3,list(mcsth[i][1] for i in ind ))
    prevlist=[0,0,0,0,0,0,0,0]
    for z in range(0,8):
        if(z == 7): 
            for i in ind:
                ax.text(i + 2 * width + width/2 + 0.05, mcsth[i][2][0] + 0.5, "ra", ha='center', va='bottom')
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], yerr=list(mcsth[i][2][1] for i in ind ), bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
        else:
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
    ax.set_ylabel('Energy (mW)')
    ax.set_xlabel('Send Rate (Mbps)')
    ax.set_title(location+' '+freq, y = 1.08)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(list(eff[k][0][:-4] for k in ind))
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.1,handles=[mcs0,mcs1,mcs2,mcs3,mcs4,mcs5,mcs6,mcs7,bee,bth])
    plt.subplots_adjust(left=0.1, right=0.8, top=0.85, bottom=0.1)
    #plt.savefig(BASE_DIR + SLASH_SEPARATOR + 'Plots' + SLASH_SEPARATOR + location + '_' + freq + '_power.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)

def throughputBarPlot(freq, location, eff, ht, mcsth):
    width = 0.20
    ind = np.arange(len(eff))
    fig, ax = plt.subplots(figsize=(10,6))
    rects1 = ax.bar(ind, list(eff[i][2][0] for i in ind ), width, color='pink', yerr=list(eff[i][2][1] for i in ind ))
    label(ax,rects1,list(eff[j][1] for j in ind))
    rects2 = ax.bar(ind + width, list(ht[i][2][0] for i in ind ), width, color='tomato', yerr=list(ht[i][2][1] for i in ind ))
    label(ax,rects2,list(ht[i][1] for i in ind ))
    #rects3 = ax.bar(ind + 2 * width, list(mcsth[i][2][0] for i in ind ), width, color='plum', yerr=list(mcsth[i][2][1] for i in ind ))
    #label(ax,rects3,list(mcsth[i][1] for i in ind ))
    prevlist=[0,0,0,0,0,0,0,0]
    for z in range(0,8):
        if(z == 7): 
            for i in ind:
                ax.text(i + 2 * width + width/2 + 0.05, mcsth[i][2][0] + 0.5, "ra", ha='center', va='bottom')
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], yerr=list(mcsth[i][2][1] for i in ind ), bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
        else:
            rects3 = ax.bar(ind + 2 * width, list((mcsth[i][2][0]*mcsth[i][3]) for i in ind ), width, color=colors[z], bottom=prevlist)
            prevlist = map(add,prevlist,list((mcsth[i][2][0])*mcsth[i][3] for i in ind ))
    ax.set_ylabel('Average throughput (Mbps)')
    ax.set_xlabel('Send Rate (Mbps)')
    ax.set_title(location+' '+freq, y = 1.08)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(list(eff[k][0][:-4] for k in ind))
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.1,handles=[mcs0,mcs1,mcs2,mcs3,mcs4,mcs5,mcs6,mcs7,bee,bth])
    plt.subplots_adjust(left=0.1, right=0.8, top=0.85, bottom=0.1)
    #plt.savefig(BASE_DIR + SLASH_SEPARATOR + 'Plots' + SLASH_SEPARATOR + location + '_' + freq + '_throughput.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)

for freq in averageThroughputDict:
    for location in sorted(averageThroughputDict[freq].keys(), key=(lambda k: int(re.findall('\d+', k)[0]))):
        print location
        effEPB = mostEfficientEPB(energyPerBitDict[freq][location])
        htEPB = highestThroughputEPB(energyPerBitDict[freq][location],averageThroughputDict[freq][location])
        mcsEPB = rateAdaptationEPB(energyPerBitDict[freq][location])
        # print effEPB
        # print htEPB
        # print mcsEPB
        energyBarPlot(freq, location, effEPB, htEPB, mcsEPB)

        effTx = mostEfficientMbps(energyPerBitDict[freq][location],averageThroughputDict[freq][location])
        htTx = highestThroughputMbps(averageThroughputDict[freq][location])
        mcsTx = rateAdaptationMbps(averageThroughputDict[freq][location])

        # print effTx
        # print htTx
        # print mcsTx
        throughputBarPlot(freq, location, effTx, htTx, mcsTx)
        
        effPow = mostEfficientPower(energyPerBitDict[freq][location],powerDict[freq][location])
        htPow = highestThroughputPower(powerDict[freq][location],averageThroughputDict[freq][location])
        mcsPow = rateAdaptationPower(powerDict[freq][location])

        powerBarPlot(freq, location, effPow, htPow, mcsPow)
