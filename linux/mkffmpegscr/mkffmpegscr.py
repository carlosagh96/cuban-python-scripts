#!/usr/bin/python3.9

# Programa para generar scripts de Bash para transcodificar con FFmpeg
# Solo se tiene en cuenta un archivo de entrada y uno de salida por cada órden/línea
# Agumentos: N [e|p] C
# N = No. de la configuración
# e = Modo escritura
# p = Modo prueba (no genera el script)
# C = Contenedor de los archivos de salida (Depende de la configuración)
# Las configuraciones se guardan en un JSON, que debe nombrarse igual que este script
# Llevado a diccionario:
# → Cada clave es el título de la configuración (texto)
# → Cada valor son los elementos de la configuración (lista)
# → Elem. 0: Las opciones de configuración de FFmpeg (texto)
# → Elem. 1: Los archivos válidos para la configuración actual (lista)
# → Elem. 2: (OPCIONAL) Argumento extra para declarar el contenedor de salida (lista)

# Escrito por Carlos Alberto González hernández
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
_thyname=_path_app_pl.stem
_path_configfile=str(_path_app_dir)+"/"+str(_thyname)+".json"

print(sys.argv)

with open(_path_configfile) as cfgs:
	cfg_raw_lst=cfgs.readlines()

cfg_raw=""
for line in cfg_raw_lst:
	cfg_raw=cfg_raw+line.strip()

cfgs=json.loads(cfg_raw)

aconfigs=list(cfgs.keys())

if len(sys.argv)>1:
	pass

else:
	c=0
	print("Configuraciones disponibles")
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
	if len(dvars)>0:
		var_autoinc="$AUTOINC"
		var_stem="$STEM"
		print("Variables detectadas en las opciones de FFmpeg:\n",dvars)
		if var_autoinc in dvars:
			print(var_autoinc,"→ Variable especial: Autoincremento")
			dvars.remove(var_autoinc)
			mod_autoinc=True

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
lbreak="\n"
things="\""

scrlines="#!/bin/bash"+lbreak

for v in dvars:
	scrlines=scrlines+v[1:]+"=\"\""+lbreak

if mod_autoinc:
	scrlines=scrlines+var_autoinc[1:]+"=1"+lbreak

for fname in vfiles:
	curr_stem=Path(fname).stem
	curr_csfx=Path(fname).suffix[1:]
	sec_init=ffmpeg_start+space+things+fname+things
	if mod_stem:
		sec_init="STEM=\""+curr_stem+"\";"+sec_init

	if out_type==_out_same:
		sfx=curr_csfx

	if out_type==_out_pick:
		sfx=out_sel

	if out_type==_out_from:
		sfx=valid_cout[0]

	sec_out=things+curr_stem+"_."+sfx+things

	if mod_autoinc:
		sec_out=sec_out+";"+var_autoinc+"=$(expr $"+var_autoinc+" +1)"

	new=sec_init+space+ffmpeg_args+space+sec_out
	scrlines=scrlines+new+lbreak

with open("Convertir.sh","w") as scr:
	scr.write(scrlines)
