# -*- coding: utf-8 -*-

import codecs
import urllib2
import config
import ckanclient
import cx_Oracle

# GUARDA EN REGISTRO_IAEST LOS DATASETS DE CINTA (Centro de Información Territorial de Aragón, Dpto de Agricultura, Ganadería y Medioambiente, Dirección General de Urbanismo)
def main():

    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    ckan.package_register_get()
    package_list = ckan.last_message

    for idx, package in enumerate(package_list):

        ckan.package_entity_get(package)
        package_entity = ckan.last_message
        #print ("PAQUETE:" + str(idx) + ": " + package_entity['title'])
        maintainer = package_entity['maintainer'];
        print(maintainer)
        connection = cx_Oracle.connect("OPENDATA/OPENDATA@" + config.OPENDATA_CONEXION_BD_DES)
        cursor = connection.cursor()
        #if maintainer.encode('utf-8').decode('utf-8').startswith('Centro de Informaci'):
        if maintainer.encode('utf-8').decode('utf-8') == 'Centro de Información Territorial de Aragón'.decode('utf-8'):
            print ("es de CINTA");
            if package_entity['state'] == 'active':
                print("y esta activo");
                cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [ package_entity['name'], 'CINTA',None])
                connection.commit()
        if maintainer.encode('utf-8').decode('utf-8') == 'Dpto. Agricultura, Ganadería y Medioambiente'.decode('utf-8'):
            print("ES DE AGRICULTURA");
            if package_entity['state'] == 'active':
                print("Y esta activo");
                cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [ package_entity['name'], 'Dpto.',None])
            connection.commit()
        if maintainer.encode('utf-8').decode('utf-8') == 'Dpto de Agricultura, Ganadería y Medioambiente'.decode('utf-8'):
            print("ES DE AGRICULTURA");
            if package_entity['state'] == 'active':
                print("Y esta activo");
                cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [ package_entity['name'], 'Dpto ',None])
            connection.commit()
        if  maintainer.encode('utf-8').decode('utf-8') == 'Dirección General de Urbanismo'.decode('utf-8'):
            print("es de urbanismo");
            if package_entity['state'] == 'active':
                print("Y esta activo");
                cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [ package_entity['name'], 'DGU',None])
                connection.commit()


    cursor.close()
    connection.close()

main()
