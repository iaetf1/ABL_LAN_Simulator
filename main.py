import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import font
import random
import configparser
import os
import subprocess
from tkinter import ttk 
from collections import OrderedDict
from test_scapy import  Sendtram, Sniffer #sendTram, getScenario,
import threading
import queue
import datetime
import time


def getScenarios(fichier):
	"""
	Chargement des scenarios a simuler
	"""
	list_scenarios = []
	with open(fichier) as txtfile:
		scenarios_d = txtfile.readlines()
		for row in scenarios_d:
			row = row.strip()
			tempon = row.split(" ")
			list_scenarios.append(tempon[0])
	return list_scenarios


def getOption(event, id_s):
	"""
	Recupere le scenario qui a ete selectionne
	"""
	global opt
	global opt_0
	global opt_1
	global opt_2
	global opt_3

	#s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))

	if id_s == 0:
		s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))
		opt = s_name.get()
	elif id_s == 1:
		s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))
		opt = s_name.get()
	elif id_s == 2:
		s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))
		opt = s_name.get()
	elif id_s == 3:
		s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))
		opt = s_name.get()

	#print(opt,"boutton:",id_s, type(opt))
	

def getDeclencheur(event, id_dcl):
	"""
	"""
	dcl_name = label_simulation.nametowidget('declencheur{}_cbbx'.format(str(id_dcl+1)))	
	opt = dcl_name.get()
	print(opt,"boutton:",id_dcl)

def boucle_t():
	while True:
		print("Boucle")

