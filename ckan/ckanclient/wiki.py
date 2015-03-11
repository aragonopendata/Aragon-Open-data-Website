#!/usr/bin/python
# -*- coding: utf-8 -*-
#modo de uso python wiki.py > fichero 
# Es importante básicamente debido a que imprime si realiza correctamente la sentencia de curl de insercion
import urllib

import config
import cx_Oracle
from time import time
from urllib import urlretrieve
import xlrd
import solr
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import os



def _download_xls_file(url):
	""" Download a xls with random name to hard disk"""
	dest = config.DOWNLOAD_TEMPORAL + "/" + str(int(time() * 100)) + ".xls"
	urlretrieve(url, dest)
	return dest

def _download_xml_file(url):
	""" Download a xls with random name to hard disk"""
	dest = config.DOWNLOAD_TEMPORAL + "/" + str(int(time() * 100)) + ".xml"
	print(dest)
	urlretrieve(url, dest)
	return dest

def _download_px_file(url):
	""" Download a px with random name to hard disk"""
	dest = config.DOWNLOAD_TEMPORAL + "/" + str(int(time() * 100)) + ".px"
	print(dest)
	urlretrieve(url, dest)
	return dest

#Función que dado un dato lo castea al tipo que sea. Devuelve en modo string
def castea_dato(dato):
# Según el tipo el valor del dato casteamos de una manera u otra
	if isinstance(dato, float) or isinstance(dato, int):
		datoCasteado=str(int(float(dato)))
	else:
		datoCasteado=dato.decode('iso-8859-15').encode('utf8')
	return datoCasteado


#Función en estado de desarollo
#sirve para obtener los datos del predicado de un fichero px
#Producción es un numero que si es 1 es para realizar en el servidor de produccion
#Si este es 0 es para preproduccion
#Si es 2 se tiene que hacer una conexión ssh entre el ordenador y el server.
#Si es -1 es para local
def _px_get(px_file, identificador, datoInicial, datoFinal, clave, dato, predicado, publicador, horientacion, produccion):
	if produccion==0:
		#PRE
		solrServer="http://preopendata.aragon.es/solrPRE"
	elif produccion==1:
		#PRO
		#Hay que modificar la configuración del apache o realizar unaa conexión ssh entre los servidores
		#solrServer="http://preopendata.aragon.es/solrPRO"
		solrServer="http://opendata.aragon.es/solr"
	elif produccion==2:
		#ssh
		solrServer="http://localhost:9999/solr"
	# Estos ficheros son log, ya que en el propio script ejecutará
	#logCurl = open("curl.log","w")
	#logCurl.write("#Se añaden sentencias de curl con fecha de "+str(datetime.now())+"\n")
	
	ficheroPx = open(px_file)
	
	if horientacion=="H":
		for i in range(1,int(dato)+1):
			linea = ficheroPx.readline()
			#print "Estamos en la linea "+ str(i)+ " y la linea es "+linea
			if i==int(clave):
				lineaClave=linea
				print "La linea donde se encuentra la clave es " + lineaClave
				#Borramos el comienzo hasta el = y el ; del final. Luego borramos las dobles comillas y parseamos
				arrayClaves = lineaClave[lineaClave.index("=")+1:len(lineaClave)-1].replace("\"", "").split(",");
				print "Las claves son "+', '.join(arrayClaves)
		
		
		#Salimos del bucle y en linea tendremos todos los datos que queremos obtener. Cerramos el fichero
		ficheroPx.close()
		datos=linea.split(" ")
		for i in range(int(datoInicial)-1, int(datoFinal)):
			
			valorClave = castea_dato(arrayClaves[i])
			valorDato = castea_dato(datos[i])
			print "Para la clave "+valorClave+ " tiene como dato "+valorDato+ " y el valor de i es "+str(i)
			
			#Ahora hay que meter el dato con curl
	
	elif horientacion=="V":
		i=1
		for linea in ficheroPx:
		
			if i==clave:
				lineaClave=linea
				print "La linea donde se encuentra la clave es " + lineaClave
				#Borramos el comienzo hasta el = y el ; del final. Luego borramos las dobles comillas y parseamos
				arrayClaves = lineaClave[lineaClave.index("=")+1:len(lineaClave)-1].replace("\"", "").split(",");
				print "Las claves son "+', '.join(arrayClaves)
			
			elif ((i>=filaInicial) and (i<=filaFinal)):
				valorClave = castea_dato(arrayClaves[i])
				valorDato = castea_dato(datos[i])
				print "Para la clave "+valorClave+ " tiene como dato "+valorDato
				
			
			i+=1
	
		ficheroPx.close()
	else:
		print "La horientacion tiene que ser H/V"
	
	
	
