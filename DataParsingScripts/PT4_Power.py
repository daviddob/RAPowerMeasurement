import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.signal as scpy
import numpy as np
import sys
from sys import platform as _platform
import json


####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    BASE_IP_DIR = "/media/tejash/Tejash/MSCS/CSEIndependentStudy/PowerMeasurementStudy/Readings"
    BASE_OP_DIR = "/media/tejash/Media/CSEIndependentStudy/Results"
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_IP_DIR = "C:\PowerMeasurementStudy\Readings"
    BASE_OP_DIR = "C:\PowerMeasurementStudy\Results"
    SLASH_SEPARATOR = "\/"
####################################################################################################################


manual_counter = 0
auto_counter = 0
base_power_manual_counter = 0
base_power_auto_counter= 0
window_size = 400

MAX_THRESHOLD = {
    '40MHz': {'MCS0': 100, 'MCS1': 100, 'MCS2': 120, 'MCS3': 150, 'MCS4': 200, 'MCS5': 300, 'MCS6': 300, 'MCS7': 300,
              'MCSRA': 300},
    '20MHz': {'MCS0': 450, 'MCS1': 550, 'MCS2': 600, 'MCS3': 650, 'MCS4': 700, 'MCS5': 800, 'MCS6': 900, 'MCS7': 900,
              'MCSRA': 900}}

MIN_THRESHOLD = {'MCS0': 10, 'MCS1': 10, 'MCS2': 10, 'MCS3': 10, 'MCS4': 16, 'MCS5': 18, 'MCS6': 40, 'MCS7': 60,
                 'MCSRA': 60}


locationPowerDictionary = {}

