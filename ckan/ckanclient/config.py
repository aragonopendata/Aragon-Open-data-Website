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
import _mssql


URL_FILE="/usr/lib/ckan/default/src/ckan/ckan/ckanclient/url.properties"
DOWNLOAD_PATH="/xxxx"
DOWNLOAD_TEMPORAL="/xxxx"
UPLOAD_DOCUMENTS="/xxx/"
URL_VISTAS="http://opendata.aragon.es/catalogo/dataset/showVista?id="
URL_DOCUMENTS="http://opendata.aragon.es/catalogo/opendata/"

#PARAMETROS_APLICACION
API_KEY="7cc367ac-67e3-4e9e-8c1e-24c75b0e03f4"
BASE_LOCATION="http://preopendata.aragon.es/catalogo/api"
INDEX_LOCATION="http://preopendata.aragon.es/catalogo/dataset/index"
RSS_LOCATION="http://preopendata.aragon.es/catalogo/feeds/dataset.atom"
DCAT_NAMESPACE = "http://www.w3.org/ns/dcat#"
DCT_NAMESPACE = "http://purl.org/dc/terms/"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
FOAF_NAMESPACE = "http://xmlns.com/foaf/0.1/"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

#CONEXION_LISTADO_VISTAS_EDITOR 
#PRE
OPENDATA_CONEXION_BD_PRE="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx)))"
#DES
OPENDATA_CONEXION_BD_DES="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx))"
#PRO
OPENDATA_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx))"

#CADENA_CONEXION_ORACLE
##AST_1
AST1_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx))"
##AST_2
AST2_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx))"

#CADENA_CONEXION_POSTGRESQL
AST3_CONEXION_BD = "host='xxx.xxxxxx.xxx' dbname='xxxx' port='xxxx' user='xxxxx' password='xxxxxx'"
OPENDATA_POSTGRE_CONEXION_BD="host='xxxxx' dbname='xxxxx'  port='xxxx' user='xxxx' password='xxxx'"

#CADENA_CONEXION_SQL_SERVER
AST4_CONEXION_BD = "host='xxxx.xxxx.xxxx', user='xxxx', password='xxxx', database='xxxx'"

#MAPEO_USUARIOS
OPENDATA_USR="xxxx"
OPENDATA_PASS="xxxx"
OPENDATA="xxxx"
AST_USR="xxxx"
AST_PASS="xxxx"
USR_ADMIN="xxxx"

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
	elif ubicacion.lower() == 'app1': #Es la conexion de storage.py correspondiente a app1
		devolver = cx_Oracle.connect(AST_USR + "/" + AST_PASS + "@" + AST1_CONEXION_BD)
	elif ubicacion.lower() == 'app2': # Es la conexion de storage.py correspondiente a app2
		devolver = cx_Oracle.connect(AST_USR + "/" + AST_PASS + "@" + AST2_CONEXION_BD)
	elif ubicacion.lower() == 'app3':# Es la conexion de storage.py correspondiente a app3 que es la de senderos
		devolver=psycopg2.connect(AST3_CONEXION_BD)
	elif ubicacion.lower() == 'opendata-postgre':
		devolver= psycopg2.connect(OPENDATA_POSTGRE_CONEXION_BD)
	elif (ubicacion.lower() == 'app4'): # Es la conexion de storage.py correspondiente a app4
		devolver= pymssql.connect(host='xxxx.xxxx.xxxx', user='xxxx', password='xxxx', database='xxxx');
	elif (ubicacion.lower() == 'app5'): # Conexion para MySLQ app5
		devolver= MySQLdb.connect(host='xxxx.xxxx.xxxx.xxxx',port=xxxx, user='xxxx', passwd='xxxx',db='xxxx');
	else:
		print 'No hay conexion para el tipo', tipo, 'y la ubicacion', ubicacion
		return None;
	return devolver



