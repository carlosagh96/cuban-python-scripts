#!/usr/bin/python3.9
# Programa para cifrado de archivos bajo la especificación Fernet
# Información usada para escribir este programa → https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/

from cryptography.fernet import Fernet
from os import name as osname
from pathlib import Path
from sys import argv

_app_dir=argv[0]
_app_name=Path(_app_dir).name
_app_stem=Path(_app_dir).stem
_key_name=_app_stem+".fernet.key"

_megabyte=1048576
_megabyte_enc=1398200

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

if len(argv)==1:

	print("Guía de uso de "+_app_name)
	print("Programa para cifrado de archivos bajo la especificación Fernet\nMás información aquí → https://github.com/fernet/spec/blob/master/Spec.md")

	print("\nArgumentos:")
	print("kg → Generar una clave nueva en el directorio actual")
	print("ks → Ver la clave")
	print("en → Cifrar archivos")
	print("de → Descifrar archivos")

	print("\nModo de empleo:")
	print("Primero debe generar una clave en el directorio donde manda a ejecutar el programa. Todo archivo que cifre con esta clave debe ser descifrado con dicha clave")
	print("Tanto para cifrar como descifrar, opcionalmente se puede especificar una ruta para cifrar un archivo específico o todos los archivos de un directorio")

	print("\nEn el directorio donde manda a ejecutar el programa:")
	print("La clave para cifrar o descifrar se llama \""+_key_name+"\"")
	print("Los archivos resultantes al cifrar se guardan en \""+_app_name+".en\"")
	print("Los archivos resultantes al descifrar se guardan en \""+_app_name+".de\"")

	print("\nEscrito por Carlos Alberto González Hernández\nTelegram: https://t.me/CarlosAGH\n2021-10-21")

if len(argv)>1:

	if argv[1]=="kg":
		key=Fernet.generate_key()
		with open(_key_name,"wb") as fkey:
			fkey.write(key)

	elif argv[1]=="ks":
		if Path(_key_name).exists():
			print(readkey())

		else:
			print("ERROR: La clave \""+_key_name+"\" no está presente")

	elif argv[1]=="en" or argv[1]=="de":

		if argv[1]=="en":
			job=_job_enc

		if argv[1]=="de":
			job=_job_dec

		odir=_app_stem+job

		fernetkey=readkey()
		key=Fernet(fernetkey)

		tfiles=[]
		if len(argv)==3:
			gpath_raw=argv[2]
			if osname=="nt":
				gpath_pl=Path(r""+gpath_raw)
			
			else:
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
			outdir=Path(_app_name+job)

			if not outdir.exists():
				outdir.mkdir()

			if _job_enc in job:
				print("Cifrando...")
				chunksize=_megabyte

			if _job_dec in job:
				print("Descifrando...")
				chunksize=_megabyte_enc

			for tfile in tfiles:
				tfile_name=tfile.name
				outfile_pl=outdir.joinpath(tfile_name)
				print(str(tfile),"→",outfile_pl)
				try:
					if outfile_pl.exists():
						raise Exception("El archivo de salida ya existe")

					with open(str(tfile),"rb") as infile:
						while True:
							chunk=infile.read(chunksize)

							if len(chunk)>0:
								if _job_enc in job:
									data=key.encrypt(chunk)

								if _job_dec in job:
									data=key.decrypt(chunk)

								with open(str(outfile_pl),"ab") as outfile:
									outfile.write(data)

							else:
								break

				except Exception as e:
					print("ERROR:\n"+str(e))

				else:
					print("Completado")

	else:
		print("ERROR: Argumento(s) no válido(s)")
