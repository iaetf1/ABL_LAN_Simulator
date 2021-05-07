# coding: utf8
from scapy.all import *
import time
import csv
import datetime
import configparser
import threading
import queue
import ctypes
import sys

"""
def getScenario():
	config = configparser.ConfigParser()
	config.read('scenario.cfg')

	dictionary = {}
	for section in config.sections():
		dictionary[section] = {}
		for option in config.options(section):
			dictionary[section][option] = config.get(section, option)
	return dictionary
"""
#----------------------Recuperation des infos pour la config reseau
list_lanData = []
with open('lan_config.txt') as txtfile:
	data_lan = txtfile.readlines()
	for row in data_lan:
		row = row.strip()
		tempon = row.split(" ")
		list_lanData.append(tempon[1])

#----------------------Classe permettant denvoyer des trames au reseau local
class Sendtram(threading.Thread): 
	def __init__(self, scenario, bouble):
		super(Sendtram, self).__init__()
		self._stop_event = threading.Event()
		self.arret = False
		self.sortie_normal = False
		self.scenario = scenario
		self.bouble = bouble

	def run(self):
		"""
		Excecution des scenarios
		"""
		if self.bouble == 1:
			while True:
				self.sending()
				if self.arret == True:
					break
		else:
			self.sending()

	
	def stop(self):
		"""
		"""
		self.arret = True
		print("arret arret:")
		
	
	

	def sending(self):
		while self.sortie_normal == False:
			"""
			Creation des scenarios
			"""
			#Recuperation des infos trames dans un dictionnaire
			dic_trameConfig = self.get_trameConfig()
			#Instantiation dun compteur pour lindex de la trame validation mission
			index_ValM = 0
			#Instantiation dun compteur pour lindex de la trame fin mission
			index_FinM = 0
			#Instantiation dun compteur pour lindex de la trame etat ihm
			index_EIHM = 0
			#-----------------------------------------------------Constitution et envoi de trames suivant le scenario 
			if self.scenario == "Geoloc":
				#-------------------------------Traitement de la trame validation mission
				if self.arret == True:
					break
				#Recuperation de la trame validation mission
				dic_Val_Miss = dic_trameConfig.get("Val_Miss")
				#Creation de la partie statique du message
				#msg_static_valmission = dic_Val_Miss.get("debut de trame")+dic_Val_Miss.get("id source")+","+dic_Val_Miss.get("id destinataire")+","+dic_Val_Miss.get("type de trame")+","+dic_Val_Miss.get("code de trame")
				#Calcul du chksum
				chksum_valmission = '7F'
				#Creation de la partie statique du message
				msg_static_valmission = dic_Val_Miss.get("debut de trame")+dic_Val_Miss.get("id source")+","+dic_Val_Miss.get("id destinataire")+","+dic_Val_Miss.get("type de trame")+","+\
				dic_Val_Miss.get("code de trame")+","+dic_Val_Miss.get("index du message")+","+dic_Val_Miss.get("repetition du message")+","+dic_Val_Miss.get("type de trame bis")+"*"+chksum_valmission
				#Constitution du message de la tram
				msg_valmission = msg_static_valmission #+","+str(index_ValM+1)+","+dic_Val_Miss.get("repetition du message")+"*"+chksum_valmission
				#Creation et envoi de la tram
				packet_valmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_valmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_valmission /= Raw(load=msg_valmission)
				answer_valM=sr1(packet_valmission, timeout=1)
				#Mise a jour de lindex
				index_ValM +=1
				time.sleep(5)
				#------------------------------Traitement des trames de geolocalisation
				#Recuperation de la latitude et de la longitude 
				list_pos = self.getPos()
				#Recuperation de la configuration de la trame geoloc
				dic_geoloc = dic_trameConfig.get("Geoloc")
				#Creation de la partie statique du message
				msg_static_geoloc = dic_geoloc.get("debut de trame")+dic_geoloc.get("id source")+","+dic_geoloc.get("id destinataire")+","+dic_geoloc.get("type de trame")+","+dic_geoloc.get("code de trame")
				#Instantiation dun compteur pour la distance odometrique de la trame geolocalisation
				d_odo = 0
				for i in range(len(list_pos)):
					if self.arret == True:
						break
					#Recuperation de la date et de lheure a laquelle chaque trame est envoyee
					t = datetime.datetime.now()
					date = "{}/{}/{}".format(str(t.year), str(t.month), str(t.day))
					heure = "{}:{}:{}".format(str(t.hour), str(t.minute), str(t.second))
					#Recuperation du nom des gares precedente, courante et suivante
					arret_TVS = self.getTVS(i)
					#Calcul du chksum
					chksum_geoloc = '0c'
					#Constitution du message de la tram
					msg_geoloc = msg_static_geoloc+","+str(i+1)+","+dic_geoloc.get("repetition du message")+","+date+","+heure+","+list_pos[i][0]+","+list_pos[i][1]+","+dic_geoloc.get("code mission")+","+\
					arret_TVS[0]+","+arret_TVS[1]+","+arret_TVS[2]+","+str(d_odo)+","+str(10)+","+dic_geoloc.get("validite gps")+","+dic_geoloc.get("validite odo")+"*"+chksum_geoloc
					#Creation et envoi de la tram
					packet_geoloc = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
					packet_geoloc /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
					packet_geoloc /= Raw(load=msg_geoloc)
					answer_geoloc=sr1(packet_geoloc, timeout=1)
					time.sleep(5)
					#Mise a jour distance odometrique
					d_odo += 76
				#-------------------------------Traitement de la trame fin mission
				if self.arret == True:
					break
				#Recuperation de la trame fin mission
				dic_Fin_Miss = dic_trameConfig.get("Fin_Miss")
				#Creation de la partie statique du message
				#msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+dic_Fin_Miss.get("code de trame")
				#Calcul du chksum
				chksum_finmission = '1A'
				#Creation de la partie statique du message
				msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+\
				dic_Fin_Miss.get("code de trame")+","+dic_Fin_Miss.get("index du message")+","+dic_Fin_Miss.get("repetition du message")+","+dic_Fin_Miss.get("type de trame bis")+"*"+chksum_finmission
				#Constitution du message de la tram
				msg_finmission = msg_static_finmission #+","+str(index_FinM+1)+","+dic_Fin_Miss.get("repetition du message")+"*"+chksum_finmission
				#Creation et envoi de la tram
				packet_finmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_finmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_finmission /= Raw(load=msg_finmission)
				answer_FinM=sr1(packet_finmission, timeout=1)
				#Mise a jour de lindex
				index_FinM +=1
			elif self.scenario == "Retournement":
				#-------------------------------Traitement des trames de geolocalisation
				#Recuperation de la latitude et de la longitude 
				list_pos = self.getPos()
				list_pos = list_pos[282:]#six des dernieres positions gps du trajet invalides-juvisy
				#Recuperation de la configuration de la trame geoloc
				dic_geoloc = dic_trameConfig.get("Geoloc")
				#Creation de la partie statique du message
				msg_static_geoloc = dic_geoloc.get("debut de trame")+dic_geoloc.get("id source")+","+dic_geoloc.get("id destinataire")+","+dic_geoloc.get("type de trame")+","+dic_geoloc.get("code de trame")
				#Instantiation dun compteur pour la distance odometrique de la trame geolocalisation
				d_odo = 21620
				nbr_pos = 282
				for i in range(len(list_pos)):
					if self.arret == True:
						break
					#Recuperation de la date et de lheure a laquelle chaque trame est envoyee
					t = datetime.datetime.now()
					date = "{}/{}/{}".format(str(t.year), str(t.month), str(t.day))
					heure = "{}:{}:{}".format(str(t.hour), str(t.minute), str(t.second))
					#Recuperation du nom des gares precedente, courante et suivante
					arret_TVS = self.getTVS(nbr_pos)
					#Calcul du chksum
					chksum_geoloc = '0c'
					#Constitution du message de la tram
					msg_geoloc = msg_static_geoloc+","+str(i+1)+","+dic_geoloc.get("repetition du message")+","+date+","+heure+","+list_pos[i][0]+","+list_pos[i][1]+","+dic_geoloc.get("code mission")+","+\
					arret_TVS[0]+","+arret_TVS[1]+","+arret_TVS[2]+","+str(d_odo)+","+str(10)+","+dic_geoloc.get("validite gps")+","+dic_geoloc.get("validite odo")+"*"+chksum_geoloc
					#Creation et envoi de la tram
					packet_geoloc = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
					packet_geoloc /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
					packet_geoloc /= Raw(load=msg_geoloc)
					answer_geoloc=sr1(packet_geoloc, timeout=1)
					time.sleep(5)
					#Mise a jour distance odometrique
					d_odo += 76
					nbr_pos += 1

				#-------------------------------Traitement de la trame fin mission
				if self.arret == True:
					break
				#Recuperation de la trame fin mission
				dic_Fin_Miss = dic_trameConfig.get("Fin_Miss")
				#Calcul du chksum
				chksum_finmission = '1A'
				#Creation de la partie statique du message
				msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+\
				dic_Fin_Miss.get("code de trame")+","+dic_Fin_Miss.get("index du message")+","+dic_Fin_Miss.get("repetition du message")+","+dic_Fin_Miss.get("type de trame bis")+"*"+chksum_finmission
				#Creation de la partie statique du message
				#msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+dic_Fin_Miss.get("code de trame")
				#Calcul du chksum
				#chksum_finmission = '1A'
				#Constitution du message de la tram
				msg_finmission = msg_static_finmission #+","+str(index_FinM+1)+","+dic_Fin_Miss.get("repetition du message")+"*"+chksum_finmission
				#Creation et envoi de la tram
				packet_finmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_finmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_finmission /= Raw(load=msg_finmission)
				answer_FinM=sr1(packet_finmission, timeout=1)
				#Mise a jour de lindex
				index_FinM +=1
				#-------------------------------Traitement de la trame etat IHM
				if self.arret == True:
					break
				#Recuperation de la trame Etat IHM
				dic_Etat_IHM = dic_trameConfig.get("Etat_IHM")
				#Creation de la partie statique du message
				msg_static_EIHM = dic_Etat_IHM.get("debut de trame")+dic_Etat_IHM.get("id source")+","+dic_Etat_IHM.get("id destinataire")+","+dic_Etat_IHM.get("type de trame")+","+dic_Etat_IHM.get("code de trame")
				#Calcul du chksum
				chksum_EIHM = '2B'
				#------------Constitution du premier message de la tram IHM 
				if self.arret == True:
					break
				qblt = "1"
				zcofp = "0"
				zop = "1"
				msg_EIHM_A = msg_static_EIHM+","+str(index_EIHM+1)+","+dic_Etat_IHM.get("repetition du message")+","+dic_Etat_IHM.get("version")+","+dic_Etat_IHM.get("r")+","+\
				dic_Etat_IHM.get("do1")+","+dic_Etat_IHM.get("do2")+","+dic_Etat_IHM.get("ga1")+","+dic_Etat_IHM.get("ga2")+","+dic_Etat_IHM.get("aiadc")+","+qblt+","+\
				dic_Etat_IHM.get("qev")+","+dic_Etat_IHM.get("qum")+","+zcofp+","+zop+","+dic_Etat_IHM.get("zcvs")+","+dic_Etat_IHM.get("etat")+","+dic_Etat_IHM.get("i2c")+","+\
				dic_Etat_IHM.get("gir")+","+dic_Etat_IHM.get("qbl")+","+dic_Etat_IHM.get("etat modem")+","+dic_Etat_IHM.get("rearmement")+","+dic_Etat_IHM.get("acquittement rearmement zb")+","+\
				dic_Etat_IHM.get("acquittement rearmement zr")+"*"+chksum_EIHM
				#------------Creation et envoi de la tram 1 IHM
				packet_EIHM_A = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_EIHM_A /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_EIHM_A /= Raw(load=msg_EIHM_A)
				answer_EIHM_A = sr1(packet_EIHM_A, timeout=1)
				#Mise a jour de lindex
				index_EIHM +=1
				time.sleep(15)
				#-----------Traitement de la trame Ferture Porte
				if self.arret == True:
					break
				#Recuperation de la trame Etat IHM
				dic_CFP = dic_trameConfig.get("Cfp")
				#Calcul du chksum
				chksum_cfp = '1b'
				#Creation de la partie statique du message
				msg_static_CFP = dic_CFP.get("debut de trame")+dic_CFP.get("id source")+","+dic_CFP.get("id destinataire")+","+dic_CFP.get("type de trame")+","+\
				dic_CFP.get("code de trame")+","+dic_CFP.get("index du message")+","+dic_CFP.get("repetition du message")+","+dic_CFP.get("type de trame bis")+"*"+chksum_cfp				
				#-----------Constitution du second message de la tram IHM
				msg_CFP = msg_static_CFP
				#-----------Creation et envoi de la tram 2 IHM
				packet_CFP = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_CFP /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_CFP /= Raw(load=msg_CFP)
				packet_CFP = sr1(packet_CFP, timeout=1)
				"""
				qblt = "1"
				zcofp = "1"
				zop = "0"
				msg_EIHM_B = msg_static_EIHM+","+str(index_EIHM+1)+","+dic_Etat_IHM.get("repetition du message")+","+dic_Etat_IHM.get("version")+","+dic_Etat_IHM.get("r")+","+\
				dic_Etat_IHM.get("do1")+","+dic_Etat_IHM.get("do2")+","+dic_Etat_IHM.get("ga1")+","+dic_Etat_IHM.get("ga2")+","+dic_Etat_IHM.get("aiadc")+","+qblt+","+\
				dic_Etat_IHM.get("qev")+","+dic_Etat_IHM.get("qum")+","+zcofp+","+zop+","+dic_Etat_IHM.get("zcvs")+","+dic_Etat_IHM.get("etat")+","+dic_Etat_IHM.get("i2c")+","+\
				dic_Etat_IHM.get("gir")+","+dic_Etat_IHM.get("qbl")+","+dic_Etat_IHM.get("etat modem")+","+dic_Etat_IHM.get("rearmement")+","+dic_Etat_IHM.get("acquittement rearmement zb")+","+\
				dic_Etat_IHM.get("acquittement rearmement zr")+"*"+chksum_EIHM
				#-----------Creation et envoi de la tram 2 IHM
				packet_EIHM_B = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_EIHM_B /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_EIHM_B /= Raw(load=msg_EIHM_B)
				answer_EIHM_B = sr1(packet_EIHM_B, timeout=1)
				#Mise a jour de lindex
				index_EIHM +=1
				"""
				time.sleep(5)
				#------------Constitution du troisieme message de la tram IHM
				if self.arret == True:
					break
				qblt = "0"
				zcofp = "0"
				zop = "0"
				msg_EIHM_C = msg_static_EIHM+","+str(index_EIHM+1)+","+dic_Etat_IHM.get("repetition du message")+","+dic_Etat_IHM.get("version")+","+dic_Etat_IHM.get("r")+","+\
				dic_Etat_IHM.get("do1")+","+dic_Etat_IHM.get("do2")+","+dic_Etat_IHM.get("ga1")+","+dic_Etat_IHM.get("ga2")+","+dic_Etat_IHM.get("aiadc")+","+qblt+","+\
				dic_Etat_IHM.get("qev")+","+dic_Etat_IHM.get("qum")+","+zcofp+","+zop+","+dic_Etat_IHM.get("zcvs")+","+dic_Etat_IHM.get("etat")+","+dic_Etat_IHM.get("i2c")+","+\
				dic_Etat_IHM.get("gir")+","+dic_Etat_IHM.get("qbl")+","+dic_Etat_IHM.get("etat modem")+","+dic_Etat_IHM.get("rearmement")+","+dic_Etat_IHM.get("acquittement rearmement zb")+","+\
				dic_Etat_IHM.get("acquittement rearmement zr")+"*"+chksum_EIHM
				#-------------Creation et envoi de la tram 3 IHM
				packet_EIHM_C = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_EIHM_C /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_EIHM_C /= Raw(load=msg_EIHM_C)
				answer_EIHM_C = sr1(packet_EIHM_C, timeout=1)
				#Mise a jour de lindex
				index_EIHM +=1
				time.sleep(5)
				#Constitution du quatrieme message de la tram IHM
				if self.arret == True:
					break
				qblt = "1"
				zcofp = "0"
				zop = "0"
				msg_EIHM_D = msg_static_EIHM+","+str(index_EIHM+1)+","+dic_Etat_IHM.get("repetition du message")+","+dic_Etat_IHM.get("version")+","+dic_Etat_IHM.get("r")+","+\
				dic_Etat_IHM.get("do1")+","+dic_Etat_IHM.get("do2")+","+dic_Etat_IHM.get("ga1")+","+dic_Etat_IHM.get("ga2")+","+dic_Etat_IHM.get("aiadc")+","+qblt+","+\
				dic_Etat_IHM.get("qev")+","+dic_Etat_IHM.get("qum")+","+zcofp+","+zop+","+dic_Etat_IHM.get("zcvs")+","+dic_Etat_IHM.get("etat")+","+dic_Etat_IHM.get("i2c")+","+\
				dic_Etat_IHM.get("gir")+","+dic_Etat_IHM.get("qbl")+","+dic_Etat_IHM.get("etat modem")+","+dic_Etat_IHM.get("rearmement")+","+dic_Etat_IHM.get("acquittement rearmement zb")+","+\
				dic_Etat_IHM.get("acquittement rearmement zr")+"*"+chksum_EIHM
				#Creation et envoi de la tram 4 IHM
				packet_EIHM_D = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_EIHM_D /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_EIHM_D /= Raw(load=msg_EIHM_D)
				answer_EIHM_D = sr1(packet_EIHM_D, timeout=1)
				#Mise a jour de lindex
				index_EIHM +=1
				time.sleep(5)
				#-------------------------------Traitement de la trame validation mission
				if self.arret == True:
					break
				#Recuperation de la trame validation mission
				dic_Val_Miss = dic_trameConfig.get("Val_Miss")
				#Calcul du chksum
				chksum_valmission = '7F'
				#Creation de la partie statique du message
				msg_static_valmission = dic_Val_Miss.get("debut de trame")+dic_Val_Miss.get("id source")+","+dic_Val_Miss.get("id destinataire")+","+dic_Val_Miss.get("type de trame")+","+\
				dic_Val_Miss.get("code de trame")+","+dic_Val_Miss.get("index du message")+","+dic_Val_Miss.get("repetition du message")+","+dic_Val_Miss.get("type de trame bis")+"*"+chksum_valmission
				#Constitution du message de la tram
				msg_valmission = msg_static_valmission #+","+str(index_ValM+1)+","+dic_Val_Miss.get("repetition du message")+"*"+chksum_valmission
				#Creation et envoi de la tram
				packet_valmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_valmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_valmission /= Raw(load=msg_valmission)
				answer_valM=sr1(packet_valmission, timeout=1)
				#Mise a jour de lindex
				index_ValM +=1
				time.sleep(5)
			elif self.scenario == "fin_mission":
				#-------------------------------Traitement de la trame fin mission
				#Recuperation de la trame fin mission
				dic_Fin_Miss = dic_trameConfig.get("Fin_Miss")
				#Calcul du chksum
				chksum_finmission = '1A'
				#Creation de la partie statique du message
				msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+\
				dic_Fin_Miss.get("code de trame")+","+dic_Fin_Miss.get("index du message")+","+dic_Fin_Miss.get("repetition du message")+","+dic_Fin_Miss.get("type de trame bis")+"*"+chksum_finmission
				#msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+dic_Fin_Miss.get("code de trame")
				
				#Constitution du message de la tram
				msg_finmission = msg_static_finmission #+","+str(index_FinM+1)+","+dic_Fin_Miss.get("repetition du message")+"*"+chksum_finmission
				#Creation et envoi de la tram
				packet_finmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_finmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_finmission /= Raw(load=msg_finmission)
				answer_FinM=sr1(packet_finmission, timeout=1)
				#Mise a jour de lindex
				index_FinM +=1
				if self.arret == True:
					break
			elif self.scenario == "fm_fp":
				#-------------------------------Traitement de la trame fin mission
				#Recuperation de la trame fin mission
				dic_Fin_Miss = dic_trameConfig.get("Fin_Miss")
				#Creation de la partie statique du message
				#msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+dic_Fin_Miss.get("code de trame")
				#Calcul du chksum
				chksum_finmission = '1A'
				#Creation de la partie statique du message
				msg_static_finmission = dic_Fin_Miss.get("debut de trame")+dic_Fin_Miss.get("id source")+","+dic_Fin_Miss.get("id destinataire")+","+dic_Fin_Miss.get("type de trame")+","+\
				dic_Fin_Miss.get("code de trame")+","+dic_Fin_Miss.get("index du message")+","+dic_Fin_Miss.get("repetition du message")+","+dic_Fin_Miss.get("type de trame bis")+"*"+chksum_finmission
				#Constitution du message de la tram
				msg_finmission = msg_static_finmission #+","+str(index_FinM+1)+","+dic_Fin_Miss.get("repetition du message")+"*"+chksum_finmission
				#Creation et envoi de la tram
				packet_finmission = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_finmission /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_finmission /= Raw(load=msg_finmission)
				answer_FinM=sr1(packet_finmission, timeout=1)
				#Mise a jour de lindex
				index_FinM +=1
				time.sleep(5)
				#if self.arret == True:
				#	break
				#-------------------------------Traitement de la trame Ferture Porte
				#Recuperation de la trame Etat IHM
				dic_CFP = dic_trameConfig.get("Cfp")
				#Calcul du chksum
				chksum_cfp = '1b'
				#Creation de la partie statique du message
				msg_static_CFP = dic_CFP.get("debut de trame")+dic_CFP.get("id source")+","+dic_CFP.get("id destinataire")+","+dic_CFP.get("type de trame")+","+\
				dic_CFP.get("code de trame")+","+dic_CFP.get("index du message")+","+dic_CFP.get("repetition du message")+","+dic_CFP.get("type de trame bis")+"*"+chksum_cfp				
				#-----------Constitution du second message de la tram IHM
				msg_CFP = msg_static_CFP
				#-----------Creation et envoi de la tram 2 IHM
				packet_CFP = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_CFP /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_CFP /= Raw(load=msg_CFP)
				packet_CFP = sr1(packet_CFP, timeout=1)
				#-------------------------------Traitement de la trame etat IHM
				"""
				#Recuperation de la trame Etat IHM
				dic_Etat_IHM = dic_trameConfig.get("Etat_IHM")
				#Creation de la partie statique du message
				msg_static_EIHM = dic_Etat_IHM.get("debut de trame")+dic_Etat_IHM.get("id source")+","+dic_Etat_IHM.get("id destinataire")+","+dic_Etat_IHM.get("type de trame")+","+dic_Etat_IHM.get("code de trame")
				#Calcul du chksum
				chksum_EIHM = '2B'
				#-----------Constitution du second message de la tram IHM
				qblt = "1"
				zcofp = "1"
				zop = "0"
				msg_EIHM_B = msg_static_EIHM+","+str(index_EIHM+1)+","+dic_Etat_IHM.get("repetition du message")+","+dic_Etat_IHM.get("version")+","+dic_Etat_IHM.get("r")+","+\
				dic_Etat_IHM.get("do1")+","+dic_Etat_IHM.get("do2")+","+dic_Etat_IHM.get("ga1")+","+dic_Etat_IHM.get("ga2")+","+dic_Etat_IHM.get("aiadc")+","+qblt+","+\
				dic_Etat_IHM.get("qev")+","+dic_Etat_IHM.get("qum")+","+zcofp+","+zop+","+dic_Etat_IHM.get("zcvs")+","+dic_Etat_IHM.get("etat")+","+dic_Etat_IHM.get("i2c")+","+\
				dic_Etat_IHM.get("gir")+","+dic_Etat_IHM.get("qbl")+","+dic_Etat_IHM.get("etat modem")+","+dic_Etat_IHM.get("rearmement")+","+dic_Etat_IHM.get("acquittement rearmement zb")+","+\
				dic_Etat_IHM.get("acquittement rearmement zr")+"*"+chksum_EIHM
				#-----------Creation et envoi de la tram 2 IHM
				packet_EIHM_B = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_EIHM_B /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_EIHM_B /= Raw(load=msg_EIHM_B)
				answer_EIHM_B = sr1(packet_EIHM_B, timeout=1)
				#Mise a jour de lindex
				index_EIHM +=1
				"""
				if self.arret == True:
					break
			elif self.scenario == "dg_fp":
				#-------------------------------Traitement des trames de geolocalisation
				#Recuperation de la latitude et de la longitude 
				list_pos = self.getPos()
				list_pos = list_pos[-1]#dernieres positions gps du trajet invalides-juvisy
				print(list_pos)
				#Recuperation de la configuration de la trame geoloc
				dic_geoloc = dic_trameConfig.get("Geoloc")
				#Creation de la partie statique du message
				msg_static_geoloc = dic_geoloc.get("debut de trame")+dic_geoloc.get("id source")+","+dic_geoloc.get("id destinataire")+","+dic_geoloc.get("type de trame")+","+dic_geoloc.get("code de trame")
				#Instantiation dun compteur pour la distance odometrique de la trame geolocalisation
				d_odo = 22000
				#Recuperation de la date et de lheure a laquelle chaque trame est envoyee
				t = datetime.datetime.now()
				date = "{}/{}/{}".format(str(t.year), str(t.month), str(t.day))
				heure = "{}:{}:{}".format(str(t.hour), str(t.minute), str(t.second))
				#Recuperation du nom des gares precedente, courante et suivante
				arret_TVS = self.getTVS(287)
				#Calcul du chksum
				chksum_geoloc = '0c'
				#Constitution du message de la tram
				msg_geoloc = msg_static_geoloc+","+str(1)+","+dic_geoloc.get("repetition du message")+","+date+","+heure+","+list_pos[0]+","+list_pos[1]+","+dic_geoloc.get("code mission")+","+\
				arret_TVS[0]+","+arret_TVS[1]+","+arret_TVS[2]+","+str(d_odo)+","+str(10)+","+dic_geoloc.get("validite gps")+","+dic_geoloc.get("validite odo")+"*"+chksum_geoloc
				#Creation et envoi de la tram
				packet_geoloc = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_geoloc /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_geoloc /= Raw(load=msg_geoloc)
				answer_geoloc=sr1(packet_geoloc, timeout=1)
				time.sleep(5)
		
				#-------------------------------Traitement de la trame Ferture Porte
				#Recuperation de la trame Etat IHM
				dic_CFP = dic_trameConfig.get("Cfp")
				#Calcul du chksum
				chksum_cfp = '1b'
				#Creation de la partie statique du message
				msg_static_CFP = dic_CFP.get("debut de trame")+dic_CFP.get("id source")+","+dic_CFP.get("id destinataire")+","+dic_CFP.get("type de trame")+","+\
				dic_CFP.get("code de trame")+","+dic_CFP.get("index du message")+","+dic_CFP.get("repetition du message")+","+dic_CFP.get("type de trame bis")+"*"+chksum_cfp				
				#-----------Constitution du second message de la tram IHM
				msg_CFP = msg_static_CFP
				#-----------Creation et envoi de la tram 2 IHM
				packet_CFP = IP(dst=str(list_lanData[0]),src=str(list_lanData[1]))
				packet_CFP /= UDP(sport=int(list_lanData[2]), dport=int(list_lanData[3]))
				packet_CFP /= Raw(load=msg_CFP)
				packet_CFP = sr1(packet_CFP, timeout=1)
			#Arret de la boucle while 
			self.sortie_normal = True
			
			

			




	def get_trameConfig(self):
		"""
		Recuperation des scenarios depuis le fichier cfg
		"""
		config = configparser.ConfigParser()
		config.read('trames.cfg')

		dictionary = {}
		for section in config.sections():
			dictionary[section] = {}
			for option in config.options(section):
				dictionary[section][option] = config.get(section, option)
		return dictionary

	def getPos(self):
		"""
		Recuperation de la latitude et de la longitude
		"""
		list_pos = []
		with open('route_points_wth_virg_as_sep.csv') as csvfile:
			data_pos = csv.reader(csvfile)#, delimiter=',')#, quotechar='|')
			data_pos = list(data_pos)
			for pos in data_pos:
				list_pos.append(pos)
		return list_pos

	def getTVS(self, numTram):
		"""
		Connaitre le TVS de la gare P, C, S en fonction de la position du train
		"""
		#------Recuperation des trigrammes des arrets
		dic_TVS = {} 
		dic_numTram = {}
		with open('trigramme.txt') as txtfile:
			data_TVS = txtfile.readlines()
			for row in data_TVS:
				row = row.strip()
				tempon = row.split(",")
				dic_TVS[tempon[0]] = tempon[1]
				dic_numTram[tempon[0]] = tempon[2]
		list_TVS = list(dic_TVS.values())
		list_numTram = list(dic_numTram.values())
		#----------------Identification des TVS des gares P,C,S
		if numTram >= int(list_numTram[0]) and numTram < int(list_numTram[1]):
			gare_name = ("",list_TVS[0],list_TVS[1])
		elif numTram >= int(list_numTram[1]) and numTram < int(list_numTram[2]):
			gare_name = (list_TVS[0],list_TVS[1],list_TVS[2])
		elif numTram >= int(list_numTram[2]) and numTram < int(list_numTram[3]):
			gare_name = (list_TVS[1],list_TVS[2],list_TVS[3])
		elif numTram >= int(list_numTram[3]) and numTram < int(list_numTram[4]):
			gare_name = (list_TVS[2],list_TVS[3],list_TVS[4])
		elif numTram >= int(list_numTram[4]) and numTram < int(list_numTram[5]):
			gare_name = (list_TVS[3],list_TVS[4],list_TVS[5])
		elif numTram == int(list_numTram[5]):
			gare_name = (list_TVS[4],list_TVS[5],"")	
		return gare_name


