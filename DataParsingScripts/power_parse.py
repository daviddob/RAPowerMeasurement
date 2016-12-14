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

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield mean(l[i:i + n])

FREQ_RATES = { 
	'SS' : 
		{'20MHz' : ['2mbps', '8mbps', '15mbps', '22mbps', '35mbps', '45mbps', '53mbps', '60mbps'],
		 '40MHz' : ['5mbps', '20mbps', '30mbps', '40mbps', '65mbps', '80mbps', '90mbps', '100mbps']
		},
	'DS' :
		{'20MHz' : ['4mbps', '16mbps', '30mbps', '44mbps', '70mbps', '80mbps', '90mbps', '100mbps'],
		 '40MHz' : ['10mbps', '40mbps', '60mbps', '80mbps', '130mbps', '160mbps', '180mbps', '200mbps']
		}
	}

for stream in os.listdir(BASE_IP_DIR):
	streamDir = BASE_IP_DIR + SLASH_SEPARATOR + stream
	for cpu in os.listdir(streamDir):
		cpuDir = streamDir + SLASH_SEPARATOR + cpu
		if os.path.isdir(cpuDir):
			powerDict ={}
			for freq in os.listdir(cpuDir):
				freqDir = cpuDir + SLASH_SEPARATOR + freq
				locationPowerDictionary = {}
				for location in os.listdir(freqDir):
					locationDir = freqDir + SLASH_SEPARATOR + location
					mcsValues = {}
					for mcs in os.listdir(locationDir):
						mcsDir = locationDir + SLASH_SEPARATOR + mcs
						
						if os.path.isdir(mcsDir):
							for reading in os.listdir(mcsDir):
								if reading.endswith('12345.txt'):
									print reading
									with open(mcsDir + SLASH_SEPARATOR + reading) as file:
										lines = file.readlines()
									powerList = []
									averagePowerList = []

									for line in lines:
										current = float(line.split(',')[0])
										voltage = float(line.split(',')[3])
										power = current * voltage
										powerList.append(power)

									# 50000 data points is 10 seconds worth of data
									windowSize = 50000
									averagePower = 0

									# calculate the average power of the first windowSize of power data
									for i in range(windowSize):
										averagePower += (powerList[i] / windowSize)

									maxPower = averagePower
									start = 0
									active = True
									threshold = 0
									rate = 0
									rateValues = {}
									# calculate the running average power over a sliding window
									for i in range(1, len(powerList) - windowSize):
										averagePower -= (powerList[i-1] / windowSize)
										averagePower += (powerList[i + windowSize] / windowSize)
										if active:
											if averagePower > maxPower:
												maxPower = averagePower
												start = i
											if averagePower < maxPower * 0.70:
												# end of test run, log the max power
												active = False
												averagePowerList.append(maxPower)
												
												# print "power at " + FREQ_RATES[freq][rate] + " [" + str(len(averagePowerList)) + "]: " + str(maxPower) + ", start: " + str(start/5000) + " seconds," +  " end: " + str((start+windowSize)/5000) + " seconds"
												if len(averagePowerList) % 5 == 0:
													rateValues[FREQ_RATES[stream][freq][rate]] = averagePowerList
													rate += 1
													averagePowerList = []
												# set the threshold to begin measuring for the next test run
												threshold = maxPower * 0.75
												maxPower = 0
										else:
											if averagePower > threshold:
												# begin measurements for new test run
												active = True
									mcsValues[mcs] = rateValues #list(chunks(averagePowerList, 5))
					locationPowerDictionary[location] = mcsValues
				powerDict[freq] = locationPowerDictionary
			if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream):
				os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream)
			if not os.path.exists(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu):
				os.makedirs(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu)
			with open(BASE_OP_DIR + SLASH_SEPARATOR + stream + SLASH_SEPARATOR + cpu + SLASH_SEPARATOR + "final_powerdata.json", 'w') as fp:
				json.dump(powerDict, fp)