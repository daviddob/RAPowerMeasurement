import os
import dpkt
import binascii
import json
from sys import platform as _platform

# dpkt only works with python 2.7 and hence use 2.7 for this script

####################################PLEASE EDIT ACCORDING TO YOUR DIRECTORY STRUCTURE##############################
if _platform == "linux" or _platform == "linux2":
    BASE_IP_DIR = "/media/tejash/Tejash/MSCS/CSEIndependentStudy/PowerMeasurementStudy/Readings"
    BASE_OP_DIR = "/media/tejash/Media/CSEIndependentStudy/Results"
    SLASH_SEPARATOR = "/"
elif _platform == "win32" or _platform == 'win64':
    BASE_IP_DIR = "F:\CSE630\Readings\DS\FixedCPU"
    BASE_OP_DIR = "F:\CSE630\Results"
    SLASH_SEPARATOR = "\/"
####################################################################################################################

resultDict = {}

for freq in os.listdir(BASE_IP_DIR):
    freqDir = BASE_IP_DIR + SLASH_SEPARATOR + freq
    #freqDir = BASE_IP_DIR + SLASH_SEPARATOR + "40MHz"
    locationDict = {}
    for location in os.listdir(freqDir):
        rateDict = {}
        locationDir = freqDir + SLASH_SEPARATOR + location + SLASH_SEPARATOR + 'mcsra'
        #locationDir = freqDir + SLASH_SEPARATOR + "Location7" + SLASH_SEPARATOR + 'mcsra'
        for reading in os.listdir(locationDir):
            readingList = [0, 0, 0, 0, 0, 0, 0, 0]
            print (reading)
            readingDir = locationDir + SLASH_SEPARATOR + reading
            if os.path.isdir(readingDir):
                for test in os.listdir(readingDir):
                    testDir = readingDir + SLASH_SEPARATOR + test
                    wiresharkFile = testDir + SLASH_SEPARATOR + "wireshark.pcap"
                    f = open(wiresharkFile,'rb')
                    print (wiresharkFile)
                    pcap = dpkt.pcap.Reader(f)
                    dl=pcap.datalink()
                    if pcap.datalink() == 127:  # Check if RadioTap
                        for timestamp, rawdata in pcap:
                            tap = dpkt.radiotap.Radiotap(rawdata)
                            mcs=binascii.hexlify(rawdata[28:29])
                            mcs=int(mcs,16)
                            if(mcs <= 7):
                                #print mcs
                                readingList[mcs] += 1
                rateDict[reading] = [i/5 for i in readingList]
        locationDict[location] = rateDict
        
    resultDict[freq] = locationDict
print (resultDict)
with open(BASE_OP_DIR + SLASH_SEPARATOR + 'ra_mcs.json', 'w') as fpJson:
    json.dump(resultDict, fpJson)