class Affichage(threading.Thread):
	def  __init__(self, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP):
		#super().__init__()
		super(Affichage, self).__init__()
		self.opt = opt
		#self.opt_FM = True
		self.q = q
		self.treeGeoloc = treeGeoloc
		self.treeValM = treeValM
		self.treeFinM = treeFinM
		self.treeIHM = treeIHM
		self.treeCFP = treeCFP
		self.arret = False
		self.FMStop = False
		self.FPStop = False
		self.DGStop = False

	def run(self):
		"""
		"""
		if self.opt == "Geoloc":
			self.affichage_geoloc()
		elif self.opt == "Retournement":
			self.affichage_retournement()
		elif self.opt == "FM":
			print("passage")
			self.affichage_FM()
		elif self.opt == "FMFP":
			self.affichage_FMFP()
		elif self.opt == "DGFP":
			self.affichage_DGFP()


	def affichage_geoloc(self):
		"""
		"""
		while self.arret == False:
			tree_value = self.q.get().values()
			tree_value = list(tree_value)
			tree_value = tuple(tree_value)
			now = datetime.datetime.now()
			current_date = now.strftime("%d-%m-%Y %H:%M:%S")
			tree_value = (current_date,) + tree_value
			#print(tree_value)
			if 'GEOLOC' in tree_value:
				print(tree_value)
				self.treeGeoloc.insert('', index='end', values=tree_value)
				self.treeGeoloc.update()
			elif 'VAL_MISS' in tree_value:
				print(tree_value)
				self.treeValM.insert('', index='end', values=tree_value)
				self.treeValM.update()
			elif 'FIN_MISS' in tree_value:
				print(tree_value)
				self.treeFinM.insert('', index='end', values=tree_value)
				self.treeFinM.update()

	def affichage_retournement(self):
		"""
		"""
		while self.arret == False:
			print("aff Retournement")
			tree_value = self.q.get().values()
			tree_value = list(tree_value)
			tree_value = tuple(tree_value)
			now = datetime.datetime.now()
			current_date = now.strftime("%d-%m-%Y %H:%M:%S")
			tree_value = (current_date,) + tree_value
			#print(tree_value)
			if 'GEOLOC' in tree_value:
				print("Geoloc",tree_value)
				self.treeGeoloc.insert('', index='end', values=tree_value)
				self.treeGeoloc.update()
			elif 'FIN_MISS' in tree_value: 
				print("aff Retour")
				print("Fin_Mission",tree_value)
				self.treeFinM.insert('', index='end', values=tree_value)
				self.treeFinM.update()
			elif 'IHM' in tree_value:
				print("IHM", tree_value)
				self.treeIHM.insert('', index='end', values=tree_value)
				self.treeIHM.update()
			elif 'VAL_MISS' in tree_value:
				print("Ret", tree_value)
				self.treeValM.insert('', index='end', values=tree_value)
				self.treeValM.update()
			elif 'CFP' in tree_value:
				self.treeCFP.insert('', index='end', values=tree_value)
				self.treeCFP.update()

	def affichage_FM(self):
		"""
		"""
		tree_value = self.q.get().values()
		tree_value = list(tree_value)
		tree_value = tuple(tree_value)
		now = datetime.datetime.now()
		current_date = now.strftime("%d-%m-%Y %H:%M:%S")
		tree_value = (current_date,) + tree_value
		if 'FIN_MISS' in tree_value: 
			self.treeFinM.insert('', index='end', values=tree_value)
			self.treeFinM.update()

	def affichage_FMFP(self):
		while self.FMStop == False or self.FPStop == False:
			tree_value = q.get().values()
			tree_value = list(tree_value)
			tree_value = tuple(tree_value)
			now = datetime.datetime.now()
			current_date = now.strftime("%d-%m-%Y %H:%M:%S")
			tree_value = (current_date,) + tree_value
			if 'FIN_MISS' in tree_value: 
				self.treeFinM.insert('', index='end', values=tree_value)
				self.treeFinM.update()
				self.FMStop = True
			elif 'CFP' in tree_value:
				self.treeCFP.insert('', index='end', values=tree_value)
				self.treeCFP.update()
				self.FPStop = True

	def affichage_DGFP(self):
		while self.DGStop == False or self.FPStop == False:
			tree_value = q.get().values()
			tree_value = list(tree_value)
			tree_value = tuple(tree_value)
			now = datetime.datetime.now()
			current_date = now.strftime("%d-%m-%Y %H:%M:%S")
			tree_value = (current_date,) + tree_value
			if 'GEOLOC' in tree_value: 
				self.treeGeoloc.insert('', index='end', values=tree_value)
				self.treeGeoloc.update()
				self.DGStop = True
			elif 'CFP' in tree_value:
				self.treeCFP.insert('', index='end', values=tree_value)
				self.treeCFP.update()
				self.FPStop = True


	def stop(self):
		"""
		"""
		self.arret = True


class Lancement(): #threading.Thread
	"""
	"""
	def __init__(self, id_s, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP):
		super().__init__()
		self.id_s = id_s
		self.opt = opt
		self.q = q
		self.treeGeoloc = treeGeoloc
		self.treeValM = treeValM
		self.treeFinM = treeFinM
		self.treeIHM = treeIHM
		self.treeCFP = treeCFP
		self.arret = False
		self.send = None
		self.affichage = None
		#self.loop = None

	def run(self):
		if self.opt == "Geoloc":
			self.send = Sendtram(self.opt, int(list_cb[self.id_s].get()))
			self.send.start() 
			#-------Affichage des infos
			self.affichage = Affichage(self.opt, self.q, self.treeGeoloc, self.treeValM, self.treeFinM, self.treeIHM, self.treeCFP)
			self.affichage.start()
		elif self.opt == "Retournement":
			#-------Envoi de la tram
			self.send = Sendtram(self.opt, int(list_cb[self.id_s].get()))
			self.send.start() 
			#-------Affichage des infos
			self.affichage = Affichage(self.opt, self.q, self.treeGeoloc, self.treeValM, self.treeFinM, self.treeIHM, self.treeCFP)
			self.affichage.start()
				

	def stop(self):
		"""
		"""
		self.send.stop()
		self.affichage.stop()
		#print("alive", self.send.is_alive())

		