#----------------------Classe permettant de sniffer le reseau local
class Sniffer(threading.Thread):
	def  __init__(self, q, portE, udpF, tcpF, interface=str(list_lanData[4])):#, portE
		super().__init__()
		self.q = q
		self.portE = portE
		self.interface = interface
		self.udpF = udpF
		self.tcpF = tcpF

	def run(self):
		if self.udpF == 0 and self.tcpF == 0:
			sniff(iface=self.interface, filter="port "+self.portE, prn=self.sniff_method) 
		elif self.udpF == 1 and self.tcpF == 0:
			sniff(iface=self.interface, filter="port "+self.portE+" and udp", prn=self.sniff_method)
		elif self.udpF == 0 and self.tcpF == 1:
			sniff(iface=self.interface, filter="port "+self.portE+" and tcp", prn=self.sniff_method)
		elif self.udpF == 1 and self.tcpF == 1:
			sniff(iface=self.interface, filter="port "+self.portE+" and udp and tcp", prn=self.sniff_method)



	def sniff_method(self, pkt):
		LANDatalake = {}
		if not pkt.haslayer(Raw):
			pass
		####### Gets raw data from the packet
		pkt_list = list(str(pkt[Raw].load))
		#pkt_list = pkt[Raw].load
		####### Get the index of the $ sign, and copy the datas after this sign.
		dollar_index = list(pkt_list).index("$")
		pkt_list = pkt_list[dollar_index:]
		packet = ''.join(pkt_list)
		####### Gets the emitter and the type of the frame. As specified by the Z2N LAN designer
		####### emitter field is at the index 0, and the type field is at the index 4
		packet = packet.split(",")
		emitter = packet[0].replace("$", "")
		if emitter == "WDB":
			typ_split = packet[6].split("*")
			typ = typ_split[0]
		else: 
			typ = packet[3]
		####### Checks if the the frame is of type "Geoloc UGS"		
		if emitter == "UGS" and typ == "GEOLOC":
			LANDatalake["type"] = packet[3]
			LANDatalake["date"] = packet[6]
			LANDatalake["heure"] = packet[7]
			LANDatalake["latitude"] = packet[8]
			LANDatalake["longitude"] = packet[9]
			LANDatalake["code_mission"] = packet[10]
			LANDatalake["gare_precedente"] = packet[11]
			LANDatalake["gare_courante"] = packet[12]
			LANDatalake["gare_suivante"] = packet[13]
			LANDatalake["distance_odo"] = packet[14]
		####### Checks if the the frame is of type "VAL_MISS"
		elif emitter == "WDB" and typ == "VAL_MISS":
			LANDatalake["id_src"] = packet[0].replace("$", "")
			LANDatalake["id_dst"] = packet[1]
			LANDatalake["type"] = packet[2]
			LANDatalake["code_trame"] = packet[3]
			LANDatalake["type_trame"] = typ
		####### Checks if the the frame is of type "FIN_MISS"
		elif emitter == "WDB" and typ == "FIN_MISS":
			LANDatalake["id_src"] = packet[0].replace("$", "")
			LANDatalake["id_dst"] = packet[1]
			LANDatalake["type"] = packet[2]
			LANDatalake["code_trame"] = packet[3]
			LANDatalake["type_trame"] = typ
		####### Checks if the the frame is of type "FIN_MISS"
		elif emitter == "WDB" and typ == "CFP":
			LANDatalake["id_src"] = packet[0].replace("$", "")
			LANDatalake["id_dst"] = packet[1]
			LANDatalake["type"] = packet[2]
			LANDatalake["code_trame"] = packet[3]
			LANDatalake["type_trame"] = typ
		####### Checks if the the frame is of type "VIE"
		elif emitter == "IHM" and typ == "VIE":
			LANDatalake["id_src"] = packet[0].replace("$", "")
			LANDatalake["id_dst"] = packet[1]
			LANDatalake["type"] = packet[3]
			LANDatalake["code_trame"] = packet[4]
			LANDatalake["qblt"] = packet[13]
			LANDatalake["zcofp"] = packet[16]
			LANDatalake["zop"] = packet[17]
				
				
			
			
		self.q.put(LANDatalake)











