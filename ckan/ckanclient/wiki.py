#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib

import config
import cx_Oracle
from time import time
from urllib import urlretrieve
import xlrd
import solr
import sys
import xml.etree.ElementTree as ET



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


def _xls_get(xls_file, identificador, sheet, filaInicial,filaFinal, clave,dato,predicado, publicador,orientacion):
        xls = xlrd.open_workbook(xls_file)
        print(int(sheet))
        sheet = xls.sheet_by_index(int(sheet)-1)

        # create a connection to a solr server
        s = solr.SolrConnection('http://localhost:8983/solr/ckan_wiki')
#	s.add(doc)
	#s.add(id=555,valor='valor', uuid='holamundo001', predicado='predicado', publicador='publicador', clave='clave',version='0')
        #s.commit()

        if orientacion=="V":
            if filaInicial==filaFinal:
                row = int(filaInicial)-1
                claveAux= sheet.row_values(row,int(clave)-1,int(clave))
                claveAux = str(claveAux[0])
                valor= sheet.row_values(row,int(dato)-1,int(dato))
		print("id: " + identificador)
		print("uuid: " + predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal))
		print("predicado: " + predicado)
		print("Pub: " + publicador)
		print("clave: " + claveAux)
		print("valor: " + str(valor[0]))
                s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux,valor=str(valor[0]))
                s.commit()

            else:
                #s.add(id=555,valor="valor", uuid="holamundo001", predicado="predicado", publicador="publicador", clave="clave",version="0")
                #s.commit()

                for row in range(filaInicial-1,filaFinal,1):
                        print("________________")
                        print("fila: " + str(filaInicial) + " clave: " + str(int(clave)) + " dato: " + str(int(dato)))
                        claveAux = sheet.row_values(row,int(clave)-1,int(clave))
                        #claveAux = str(claveAux[0].encode('utf-8'))
                        try:
				claveAux = round(claveAux[0])
                        except:
				claveAux = claveAux[0]
			#print "Codigo INE "+str(claveAux)
                        valorAux = sheet.row_values(row,int(dato)-1,int(dato))
                        print("dato: " + str(sheet.row_values(row,int(dato)-1,int(dato))))
                        #print("Time: " + str(time()))
                        #print("valor: " +str(valorAux[0]))  
                        # print("________________")
			#print("predicado: " + predicado)
			#print("uuid: " + predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal))
			#print("identificador: " + str(identificador))
			#print("publicador: " + publicador)
			print("codigo INE: " + str(claveAux))
			#print("valor: " + str(valorAux[0]))

			#s.add(uuid="UUID", predicado="PREDICADO", publicador="PUBLICADOR", clave="CLAVE",valor="VALOR")
			#print("id=" + str(identificador) + ", uuid=" + predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal) + ", predicado=" + predicado + ", publicador=" + publicador + ", clave=" + claveAux + ",  valor=" + str(valorAux[0])
                 
			print("id: " + str(identificador))
	                print("uuid: " + "predicado"  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal))
        	        print("predicado: " + predicado)
                	print("Pub: " + publicador)
               		print("clave: " + str(3))
                	print("valor: " + str(valorAux[0]))

       
			s.add(id="aaa23", uuid="predicado3212", predicado="predicado", publicador=publicador, clave=str(3), valor="A")
                        s.commit()
        else:
            if filaInicial==filaFinal:
                col = int(filaInicial)-1
                claveAux= sheet.col_values(col,int(clave)-1,int(clave))
                claveAux = str(claveAux[0].encode('utf-8'))
                valor= sheet.col_values(col,int(dato)-1,int(dato))

                s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valor[0]))
                s.commit()

            else:
                for col in range(filaInicial-1,filaFinal,1):
                        print("fila: " + str(filaInicial) + " clave: " + str(int(clave)) + " dato: " + str(int(dato)))
                        claveAux = sheet.col_values(col,int(clave)-1,int(clave))
                        claveAux = str(claveAux[0].encode('utf-8'))
                        valorAux = sheet.col_values(col,int(dato)-1,int(dato))
                        print("dato: " + str(sheet.row_values(col,int(dato)-1,int(dato))))
                        s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valorAux[0]))
                        s.commit()

def _xml_get(xml_file, identificador, sheet, filaInicial,filaFinal, clave,dato,predicado, publicador,orientacion):


            tree = ET.parse(xml_file)
            root = tree.getroot()

            # create a connection to a solr server
            s = solr.SolrConnection('http://localhost:8983/solr/ckan_wiki')


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
                    
                    s.add(id=identificador, uuid=predicado  + "_" + str(time()) + "_" + str(filaInicial) + str(filaFinal) + "_" + str(x), predicado=predicado, publicador=publicador, clave=claveAux.decode('utf-8'),valor=str(valor))
                    s.commit()

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
        s = solr.SolrConnection('http://localhost:8983/solr/ckan_wiki')
        # add a document to the index
        s.delete_query('*:*')
        s.commit()


def eliminar_entradas_solr(identificador):

    # create a connection to a solr server
    print("Se elimina la entrada con id: " + str(identificador))
    s = solr.SolrConnection('http://localhost:8983/solr/ckan_wiki')
    # add a document to the index
    s.delete_query('id:' + str(identificador))
    s.commit()

def main():

    
    connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
    cursor = connection.cursor()
    
    #print("Eliminamos todo lo que hay en el solr de ckan_wiki")
    ##eliminar_todas_entradas_solr()
    registros = cursor.execute("SELECT * FROM OPENDATA.opendata_v_wiki")
    print sys.argv
    print len(sys.argv)
    force = False
    if (len(sys.argv) == 2):
        if sys.argv[1] == "force":
            print "si"
            force = True

    lista = []
    print("Comienza con los registros")
    i=1
    for r in registros:
        print "Comienza Registro " + str(i)
        print "Es " + str(r) 
        #Estan mal los indices hay que revisarlos todos, esta el numero de registro antes, cocn lo que hay que hacer todo +1 :D
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
                _xls_get(xls_file,identificador,bloque,filaInicial,filaFinal, clave, dato, predicado, publicador, orientacion)
                connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
                cursor = connection.cursor()
                #eliminar_todas_entradas_solr()
                #cursor.execute("UPDATE opendata_wiki set indexado=1 where id=" + str(identificador))
                #connection.commit()
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




    cursor.close()
    connection.close()


main()
