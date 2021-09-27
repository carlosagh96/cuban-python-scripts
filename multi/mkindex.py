#!/usr/bin/python3.5
# Script para crear un archivo "index.html" a partir de páginas web guardadas
# Escrito por Carlos Alberto González Hernández

# Modo de empleo

# Para crear un archivo "index.html" con este script, debe crear para el directorio donde están las páginas, un archivo de configuración con el mismo nombre del script pero con sufijo "conf"
# Por ejemplo, si este script se llama "mkindex.py" o "mkindex", el archivo de configuración debe llamarse "mkindex.cfg"
#
# El formato del archivo de configuración es sencillo:
# La primera línea es el título, la segunda línea es una descripción (solo un párrafo no más) y la tercera es el pie de página, tan sencillo como eso. El título es obligatorio, todo lo demás es opcional

# Para ejecutar en sistemas Unix, cree un enlace o haga una copia a /usr/bin o /bin

# 2021-08-22

title=""
description=""
footer=""

# Ejecución del script

import os
import sys
import urllib.parse

from pathlib import Path

errormsg=""

if len(errormsg)==0:
	ls_raw=os.listdir()

	if len(ls_raw)==0:
		errormsg="Este directorio está vacío"

if len(errormsg)==0:
	program_path=sys.argv[0]
	program_name=Path(program_path).name

	if program_name.endswith(".py"):
		configfile=program_name[:-3]+".cfg"

	else:
		configfile=program_name+".cfg"

	if not os.path.exists(configfile):
		errormsg="El archivo de configuración \""+configfile+"\" no sestá presente en este directorio"

if len(errormsg)==0:
	title=""
	footer=""

	try:

		with open(configfile,"rt") as cfg:
			cfg_dump=cfg.readlines()

		if len(cfg_dump)==0:
			raise Exception("El archivo está vacío")

		else:
			title=cfg_dump[0].strip()
			if len(cfg_dump)>0:
				try:
					description=cfg_dump[1].strip()
				except:
					pass

				try:
					footer=cfg_dump[2].strip()
				except:
					pass

	except Exception as e:
		errormsg="Fallo de lectura del archivo de configuración. "+str(e)

if len(errormsg)==0:
	ls_html=[]

	for line in ls_raw:
		if not line=="index.html":
			if line.endswith(".html"):
				ls_html=ls_html+[line]

	if len(ls_html)>0:
		ls_html.sort()

	else:
		errormsg="No hay archivos HTML para procesar"

if len(errormsg)==0:
	with open("index.html","wt") as ifile:
		ifile.write("<html>\n")
		ifile.write("\t<meta content=\"text/html;charset=utf-8\">\n")
		ifile.write("\t<head>\n")
		ifile.write("\t\t<title>\n")
		ifile.write("\t\t\t"+title+"\n")
		ifile.write("\t\t</title>\n")
		ifile.write("\t</head>\n")
		ifile.write("\t<body>\n")
		ifile.write("\t\t<p><h1>"+title+"</h1>\n")

		if len(description)>0:
			ifile.write("\t\t<p>"+description+"\n")
		else:
			print("No hay descripción")

		for link_raw in ls_html:
			name=link_raw[:-5]
			link=urllib.parse.quote_plus(link_raw)
			ifile.write("\t\t<p><a href=\""+link_raw+"\">"+name+"</a>\n")

		if len(footer)>0:
			ifile.write("\t\t<p>"+footer+"\n")
		else:
			print("No hay pie de página")

		ifile.write("\t</body>\n")
		ifile.write("</html>\n")

if len(errormsg)>0:
	print("Error:",errormsg)

else:
	print("Archivo \"index.html\" terminado")
