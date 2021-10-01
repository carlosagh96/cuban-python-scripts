#!/usr/bin/python3.9

# Programa para generar scripts de Bash para transcodificar con FFmpeg
# Solo se tiene en cuenta un archivo de entrada y uno de salida por cada órden/línea
# Las configuraciones se guardan en un JSON, que debe nombrarse igual que este script

# Llevado a diccionario el JSON:
# → Cada clave es el título de la configuración (texto)
# → Cada valor son los elementos de la configuración (lista)
# → Elem. 0: Las opciones de configuración de FFmpeg exceptuando el archivo de entrada y el de salida (texto)
# → Elem. 1: Los archivos válidos para la configuración actual (lista)
# → Elem. 2: (OPCIONAL) Argumento extra para declarar el contenedor de salida (lista)

# Variables:
# Las variables son reconocidas en la configuración, por cada variable se le da la oportunidad de darle valor al inico del script ya hecho
# Sin embargo, tenga en cuenta que hay variables especiales, todas ellas son texto

# Variables especiales:
# APPDIR → El directorio del programa. Puede guardar archivos junto a este programa y usarlos. Tenga en cuenta que la ruta es absoluta y no termina en "/"
# STEM → EL tallo del nombre del archivo de entrada actual, es decir, el nombre del archivo sin el sufijo. Útil para declarar archivos de entrada para trabajar el archivo en cuestión
# AUTOINC → Autoincremento, ideal para enumeraciones de episodios de series, etc... al usarla aparecerán en el script las variables AUTONUM y MAXNUM. AUTONUM es el numero inicial, MAXNUM es el máximo y AUTOINC es el resultado de procesar ambos antes de ejecutar la órden de FFmpeg con el archivo actual. Después de la órden de FFmpeg, AUTONUM aumenta en 1 y asi sucesivamente hasta el último

# Programa escrito por Carlos Alberto González hernández
# https://t.me/CarlosAGH

import json
import os
import re
import sys

from pathlib import Path

_path_app_rel=sys.argv[0]
_path_app_pl=Path(_path_app_rel)
_path_app=_path_app_pl.resolve()
_path_app_dir=_path_app_pl.parent.resolve()
_thystem=_path_app_pl.stem
_thyname=_path_app_pl.name
_path_configfile=str(_path_app_dir)+"/"+str(_thystem)+".json"

# print(sys.argv)

try:
	with open(_path_configfile) as cfgs:
		cfg_raw_lst=cfgs.readlines()

except Exception as e:
	print("ERROR: mientras se leía la configuración\n",_path_configfile)
	print(e)
	exit()

cfg_raw=""
for line in cfg_raw_lst:
	cfg_raw=cfg_raw+line.strip()

cfgs=json.loads(cfg_raw)

aconfigs=list(cfgs.keys())

if len(sys.argv)>1:
	pass

else:
	print("[Uso del programa]")
	print(_thyname,"NConf Modo Opcs\nNConf: Seleccionar la configuración\nModo: Puede ser 'e' o 'p'\nEl primero es para escribir el archivo 'Convertir.sh', el segundo es sólo para probar\nOpcs: Según la configuración que elija, se le va a pedir que obligatoriamente elija un formato contenedor para la salida (el punto del sufijo se omite)")
	c=0
	print("\n[Configuraciones disponibles]")
	for t in aconfigs:
		print(c,t)
		c=c+1

	exit()

_error_nvarg="ERROR: Argumento no válido"

# Get the first argument: The selected config
try:
	sconfig=int(sys.argv[1])

except:
	print(_error_nvarg)
	exit()

else:
	print("[Seleccionando la configuración]")
	print("Ha seleccionado la no.",sconfig)

# Check if the indexed config exists
try:
	assert sconfig>-1 and sconfig<len(aconfigs)

except:
	print("ERROR: La configuración solicitada no existe")
	exit()

