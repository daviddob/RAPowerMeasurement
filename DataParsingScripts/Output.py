import json
import matplotlib.pyplot as plt
import numpy as np
import re
from sys import platform as _platform

####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    BASE_DIR = '/media/PowerMeasurementStudy/Results'
    THROUGHPUT_FILE = '/media/PowerMeasurementStudy/Results/throughput.json'
    CPU_FILE = '/media/PowerMeasurementStudy/Results/cpu_result.json'
    POWER_FILE = '/media/PowerMeasurementStudy/Results/power_output.json'
    RA_MCS_FILE = '/media/PowerMeasurementStudy/Results/ra_mcs.json'
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_DIR = 'C:\PowerMeasurementStudy\Results'
    THROUGHPUT_FILE = 'C:\PowerMeasurementStudy\Results\/throughput.json'
    CPU_FILE = 'C:\PowerMeasurementStudy\Results\cpu_result.json'
    POWER_FILE = 'C:\PowerMeasurementStudy\Results\power_output.json'
    RA_MCS_FILE = 'C:\PowerMeasurementStudy\Results\/ra_mcs.json'
    SLASH_SEPARATOR = "\/"
####################################################################################################################



removedLocations = {'20MHz':['Location24','Location19'],
                    '40MHz':['Location2','Location3','Location14','Location18','Location13','Location10']}

throughputFile = open(THROUGHPUT_FILE)
throughputStr = throughputFile.read()
throughputDict = json.loads(throughputStr)

cpuFile = open(CPU_FILE)
cpuStr = cpuFile.read()
cpuDict = json.loads(cpuStr)

powerFile = open(POWER_FILE)
powerStr = powerFile.read()
powerDict = json.loads(powerStr)

resultDict = {}