def lancer(id_s):
	"""
	Deroulement du scenario selectionner et affichage des informations des trames reseaux 
	"""
	global scenar_1
	global scenar_2
	global scenar_3
	global scenar_4
	
	
	if id_s == 0:
		scenar_1 = Lancement(id_s, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)#lancement(id_s)
		scenar_1.run()
	elif id_s == 1:
		scenar_2 = Lancement(id_s, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)#lancement(id_s)
		scenar_2.run()
	elif id_s == 2:
		scenar_3 = Lancement(id_s, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)#lancement(id_s)
		scenar_3.run()
	elif id_s == 3:
		scenar_4 = Lancement(id_s, opt, q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)#lancement(id_s)
		scenar_4.run()
	
def arreter(id_s):
	"""
	"""
	if id_s == 0:
		scenar_1.stop()
	elif id_s == 1:
		scenar_2.stop()
	elif id_s == 2:
		scenar_3.stop()
	elif id_s == 3:
		scenar_4.stop()
	

def boucler(id_s):
	"""
	"""
	b_name = label_simulation.nametowidget('boucle{}'.format(str(id_s+1)))	
	print(list_cb[id_s].get())


def lancerFM():
	"""
	Lancer le scenario selectionner
	"""
	#-------Envoi de la tram
	send = Sendtram("fin_mission", 0)
	send.start()
	#-------Affichage des infos
	affichage = Affichage("FM", q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)
	affichage.start()
	

def lancerFMFP():
	"""
	Lancer le scenario selectionner
	"""
	#-------Envoi de la tram
	send = Sendtram("fm_fp", 0)
	send.start()
	#-------Affichage des infos
	affichage = Affichage("FMFP", q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)
	affichage.start()
	

def lancerDGFP():
	"""
	Lancer le scenario selectionner
	"""
	#-------Envoi de la tram
	send = Sendtram("dg_fp", 0)
	send.start()
	#-------Affichage des infos
	affichage = Affichage("DGFP", q, treeGeoloc, treeValM, treeFinM, treeIHM, treeCFP)
	affichage.start()

def validation_lan():
	"""
	"""
	global q
	#Recuperation du port decoute
	portE = entryPE.get()
	print(type(entryPE.get()))
	#Recuperation de avec ou sans udp
	udp_filtre = udp_value.get()
	print(type(udp_filtre))
	#Recuperation de avec ou sans tcp
	tcp_filtre = tcp_value.get()
	print(tcp_filtre)
	#---------Mise en ecoute du reseau local
	q = queue.Queue()
	sniffer = Sniffer(q, portE, udp_filtre, tcp_filtre)
	sniffer.start()

	
	