print (
    'input directory: ' + BASE_IP_DIR + ' :::: output directory: ' + BASE_OP_DIR + ' ::: ' + 'Slash Separator:' + SLASH_SEPARATOR)

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + SLASH_SEPARATOR + freq
    for location in os.listdir(freqDir):
        locationDir = freqDir + SLASH_SEPARATOR + location
        for mcs in os.listdir(locationDir):
            mcsDir = locationDir + SLASH_SEPARATOR + mcs
            avgPowerList = []
            mcsValues = {}
            manualEdit = False
            if not os.path.exists(os.path.dirname(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt')):
                os.makedirs(os.path.dirname(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt'))
            mcsFile = open(
                BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt',
                'w')
            for reading in os.listdir(mcsDir):
                readingDir = mcsDir + SLASH_SEPARATOR + reading
                try:
                    with open(readingDir + SLASH_SEPARATOR + freq + "_" + mcs + "_" + reading + ".txt") as logFile:
                        lines = logFile.readlines()
                    print(logFile.name)
                except IOError:
                    continue
                powerList = []

                opFile = BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + reading + SLASH_SEPARATOR + "extracted_power_reading.txt"
                if not os.path.exists(os.path.dirname(opFile)):
                    os.makedirs(os.path.dirname(opFile))
                fileHandle = open(opFile, 'w')

                count = 0
                for line in lines:
                    current = float(line.split(',')[0])
                    voltage = float(line.split(',')[3])
                    power = current * voltage
                    powerList.append(power)
                    fileHandle.write('{0:3d} {1:15f} \n'.format(count, power))
                    count += 1

                medPowerList = scpy.medfilt(powerList, kernel_size=799)

                # Plotting graph here
                with PdfPages(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + reading + SLASH_SEPARATOR + "pt4_graph_pdf.pdf") as pdf:
                    plt.plot(powerList, c='r', marker='o', markersize=0.0, linewidth=0.1)
                    plt.title('Power')
                    plt.plot(np.convolve(powerList, np.ones(799) / 799, mode='valid'), c='g')
                    plt.plot(medPowerList, c='b', marker='o', markersize=0.0, linewidth=0.1)
                    plt.axis([0, 85000, 0, 5000])
                    pdf.savefig(dpi=200)
                    plt.close()

                # Now extracting start index and end index
                windowSize = 1300
                gotEndIndex = False
                startIndex = 0
                avgBasePower =0
                baseStartIndex = 0
                baseEndIndex = 0
                baseWindowSize = 1200
                endIndex = 0
                avgPower = 0
                for i in range(len(medPowerList) - windowSize - 1):
                    if not gotEndIndex:
                        if medPowerList[i] - medPowerList[i + windowSize] > MAX_THRESHOLD[freq][mcs] and 65000 <= i <= 81000:
                            endIndex = i
                            print(endIndex)
                            gotEndIndex = True
                    else:
                        if medPowerList[i + windowSize] - medPowerList[i] > MAX_THRESHOLD[freq][mcs] / 2:
                            if endIndex - 7000 <= i <= endIndex - 800:
                                endIndex = i
                                print (endIndex)
                                gotEndIndex = True
                        if medPowerList[i + windowSize] - medPowerList[i] > MAX_THRESHOLD[freq][
                            mcs] and 20000 <= i <= 40000:
                            startIndex = i + windowSize
                            print (startIndex)
                for count in range(1000,9000,1):
                    temp_arr = np.array(medPowerList[count:count+baseWindowSize])
                    if (np.std(temp_arr,ddof=1))<50 :
                        baseStartIndex = count
                        baseEndIndex = count+baseWindowSize
                        print('base start index:'+ str(baseStartIndex) +" base end index:"+ str(baseEndIndex))
                        avgBasePower = sum(powerList[baseStartIndex:baseEndIndex:1]) / (baseEndIndex - baseStartIndex)
                        break

                mcsFile.write('Base Power : ' + str(avgBasePower) + '\t')

                if 40000 < endIndex - startIndex < 55000 and startIndex != 0 and endIndex != 0:
                    avgPower = sum(powerList[startIndex:endIndex:1]) / (endIndex - startIndex)
                    mcsFile.write('Power : ' + str(avgPower) + '\t')
                    mcsFile.write('Start Index : ' + str(startIndex) + '\t')
                    mcsFile.write('End Index : ' + str(endIndex) + '\n')

                elif endIndex == 0 and mcs == 'MCS0':
                    startIndex = 40000
                    endIndex = 60000
                    avgPower = sum(powerList[startIndex:endIndex:1]) / (endIndex - startIndex)
                    mcsFile.write('Power : ' + str(avgPower) + '\t')
                    mcsFile.write('Start Index(fixed): ' + str(startIndex) + '\t')
                    mcsFile.write('End Index(fixed) : ' + str(endIndex) + '\n')

                elif endIndex != 0:
                    smallWindow = 799
                    for i in range(endIndex - 55000, endIndex - 40000):
                        if medPowerList[i + smallWindow] - medPowerList[i] > MAX_THRESHOLD[freq][mcs] / 1.5:
                            startIndex = i + smallWindow
                    if startIndex == 0:
                        startIndex = endIndex - 50000
                    print ("start: " + str(startIndex) + " end " + str(endIndex))
                    avgPower = sum(powerList[startIndex:endIndex:1]) / (endIndex - startIndex)
                    mcsFile.write('Power : ' + str(avgPower) + '\t')
                    mcsFile.write('Start Index(from end index): ' + str(startIndex) + '\t')
                    mcsFile.write('End Index : ' + str(endIndex) + '\n')

                else:
                    manualEdit = True
                    manual_counter += 1
                    print('calculate manually')

                if not manualEdit:
                    auto_counter += 1

                if avgBasePower != 0:
                    base_power_auto_counter += 1
                else:
                    base_power_manual_counter += 1

                if avgPower != 0 and avgBasePower == 0:
                    print ('Script failed due to base power. check base power manually. ')

                avgPowerList.append(avgPower)

            if len(avgPowerList) != 0:

                if manualEdit:
                    mcsFile.write("Average Power for MCS : check manually")
                    mcsValues[mcs] = 'calculate manually'
                else:
                    mcsFile.write("Average Power for MCS : " + str(sum(avgPowerList) / len(avgPowerList)))
                    mcsValues[mcs] =  sum(avgPowerList) / len(avgPowerList)
        locationPowerDictionary[location] = mcsValues


    with open(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + "final_" + freq + "data.json", 'w') as fp:
        json.dump(locationPowerDictionary, fp)

    print("manual_count : " + str(manual_counter) + "auto counter: " + str(auto_counter))