for freq in throughputDict:
    freqDict = {}
    raThroughputList = []
    raCPUList = []
    raWIFIList = []
    raEnergyPerBitListWifi = []
    raEnergyPerBitListTotal = []

    bestEfficientThWifiList = []
    bestEfficientMCSWifiList = []
    bestEfficientCPUWifiList = []
    bestEfficientWIFIWifiList = []
    bestEfficientEnergyPerBitWifiList = []

    bestEfficientThTotalList = []
    bestEfficientMCSTotalList = []
    bestEfficientCPUTotalList = []
    bestEfficientWIFITotalList = []
    bestEfficientEnergyPerBitTotalList = []

    highestThroughputMCSList = []
    highestThroughputList = []
    highestThroughputValList = []
    highestThroughputCPUList = []
    highestThroughputWIFIList = []
    highestThroughputEnergyPerBitListWifi = []
    highestThroughputEnergyPerBitListTotal = []

    locationList = []

    for location in sorted(throughputDict[freq].keys(), key=(lambda k: int(re.findall('\d+', k)[0]))):
        if location not in removedLocations[freq]:
            raThroughputList.append(throughputDict[freq][location]['MCSRA'])
            raCPUList.append(cpuDict[freq][location]['MCSRA'])
            raWIFIList.append(powerDict[freq][location]['MCSRA'] - cpuDict[freq][location]['MCSRA'])
            raEnergyPerBitListWifi.append((powerDict[freq][location]['MCSRA'] - cpuDict[freq][location]['MCSRA'])/(throughputDict[freq][location]['MCSRA']*1000000))
            raEnergyPerBitListTotal.append((powerDict[freq][location]['MCSRA'])/(throughputDict[freq][location]['MCSRA']*1000000))

            del(throughputDict[freq][location]['MCSRA'])

            highestThroughputMcs = max(throughputDict[freq][location].keys(), key=(lambda k: throughputDict[freq][location][k]))
            highestThroughputMCSList.append(highestThroughputMcs)
            highestThroughputList.append(throughputDict[freq][location][highestThroughputMcs])
            highestThroughputValList.append(highestThroughputMcs)
            highestThroughputCPUList.append(cpuDict[freq][location][highestThroughputMcs])
            highestThroughputWIFIList.append(powerDict[freq][location][highestThroughputMcs]-cpuDict[freq][location][highestThroughputMcs])
            highestThroughputEnergyPerBitListWifi.append((powerDict[freq][location][highestThroughputMcs] - cpuDict[freq][location][highestThroughputMcs])/(throughputDict[freq][location][highestThroughputMcs]*1000000))
            highestThroughputEnergyPerBitListTotal.append((powerDict[freq][location][highestThroughputMcs])/(throughputDict[freq][location][highestThroughputMcs]*1000000))

            efficientMcsWifi = min(throughputDict[freq][location].keys(), key=(lambda k: (powerDict[freq][location][k] - cpuDict[freq][location][k])/throughputDict[freq][location][k]))
            efficientMcsTotal= min(throughputDict[freq][location].keys(), key=(lambda k: powerDict[freq][location][k]/throughputDict[freq][location][k]))
            bestEfficientMCSWifiList.append(efficientMcsWifi)
            bestEfficientMCSTotalList.append(efficientMcsTotal)
            bestEfficientThWifiList.append(throughputDict[freq][location][efficientMcsWifi])
            bestEfficientThTotalList.append(throughputDict[freq][location][efficientMcsTotal])
            bestEfficientCPUWifiList.append(cpuDict[freq][location][efficientMcsWifi])
            bestEfficientWIFIWifiList.append(powerDict[freq][location][efficientMcsWifi]-cpuDict[freq][location][efficientMcsWifi])
            bestEfficientCPUTotalList.append(cpuDict[freq][location][efficientMcsTotal])
            bestEfficientWIFITotalList.append(powerDict[freq][location][efficientMcsTotal]-cpuDict[freq][location][efficientMcsTotal])
            bestEfficientEnergyPerBitWifiList.append((powerDict[freq][location][efficientMcsWifi] - cpuDict[freq][location][efficientMcsWifi])/(throughputDict[freq][location][efficientMcsWifi]*1000000))
            bestEfficientEnergyPerBitTotalList.append((powerDict[freq][location][efficientMcsTotal])/(throughputDict[freq][location][efficientMcsTotal]*1000000))

            loc = 'L' + location[-2:]
            if loc[1] == 'n':
                loc = loc[0]+loc[2]
            locationList.append(loc)

    freqDict['RA_TH'] = raThroughputList
    freqDict['RA_MCS'] = ['RA' for number in range(len(raThroughputList))]
    freqDict['RA_CPU'] = raCPUList
    freqDict['RA_WIFI'] = raWIFIList
    freqDict['RA_EPB'] = raEnergyPerBitListWifi
    freqDict['RA_EPB_TOTAL'] = raEnergyPerBitListTotal

    freqDict['HS_TH'] = highestThroughputList
    freqDict['HS_MCS'] = highestThroughputMCSList
    freqDict['HS_CPU'] = highestThroughputCPUList
    freqDict['HS_WIFI'] = highestThroughputWIFIList
    freqDict['HS_EPB'] = highestThroughputEnergyPerBitListWifi
    freqDict['HS_EPB_TOTAL'] = highestThroughputEnergyPerBitListTotal

    freqDict['EE_TH_WIFI'] = bestEfficientThWifiList
    freqDict['EE_MCS_WIFI'] = bestEfficientMCSWifiList
    freqDict['EE_CPU_WIFI'] = bestEfficientCPUWifiList
    freqDict['EE_WIFI_WIFI'] = bestEfficientWIFIWifiList
    freqDict['EE_EPB_WIFI'] = bestEfficientEnergyPerBitWifiList

    freqDict['EE_TH_TOTAL'] = bestEfficientThTotalList
    freqDict['EE_MCS_TOTAL'] = bestEfficientMCSTotalList
    freqDict['EE_CPU_TOTAL'] = bestEfficientCPUTotalList
    freqDict['EE_WIFI_TOTAL'] = bestEfficientWIFITotalList
    freqDict['EE_EPB_TOTAL'] = bestEfficientEnergyPerBitTotalList

    freqDict['LOC'] = locationList
    resultDict[freq] = freqDict


GoodLinks = {'20MHz':['L1','L2','L8','L9'],
             '40MHz':['L1','L16','L20','L21','L22']}
MediumLinks = {'20MHz':['L3','L10','L13','L15','L16','L17','L18','L20','L23'],
               '40MHz':['L5','L15','L17','L23','L24','L25','L26']}