#------------------------------------------------Creation de la fenetre principale
root = tk.Tk()
root.title("ABL LAN Simulator")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo_sncf.png'))
root.minsize(920, 1000)
root.configure(bg='#09041A')
root.resizable(width=False, height=False)
#------------------------------------------------Creation du label simulation
label_simulation = tk.LabelFrame(root, text="Simulation scenarios", bg='#09041A', fg='#F4F2F2', width=435, height=150, borderwidth=1)
label_simulation.grid_propagate(0)
label_simulation.place(x=5, y=5)
#-----------------Recuperation de la liste des scenarios
scenarios = getScenarios('scenario.txt')
#-----------------
list_cb = [tk.IntVar() for i in range(4)]
for i in range(4):
	#--------Creation des labels scenario
	labelCam = tk.Label(label_simulation, text="Scenario {}".format(str(i+1)), bg='#09041A', fg='#F4F2F2') 
	labelCam.grid(row=i, column=0, padx=10, pady=5)
	#--------Creation des combobox des scenarios
	#list_opt = ["Option 1", "Option 2", "Option 3", "Option 4"]
	s_cbbx = ttk.Combobox(label_simulation, name='s{}_cbbx'.format(str(i+1)), values=scenarios, width=7)
	s_cbbx.state(['!disabled', 'readonly'])
	s_cbbx.bind("<<ComboboxSelected>>", lambda event, i=i:getOption(event, i))
	s_cbbx.grid(row=i, column=1, padx=10, pady=5, sticky='nw')
	#-------Creation du widget lancer 
	lancerWidget = tk.Button(label_simulation, name='lancer'+str(i), text="LANCER", command=lambda i=i: lancer(i))
	lancerWidget['font'] = font.Font(size=5)
	lancerWidget.grid(row=i, column=2, padx=10, pady=5)
	#-------Creation du widget arreter 
	arreterWidget = tk.Button(label_simulation, name='arreter'+str(i), text="ARRETER", command=lambda i=i: arreter(i))
	arreterWidget['font'] = font.Font(size=5)
	arreterWidget.grid(row=i, column=3, padx=10, pady=5)
	#--------Creation des labels boucle
	label_boucle = tk.Label(label_simulation, text="Boucle", bg='#09041A', fg='#F4F2F2') 
	label_boucle.grid(row=i, column=4, padx=0, pady=5)
	#--------Creation du widget boucle
	boucle = tk.Checkbutton(label_simulation,  name="boucle{}".format(str(i+1)), variable=list_cb[i], bg='#09041A', command=lambda i=i: boucler(i))
	boucle.grid(row=i, column=5, padx=10, pady=5)
	"""
	#--------Creation des labels declencheurs
	label_declencheur = tk.Label(label_simulation, text="Declencheur", bg='#09041A', fg='#F4F2F2') 
	label_declencheur.grid(row=i, column=6, padx=0, pady=5)
	#--------Creation des combobox de declenchements
	list_declencheur = ["FM", "FM+FP", "DG+FP"]
	declencheur_cbbx = ttk.Combobox(label_simulation, name='declencheur{}_cbbx'.format(str(i+1)), values=list_declencheur, width=6)
	declencheur_cbbx.state(['!disabled', 'readonly'])
	declencheur_cbbx.bind("<<ComboboxSelected>>", lambda event, i=i:getDeclencheur(event, i))
	declencheur_cbbx.grid(row=i, column=7, padx=10, pady=5, sticky='nw')
	"""

print(boucle.winfo_name())

#---------------------------------------------------Creation du label configuration
label_config = tk.LabelFrame(root, text="Configuration", bg='#09041A', fg='#F4F2F2', width=175, height=150, borderwidth=1)
label_config.grid_propagate(0)
label_config.place(x=440, y=5)
#--------Creation du label port decoute
labelPE = tk.Label(label_config, text="Port d'ecoute", bg='#09041A', fg='#F4F2F2') 
labelPE.grid(row=0, column=0, padx=10, pady=5)
#--------Creation de la zone de saisie du numero de port
entryPE = tk.Entry(label_config, bg='#F4F2F2', fg='#09041A', width=6)#,command=getSaisie)#textvariable=saisie,
entryPE.grid(row=0, column=1, padx=0, pady=5)
#--------Creation du label protocole UDP
labelProtocole = tk.Label(label_config, text="Protocle UDP", bg='#09041A', fg='#F4F2F2') 
labelProtocole.grid(row=1, column=0, padx=10, pady=5)#, sticky='nw')
#--------Creation du boutton protocole UDP
udp_value = tk.IntVar()
boutton_UDP = tk.Checkbutton(label_config, variable=udp_value, bg='#09041A')#, command=surimpression)#, relief="solid")
boutton_UDP.grid(row=1, column=1, padx=0, pady=5, sticky='w')
#--------Creation du label protocole TCP
labelProtocole = tk.Label(label_config, text="Protocle TCP", bg='#09041A', fg='#F4F2F2') 
labelProtocole.grid(row=2, column=0, padx=10, pady=5)#, sticky='nw')
#--------Creation du boutton protocole TCP
tcp_value = tk.IntVar()
boutton_TCP = tk.Checkbutton(label_config, variable=tcp_value, bg='#09041A', relief="flat")#, command=surimpression)#, relief="solid")
boutton_TCP.grid(row=2, column=1, padx=0, pady=5, sticky='w')
#-------Creation du boutton valider pour la validation de la configuration reseau
validation_button = tk.Button(label_config, text="Valider", command=validation_lan)
validation_button['font'] = font.Font(size=5)
validation_button.grid(row=3, column=0, padx=15, pady=5, sticky='w')

