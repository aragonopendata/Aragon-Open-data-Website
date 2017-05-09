#!/usr/bin/python
# -*- coding: utf-8 -*-
#RUTAS_APLICACION
import os
import re
import urllib
import uuid
import pymssql
import cx_Oracle
import psycopg2
import MySQLdb
#import ckan.model as model
#import ckan.new_authz as new_authz
import _mssql


URL_FILE="/usr/lib/ckan/default/src/ckan/ckan/ckanclient/url.properties"
DOWNLOAD_PATH="/data/ckan_tmp"
DOWNLOAD_TEMPORAL="/data/ckan_tmp"
UPLOAD_DOCUMENTS="/data/ckan_ficheros/opendata/"
URL_VISTAS="http://opendata.aragon.es/catalogo/dataset/showVista?id="
URL_DOCUMENTS="http://opendata.aragon.es/catalogo/opendata/"

#PARAMETROS_APLICACION
API_KEY="7cc367ac-67e3-4e9e-8c1e-24c75b0e03f4"
BASE_LOCATION="http://opendata.aragon.es/catalogo/api"
INDEX_LOCATION="http://opendata.aragon.es/catalogo/dataset/index"
RSS_LOCATION="http://opendata.aragon.es/catalogo/feeds/dataset.atom"
DCAT_NAMESPACE = "http://www.w3.org/ns/dcat#"
DCT_NAMESPACE = "http://purl.org/dc/terms/"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
FOAF_NAMESPACE = "http://xmlns.com/foaf/0.1/"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#CONEXION_LISTADO_VISTAS_EDITOR - segun entorno modificar "storage.py" - "package.py"
#PRE
OPENDATA_CONEXION_BD_PRE="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpre1.dga.es)(PORT=1523))(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpre2.dga.es)(PORT=1523))(CONNECT_DATA=(SERVICE_NAME=preapp1.dga.es)))"
#DES
OPENDATA_CONEXION_BD_DES="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=backdes1.dga.es)(PORT=1523))(CONNECT_DATA=(SERVICE_NAME=desapp1.dga.es)))"
#PRO
OPENDATA_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpro1.dga.es)(PORT=1523))(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpro2.dga.es)(PORT=1523))(CONNECT_DATA=(SERVICE_NAME=proapp1.dga.es)))"

#CADENA_CONEXION_ORACLE
##AST_1
AST1_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpre1.dga.es)(PORT=1523))(ADDRESS=(PROTOCOL=TCP)(HOST=vir_backpre2.dga.es)(PORT=1523))(CONNECT_DATA=(SERVICE_NAME=preapp1.dga.es)))"
##AST_2
AST2_CONEXION_BD="(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=pre01-scan.aragon.local)(PORT=47034)))(CONNECT_DATA=(SERVER = DEDICATED)(SERVICE_NAME = ASTJ2EE_GN1_01.ARAGON.LOCAL)))"
##AST_5
AST5_CONEXION_BD="(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=boz-sitar-01.aragon.local)(PORT=1521)))(CONNECT_DATA=(SERVER = DEDICATED)(SERVICE_NAME = gispro.aragon.es)))"

#CADENA_CONEXION_POSTGRESQL
AST3_CONEXION_BD = "host='senderos.turismodearagon.com' dbname='senderos' port='5432' user='opendata_usr' password='D4t4Arag0n'"
OPENDATA_POSTGRE_CONEXION_BD="host='localhost' dbname='ckan_default'  port='5432' user='ckan_default' password='ckan_default'"
OPENDATA_CAMPUS_CONEXION_BD="host='localhost' dbname='campusopendatadb'  port='5432' user='user_campusopendata' password='C0ntr4$3n4_d3_c4mpU$0p3nD4t4'"

#CADENA_CONEXION_SQL_SERVER
AST4_CONEXION_BD = "host='bov-domus-01.aragon.local', user='OPENDATA_USR', password='OPENDATA_PSW', database='BD_COLECCION_WEB'"

#MAPEO_USUARIOS
OPENDATA_USR="OPENDATA_USR"
OPENDATA_PASS="OPENDATA_USR"
OPENDATA="OPENDATA"
AST_USR="OPENDATA_USR"
AST_PASS="OPENDATA_USR"
USR_ADMIN="admin"

#PILA_CONEXION

#Funcio de conexio segun los datos que le hemos metido como parametro nos devolvera una conexio a dicha base de datos
#ubicacion es la ubicacio, puede ser des-opendata-oracle, pre-opendata-oracle, pro-opendata-oracle.....
def conexion(ubicacion):
	if ubicacion.lower() == 'pre-opendata-oracle':
		devolver = cx_Oracle.connect(OPENDATA_USR + "/" + OPENDATA_PASS + "@" + OPENDATA_CONEXION_BD_PRE)
	elif ubicacion.lower() == 'pro-opendata-oracle':
		devolver = cx_Oracle.connect(OPENDATA_USR + "/" + OPENDATA_PASS + "@" + OPENDATA_CONEXION_BD)
	elif ubicacion.lower() == 'des-opendata-oracle':
		devolver = cx_Oracle.connect(OPENDATA_USR + "/" + OPENDATA_PASS + "@" + OPENDATA_CONEXION_BD_DES)
	elif ubicacion.lower() == 'app1': #Es la conexion de storage.py correspondiente a app1-ORACLE
		devolver = cx_Oracle.connect(AST_USR + "/" + AST_PASS + "@" + AST1_CONEXION_BD)
	elif ubicacion.lower() == 'app2': # Es la conexion de storage.py correspondiente a app2-ORACLE
		devolver = cx_Oracle.connect(AST_USR + "/" + AST_PASS + "@" + AST2_CONEXION_BD)
	elif ubicacion.lower() == 'app6': # Es la conexion de storage.py correspondiente a app6-ORACLE
		devolver = cx_Oracle.connect(AST_USR + "/" + AST_PASS + "@" + AST5_CONEXION_BD)
	elif ubicacion.lower() == 'app3':# Es la conexion de storage.py correspondiente a app3 que es la de senderos
		devolver=psycopg2.connect(AST3_CONEXION_BD)
	elif ubicacion.lower() == 'opendata-postgre':
		devolver= psycopg2.connect(OPENDATA_POSTGRE_CONEXION_BD)
	elif ubicacion.lower() == 'opendata-campus':#Es la conexion para la base de datos del campus
		devolver= psycopg2.connect(OPENDATA_CAMPUS_CONEXION_BD)
	elif (ubicacion.lower() == 'app4'): # Es la conexion de storage.py correspondiente a app4
		devolver= pymssql.connect(host='bov-domus-01.aragon.local', user='OPENDATA_USR', password='OPENDATA_PSW', database='BD_COLECCION_WEB');
	elif (ubicacion.lower() == 'app5'): # Conexion para MySLQ app5
		devolver= MySQLdb.connect(host='194.179.110.14',port=3306, user='OPENDATA_USR', passwd='0p3n-DATA',db='webiaf');
	else:
		print 'No hay conexion para el tipo', tipo, 'y la ubicacio', ubicacion
		return None;
	return devolver




