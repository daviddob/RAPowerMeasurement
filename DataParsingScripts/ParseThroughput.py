import linecache
import os
import json
from sys import platform as _platform

####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    BASE_IP_DIR = "/media/tejash/Tejash/MSCS/CSEIndependentStudy/PowerMeasurementStudy/Readings"
    BASE_OP_DIR = "/media/tejash/Media/CSEIndependentStudy/Results"
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_IP_DIR = "D:\Readings"
    BASE_OP_DIR = "D:\Results"
    SLASH_SEPARATOR = "\/"
####################################################################################################################


for stream in os.listdir(BASE_IP_DIR):
    streamDir = BASE_IP_DIR + SLASH_SEPARATOR + stream
    for cpu in os.listdir(streamDir):
        cpuDir = streamDir + SLASH_SEPARATOR + cpu
        if os.path.isdir(cpuDir):
            resultDict = {}
            for freq in os.listdir(cpuDir):
                freqDir = cpuDir + SLASH_SEPARATOR + freq
                freqDict = {}
                if os.path.isdir(freqDir):
                    for location in os.listdir(freqDir):
                        locationDict = {}
                        locationDir = freqDir + SLASH_SEPARATOR + location
                        if os.path.isdir(locationDir):
                            for mcs in os.listdir(locationDir):
                                mcsDir = locationDir + SLASH_SEPARATOR + mcs
                                throughputSum = 0
                                numSample = 0
                                if os.path.isdir(mcsDir):
                                    mcsDict = {}
                                    for reading in os.listdir(mcsDir):
                                        readingDir = mcsDir + SLASH_SEPARATOR + reading
                                        if os.path.isdir(readingDir):
                                            readingList = []
                                            for test in os.listdir(readingDir):
                                                testDir = readingDir + SLASH_SEPARATOR + test

                                                iperfFile = testDir + SLASH_SEPARATOR + "iperf.out"
                                                print iperfFile
                                                if os.path.isfile(iperfFile):
                                                    lineNum = 8   # for finding the bandwidth value
                                                    if len(linecache.getline(iperfFile, lineNum).split("/sec")) != 2:
                                                        # lineNum += 1   
                                                        readingList.append(0)
                                                    else:                                                       #increase linunumber if not found in the current line
                                                        line = linecache.getline(iperfFile, lineNum)
                                                        if line != '':
                                                            throughput = float(line.split("/sec")[0].split(" ")[-2])
                                                            if line.split("/sec")[0].split(" ")[-1] == 'Kbits':
                                                                # throughputSum += throughput/1000
                                                                readingList.append(throughput/1000)
                                                                numSample += 1
                                                            elif line.split("/sec")[0].split(" ")[-1] == 'Mbits':
                                                                # throughputSum += throughput
                                                                readingList.append(throughput)
                                                                numSample += 1
                                            mcsDict[reading] = readingList
                                    locationDict[mcs] = mcsDict #throughputSum/numSample    
                        freqDict[location] = locationDict
                resultDict[freq] = freqDict
            if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream):
                os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream)
            if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu):
                os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu)
            with open(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu + SLASH_SEPARATOR + 'throughput.json', 'w') as fpJson:
                json.dump(resultDict, fpJson)