#--------------------------------------------------Creation du label simulation declencheur
label_declencheur = tk.LabelFrame(root, text="Simulation declencheurs", bg='#09041A', fg='#F4F2F2', width=295, height=150, borderwidth=1)
label_declencheur.grid_propagate(0)
label_declencheur.place(x=615, y=5)
#--------Creation du label Fin Mission
label_FM = tk.Label(label_declencheur, text="Fin Mission", bg='#09041A', fg='#F4F2F2') 
label_FM.grid(row=0, column=0, padx=5, pady=5, sticky='w')
#--------Creation du boutton Lancer Fin Mission
boutton_lancerFM = tk.Button(label_declencheur, text="LANCER", command=lancerFM)
boutton_lancerFM['font'] = font.Font(size=5)
boutton_lancerFM.grid(row=0, column=1, padx=10, pady=5, sticky='w')
#--------Creation du label Fin Mission + Fermeture Portes
label_FMFP = tk.Label(label_declencheur, text="Fin Mission + Fermeture Portes", bg='#09041A', fg='#F4F2F2') 
label_FMFP.grid(row=1, column=0, padx=5, pady=5, sticky='w')
#--------Creation du boutton Lancer Fin Mission + Fermeture Portes
boutton_lancerFMFP = tk.Button(label_declencheur, text="LANCER", command=lancerFMFP)
boutton_lancerFMFP['font'] = font.Font(size=5)
boutton_lancerFMFP.grid(row=1, column=1, padx=10, pady=5, sticky='w')
#--------Creation du label Der Gare + Fermeture Portes
label_DGFP = tk.Label(label_declencheur, text="Der Gare + Fermeture Portes", bg='#09041A', fg='#F4F2F2') 
label_DGFP.grid(row=2, column=0, padx=5, pady=5, sticky='w')
#--------Creation du boutton Lancer Der Gare + Fermeture Portes
boutton_lancerDGFP = tk.Button(label_declencheur, text="LANCER", command=lancerDGFP)
boutton_lancerDGFP['font'] = font.Font(size=5)
boutton_lancerDGFP.grid(row=2, column=1, padx=10, pady=5, sticky='w')

#-----------------------------------------------------Trame de geolocalisation
#----------------Creation du titre trame de geolocalisation
label_geoloc = tk.LabelFrame(root, text="Trame de Geolocalisation", labelanchor='n', bg='#09041A', fg='#F4F2F2', width=905, height=20, borderwidth=1)
label_geoloc.grid_propagate(0)
label_geoloc.place(x=5, y=155)
#---------------Style treegeoloc
style = ttk.Style()
style.configure("Treeview", bg="#09041A", fg='#F4F2F2', rowheight=25, fieldbackground="#09041A")
style.map("Treeview", bg=[('selected', '#090C20')])
#-----------------------------------------------------
#--------------Treeview Frame
treeGeoloc_frame = tk.Frame(root)
treeGeoloc_frame.place(x=5, y=176)
#--------------Barre de defilement
sb_geoloc = ttk.Scrollbar(treeGeoloc_frame)
sb_geoloc.pack(side="right", fill="y")
#--------------TreeView TrameGeoloc
treeGeoloc = ttk.Treeview(treeGeoloc_frame, height=5)
treeGeoloc.configure(yscrollcommand=sb_geoloc.set)
#--------------Configurer la barre de defilement
sb_geoloc.config(command=treeGeoloc.yview)
treeGeoloc.pack()
#---------------
geoloc_layout =[("horodate",[80,"Horodate"]), ("type",[70,"Type"]), ("date",[90, "Date"]), ("heure",[100, "Heure"]),
                   ("latitude",[100, "Lat."]), ("longitude",[100, "Lon."]), ("code_mission",[70, "Mission"]),
                   ("gare_precedente",[60, "Gare P"]),("gare_courante",[60, "Gare C"]),("gare_suivante",[60, "Gare S"]),
                   ("distance_odo",[96, "Dist Odo"])]
