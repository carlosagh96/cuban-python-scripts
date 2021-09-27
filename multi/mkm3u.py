#!/usr/bin/python3.5
# Script para crear listas de reproducción M3U
# Escrito por Carlos Alberto González Hernández

import argparse
import os
import sys

from pathlib import Path

# print("sys.argv =",sys.argv)

ksuffixes=[".avi",".cue",".flac",".flv",".m4a",".m4v",".m4v",".mkv",".mp3",".mp4",".mpg",".ogg",".rm",".rmvb",".wav",".webm",".wma"]

m3u_filename=Path("./").absolute().name+".m3u"

# print("m3u_filename =",m3u_filename)

filelist_raw=[]

if len(sys.argv)>1:
	index=0
	for f in sys.argv:
		if index>0:
			if os.path.isfile(f):
				filelist_raw=filelist_raw+[f]

		index=index+1
else:
	filelist_raw=os.listdir("./")

if len(filelist_raw)==0:
	exit()

filelist_raw.sort()

# print("filelist_raw =",filelist_raw)

m3u_content=[]
for f in filelist_raw:
	fsuffix=Path(f).suffix
	for s in ksuffixes:
		if fsuffix==s:
			m3u_content=m3u_content+[f]

if len(m3u_content)==0:
	exit()

# print("m3u_content =",m3u_content)

with open(m3u_filename,"w") as m3u_file:
	for line in m3u_content:
		m3u_file.write(line+"\n")