BadLinks = {'20MHz':['L4','L5','L11','L12','L22','L25'],
            '40MHz':['L6','L7','L9']}


def barPlot(freq, type, yLabel, xLabel, title):
    width = 0.20
    ind = np.arange(len(resultDict[freq]['LOC']))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, resultDict[freq]['RA_' + type], width, color='pink')
    label(ax,rects1,resultDict[freq]['RA_MCS'])
    rects2 = ax.bar(ind + width, resultDict[freq]['HS_' + type], width, color='tomato')
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in ind])
    rects3 = ax.bar(ind + 2 * width, resultDict[freq]['EE_' + type + '_WIFI'], width, color='plum')
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_WIFI'][i])[0] for i in ind])
    rects4 = ax.bar(ind + 3 * width, resultDict[freq]['EE_' + type + '_TOTAL'], width, color='c')
    label(ax,rects4,[re.findall('\d+', resultDict[freq]['EE_MCS_TOTAL'][i])[0] for i in ind])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title+' '+freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(resultDict[freq]['LOC'])
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('RA', 'HSM', 'BEE(WIFI Power)', 'BEE(Total Power)'))
    plt.show()


def barPlot2(freq, type, yLabel, xLabel, title):
    width = 0.25
    ind = np.arange(len(resultDict[freq]['LOC']))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, resultDict[freq]['RA_' + type], width, color='pink')
    label(ax,rects1,resultDict[freq]['RA_MCS'])
    rects2 = ax.bar(ind + width, resultDict[freq]['HS_' + type], width, color='tomato')
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in ind])
    rects3 = ax.bar(ind + 2 * width, resultDict[freq]['EE_' + type + '_WIFI'], width, color='plum')
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_WIFI'][i])[0] for i in ind])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title+' '+freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(resultDict[freq]['LOC'])
    ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
    plt.show()


def barPlot3(freq, type, yLabel, xLabel, title):
    width = 0.25
    ind = np.arange(len(resultDict[freq]['LOC']))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, resultDict[freq]['RA_' + type+'_TOTAL'], width, color='pink')
    label(ax,rects1,resultDict[freq]['RA_MCS'])
    rects2 = ax.bar(ind + width, resultDict[freq]['HS_' + type+'_TOTAL'], width, color='tomato')
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in ind])
    rects3 = ax.bar(ind + 2 * width, resultDict[freq]['EE_' + type + '_TOTAL'], width, color='plum')
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_TOTAL'][i])[0] for i in ind])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title+' '+freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(resultDict[freq]['LOC'])
    ax.legend((rects1[0], rects2[0], rects3[0]), ('RA', 'HSM', 'BEE'))
    plt.show()


def label(ax, rects, list):
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width()/2., 1.02*height,'%s' % list[i],ha='center', va='bottom')


def barPlotLinkType(freq, type, yLabel, xLabel, title, linkType, linkTypeList):
    index = [resultDict[freq]['LOC'].index(i) for i in linkTypeList[freq]]
    width = 0.20
    ind = np.arange(len(index))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, [resultDict[freq]['RA_'+type][i] for i in index], width, color='pink')
    label(ax,rects1,[resultDict[freq]['RA_MCS'][i] for i in index])
    rects2 = ax.bar(ind + width, [resultDict[freq]['HS_'+type][i] for i in index], width, color='tomato')
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in index])
    rects3 = ax.bar(ind + 2 * width, [resultDict[freq]['EE_'+type+'_WIFI'][i] for i in index], width, color='plum')
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_WIFI'][i])[0] for i in index])
    rects4 = ax.bar(ind + 3 * width, [resultDict[freq]['EE_'+type+'_TOTAL'][i] for i in index], width, color='c')
    label(ax,rects4,[re.findall('\d+', resultDict[freq]['EE_MCS_TOTAL'][i])[0] for i in index])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title+" "+linkType+" "+freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels([resultDict[freq]['LOC'][i] for i in index])
    ax.legend((rects1[0], rects2[0], rects3[0],rects4[0]), ('RA', 'HSM','BEE(WIFI Power)','BEE(Total Power)'))
    plt.show()