#---------------
geoloc_layout = OrderedDict(geoloc_layout)
geoloc_columns = [key for key,_ in geoloc_layout.items()]
treeGeoloc["columns"] = geoloc_columns
treeGeoloc['show'] = 'headings'
#---------------
for key, value in geoloc_layout.items():
    treeGeoloc.heading(key, text = value[1], anchor=tk.W)
    treeGeoloc.column(key, width=value[0], minwidth=value[0], stretch=tk.YES)
#-----------------------------------------------------Trame Val_Mission
#--------------Creation du titre trame Val_Mission
label_geoloc = tk.LabelFrame(root, text="Trame de Validation Mission", labelanchor='n', bg='#09041A', fg='#F4F2F2', width=905, height=20, borderwidth=1)
label_geoloc.grid_propagate(0)
label_geoloc.place(x=5, y=325)
#--------------Treeview Frame
treeValM_frame = tk.Frame(root)
treeValM_frame.place(x=5, y=345)
#--------------Barre de defilement
sb_ValM = ttk.Scrollbar(treeValM_frame)
sb_ValM.pack(side="right", fill="y")
#--------------TreeView Val_Mission
treeValM = ttk.Treeview(treeValM_frame, height=5)
treeValM.configure(yscrollcommand=sb_ValM.set)
#--------------Configurer la barre de defilement
sb_ValM.config(command=treeValM.yview)
treeValM.pack()
#--------------
valM_layout = [("horodate",[187,"Horodate"]), ("id_src",[170,"Source"]), ("id_dst",[170,"Destination"]), ("type",[90,"Type"]), ("code_trame",[135, "Code Trame"]), ("type_trame",[135, "Type Trame"])]
valM_layout = OrderedDict(valM_layout)
valM_columns = [key for key,_ in valM_layout.items()]
treeValM["columns"] = valM_columns
treeValM['show'] = 'headings'
#---------------
for key, value in valM_layout.items():
    treeValM.heading(key, text = value[1], anchor=tk.W)
    treeValM.column(key, width=value[0], minwidth=value[0], stretch=tk.YES)
#-----------------------------------------------------Trame Fin_Mission
#--------------Creation du titre trame Fin_Mission
label_geoloc = tk.LabelFrame(root, text="Trame de Fin Mission", labelanchor='n', bg='#09041A', fg='#F4F2F2', width=905, height=20, borderwidth=1)
label_geoloc.grid_propagate(0)
label_geoloc.place(x=5, y=495)
#--------------Treeview Frame
treeFinM_frame = tk.Frame(root)
treeFinM_frame.place(x=5, y=513)
#--------------Barre de defilement
sb_FinM = ttk.Scrollbar(treeFinM_frame)
sb_FinM.pack(side="right", fill="y")
#--------------TreeView Fin_Mission
treeFinM = ttk.Treeview(treeFinM_frame, height=5)
treeFinM.configure(yscrollcommand=sb_FinM.set)
#--------------Configurer la barre de defilement
sb_FinM.config(command=treeFinM.yview)
treeFinM.pack()
#--------------
finM_layout = [("horodate",[187,"Horodate"]), ("id_src",[170,"Source"]), ("id_dst",[170,"Destination"]), ("type",[90,"Type"]), ("code_trame",[135, "Code Trame"]), ("type_trame",[135, "Type Trame"])]
finM_layout = OrderedDict(finM_layout)
finM_columns = [key for key,_ in finM_layout.items()]
treeFinM["columns"] = finM_columns
treeFinM['show'] = 'headings'
#---------------
for key, value in finM_layout.items():
    treeFinM.heading(key, text = value[1], anchor=tk.W)
    treeFinM.column(key, width=value[0], minwidth=value[0], stretch=tk.YES)