#Función en estado de desarollo
#sirve para obtener los datos del predicado de un fichero xls
#Producción es un numero que si es 1 es para realizar en el servidor de produccion
#Si este es 0 es para preproduccion
#Si es 2 se tiene que hacer una conexión ssh entre el ordenador y el server.
#Si es -1 es para local
def _xls_get(xls_file, identificador, sheet, filaInicial,filaFinal, clave,dato,predicado, publicador,orientacion, produccion):
	xls = xlrd.open_workbook(xls_file)
	print(int(sheet))
	sheet = xls.sheet_by_index(int(sheet)-1)
	
	
	if produccion==0:
		#PRE
		solrServer="http://preopendata.aragon.es/solrPRE"
	elif produccion==1:
		#PRO
		#Hay que modificar la configuración del apache o realizar unaa conexión ssh entre los servidores
		#solrServer="http://preopendata.aragon.es/solrPRO"
		solrServer="http://opendata.aragon.es/solr"
	elif produccion==2:
		#ssh
		solrServer="http://localhost:9999/solr"
	
	# create a connection to a solr server
	#SolR de Pre o PRO desde local (hay que poner los tuneles ssh
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan_wiki2')
	#SolR de localhost
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan-wiki')
	#s.add(doc)
	#s.add(id=555,valor='valor', uuid='holamundo001', predicado='predicado', publicador='publicador', clave='clave',version='0')
	#s.commit()
	# Abrimos los dos ficheros que contendran el historial del contenido subido a SolR y modificaciones a Oracle
	# Estos ficheros son log, ya que en el propio script ejecutará
	logCurl = open("curl.log","w")
	logCurl.write("#Se añaden sentencias de curl con fecha de "+str(datetime.now())+"\n")
	if orientacion=="V":
		if filaInicial==filaFinal:
			print("Tiene la misma fila inicial que final")
			row = int(filaInicial)-1
			print 'row es ', row
			claveAux= sheet.row_values(row,int(clave)-1,int(clave))
			#print("LA clave es "+ claveAux[0].replace('\xa0', ' '))
			
			#claveAux = str(claveAux[0].replace('\xc2\xa0', ' ')) #Hay que quitar los NO-BREAK SPACE
			claveAux = str(claveAux[0])
			valor= sheet.row_values(row,int(dato)-1,int(dato))
			
                
			# Según el tipo de la clave casteamos de una manera u otra
			if isinstance(claveAux[0], float):
				valorClave=str(int(float(claveAux[0])))
			else:
				valorClave=claveAux[0].encode('utf-8')
			print "Valor de la clave "+ valorClave

			# Según el tipo el valor del dato casteamos de una manera u otra
			if isinstance(valor[0], float) or isinstance(valor[0], int):
				valorCelda=str(int(float(valor[0])))
			else:
				valorCelda=valor[0].encode('utf-8')
			nomuuid = predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal)
			sentenciaCurl = "curl "+solrServer+"/ckan_wiki/update?commit=true -H 'Content-Type: text/xml' --data-binary '<add><doc><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc></add>'"
			docCurl = "<docUnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc>"
			logCurl.write(sentenciaCurl+"\n")
			##aquí va la ejecución del comando
			os.system(sentenciaCurl)

		else:
			for row in range(filaInicial-1,filaFinal,1):
				#print("_____________________________")
				#print("Comienza Registro")
				#print("fila: " + str(filaInicial) + " clave: " + str(int(clave)) + " dato: " + str(int(dato)))
				claveAux = sheet.row_values(row,int(clave)-1,int(clave))
				

				# Según el tipo de la clave casteamos de una manera u otra
				if isinstance(claveAux[0], float):
					valorClave=str(int(float(claveAux[0])))
				else:
					valorClave=claveAux[0].encode('utf-8')
				#print "Valor de la clave "+ valorClave

				valorAux = sheet.row_values(row,int(dato)-1,int(dato))
				#print("El valor es "+ str(valorAux[0]))
				# Según el tipo el valor del dato casteamos de una manera u otra
				if isinstance(valorAux[0], float) or isinstance(valorAux[0], int):
					valorCelda=str(int(float(valorAux[0])))
				else:
					valorCelda=valorAux[0].encode('utf-8')
				

				nomuuid = predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal)
				sentenciaCurl = "curl "+solrServer+"/ckan_wiki/update?commit=true -H 'Content-Type: text/xml' --data-binary '<add><doc><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc></add>'"
				docCurl = "<doc><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc>"
				logCurl.write(sentenciaCurl+"\n")
				##aquí va la ejecución del comando
				os.system(sentenciaCurl)

				#print("La sentencia Curl es "+sentenciaCurl)

				# s.add(id=identificador, uuid="'"+str(nomuuid)+"'", predicado="'"+str(predicado)+"'", publicador=str(publicador)+"'", clave="'"+str(valorClave)+"'", valor="'"+str(valorCelda)+"'", version="0")
				#s.commit()
				#Pruebas
				# add a document to the index
				#s.add(id=identificador, clave=valorClave, valor=valorCelda, publicador=publicador, predicado=predicado, uuid=nomuuid)
				#s.commit()
				#finPruebas
				#print("Se añadio el "+identificador)

