import os
import time

TIMEOUT = 18
mcs = 3
freq = "40Mhz"
location = "Location3"

BASE_DIR = "/home/ub/sarang/data"

if freq == '20Mhz':
	mcs_limit = [6.5, 13.0, 19.5, 26.0, 39.0, 52.0, 58.5, 65.0, 65.0]
	exp_rate = [2, 8, 15, 22, 35, 45, 53, 60]
else:
	mcs_limit = [13.5, 27.0, 40.5, 54.0, 81.0, 108.0, 121.5, 135.0, 135.0]
	exp_rate = [7, 16, 30, 44, 70, 90, 110, 125]


os.system("iw phy phy0 interface add mon0 type monitor")
os.system("ifconfig mon0 up")

for i in range(8):
    if exp_rate[i] < mcs_limit[mcs]:
        for j in range(1,6):
            wireshark_file = BASE_DIR + "/" + freq + "/" + location + "/mcs" + str(mcs) + "/" + str(exp_rate[i]) + "mbps/" + str(j) + "/wireshark.pcap"
            if not os.path.exists(os.path.dirname(wireshark_file)):
                os.makedirs(os.path.dirname(wireshark_file)) 
            os.system('timeout 18 tcpdump -i mon0 -n udp -w' + wireshark_file)