def stackedBarPlotCpuWifi(freq, yLabel, xLabel, title):
    width = 0.20
    ind = np.arange(len(resultDict[freq]['LOC']))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, resultDict[freq]['RA_WIFI'], width, color='pink')
    rects2 = ax.bar(ind + width, resultDict[freq]['HS_WIFI'], width, color='tomato')
    rects3 = ax.bar(ind + 2 * width, resultDict[freq]['EE_WIFI_WIFI'], width, color='plum')
    rects4 = ax.bar(ind + 3 * width, resultDict[freq]['EE_WIFI_TOTAL'], width, color='m')
    rects5 = ax.bar(ind, resultDict[freq]['RA_CPU'], width, color='grey',bottom=resultDict[freq]['RA_WIFI'])
    label(ax,rects1,resultDict[freq]['RA_MCS'])
    rects6 = ax.bar(ind + width, resultDict[freq]['HS_CPU'], width, color='orange', bottom=resultDict[freq]['HS_WIFI'])
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in ind])
    rects7 = ax.bar(ind + 2 * width, resultDict[freq]['EE_CPU_WIFI'], width, color='c', bottom=resultDict[freq]['EE_WIFI_WIFI'])
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_WIFI'][i])[0] for i in ind])
    rects8 = ax.bar(ind + 3 * width, resultDict[freq]['EE_CPU_TOTAL'], width, color='y', bottom=resultDict[freq]['EE_WIFI_TOTAL'])
    label(ax,rects4,[re.findall('\d+', resultDict[freq]['EE_MCS_TOTAL'][i])[0] for i in ind])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title + " " + freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(resultDict[freq]['LOC'])
    ax.legend((rects1[0], rects2[0], rects3[0],rects4[0], rects5[0], rects6[0], rects7[0], rects8[0]), ('RA WIFI', 'HSM WIFI', 'BEE WIFI (WIFI Power)','BEE WIFI (Total Power)','RA CPU','HSM CPU','BEE CPU(WIFI Power)','BEE CPU(Total Power)'))
    plt.show()


