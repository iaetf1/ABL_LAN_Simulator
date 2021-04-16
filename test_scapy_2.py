# coding: utf8
from scapy.all import *


def sniffeur(pkt):
	global LANDatalake

	if not pkt.haslayer(Raw):
		pass
	####### Gets raw data from the packet
	#pkt_list = list(str(pkt[Raw].load))
	pkt_list = pkt[Raw].load
	####### Get the index of the $ sign, and copy the datas after this sign.
	"""
	try:
		dollar_index = list(pkt_list).index("$")
	except:
		dollar_index = 0
		pkt_list = pkt_list[dollar_index:]
		packet = ''.join(pkt_list)
	"""
	return pkt_list

pkts = sniff(prn=sniffeur, filter='port 50000', iface='enp2s0')#lambda x:x.summary
#print(LANDatalake)




   
        
    
        


   
            

            
           

            

            

         