#horientacion = H FUNCIONA
	else:
		if filaInicial==filaFinal:
			col = int(filaInicial)-1
			# Según el tipo de la clave casteamos de una manera u otra
			if isinstance(claveAux[0], float):
				valorClave=str(int(float(claveAux[0])))
			else:
				valorClave=claveAux[0].encode('utf-8')
			#print "Valor de la clave "+ valorClave

			valorAux = sheet.col_values(col,int(dato)-1,int(dato))
			#print("El valor es "+ str(valorAux[0]))
			# Según el tipo el valor del dato casteamos de una manera u otra
			if isinstance(valorAux[0], float) or isinstance(valorAux[0], int):
				valorCelda=str(int(float(valorAux[0])))
			else:
				valorCelda=valorAux[0].encode('utf-8')
			
			logCurl.write(sentenciaCurl+"\n")
			##aquí va la ejecución del comando
			os.system(sentenciaCurl)


			#s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valor[0]))
			#s.commit()

		else:
			for col in range(filaInicial-1,filaFinal,1):
			
			
			#print("_____________________________")
				#print("Comienza Registro")
				#print("fila: " + str(filaInicial) + " clave: " + str(int(clave)) + " dato: " + str(int(dato)))
				claveAux = sheet.col_values(col,int(clave)-1,int(clave))

				# Según el tipo de la clave casteamos de una manera u otra
				if isinstance(claveAux[0], float):
					valorClave=str(int(float(claveAux[0])))
				else:
					valorClave=claveAux[0].encode('utf-8')
				#print "Valor de la clave "+ valorClave

				valorAux = sheet.col_values(col,int(dato)-1,int(dato))
				#print("El valor es "+ str(valorAux[0]))
				# Según el tipo el valor del dato casteamos de una manera u otra
				if isinstance(valorAux[0], float) or isinstance(valorAux[0], int):
					valorCelda=str(int(float(valorAux[0])))
				else:
					valorCelda=valorAux[0].encode('utf-8')
				
				nomuuid = predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal)
				sentenciaCurl = "curl "+solrServer+"/ckan_wiki/update?commit=true -H 'Content-Type: text/xml' --data-binary '<add><doc><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc></add>'"
				docCurl = "<doc><field name=\"id\">"+str(identificador)+"</field><field name=\"clave\">"+valorClave+"</field><field name=\"valor\">"+valorCelda+"</field><field name=\"publicador\">"+publicador+"</field><field name=\"predicado\">"+predicado+"</field><field name=\"uuid\">"+nomuuid+"</field></doc>"
				logCurl.write(sentenciaCurl+"\n")
				##aquí va la ejecución del comando
				os.system(sentenciaCurl)
				
				#s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valorAux[0]))
				#s.commit()

	#cerramos los ficheros de log
	logCurl.write("\n\n")
	logCurl.close()

#Este hay que revisarlo
def _xml_get(xml_file, identificador, sheet, filaInicial,filaFinal, clave,dato,predicado, publicador,orientacion):

	tree = ET.parse(xml_file)
	root = tree.getroot()

	# create a connection to a solr server
	#SolR de Pre o PRO desde local (hay que poner los tuneles ssh
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan_wiki2')
	#SolR de localhost
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan-wiki')


	if (sheet!="" and sheet is not None):
		print("inicio: " + str(filaInicial))
		print("fin: " + str(filaFinal))
		print("dato: " + dato)
		print("clave: " + clave)
		print("bloque: " + str(sheet))

		for child in root:
			print(child.tag, child.attrib)

			# sheet - linea - clave/posic
			for x in range(filaInicial-1,filaFinal):
				print(root[sheet][x][int(clave)].text)
				print(root[sheet][x][int(dato)].text)
				claveAux = root[sheet][x][int(clave)].text
				valor = root[sheet][x][int(dato)].text

				#s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal) + "_" + str(x), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valor))
				#s.commit()

	else:
		for x in range (filaInicial-1,filaFinal-1):
			print(root[x][int(dato)-1].text)
			valor = root[x][int(dato)-1].text

			if clave != "" and clave is not None:
				print("clave es distinto de vacio: ")
				clave = root[x][int(clave)-1].text
			else:
				clave=""

			print("id=" + str(identificador))
			print("uuid=" + predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal) + "_" + str(x))
 			print("predicado=" + predicado)
			print("publicador=" + publicador)
			print("clave= " + clave)
			#s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valor[0]))
			#s.commit()



