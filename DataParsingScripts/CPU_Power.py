import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.signal as scpy
import numpy as np
import json
from sys import platform as _platform

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




PBASE = {250000: [272.474, 271.842, 271.53, 271.852], 300000: [271.104, 272.486, 272.03, 272.26],
         350000: [274.074, 274.464, 274.438, 274.784],
         400000: [276.638, 278.324, 278.472, 278.71], 450000: [280.316, 282.288, 282.458, 282.206],
         500000: [282.734, 286.15, 286.534, 297.424],
         550000: [289.026, 293.666, 294.028, 293.92], 600000: [296.642, 303.81, 303.726, 304.218],
         800000: [316.312, 322.694, 324.194, 324.376],
         900000: [316.654, 326.832, 327.012, 327.394], 1000000: [320.892, 333.566, 334.242, 334.408],
         1100000: [330.632, 346.04, 345.538, 345.854],
         1200000: [333.446, 349.764, 350.918, 350.49], 1300000: [341.114, 362.114, 360.046, 360.96],
         1400000: [342.658, 366.076, 367.052, 366.768],
         1500000: [350.784, 377.378, 378.732, 378.084], 1600000: [359.274, 390.258, 394.278, 394.934]}

PDELTA = {250000: [98.916, 73.25, 62.186, 51.776],
          300000: [112.914, 82.04, 72.174, 58.5505],
          350000: [122.068, 91.776, 76.15733333, 71.2435],
          400000: [140.754, 108.544, 79.314, 62.1025],
          450000: [185.69, 131.847, 116.9186667, 117.4105],
          500000: [203.144, 153.189, 155.5666667, 117.142],
          550000: [242.674, 167.922, 163.7353333, 155.8265],
          600000: [260.47, 196.598, 190.9933333, 195.074],
          800000: [414.8805, 389.577, 388.2896667, 389.38725],
          900000: [501.128, 466.293, 467.3666667, 476.7625],
          1000000: [627.848, 574.99, 585.3686667, 605.2075],
          1100000: [721.372, 683.288, 700.2853333, 739.1955],
          1200000: [860.934, 814.033, 838.0933333, 905.5035],
          1300000: [866.0236901, 815.0036275, 1148.650497, 887.4576398],
          1400000: [950.821496, 895.8988415, 1256.795429, 977.4810935],
          1500000: [1029.037301, 973.124055, 1363.383362, 1066.127547],
          1600000: [1106.889107, 1049.560269, 1468.680628, 1153.390501]}

THRESHOLD = {'20MHz': {'MCS0': 100, 'MCS1': 50, 'MCS2': 50, 'MCS3': 70, 'MCS4': 100, 'MCS5': 120, 'MCS6': 150, 'MCS7': 150, 'MCSRA': 150},
            '40MHz': {'MCS0': 100, 'MCS1': 70, 'MCS2': 80, 'MCS3': 120, 'MCS4': 150, 'MCS5': 250, 'MCS6': 280, 'MCS7': 300, 'MCSRA': 300}}


