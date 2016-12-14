#!/bin/sh

mcs0=0x1
mcs1=0x2
mcs2=0x4
mcs3=0x8
mcs4=0x10
mcs5=0x20
mcs6=0x40
mcs7=0x80
mcsra=0xFF
file1=~/compat-wireless-3.6.2-1-snpc/drivers/net/wireless/ath/ath9k/init.c
file2=~/compat-wireless-3.6.2-1-snpc/drivers/net/wireless/ath/ath9k/htc_drv_init.c

mcs=$(eval "echo \$$1")

sed -i "301s/.*/ht_info->mcs.rx_mask[0]=$mcs;/" "$file1"
sed -i "528s/.*/ht_info->mcs.rx_mask[0]=$mcs;/" "$file2"

cd ~/compat-wireless-3.6.2-1-snpc
make unload
make clean
make
make install
modprobe ath9k

cd ~/sarang
iw reg set US
killall hostapd 
sleep 5 
hostapd -B hostapd_`echo $2`Mhz.conf
ifconfig wlan3 10.0.0.10
