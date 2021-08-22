#!/usr/bin/python3.5
# Script para comprobar integridad de archivos a partir de listas MD5 o SHA256

# Las listas pueden crearse usando este programa. También pueden crearse desde cualquier sistema UNIX de esta forma:
# $ md5sum *|sed 's/ */\t/'>archivos.md5
# $ sha256sum *|sed 's/ */\t/'>archivos.sha256

# Escrito por Carlos Alberto González Hernández
# Telegram: https://t.me/CarlosAGH

# 2021-08-12

import hashlib
import os
import random
import sys
import time

from pathlib import Path

proceed=False

tab="\t"

md5file="md5"
sha256file="sha256"
hashtypes=[md5file,sha256file]

chosenfile=""

error_suffix="Error: El tipo de hash no es válido, revise el sufijo"
error_file_missing="Error: El archivo no está presente en el directorio actual"


arg_build="-gen"
arg_check="-ver"

def get_some_stuff():
	htype=""
	namae=""
	autoname=False
	if len(sys.argv)==3:
		namae_tmp=sys.argv[2]
		if namae.startswith(".") or namae.startswith("-") or namae.startswith("-"):
			if len(namae)>1:
				idx=0
				for c in namae:
					namae=namae+c
					idx=idx+1

			else:
				autoname=True

		else:
			namae=sys.argv[2]

	else:
		autoname=True

	if autoname:
		if sys.argv[1]==arg_build:
			namae=time.strftime("%Y-%m-%d-%H-%M-%S")+"."+hashtypes[0]

		if sys.argv[1]==arg_check:
			namae="revisar."+hashtypes[0]

		print("Usando nombre automático:\n\""+namae+"\"")

	f=Path(namae)
	s=f.suffix
	valid=False
	for h in hashtypes:
		if "."+h==s:
			htype=h
			valid=True

	return [namae,htype,valid]

def make_hash(fname,htpe):
	if htpe==md5file:
		d=hashlib.md5()

	if htpe==sha256file:
		d=hashlib.sha256()

	if os.path.exists(fname):
		with open(fname,"rb") as f:
			for chunk in iter(lambda: f.read(1024), b""):
				d.update(chunk)

		out=d.hexdigest()

	else:
		out="No se encuentra presente"

	return out

if len(sys.argv)>1 and len(sys.argv)<4:
	if sys.argv[1]==arg_check:
		stuff=get_some_stuff()
		legit=stuff[2]
		if legit:
			chtype=stuff[1]
			chksumfile=stuff[0]
			if os.path.exists(chksumfile):
				if os.path.isfile(chksumfile):
					tfile=open(chksumfile,"r")
					lines_raw=tfile.readlines()
					lines=[]
					try:
						for line in lines_raw:
							splitme=line.split(tab)
							ohash=splitme[0]
							thefile=splitme[1].strip()
							lines=lines+[[ohash,thefile]]

					except Exception as e:
						print(e)

					else:
						if len(lines)>0:

							errlist=[]

							logfile=open(chksumfile+".log","w")

							print("\nVerificando integridad de los archivos presentes con el archivo:\n\""+chksumfile+"\"\n")
							for i in lines:
								calculated=make_hash(i[1],chtype)
								if i[0]==calculated:
									v=True

								else:
									v=False

								print_this="Archivo = "+i[1]+"; Hash guardado = "+i[0]+"; Hash calculado = "+calculated
								logfile.write(print_this+"\n")
								print(print_this)

								if not v:
									errlist=errlist+[i[1]]

							if len(errlist)>0:
								if len(errlist)==1:
									print_this="\nSe detectó un error\n"

								else:
									print_this="\nSe detectaron errores\n"

								logfile.write("# Errores\n")
								print(print_this)

								for e in errlist:
									logfile.write(str(e)+"\n")
									print(e)

								print("")

							else:
								print("\nNo se detectaron errores\n")

							logfile.close()

						else:
							print("???")

					tfile.close()

				else:
					print("Error: La ruta no es un archivo")

			else:
				print(error_file_missing)

		else:
			print(error_suffix)

	elif sys.argv[1]==arg_build:
		stuff=get_some_stuff()
		legit=stuff[2]
		if legit:
			chksumfile=stuff[0]
			chtype=stuff[1]
			lsout_raw=os.listdir(".")
			if len(lsout_raw)>0:
				lsout_raw.sort()
				lsout=[]
				for fse in lsout_raw:
					if os.path.isfile(fse):
						lsout=lsout+[fse]

				if len(lsout)>0:
					print("\nCalculando hashes y escribiendo archivo \""+chksumfile+"\"\n")
					tfile=open(chksumfile,"w")
					for namae in lsout:
						thehash=make_hash(namae,chtype)
						tfile.write(thehash+tab+namae+"\n")
						print("Archivo =",namae,"; Hash obtenido =",thehash)

					tfile.close()

				else:
					print("No hay archivos")

			else:
				print("Aquí no hay nada")

	else:
		print("Error: Argumento desconocido:",sys.argv[1])
		print(sys.argv)

elif len(sys.argv)>3:
	print("Error: Cantidad de argumentos errónea")

else:
	program_raw=sys.argv[0]
	program=Path(program_raw).name
	print("\nGuía de usuario del programa \""+program+"\"\n")
	print("Este programa verifica la autenticidad de archivos a partir de un archivo de hashes, que también se crean con este programa.\n")
	print("El programa trabaja con los archivos que se tengan delante. Si va a verificar archivos, el archivo de hashes debe estar junto a los archivos. Si va a generar un archivo de hashes, el archivo de hashes se genera según los archivos presentes. La velocidad de procesamiento depende de las prestaciones de su equipo y del tamaño de los archivos.\n")
	print("Cuando se verifican los archivos, se va mostrando el progreso archivo por archivo y al final se dice si hubo o no errores y se dice cuáles son los archivos con errores. Junto a esto se crea también un archivo LOG que sirve de informe.\n")
	print("Los archivos de hashes deben tener un sufijo (extensión) que identifique al hash, por ejemplo, un archivo de hashes MD5 lleva el sufijo \".md5\".\n")
	ah=""
	htc=0
	for ht in hashtypes:
		ah=ah+ht
		htc=htc+1
		if htc<len(hashtypes):
			ah=ah+", "

	print("Los hashes/sufijos aceptados son "+ah+". El hash MD5 se usa de forma predeterminada.\n")
	print("Uso general y ejemplos\n")
	print(tab+program+" [ "+arg_build+" | "+arg_check+" ] "+"\"Nombre Del Archivo.hash\"\n")
	print("Ejemplo: Verificar archivos usando el archivo de hashes por omisión (revisar.md5)\n")
	print(tab+program+" "+arg_check+"\n")
	print("Ejemplo: Generar archivo de hashes con nombre automático. El nombre automático en este caso se basa en la fecha y la hora.\n")
	print(tab+program+" "+arg_build+"\n")
	print("Ejemplo: Verificar archivos usando un archivo de hashes específico\n")
	r1=random.randint(0,len(hashtypes)-1)
	print(tab+program+" "+arg_check+" "+"Recibidos."+hashtypes[r1]+"\n")
	r2=random.randint(0,len(hashtypes)-1)
	print("Ejemplo: Generar archivo de hashes bajo un nombre específico\n")
	print(tab+program+" "+arg_check+" "+"Enviar."+hashtypes[r2]+"\n")
	print("Versión 2021-08-13. Programa escrito por Carlos Alberto González Hernández. Telegram https://t.me/CarlosAGH\n")
