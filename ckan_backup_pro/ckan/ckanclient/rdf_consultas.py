#!/usr/bin/python
# -*- coding: utf-8 -*-

import ckanclient
import config
import json
import csv
import config as configuracion


def main():

    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    tag_list = ckan.tag_register_get()

    # Se escriben las etiquetas y grupos
    f=open(configuracion.DOWNLOAD_PATH + '/' + "etiqygrupos.txt", 'w+')
    f.write("LISTADO DE TAGS ")
    f.write("(Hay: " + str(len(tag_list)) + ")\n")
    f.write("---------------\n")

    for idx, tag in enumerate(tag_list):
        f.write(str(idx+1).encode('ISO-8859-1') + ": " + tag.encode('ISO-8859-1') + "\n")

    group_list = ckan.group_register_get()
    f.write("\nLISTADO DE GRUPOS ")

    lista = []
    for idx, grupo in enumerate(group_list):
        if ckan.group_entity_get(grupo).get('type')=='group':
            lista.append(ckan.group_entity_get(grupo).get('name'))


    f.write("(Hay: " + str(len(lista)) + ")\n")
    f.write("---------------\n")

    for idx, grupo in enumerate(lista):
        f.write(str(idx+1) + ": " + grupo + "\n")

    f.close()



    # DATASETS
    lista = []
    package_list = ckan.package_register_get()
    for  idx, paquete in enumerate(package_list):
        ckan.package_entity_get(paquete)
        package_entity = ckan.last_message
        if 'iaest' in package_entity.get('author').lower():
            lista.append(package_entity)

    nombreFichero = 'datasets_iaest.csv'


    with open(configuracion.DOWNLOAD_PATH + '/' + nombreFichero, 'w+') as csvfile:
        datoExtrasIAEST=""
        #Se copian los indices superiores
        spamwriter = csv.writer(csvfile)
        indices= []
        for idx, item in enumerate(lista):
            for item2 in item:
                if idx==0:
                    indices.append(item2)
        spamwriter.writerow(indices)

        #Se recorren los resultados
        for idx, item in enumerate(lista):
            linea =[]
            for item2 in item:
                try:
                    dato = item[json.dumps(item2).replace('"','')].encode('ISO-8859-1')
                except AttributeError:
                    listaInterna = item[json.dumps(item2).replace('"','')]
                    dato = ""
                    if listaInterna is not None:
                        if type(listaInterna).__name__ == 'list':
                            for itemListaInterna in listaInterna:
                                try:
                                    if type(itemListaInterna).__name__ =="dict":
                                        dato = ""
                                        if json.dumps(item2).replace('"','') == 'extrasIAEST':

                                            datoExtrasIAEST = datoExtrasIAEST +  str(itemListaInterna['key'].encode('ISO-8859-1')) + ": " + str(itemListaInterna['value'].encode('ISO-8859-1')) + ";"

                                        elif json.dumps(item2).replace('"','') == 'resources':
                                            datoExtrasIAEST = datoExtrasIAEST +  str(itemListaInterna['name'].encode('ISO-8859-1'))  + ";"
                                        else:
                                            for itemIntListaInterna in itemListaInterna:
                                                dato= dato + str(json.dumps(itemIntListaInterna).replace('"','')) + ": " + str(itemListaInterna[json.dumps(itemIntListaInterna).replace('"','')].encode('ISO-8859-1')) + ";"
                                    else:
                                        dato = dato + itemListaInterna.encode('ISO-8859-1') + ";"

                                except AttributeError:
                                    for itemListaInternab in itemListaInterna:
                                        dato = dato + itemListaInternab.encode('ISO-8859-1') + ";"
                        else:
                            dato= listaInterna

                    else:
                        dato= listaInterna


                if datoExtrasIAEST and datoExtrasIAEST!= "":
                    dato= datoExtrasIAEST
                    datoExtrasIAEST=""
                linea.append(dato)
            spamwriter.writerow(linea)
        csvfile.close()





main()