#!/usr/bin/python3.9
# Programa para cifrado de archivos bajo la especificación Fernet
# Más información aquí → https://github.com/fernet/spec/blob/master/Spec.md
# Información usada para escribir este programa → https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/

import os
import sys

from cryptography.fernet import Fernet
from pathlib import Path

_app_dir=sys.argv[0]
_app_name=Path(_app_dir).name
_app_stem=Path(_app_dir).stem
_key_name=_app_stem+".fernet.key"

_kilobyte=1024
_megabyte=_kilobyte*_kilobyte

_job_enc=".en"
_job_dec=".de"

def readkey():
	with open(_key_name) as fkey:
		k=fkey.read()

	return k

def pathscan(plobject):
	ls_raw=list(Path(plobject).glob("*"))

	ls_files=[]
	for fse in ls_raw:
		if fse.is_file():
			ls_files=ls_files+[fse]

	del ls_raw

	return ls_files

if len(sys.argv)==1:

	print("Guía de uso de "+_app_name)
	print("Programa para cifrado de archivos bajo la especificación Fernet\nMás información aquí → https://github.com/fernet/spec/blob/master/Spec.md")

	print("\nArgumentos:")
	print("kg → Generar una clave nueva en el directorio actual")
	print("ks → Ver la clave")
	print("en → Cifrar archivos")
	print("de → Descifrar archivos")

	print("\nModo de empleo:")
	print("Primero debe generar una clave (\""+_key_name+"\") en el directorio donde manda a ejecutar el programa. Todo archivo que cifre con esta clave debe ser descifrado con esta misma clave")
	print("Tanto para cifrar como descifrar, opcionalmente se puede especificar una ruta para cifrar un archivo específico o todos los archivos de un directorio")

	print("\nEscrito por Carlos Alberto González Hernández\nTelegram: https://t.me/CarlosAGH")

if len(sys.argv)>1:

	if sys.argv[1]=="kg":
		key=Fernet.generate_key()
		with open(_key_name,"wb") as fkey:
			fkey.write(key)

	elif sys.argv[1]=="ks":
		if os.path.exists(_key_name):
			print(readkey())

		else:
			print("ERROR: La clave \""+_key_name+"\" no está presente")

	elif sys.argv[1]=="en" or sys.argv[1]=="de":

		if sys.argv[1]=="en":
			job=_job_enc

		if sys.argv[1]=="de":
			job=_job_dec

		odir=_app_stem+job

		fernetkey=readkey()
		key=Fernet(fernetkey)

		tfiles=[]
		if len(sys.argv)==3:
			gpath_raw=sys.argv[2]
			gpath_pl=Path(gpath_raw)

			if gpath_pl.exists():
				if gpath_pl.is_file():
					tfiles=[gpath_pl]

				elif gpath_pl.is_dir():
					tfiles=pathscan(gpath_pl)

				else:
					print("???")

			else:
				print("ERROR: La ruta no existe")

		else:
			gpath_pl=Path(".")
			tfiles=pathscan(gpath_pl)

		tfiles_copy=tfiles.copy()
		for tfile in tfiles_copy:
			if tfile.name==_app_name:
				tfiles.remove(Path(_app_name))

			if tfile.name==_key_name:
				tfiles.remove(Path(_key_name))

		if len(tfiles)==0:
			print("ERROR: No hay archivos para cifrar")

		else:
			print("tfiles =",tfiles)

			outdir=Path(_app_name+job)

			if not outdir.exists():
				outdir.mkdir()

			if _job_enc in job:
				print("Cifrando...")

			if _job_dec in job:
				print("Descifrando...")


			for tfile in tfiles:
				tfile_name=tfile.name
				outfile_pl=outdir.joinpath(tfile_name)
				print(tfile,"→",outfile_pl)
				with open(str(tfile),"rb") as infile:
					while True:
						chunk=infile.read(_megabyte)

						if len(chunk)>0:
							if _job_enc in job:
								data=key.encrypt(chunk)

							if _job_dec in job:
								data=key.decrypt(chunk)

							with open(str(outfile_pl),"wb") as outfile:
								outfile.write(data)

						else:
							break

	else:
		print("ERROR: Argumento(s) no válido(s)")