def stackedBarPlotCpuWifiEpb(freq, yLabel, xLabel, title):
    width = 0.20
    ind = np.arange(len(resultDict[freq]['LOC']))
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, [resultDict[freq]['RA_WIFI'][i]/(resultDict[freq]['RA_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='pink')
    rects2 = ax.bar(ind + width, [resultDict[freq]['HS_WIFI'][i]/(resultDict[freq]['HS_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='tomato')
    rects3 = ax.bar(ind + 2 * width, [resultDict[freq]['EE_WIFI_WIFI'][i]/(resultDict[freq]['EE_TH_WIFI'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='plum')
    rects4 = ax.bar(ind + 3 * width, [resultDict[freq]['EE_WIFI_TOTAL'][i]/(resultDict[freq]['EE_TH_TOTAL'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='m')

    rects5 = ax.bar(ind, [resultDict[freq]['RA_CPU'][i]/(resultDict[freq]['RA_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='grey',bottom=[resultDict[freq]['RA_WIFI'][i]/(resultDict[freq]['RA_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))])
    label(ax,rects1,resultDict[freq]['RA_MCS'])
    rects6 = ax.bar(ind + width, [resultDict[freq]['HS_CPU'][i]/(resultDict[freq]['HS_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='orange', bottom=[resultDict[freq]['HS_WIFI'][i]/(resultDict[freq]['HS_TH'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))])
    label(ax,rects2,[re.findall('\d+', resultDict[freq]['HS_MCS'][i])[0] for i in ind])
    rects7 = ax.bar(ind + 2 * width, [resultDict[freq]['EE_CPU_WIFI'][i]/(resultDict[freq]['EE_TH_WIFI'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='c', bottom=[resultDict[freq]['EE_WIFI_WIFI'][i]/(resultDict[freq]['EE_TH_WIFI'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))])
    label(ax,rects3,[re.findall('\d+', resultDict[freq]['EE_MCS_WIFI'][i])[0] for i in ind])
    rects8 = ax.bar(ind + 3 * width, [resultDict[freq]['EE_CPU_TOTAL'][i]/(resultDict[freq]['EE_TH_TOTAL'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))], width, color='y', bottom=[resultDict[freq]['EE_WIFI_TOTAL'][i]/(resultDict[freq]['EE_TH_TOTAL'][i]*1000000) for i in range(len(resultDict[freq]['LOC']))])
    label(ax,rects4,[re.findall('\d+', resultDict[freq]['EE_MCS_TOTAL'][i])[0] for i in ind])
    ax.set_ylabel(yLabel)
    ax.set_xlabel(xLabel)
    ax.set_title(title + " " + freq)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(resultDict[freq]['LOC'])
    ax.legend((rects1[0], rects2[0], rects3[0],rects4[0], rects5[0], rects6[0], rects7[0], rects8[0]), ('RA WIFI', 'HSM WIFI', 'BEE WIFI (WIFI Power)','BEE WIFI (Total Power)','RA CPU','HSM CPU','BEE CPU(WIFI Power)','BEE CPU(Total Power)'))
    plt.show()
################################ FOR 20 MHZ ###################################

# Throughput for all the locations
barPlot('20MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput All Links')

# Energy per Bit for all the locations
barPlot2('20MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per Bit All Links Based on WIFI Power')

# Energy per Bit for all the locations
barPlot3('20MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per Bit All Links Based on Total Power')

# Stacked plot for CPU vs WIFI
stackedBarPlotCpuWifi('20MHz', 'Power', 'Locations', 'CPU and WiFi Usage All Links')

stackedBarPlotCpuWifiEpb('20MHz', 'EPB', 'Locations', 'CPU and WiFi Energy Per Bit All Links')

# Throughput for each Link Type
barPlotLinkType('20MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Good Links', GoodLinks)

barPlotLinkType('20MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Medium Links', MediumLinks)

barPlotLinkType('20MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Bad Links', BadLinks)

# Energy Per Bit for each Link Type
barPlotLinkType('20MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Good Links', GoodLinks)

barPlotLinkType('20MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Medium Links', MediumLinks)

barPlotLinkType('20MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Bad Links', BadLinks)

################################ FOR 40 MHZ ###################################

# Throughput for all the locations
barPlot('40MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput All Links')

# Energy per Bit for all the locations
barPlot2('40MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per Bit All Links Based on WIFI Power')

# Energy per Bit for all the locations
barPlot3('40MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per Bit All Links Based on Total Power')

# Stacked plot for CPU vs WIFI
stackedBarPlotCpuWifi('40MHz', 'Power', 'Locations', 'CPU and WiFi Usage All Links')

stackedBarPlotCpuWifiEpb('40MHz', 'EPB', 'Locations', 'CPU and WiFi Energy Per Bit All Links')

# Throughput for each Link Type
barPlotLinkType('40MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Good Links', GoodLinks)

barPlotLinkType('40MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Medium Links', MediumLinks)

barPlotLinkType('40MHz', 'TH', 'Throughput Mbps', 'Locations', 'Throughput', 'Bad Links', BadLinks)

# Energy Per Bit for each Link Type
barPlotLinkType('40MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Good Links', GoodLinks)

barPlotLinkType('40MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Medium Links', MediumLinks)

barPlotLinkType('40MHz', 'EPB', 'Energy Per bit', 'Locations', 'Energy Per bit', 'Bad Links', BadLinks)

###########################################FOR HISTOGRAM PLOT#########################################################

def histPlot(mcsList, freq, location):
    width = 0.75
    ind = np.arange(len(mcsList))
    fig, ax = plt.subplots()
    rects = ax.bar(ind, mcsList, width, color='c')
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width()/2., 1.02*height,'{:.2%}.'.format(mcsList[i]/sum(mcsList)), ha='center', va='bottom')
    ax.set_ylabel('count')
    ax.set_xlabel('MCS Index')
    ax.set_title(freq+' '+location+' histogram')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(ind)
    plt.show()
raMCSFile = open(RA_MCS_FILE)
raMCSStr = raMCSFile.read()
raMCSDict = json.loads(raMCSStr)

for freq in raMCSDict:
    for location in raMCSDict[freq]:
        histPlot(raMCSDict[freq][location], freq, location)