resultDict = {}

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + SLASH_SEPARATOR + freq
    freqDict = {}
    for location in os.listdir(freqDir):
        locationDict = {}
        locationDir = freqDir + SLASH_SEPARATOR + location
        for mcs in os.listdir(locationDir):
            mcsDir = locationDir + SLASH_SEPARATOR + mcs
            avgPowerList = []
            powerBaseList = []
            manualEdit = False
            avgFile = BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + 'PowerAvg.txt'
            if not os.path.exists(os.path.dirname(avgFile)):
                os.makedirs(os.path.dirname(avgFile))
            mcsFile = open(avgFile, 'w')
            for reading in os.listdir(mcsDir):
                readingDir = mcsDir + SLASH_SEPARATOR + reading
                logFilePath1 = readingDir + SLASH_SEPARATOR + "log_" + freq + "_" + mcs + "_" + reading
                logFilePath2 = readingDir + SLASH_SEPARATOR + freq + "_" + mcs + "_" + reading
                logFilePath3 = readingDir + SLASH_SEPARATOR + mcs.lower() + "_" + reading

                if os.path.isfile(logFilePath1):
                    print(logFilePath1)
                    with open(logFilePath1) as logFile:
                        lines = logFile.readlines()
                elif os.path.isfile(logFilePath2):
                    print(logFilePath2)
                    with open(logFilePath2) as logFile:
                        lines = logFile.readlines()
                elif os.path.isfile(logFilePath3):
                    print(logFilePath3)
                    with open(logFilePath3) as logFile:
                        lines = logFile.readlines()
                count = 1
                powerList = []
                freqList = []
                medPowerList = []
                avgPower = 0
                opFile = BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + reading + SLASH_SEPARATOR + "file.txt"
                if not os.path.exists(os.path.dirname(opFile)):
                    os.makedirs(os.path.dirname(opFile))
                fileHandle = open(opFile, 'w')
                for line in lines[0::2]:
                    cpuFreq = int(line.split(' ')[2])
                    freqList.append(cpuFreq)
                    cpuUtil0 = float(line.split(' ')[3])
                    cpuUtil1 = float(line.split(' ')[4])
                    cpuUtil2 = float(line.split(' ')[5])
                    cpuUtil3 = float(line.split(' ')[6])
                    numCoreActive = ((0 if cpuUtil0 == 0 else 1) + (0 if cpuUtil1 == 0 else 1) + (0 if cpuUtil2 == 0 else 1) + (0 if cpuUtil3 == 0 else 1))
                    if numCoreActive <= 0:
                        numCoreActive = 1
                    power = PBASE[cpuFreq][numCoreActive-1] + (PDELTA[cpuFreq][0] * cpuUtil0)/100 + (PDELTA[cpuFreq][1] * cpuUtil1)/100 + (PDELTA[cpuFreq][2] * cpuUtil2)/100 + (PDELTA[cpuFreq][3] * cpuUtil3)/100
                    powerList.append(power)
                    medPowerList = scpy.medfilt(powerList, kernel_size=15)
                    fileHandle.write('{0:3d} {1:15f} \n'.format(count, power))
                    count += 1
                with PdfPages(BASE_OP_DIR + SLASH_SEPARATOR + freq + SLASH_SEPARATOR + location + SLASH_SEPARATOR + mcs + SLASH_SEPARATOR + reading + SLASH_SEPARATOR + "graph_pdf.pdf") as pdf:

                    plt.plot(freqList, c='r', marker='o', markersize=2)
                    plt.title('Frequency')
                    plt.axis([0, 200, 0, 2000000])
                    pdf.savefig()
                    plt.close()

                    plt.plot(powerList, c='r', marker='o', markersize=2)
                    plt.plot(np.convolve(powerList, np.ones(11)/11, mode='valid'), c='g')
                    plt.plot(medPowerList, c='b', marker='o', markersize=2)
                    plt.title('Power')
                    plt.axis([0, 200, 0, 2000])
                    pdf.savefig()
                    plt.close()
                    startIndex = 0
                    endIndex = 0
                    avgPower = 0
                    windowSize = 10
                    for i in range(len(medPowerList) - windowSize - 1):
                        if medPowerList[i+windowSize] - medPowerList[i] > THRESHOLD[freq][mcs] and 20 <= i <= 80:
                            startIndex = i + windowSize
                        elif medPowerList[i] - medPowerList[i+windowSize] > THRESHOLD[freq][mcs] and 120 <= i <= 180:
                            endIndex = i + windowSize
                    if 80 < endIndex - startIndex < 110 and startIndex != 0 and endIndex != 0:
                        avgPower = sum(powerList[startIndex:endIndex:1])/(endIndex - startIndex)
                        mcsFile.write('Power : ' + str(avgPower) + '\t')
                        mcsFile.write('Start Index : ' + str(startIndex) + '\t')
                        mcsFile.write('End Index : ' + str(endIndex) + '\n')
                    elif endIndex != 0:
                        smallWindow = 5
                        for i in range(endIndex - 110, endIndex - 80):
                            if medPowerList[i+smallWindow] - medPowerList[i] > 50:
                                startIndex = i + smallWindow
                        if startIndex == 0:
                            startIndex = endIndex - 100
                        avgPower = sum(powerList[startIndex:endIndex:1])/(endIndex - startIndex)
                        mcsFile.write('Power : ' + str(avgPower) + '\t')
                        mcsFile.write('Start Index(from end index): ' + str(startIndex) + '\t')
                        mcsFile.write('End Index : ' + str(endIndex) + '\n')
                    elif endIndex == 0:
                        startIndex = 80
                        endIndex = 120
                        avgPower = sum(powerList[startIndex:endIndex:1])/(endIndex - startIndex)
                        if avgPower != 0:
                            mcsFile.write('Power : ' + str(avgPower) + '\t')
                            mcsFile.write('Start Index(fixed): ' + str(startIndex) + '\t')
                            mcsFile.write('End Index(fixed) : ' + str(endIndex) + '\n')
                        else:
                            manualEdit = True
                            print('calculate manually')
                    else:
                        manualEdit = True
                        print('calculate manually')
                    avgPowerList.append(avgPower)
                    powerBaseList.append(sum(medPowerList[1:10])/10)     # using median list as it gives a better picture comapred to actual power
            if manualEdit:
                mcsFile.write("Average Power for MCS : check manually")
                locationDict[mcs] = 0
            else:
                diffPower = sum([i - j for i, j in zip(avgPowerList, powerBaseList)])/len(avgPowerList)       # subtracting base power from the avg power to get the diff ie Pcpu - Pbase
                mcsFile.write("Average Power for MCS : " + str(diffPower))
                locationDict[mcs] = diffPower
        freqDict[location] = locationDict
    resultDict[freq] = freqDict

with open(BASE_OP_DIR + SLASH_SEPARATOR + 'cpu_result.txt', 'w') as fpText:
    for freq in resultDict:
        fpText.write('\t' + freq + '\n\n')
        for location in resultDict[freq]:
            fpText.write(location + '\t')
            for i in range(8):
                mcs = 'MCS' + str(i)
                if mcs in resultDict[freq][location].keys():
                    fpText.write(str(resultDict[freq][location][mcs]) + '\t')
            fpText.write(str(resultDict[freq][location]['MCSRA']) + '\t')
            fpText.write('\n')
        fpText.write('\n\n')
