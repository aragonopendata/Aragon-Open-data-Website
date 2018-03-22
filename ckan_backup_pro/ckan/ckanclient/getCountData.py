#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
DIR='/var/www/wolfcms/public/'


#Método que obtiene el numero de dataset y recursos haciendo uso de la api
#Nombre es el nombre final que tendra el fichero y servidor el servidor donde se hara preopendata o opendata
def obtenDatos(nombre, servidor):
	sentenciaCurl = 'curl  \"' + servidor+'/catalogo/api/getDataCount\" > '+ DIR+nombre
	os.system(sentenciaCurl)
	with open(DIR+nombre) as data_file:
		datos = json.load(data_file)
	os.remove(DIR+nombre)
	return datos
#	pprint(data)
#	print data[0]["datasetCount"]

#método que genera el script con los datos de la variable
def generaJavascript(datos):
	fichero=DIR+'getDataCount.js'
	f = open(fichero, "w")
#	f.write("<script type=\"text/javascript\">\n")
	for dato in datos:
		f.write('\tvar datasetCount = '+str(dato["datasetCount"])+';\n')
		f.write('\tvar resourceCount = '+str(dato["resourceCount"])+';\n')
#	f.write("</script>\n")
	f.close()
	
	
def main():
	if (len(sys.argv) == 2):
		if (str(sys.argv[1]).lower() != 'pre') and (str(sys.argv[1]).lower() != 'pro'):
			print 'Este script obtiene el número de dataset y recursos haciendo uso de la api y genera un javascript que contiene su valor'
			print 'Uso: python getCountData.py pre|pro'
		else:
			servidor=''
			if (str(sys.argv[1]).lower() == 'pre'):
				servidor='http://preopendata.aragon.es'
			elif (str(sys.argv[1]).lower() == 'pro'):
				servidor='http://opendata.aragon.es'
			datos=obtenDatos('temporal.json', servidor)
			generaJavascript(datos)
	else:
		print 'Este script obtiene el número de dataset y recursos haciendo uso de la api y genera un javascript que contiene su valor'
		print 'Uso: python getCountData.py pre|pro'

main()