def eliminar_todas_entradas_solr():

	# create a connection to a solr server
	#SolR de Pre o PRO desde local (hay que poner los tuneles ssh
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan_wiki2')
	#SolR de localhost
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan-wiki')
	# add a document to the index
	#s.delete_query('*:*')
	#s.commit()
	logCurl = open("curl.log","w")
	logCurl.write("\n\n#Se van a BORRAR todos los datos en SolR con fecha de "+str(datetime.now())+"\n\n")
	logCurl.close()
	#Sentencia para borrar todo
	sentenciaBorrar = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<delete><query>*:*</query></delete>'"
	os.system(sentenciaBorrar)
	sentenciaCommit = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<commit />'"
	os.system(sentenciaCommit)
	sentenciaOptimize = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<optimize />'"
	os.system(sentenciaCommit)

def eliminar_entradas_solr(identificador):

	# create a connection to a solr server
	#print("Se elimina la entrada con id: " + str(identificador))
	#SolR de Pre o PRO desde local (hay que poner los tuneles ssh
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan_wiki2')
	#SolR de localhost
	#s = solr.SolrConnection('"+solrServer+"/solr/ckan-wiki')
	# add a document to the index
	#s.delete_query('id:' + str(identificador))
	#s.commit()
	logCurl = open("curl.log","w")
	logCurl.write("\n\n#Se van a BORRAR el datos con identificador " +str(identificador)+ " en SolR con fecha de "+str(datetime.now())+"\n\n")
	logCurl.close()
	sentenciaBorrar = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<delete><query>id:"+str(identificador)+"</query></delete>'"
	os.system(sentenciaBorrar)
	sentenciaCommit = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<commit />'"
	os.system(sentenciaCommit)
	sentenciaOptimize = "curl "+solrServer+"/ckan_wiki/update -H \"Content-type: text/xml\" --data-binary '<optimize />'"
	os.system(sentenciaCommit)

