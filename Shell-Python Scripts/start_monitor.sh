#! /bin/bash

iw phy phy0 interface add mon0 type monitor
ifconfig mon0 up
iw dev mon0 set freq 5180
