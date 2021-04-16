# coding: utf8
from scapy.all import *
import time

packet = IP(dst='192.168.0.255',src='192.168.0.200')
packet /= UDP(sport=45290, dport=50000)
msg = '$UGS,BROA,E,,GEOLOC'
packet /= Raw(load=msg)

#bind_layers(IP, UDP, sport=45290)
#bind_layers(IP, UDP, dport=50000)

while True:
	time.sleep(1)
	answer=sr1(packet, timeout=1)
	#answer.show()
	#packet.show()


#$UGS,BROA,E,GEOLOC,40,1,2021/03/10,08:24:19,,,ROPE,,GDS,CLX,,1615364659,0,0*0C