#-----------------------------------------------------Trame Etat IHM
#--------------Creation du titre trame Etat IHM
label_geoloc = tk.LabelFrame(root, text="Trame Etat IHM", labelanchor='n', bg='#09041A', fg='#F4F2F2', width=905, height=20, borderwidth=1)
label_geoloc.grid_propagate(0)
label_geoloc.place(x=5, y=660)
#--------------Treeview Frame
treeIHM_frame = tk.Frame(root)
treeIHM_frame.place(x=5, y=680)
#--------------Barre de defilement
sb_IHM = ttk.Scrollbar(treeIHM_frame)
sb_IHM.pack(side="right", fill="y")
#--------------TreeView Fin_Mission
treeIHM = ttk.Treeview(treeIHM_frame, height=5)
treeIHM.configure(yscrollcommand=sb_IHM.set)
#--------------Configurer la barre de defilement
sb_IHM.config(command=treeIHM.yview)
treeIHM.pack()
#--------------
IHM_layout = [("horodate",[150,"Horodate"]), ("id_src",[150,"Source"]), ("id_dst",[150,"Destination"]), ("type",[88,"Type"]), ("code_trame",[110, "Code Mission"]), 
				("qblt",[80, "QBLT"]), ("zcofp",[80, "ZCOFP"]), ("zop",[80, "ZOP"])]
IHM_layout = OrderedDict(IHM_layout)
IHM_columns = [key for key,_ in IHM_layout.items()]
treeIHM["columns"] = IHM_columns
treeIHM['show'] = 'headings'
#---------------
for key, value in IHM_layout.items():
    treeIHM.heading(key, text = value[1], anchor=tk.W)
    treeIHM.column(key, width=value[0], minwidth=value[0], stretch=tk.YES)

#-----------------------------------------------------Trame Fermeture Porte
#--------------Creation du titre trame Fin_Mission
label_geoloc = tk.LabelFrame(root, text="Trame CFP", labelanchor='n', bg='#09041A', fg='#F4F2F2', width=905, height=20, borderwidth=1)
label_geoloc.grid_propagate(0)
label_geoloc.place(x=5, y=830)
#--------------Treeview Frame
treeFP_frame = tk.Frame(root)
treeFP_frame.place(x=5, y=850)
#--------------Barre de defilement
sb_FP = ttk.Scrollbar(treeFP_frame)
sb_FP.pack(side="right", fill="y")
#--------------TreeView Fermeture Porte
treeCFP = ttk.Treeview(treeFP_frame, height=5)
treeCFP.configure(yscrollcommand=sb_FP.set)
#--------------Configurer la barre de defilement
sb_IHM.config(command=treeCFP.yview)
treeCFP.pack()
#--------------
FP_layout = [("horodate",[187,"Horodate"]), ("id_src",[170,"Source"]), ("id_dst",[170,"Destination"]), ("type",[90,"Type"]), ("code_trame",[135, "Code Trame"]), ("type_trame",[135, "Type Trame"])]
FP_layout = OrderedDict(FP_layout)
FP_columns = [key for key,_ in FP_layout.items()]
treeCFP["columns"] = FP_columns
treeCFP['show'] = 'headings'
#---------------
for key, value in FP_layout.items():
    treeCFP.heading(key, text = value[1], anchor=tk.W)
    treeCFP.column(key, width=value[0], minwidth=value[0], stretch=tk.YES)



root.mainloop()

