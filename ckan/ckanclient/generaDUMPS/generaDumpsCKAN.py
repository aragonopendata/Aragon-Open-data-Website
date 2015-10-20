 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#Este script sirve para hacer dumps de la base de datos de ckan

import sys
import os
import re
from os import path
import time
from time import gmtime, strftime
import zipfile


DIRDUMP ="/data/dumps/ddbb/"
compresion = zipfile.ZIP_DEFLATED

#Hace un listado de los dumps dentro del directorio DIRDUMP y devuelve sus nombres en una array
def lsSQL():
	lstFiles=[]
	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(DIRDUMP)   #os.walk()Lista directorios y ficheros
	for root, dirs, files in lstDir:
		for fichero in files:
			(nombreFichero, extension) = path.splitext(fichero)
			if(extension == ".sql"):
				lstFiles.append(nombreFichero+extension)
	return lstFiles


#Da el tiempo del ficheros
def dataFile(pathFile):
	if path.isfile(pathFile):
		return path.getmtime(pathFile)
	else:
		return ""
		

#obten las fechas de los ficheros donde estan el dump. Las fechas son del tipo time.localtime
def obtenFechas(ficheros):
	lstData=[]
	for fichero in ficheros:
		time.localtime(dataFile(DIRDUMP+fichero))
		lstData.append(time.localtime(dataFile(DIRDUMP+fichero)))
	return lstData

#obtenemos el nombre del fichero más antiguo
def ficheroMasAntiguo():
	ficheros = lsSQL()
	fechas=obtenFechas(ficheros)
	if len(fechas)==0:
		print 'No hay ficheros'
		return None
	elif len(fechas)==1:
		print 'Sólo hay uno'
		return ficheros[0]
	else:
		dataMasAntigua = fechas[0]
		i=0
		x=0 #la x-esima campo del array que es el que sera más antiguo
		while i<len(fechas):
			if dataMasAntigua > fechas[i]:
				dataMasAntigua = fechas [i]
				x=i
			i+=1
		return ficheros[x]
		


#Genera el nombre que tiene que tener el dump
def generaNombreFichero():
	return "ckan_"+strftime("%Y%m%d-%H:%M:%S", time.localtime(time.time()))+"_dump.sql"
	

#Borrar fichero 
def borraFicheroMasAntiguo():
	ficheroAntiguo=ficheroMasAntiguo()
	if path.exists(DIRDUMP+ficheroAntiguo):
		print 'Se va a borrar el fichero', ficheroAntiguo
		os.remove(DIRDUMP+ficheroAntiguo)

#Creamos el fichero
def crearFicheroDump(desarrollo=None):
	print 'desarrollo es',desarrollo
	if desarrollo is not None:
		archi=open(DIRDUMP+generaNombreFichero(),'w')
		#Aki generamos el fichero
		archi.close()
		print 'Creamos el dump',generaNombreFichero()
	else:
		print 'Metemos haciendo uso del paster'
		os.chdir(DIRDUMP)
		print '. /usr/lib/ckan/default/bin/activate'
		print 'paster --plugin=ckan db dump --config=/etc/ckan/default/production.ini '+generaNombreFichero()
		print 'deactivate'
		#comando= ". /usr/lib/ckan/default/bin/activate"
		#os.system(comando)
		comando ="paster --plugin=ckan db dump --config=/etc/ckan/default/production.ini "+generaNombreFichero()
		os.system(comando)
		#comando = "deactivate"
		#os.system(comando)
		print 'Se finaliza de hacer el dump de hacer el dump'
	
#Esta función lo que hace es un zip de todo los  ficheros y los borra
def comprimeDumps():
	ficheros=lsSQL()
	print 'Creando el archivo Zip'
	zf = zipfile.ZipFile(DIRDUMP+'dumps_de_'+strftime("%Y-%m", time.localtime(time.time()))+'.zip', mode='w')
	os.chdir(DIRDUMP)
	try:
		print 'Agregamos los ficheros'
		for fichero in ficheros:
			if path.exists(fichero):
				zf.write(fichero, compress_type=compresion)
				os.remove(fichero)
	finally:
		print 'Cerrando archivo'
		zf.close()

	
def main():
	if (len(sys.argv) == 1):
		ficheros=lsSQL()
		if len(ficheros)<5:
			#Hacemos el dump
			#crearFicheroDump(desarrollo='desarrollo')
			crearFicheroDump()
		elif len(ficheros)==5:
			borraFicheroMasAntiguo()
			#crearFicheroDump(desarrollo='desarrollo')
			crearFicheroDump()
		else:
			print 'Tenemos', len(ficheros),'Ficheros y procedemos a borrar'
			while len(ficheros)>=5:
				borraFicheroMasAntiguo()
				ficheros=lsSQL()
				print 'Tenemos', len(ficheros),'Ficheros y procedemos a borrar'
			#crearFicheroDump(desarrollo='desarrollo')
			crearFicheroDump()
	elif (len(sys.argv) == 2):
		if (str(sys.argv[1]).lower() == 'zip'):
			comprimeDumps()
		else:
			print 'Este script crea dumps de la base de datos'
			print 'Uso: python generaDumpsCKAN.py [zip]'
	else:
		print 'Este script crea dumps de la base de datos'
		print 'Uso: python generaDumpsCKAN.py [zip]'
	
	
	
main()
