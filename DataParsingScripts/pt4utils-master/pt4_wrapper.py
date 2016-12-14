import os
import sys
from pt4_filereader import Pt4FileReader
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
            for freq in os.listdir(cpuDir):
                freqDir = cpuDir + SLASH_SEPARATOR + freq
                for location in os.listdir(freqDir):
                    locationDir = freqDir + SLASH_SEPARATOR + location
                    for mcs in os.listdir(locationDir):
                        mcsDir = locationDir + SLASH_SEPARATOR + mcs
                        if os.path.isdir(mcsDir):
                            for reading in os.listdir(mcsDir):
                                readingDir = mcsDir + SLASH_SEPARATOR + reading
                                # print (readingDir + "/" + "log_" + freq + "_" + mcs + "_" + reading)
                                if reading.endswith('.pt4'):
                                    try:
                                        with open(readingDir) as logFile:
                                            lines = logFile.readlines()
                                        print(logFile.name)
                                    except IOError:
                                        print('Error reading file: '+readingDir)
                                    if not os.path.exists(os.path.splitext(logFile.name)[0] + ".txt"):
                                        file = open(os.path.splitext(logFile.name)[0] + ".txt", 'w')
                                        for smpl in Pt4FileReader.readAsVector(logFile.name):
                                            file.write(str(smpl[2]) + '\n')