else:
	configtitle=aconfigs[sconfig]
	theconfig=cfgs.get(configtitle)
	ffmpeg_args=theconfig[0]
	valid_cin=theconfig[1]
	print("Nombre:\n",configtitle)
	print("Argumentos FFmpeg:\n",ffmpeg_args)
	print("Contenedores de entrada válidos:\n",valid_cin)

	_msg_same_cout="El contenedor de salida es el mismo que el de origen"

	# Output file container types: Get default from config, pick one from config or pick same as input
	_out_from="FROM"
	_out_pick="PICK"
	_out_same="SAME"

	out_type=_out_same

	if len(theconfig)>2:

		valid_cout=theconfig[2]
		if len(valid_cout)==1:
			print("Contenedor de salida (Se establece automáticamente):",valid_cout[0])
			out_type=_out_from

		elif len(valid_cout)>1:
			print("Contenedores de salida válidos (Debe elegir uno):",valid_cout)
			out_type=_out_pick

		else:
			print(_msg_same_cout)

	else:
		print(_msg_same_cout)

	shvp=re.compile(r"\$\w*")
	dvars=shvp.findall(ffmpeg_args)

	mod_autoinc=False
	mod_stem=False
	mod_appdir=False
	if len(dvars)>0:
		var_autoinc="$AUTOINC"
		var_stem="$STEM"
		var_appdir="$APPDIR"

		print("Variables detectadas en las opciones de FFmpeg:\n",dvars)

		if var_autoinc in dvars:
			print(var_autoinc,"→ Variable especial: Autoincremento")
			dvars.remove(var_autoinc)
			mod_autoinc=True

		if var_appdir in dvars:
			print(var_appdir,"→ Variable especial: Directorio del programa")
			dvars.remove(var_appdir)
			mod_appdir=True

		if var_stem in dvars:
			print(var_stem,"→ Variable especial: Tallo")
			dvars.remove(var_stem)
			mod_stem=True


if len(sys.argv)>2:
	pass

else:
	exit()

print("")

vargs=["p","e"]

valid=False
for arg in vargs:
	if arg==sys.argv[2]:
		valid=True

	if valid:
		break

if not valid:
	print(_error_nvarg)
	exit()

if sys.argv[2]==vargs[1]:
	print("[Modo escritura]")

else:
	print("[Modo de prueba]")

execdir_pl=Path("./")
stuff_pl=list(execdir_pl.glob("*"))
vfiles=[]
for fpl in stuff_pl:
	if fpl.is_file():
		fpl_sfx=fpl.suffix
		for s in valid_cin:
			if fpl_sfx==s:
				vfiles=vfiles+[fpl.name]

vfiles.sort()

if len(vfiles)>0:
	print("Archivos válidos:\n",vfiles)

else:
	print("ERROR: No se encontraron archivos válidos para esta configuración")
	exit()

if sys.argv[2]==vargs[0]:
	print("El script no se genera en el modo de prueba")
	exit()

if out_type==_out_pick:
	if len(sys.argv)==4:
		out_sel=sys.argv[3]

	else:
		print("ERROR: Falta el contenedor de salida")
		exit()

	valid_cout_args=[]
	for vout in valid_cout:
		valid_cout_args=valid_cout_args+[vout[1:]]

	if out_sel in valid_cout_args:
		print("Los archivos de salida serán en",out_sel)

	else:
		print("ERROR: El contenedor",out_sel,"no es aceptado por la configuración actual")
		exit()

else:
	if len(sys.argv)==4:
		print(_error_nvarg)
		exit()

maxfiles=len(vfiles)

ffmpeg_start="ffmpeg -i"

space=" "
dot="."
uscore="_"
lbreak="\n"
things="\""

scrlines="#!/bin/bash"+lbreak

for v in dvars:
	scrlines=scrlines+v[1:]+"=\"\""+lbreak

if mod_autoinc:
	scrlines=scrlines+"AUTONUM=1"+lbreak
	scrlines=scrlines+"MAXNUM="+str(maxfiles)+lbreak

if mod_appdir:
	scrlines=scrlines+"APPDIR="+things+str(_path_app_dir)+things+lbreak

for fname in vfiles:
	curr_stem=Path(fname).stem
	curr_csfx=Path(fname).suffix[1:]
	sec_init=ffmpeg_start+space+things+fname+things
	if mod_stem:
		sec_init="STEM=\""+curr_stem+"\";"+sec_init

	if mod_autoinc:
		sec_init=var_autoinc[1:]+"=$(seq -w $AUTONUM"+space+"$MAXNUM"+"|head -n1);"+sec_init

	if out_type==_out_same:
		sfx=curr_csfx

	if out_type==_out_pick:
		sfx=out_sel

	if out_type==_out_from:
		sfx=valid_cout[0][1:]

	outname=curr_stem+dot+sfx
	if outname==fname:
		outname=curr_stem+uscore+dot+sfx

	sec_out=things+outname+things

	if mod_autoinc:
		sec_out=sec_out+";AUTONUM=$(expr $AUTONUM + 1)"

	new=sec_init+space+ffmpeg_args+space+sec_out
	scrlines=scrlines+new+lbreak

try:
	with open("Convertir.sh","w") as scr:
		scr.write(scrlines)

except Exception as e:
	print("ERROR mientras se generaba el archivo")
	print(e)

else:
	print("Archivo 'Convertir.sh' escrito")
