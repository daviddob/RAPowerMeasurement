import os

# A Simple utility for renaming the monitor pcap files after dumping the tar files
# since chosing rename in winrar will add (1) to the filename rather than _mon which
# is preferable.

for root, dirs, files in os.walk("D:/Readings"):
	for file in files:
		if file.endswith("(1).pcap"):
			path = os.path.join(root, file)
			os.rename(path, path.replace("(1)", "_mon"))