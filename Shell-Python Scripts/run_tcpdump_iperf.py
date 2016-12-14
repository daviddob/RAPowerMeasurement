import os
import time
import subprocess
import sys

BASE_DIR = "/home/ubwins/sarang/data"

mcs = int(sys.argv[1])
freq = sys.argv[2]
location = sys.argv[3]

if freq == '20':
	mcs_limit = [6.5, 13.0, 19.5, 26.0, 39.0, 52.0, 58.5, 65.0, 65.0]
	exp_rate = [2, 8, 15, 22, 35, 45, 53, 60]
else:
	mcs_limit = [13.5, 13.0, 19.5, 26.0, 39.0, 52.0, 58.5, 65.0, 65.0]
	exp_rate = [2, 8, 15, 22, 35, 45, 53, 60]

print mcs_limit

os.system("iw phy phy0 interface add mon0 type monitor")
os.system("ifconfig mon0 up")

for i in range(8):
    if exp_rate[i] < mcs_limit[mcs]:
        for j in range(1,6):
            wireshark_file = BASE_DIR + "/" + freq + "/" + location + "/mcs" + str(mcs) + "/" + str(exp_rate[i]) + "mbps/" + str(j) + "/wireshark.pcap"
            iperf_file = BASE_DIR + "/" + freq + "/" + location + "/mcs" + str(mcs) + "/" + str(exp_rate[i]) + "mbps/" + str(j) + "/iperf.out"
            if not os.path.exists(os.path.dirname(wireshark_file)):
                os.makedirs(os.path.dirname(wireshark_file)) 
            p1 = subprocess.Popen(["timeout","18", "tcpdump", "-i", "wlp3s0", "-n", "udp", "-w", wireshark_file])
            p2 = subprocess.Popen(["timeout", "18", "iperf", "-s", "-u"],stdout=iperf_file)
            p1.wait()
            p2.wait()
