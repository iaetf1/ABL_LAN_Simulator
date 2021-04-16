import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import font
import random
import configparser
import os
import subprocess




def getOption(event, id_s):
	"""
	"""
	s_name = label_simulation.nametowidget('s{}_cbbx'.format(str(id_s+1)))	
	opt = s_name.get()
	print(opt,"boutton:",id_s)

def getDeclencheur(event, id_dcl):
	"""
	"""
	dcl_name = label_simulation.nametowidget('declencheur{}_cbbx'.format(str(id_dcl+1)))	
	opt = dcl_name.get()
	print(opt,"boutton:",id_dcl)

def lancer(id_s):
	"""
	Lancer le scenario selectionner
	"""
	print(id_s)
	if id_s == 0:
		print(entryPE.get())
	
def arreter(id_s):
	"""
	"""
	print(id_s)

def boucler(id_s):
	"""
	"""
	b_name = label_simulation.nametowidget('boucle{}'.format(str(id_s+1)))	
	print(list_cb[id_s].get())

def getSaisie():
	print(entryPE.get())

def getPtlCom():
	print(radio_var.get())


#Creation de la fenetre principale
root = tk.Tk()
root.title("ABL LAN Simulator")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='logo_sncf.png'))
root.minsize(820, 615)
root.configure(bg='#09041A')
root.resizable(width=False, height=False)
#------------------------------------------------Creation du label simulation
label_simulation = tk.LabelFrame(root, text="Simulation scenarios", bg='#09041A', fg='#F4F2F2', width=605, height=150, borderwidth=1)
label_simulation.grid_propagate(0)
label_simulation.place(x=5, y=5)
#-----------------
list_cb = [tk.IntVar() for i in range(4)]
for i in range(4):
	#--------Creation des labels scenario
	labelCam = tk.Label(label_simulation, text="Scenario {}".format(str(i+1)), bg='#09041A', fg='#F4F2F2') 
	labelCam.grid(row=i, column=0, padx=10, pady=5)
	#--------Creation des combobox des scenarios
	list_opt = ["Option 1", "Option 2", "Option 3", "Option 4"]
	s_cbbx = ttk.Combobox(label_simulation, name='s{}_cbbx'.format(str(i+1)), values=list_opt, width=7)
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
	#--------Creation des labels declencheurs
	label_declencheur = tk.Label(label_simulation, text="Declencheur", bg='#09041A', fg='#F4F2F2') 
	label_declencheur.grid(row=i, column=6, padx=0, pady=5)
	#--------Creation des combobox de declenchements
	list_declencheur = ["FM", "FM+FP", "DG+FP"]
	declencheur_cbbx = ttk.Combobox(label_simulation, name='declencheur{}_cbbx'.format(str(i+1)), values=list_declencheur, width=6)
	declencheur_cbbx.state(['!disabled', 'readonly'])
	declencheur_cbbx.bind("<<ComboboxSelected>>", lambda event, i=i:getDeclencheur(event, i))
	declencheur_cbbx.grid(row=i, column=7, padx=10, pady=5, sticky='nw')

print(boucle.winfo_name())

#---------------------------------------------------Creation du label configuration
label_config = tk.LabelFrame(root, text="Configuration", bg='#09041A', fg='#F4F2F2', width=200, height=150, borderwidth=1)
label_config.grid_propagate(0)
label_config.place(x=615, y=5)
#--------Creation du label port decoute
labelPE = tk.Label(label_config, text="Port d'ecoute", bg='#09041A', fg='#F4F2F2') 
labelPE.grid(row=0, column=0, padx=10, pady=5)
#--------Creation de la zone de saisie du numero de port
saisie = tk.StringVar()
entryPE = tk.Entry(label_config, bg='#F4F2F2', fg='#09041A', width=6)#,command=getSaisie)#textvariable=saisie,
entryPE.grid(row=0, column=1, padx=0, pady=5)
#--------Creation du label protocole UDP
labelProtocole = tk.Label(label_config, text="Protocle UDP", bg='#09041A', fg='#F4F2F2') 
labelProtocole.grid(row=1, column=0, padx=10, pady=5, sticky='nw')
#--------Creation du label protocole TCP
labelProtocole = tk.Label(label_config, text="Protocle TCP", bg='#09041A', fg='#F4F2F2') 
labelProtocole.grid(row=2, column=0, padx=10, pady=5, sticky='nw')
#--------Creation du boutton radio protocole de communication
radio_var = tk.IntVar()
for i in range(2):
	boutton_protocole = tk.Radiobutton(label_config, variable=radio_var, value=i, bg='#09041A', command=getPtlCom)
	boutton_protocole.grid(row=i+1, column=1)



