import os
import sys
from sys import platform as _platform
import json

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

def mean(numbers):
	return float(sum(numbers)) / max(len(numbers), 1)

for stream in os.listdir(BASE_IP_DIR):
	streamDir = BASE_IP_DIR + SLASH_SEPARATOR + stream
	for cpu in os.listdir(streamDir):
		cpuDir = streamDir + SLASH_SEPARATOR + cpu
		if os.path.isdir(cpuDir):
			resultDict = {}

			for freq in os.listdir(cpuDir):
				freqDir = cpuDir + SLASH_SEPARATOR + freq
				freqDict = {}
				for location in os.listdir(freqDir):
					locationDir = freqDir + SLASH_SEPARATOR + location
					locationDict = {}
					for mcs in os.listdir(locationDir):
						mcsDir = locationDir + SLASH_SEPARATOR + mcs
						mcsDict = {}
						if os.path.isdir(mcsDir):
							for rate in os.listdir(mcsDir):
								rateDir = mcsDir + SLASH_SEPARATOR + rate
								
								if os.path.isdir(rateDir):
									rateDict = []
									for test in os.listdir(rateDir):
										testDir = rateDir + SLASH_SEPARATOR + test
										for log in os.listdir(testDir):
											if log.startswith(freq) and stream != 'DS':
												powerList = []
												averagePowerList = []
												print testDir + SLASH_SEPARATOR + log
												with open(testDir + SLASH_SEPARATOR + log) as file:
													lines = file.readlines()

												for line in lines[0::2]:
													cpuFreq = int(line.split(' ')[2])
													cpuUtil0 = float(line.split(' ')[3])
													cpuUtil1 = float(line.split(' ')[4])
													cpuUtil2 = float(line.split(' ')[5])
													cpuUtil3 = float(line.split(' ')[6])
													numCoreActive = ((0 if cpuUtil0 == 0 else 1) + (0 if cpuUtil1 == 0 else 1) + (0 if cpuUtil2 == 0 else 1) + (0 if cpuUtil3 == 0 else 1))
													if numCoreActive <= 0:
														numCoreActive = 1
													power = PBASE[cpuFreq][numCoreActive-1] + (PDELTA[cpuFreq][0] * cpuUtil0)/100 + (PDELTA[cpuFreq][1] * cpuUtil1)/100 + (PDELTA[cpuFreq][2] * cpuUtil2)/100 + (PDELTA[cpuFreq][3] * cpuUtil3)/100
													powerList.append(power)

												# 100 data points is 10 seconds worth of data
												windowSize = 100
												averagePower = 0

												# calculate the average power of the first windowSize of power data
												for i in range(windowSize):
													averagePower += (powerList[i] / windowSize)
													averagePowerList.append(averagePower)

													maxPower = averagePower
													start = 0
													active = True
													threshold = 0
												# calculate the running average power over a sliding window
												for i in range(1, len(powerList) - windowSize):
													averagePower -= (powerList[i-1] / windowSize)
													averagePower += (powerList[i + windowSize] / windowSize)
													# print averagePower
													averagePowerList.append(averagePower)
													# print str(max(averagePowerList)) + " " + str(len(averagePowerList)) + " " + str([i for i, j in enumerate(averagePowerList) if j == max(averagePowerList)])
												rateDict.append(max(averagePowerList))
									if rateDict == []:
										rateDict = [0, 0, 0, 0, 0]
									mcsDict[rate] = rateDict
							locationDict[mcs] = mcsDict
					freqDict[location] = locationDict
				resultDict[freq] = freqDict
			if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream):
				os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream)
			if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu):
				os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu)
			with open(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu + SLASH_SEPARATOR +  "final_cpudata.json", 'w') as fp:
				json.dump(resultDict, fp)


