@echo off
echo %1
echo %~d1%~p1wireshark_corrupt.pcap
MOVE %1 %~d1%~p1temp.pcap
F:\CSE630\pcapfix-1.1.0-win32\pcapfix.exe %~d1%~p1temp.pcap -o %~d1%~p1wireshark.pcap
if errorlevel 1 (
   MOVE %~d1%~p1temp.pcap %~d1%~p1wireshark_corrupt.pcap
) else (
   echo "File all good"
   MOVE %~d1%~p1temp.pcap %~d1%~p1wireshark.pcap
)