"""
#-------Creation du label Repertoire videos
repVideo = tk.Label(label_config, text="Repertoire videos", bg='#09041A', fg='#F4F2F2') 
repVideo.grid(row=1, column=0, padx=10)
#-------Creation du widget parcourrir
parcourrirWidget = tk.Button(label_config, text="Parcourrir", command=parcourrir, width=4)
parcourrirWidget['font'] = font.Font(size=5)
parcourrirWidget.grid(row=1, column=1, pady=10)
#-------Creation du label Surimpression
surimpLabel = tk.Label(label_config, text="Surimpression", bg='#09041A', fg='#F4F2F2') 
surimpLabel.place(x=475, y=0)
#--------Creation du widget Surimpression
checkValue = tk.IntVar()
surimpWidget = tk.Checkbutton(label_config, variable=checkValue, bg='#09041A', command=surimpression, relief="solid")
surimpWidget.place(x=585, y=0)
#--------Creation du label couleur texte
couleurTextLabel = tk.Label(label_config, text="Couleur Texte", bg='#09041A', fg='#F4F2F2') 
#couleurTextLabel.grid(row=0, column=2, sticky='ne', ipadx=50)
couleurTextLabel.place(x=250, y=0)
#--------Creation de la combobox couleur texte
list_couleur = ["Blanc", "Rouge", "Vert"]
selectedValueCouleur = tk.StringVar()
couleurCam_Combo = ttk.Combobox(label_config, textvariable=selectedValueCouleur, values=list_couleur, width=5)
couleurCam_Combo.current(0)
couleurCam_Combo.state(['!disabled', 'readonly'])
couleurCam_Combo.bind("<<ComboboxSelected>>", couleurTexte)
couleurCam_Combo.place(x=360, y=0)
#--------Creation du label couleur texte
posTextLabel = tk.Label(label_config, text="Position Texte", bg='#09041A', fg='#F4F2F2') 
posTextLabel.place(x=250, y=35)
#--------Creation de la combobox couleur texte
list_pos = ["ne", "no", "se", "so"]
selectedValuePos = tk.StringVar()
couleurCam_Combo = ttk.Combobox(label_config, textvariable=selectedValuePos, values=list_pos, width=5)
couleurCam_Combo.current(0)
couleurCam_Combo.state(['!disabled', 'readonly'])
couleurCam_Combo.bind("<<ComboboxSelected>>", positionTexte)
couleurCam_Combo.place(x=360, y=35)
#-------Creation du widget charger configuration
chgConfigWidget = tk.Button(root, text="CHARGER", command=chargerConfig)
chgConfigWidget.place(x=520, y=80)
#-------Creation du widget lancer tout
lancerToutWidget = tk.Button(root, text="LANCER TOUT", command=lancerTout, width=12)
lancerToutWidget.place(x=660, y=14)
#-------Creation du widget arreter tout
arreterToutWidget = tk.Button(root, text="ARRETER TOUT", command=arreterTout, width=12)
arreterToutWidget.place(x=660, y=60)

#--------------------------------------
#--------------------------------------
#-------Creation du label nom camera
nomCameraLabel = tk.Label(root, text="Camera", bg='#09041A', fg='#F4F2F2')
nomCameraLabel.place(x=10, y=150) 
#-------Creation du label emplacement
emplacementLabel = tk.Label(root, text="Emplacement", bg='#09041A', fg='#F4F2F2')
emplacementLabel.place(x=80, y=150) 
#-------Creation du label adresse IP
adresseIPLabel = tk.Label(root, text="Adresse IP", bg='#09041A', fg='#F4F2F2')
adresseIPLabel.place(x=190, y=150) 
#-------Creation du label URL RTSP
urlRtspLabel = tk.Label(root, text="URL RTSP", bg='#09041A', fg='#F4F2F2')
urlRtspLabel.place(x=300, y=150) 
#-----------------
#-----------Creation de la base
baseFrame = tk.Frame(root, bg='#09041A', width=800, height=435)#, bg='#09041A'
baseFrame.place(x=0, y=175)
#-----------Creation du canvas
mon_canvas = tk.Canvas(baseFrame, bg='#09041A', width=800, height=435)
mon_canvas.pack(side="left", fill="both", expand=1)
#-----------Ajouter la barre de defilement
barDefillement = ttk.Scrollbar(baseFrame, orient="vertical", command=mon_canvas.yview)
barDefillement.pack(side="right", fill="y")
#-----------Configurer le canvas
mon_canvas.configure(yscrollcommand=barDefillement.set)
mon_canvas.bind('<Configure>', lambda e: mon_canvas.configure(scrollregion=mon_canvas.bbox("all")))
#-----------Creation de la frame deux
scdFrame = tk.Frame(mon_canvas, bg='#09041A', name='canevas')
#-----------Ajouter la scd frame a une fenetre dans le canvas
mon_canvas.create_window((0,0), window=scdFrame, anchor="nw")

for i in range(56):
	#v = list_videoName[i]

	#-------Creation de la frame nom camera
	nomCameraFrame = tk.Label(scdFrame, name='camera'+str(i), bg='#C2C2CD', fg='#09041A', width=6, height=1)
	nomCameraFrame.grid(row=i, column=0, padx=10, pady=10)
	#-------Creation de la frame emplacement
	emplacementFrame = tk.Label(scdFrame, name='position'+str(i), bg='#C2C2CD', fg='#09041A', width=11, height=1)
	emplacementFrame.grid(row=i, column=1, padx=10, pady=10)
	#-------Creation de la frame adresse IP
	adresseIPFrame = tk.Label(scdFrame, name='ip'+str(i), bg='#C2C2CD', fg='#09041A', width=11, height=1)
	adresseIPFrame.grid(row=i, column=2, padx=10, pady=10)
	#-------Creation de la frame URL RTSP
	urlRtspFrame = tk.Label(scdFrame, name='rtsp'+str(i), bg='#C2C2CD', fg='#09041A', width=41, height=1)
	urlRtspFrame.grid(row=i, column=3, padx=10, pady=10)
	#-------Creation du widget lancer 
	lancerWidget = tk.Button(scdFrame, name='lancer'+str(i), text="LANCER", command=lambda i=i: lancer(i))
	lancerWidget['font'] = font.Font(size=5)
	lancerWidget.grid(row=i, column=4, padx=10, pady=10)
	#-------Creation du widget arreter 
	arreterWidget = tk.Button(scdFrame, name='arreter'+str(i), text="ARRETER", command=lambda i=i: arreter(i))
	arreterWidget['font'] = font.Font(size=5)
	arreterWidget.grid(row=i, column=5, padx=10, pady=10)
"""
root.mainloop()