def main():
	if (len(sys.argv) != 2):
		print 'Este script Subir datos a SOLR'
		print 'Uso: python wiki.py pre|pro|ssh '
	else:
		if (str(sys.argv[1]).lower() != 'pre') and (str(sys.argv[1]).lower() != 'pro') and (str(sys.argv[1]).lower() != 'ssh'):
			print 'Este script Subir datos a SOLR'
			print 'Uso: python wiki.py pre|pro '
		else :
			if (str(sys.argv[1]).lower() == 'pre'):
				print 'Los cambios se va a realizar en PREOPENDATA'
				produccion = 0 #Prepoduccion
			elif (str(sys.argv[1]).lower() == 'pro'):
				print 'Los cambios se va a realizar en OPENDATA'
				produccion = 1 #Prepoduccion
			elif (str(sys.argv[1]).lower() == 'ssh'): #Este modo es más comodo para subir ya que no tengo que hacer contacto de pre con pro
				print 'Los cambios se va a realizar en OPENDATA usando los tuneles ssh'
				produccion = 2
			if produccion==0:
				#PRE
				connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.AST2_CONEXION_BD)
			elif produccion==1:
				#PRO
				connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.AST1_CONEXION_BD)
			elif produccion==2:
				#PRO usando tuneles ssh
				connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.AST1_CONEXION_BD)
	
	
	
	
			cursor = connection.cursor()

			#print("Eliminamos todo lo que hay en el solr de ckan_wiki2")
			#eliminar_todas_entradas_solr()
			#registros = cursor.execute("SELECT * FROM OPENDATA.opendata_v_wiki WHERE indexado=0 AND orientacion LIKE 'V' AND formato = 'XLS'")
			registros = cursor.execute("SELECT * FROM OPENDATA.opendata_v_wiki WHERE indexado=0")
			print sys.argv
			print len(sys.argv)
			force = False
			if (len(sys.argv) == 2):
				if sys.argv[1] == "force":
					print "si"
					force = True

			lista = []
			print("Comienza con los registros")

			logOracle = open("oracle.log","w")
			logOracle.write("#Se añaden sentencias de oracle con fecha de "+str(datetime.now())+"\n")
			i=1
			for r in registros:
				print "Comienza Registro " + str(i)
				print "Es " + str(r) 
				i+=1
				lista.append(r)
				if r[6] == 'XLS':
					print("es un XLS")
					xls_file = _download_xls_file(r[8])

					identificador= r[0]
					filaInicial = r[1]
					filaFinal = r[2]
					bloque = r[3]
					clave = r[4]
					dato = r[5]
					predicado = r[7]
					publicador = r[9]
					orientacion = r[10]
					indexado = r[11]
		#Aqui es donde realizamos lo de curl
					print "indexado: " + str(indexado) + " con id: " + str(identificador)
					print "El fichero esta " + str(r[8])
					print "El fichero es " + str(xls_file) 
					print "Identificador " + str(identificador)
					print "Fila inicial " + str(filaInicial)
					print "bloque " + str(bloque)
					print "predicado " + str(predicado)
					print "publicador " + str(publicador)
					print "horientacion " + str(orientacion)

					#eliminar_todas_entradas_solr()

					if (force == True or indexado!=1):
						if (indexado==1):
							eliminar_entradas_solr(identificador)
						_xls_get(xls_file,identificador,bloque,filaInicial,filaFinal, clave, dato, predicado, publicador, orientacion, produccion)
						connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
						cursor = connection.cursor()
						#eliminar_todas_entradas_solr()
						#cursor.execute("UPDATE opendata_wiki set indexado=1 where id=" + str(identificador))
						#connection.commit()
						#cursor.execute("EXEC OPENDATA_PCK_ACCIONES.OPENDATA_PR_UP_WIKI("+str(identificador)+", 1)") ESto no vale, así que hay que ejecutar los execute a parte hasta hacer las modificaciones pertinentes
						logOracle.write("EXEC OPENDATA_PCK_ACCIONES.OPENDATA_PR_UP_WIKI("+str(identificador)+", 1)\n")
				               
				elif r[6] == 'XML':
					print("es XML")
					#estos habría que revisarlos, pero me supongo que estaran mal
					identificador= r[0]
					filaInicial = r[1]
					bloque = r[2]
					clave = r[3]
					dato = r[4]
					predicado = r[6]
					filaFinal = r[8]
					publicador = r[9]
					orientacion = r[10]
					indexado = r[11]

					print "indexado: " + str(indexado) + " con id: " + str(identificador)
		 
					xml_file = _download_xml_file(r[7])

					if (force == True or indexado!=1):
						if (indexado==1):
							eliminar_entradas_solr(identificador)
				            
							# _xml_get(xml_file,identificador,bloque,filaInicial,filaFinal, clave, dato, predicado, publicador, orientacion)
							#connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
							#cursor = connection.cursor()
							#eliminar_todas_entradas_solr()
							#cursor.execute("UPDATE opendata_wiki set indexado=1 where id=" + str(identificador))
							#connection.commit()
				elif r[6] == 'PX':
					print("es PX")
					px_file = _download_px_file(r[8])

					identificador= r[0]
					filaInicial = r[1]
					filaFinal = r[2]
					bloque = r[3]
					clave = r[4]
					dato = r[5]
					predicado = r[7]
					publicador = r[9]
					orientacion = r[10]
					indexado = r[11]
					#Aqui es donde realizamos lo de curl
					print "indexado: " + str(indexado) + " con id: " + str(identificador)
					print "El fichero esta " + str(r[8])
					print "El fichero es " + str(px_file) 
					print "Identificador " + str(identificador)
					print "Fila inicial " + str(filaInicial)
					print "bloque " + str(bloque)
					print "predicado " + str(predicado)
					print "publicador " + str(publicador)
					print "horientacion " + str(orientacion)
					if (force == True or indexado!=1):
						if (indexado==1):
							eliminar_entradas_solr(identificador)
						_px_get(px_file,identificador,filaInicial,filaFinal, clave, dato, predicado, publicador, orientacion, produccion)
						#connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
						#cursor = connection.cursor()
						#eliminar_todas_entradas_solr()
						#cursor.execute("UPDATE opendata_wiki set indexado=1 where id=" + str(identificador))
						#connection.commit()
						#cursor.execute("EXEC OPENDATA_PCK_ACCIONES.OPENDATA_PR_UP_WIKI("+str(identificador)+", 1)") ESto no vale, así que hay que ejecutar los execute a parte hasta hacer las modificaciones pertinentes
						#logOracle.write("EXEC OPENDATA_PCK_ACCIONES.OPENDATA_PR_UP_WIKI("+str(identificador)+", 1)\n")


			logOracle.write("\n\n")
			logOracle.close()
			cursor.close()
			connection.close()
	
	
	print 'FIN'


main()

