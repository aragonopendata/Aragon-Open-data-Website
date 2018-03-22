
import config as configuracion

#import config as configuracion
import cx_Oracle
import psycopg2
import pymssql
import MySQLdb


class ConexionDB:
    'Clase para crear conexiones a base de datos'
    def __init__(self,cadena,tipo):          
        self.cadena = cadena
        self.tipo = tipo
   
def conexion(ubicacion):
    '''
    conexion
    Parametros de Entrada: String con el nombre de la base de datos.
    Parametros de salida: Objeto tipo ConexioDB
    '''
    if ubicacion.lower() == 'pre-opendata-oracle':
        devolver = ConexionDB(cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.OPENDATA_CONEXION_BD_PRE),"oracle")
    elif ubicacion.lower() == 'pro-opendata-oracle':
       devolver = ConexionDB(cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.OPENDATA_CONEXION_BD),"oracle")
    elif ubicacion.lower() == 'des-opendata-oracle':
        devolver = ConexionDB(cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.OPENDATA_CONEXION_BD_DES),"oracle")
    elif ubicacion.lower() == 'app1': #Es la conexion de storage.py correspondiente a app1
        devolver = ConexionDB(cx_Oracle.connect(configuracion.AST_USR + "/" + configuracion.AST_PASS + "@" + configuracion.AST1_CONEXION_BD),"oracle")
    elif ubicacion.lower() == 'app2': # Es la conexion de storage.py correspondiente a app2
        devolver = ConexionDB(cx_Oracle.connect(configuracion.AST_USR + "/" + configuracion.AST_PASS + "@" + configuracion.AST2_CONEXION_BD),"oracle") 
    elif ubicacion.lower() == 'app3':# Es la conexion de storage.py correspondiente a app3 que es la de senderos
         devolver = ConexionDB(psycopg2.connect(configuracion.AST3_CONEXION_BD),"postgre")
    elif ubicacion.lower() == 'opendata-postgre':
        devolver= ConexionDB(psycopg2.connect(configuracion.OPENDATA_POSTGRE_CONEXION_BD),"postgre")
    elif (ubicacion.lower() == 'app4'): # Es la conexion de storage.py correspondiente a app4
        devolver = ConexionDB(pymssql.connect(host='bov-domus-01.aragon.local', user='OPENDATA_USR', password='OPENDATA_PSW', database='BD_COLECCION_WEB'),"sqlserver")
    elif (ubicacion.lower() == 'app5'): # Conexion para MySLQ app5
        devolver = ConexionDB(MySQLdb.connect(host='194.179.110.14',port=3306, user='OPENDATA_USR', passwd='0p3n-DATA',db='webiaf'),"mysql")
    else:
        print 'No hay conexion para el tipo para la ubicacion : ', ubicacion
        return None;
    return devolver