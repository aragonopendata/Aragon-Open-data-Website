# -*- coding: utf-8 -*-

import codecs
import urllib2
import config
import ckanclient

def main():
    import datetime

    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    ckan.package_register_get()
    package_list = ckan.last_message

    numComprobaciones = 0
    numErrores = 0


    myFile = codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'w', encoding='utf-8')
    myFile.write('LISTADO DE URLs. Fecha de comprobacion: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")
    myFile.write("---------------------------------------------------------\n")
    myFile.write( "Error\tURL que falla" + "\t\t\t" + "Dataset en el que se encuentra\n")
    myFile.write("---------------------------------------------------------------------------\n")
    myFile.close()

    timeOut = 30
    for idx, package in enumerate(package_list):

        ckan.package_entity_get(package)
        package_entity = ckan.last_message
        #print ("PAQUETE:" + str(idx) + ": " + package_entity['title'])
        url = package_entity['url']

        if url is not None and url != "":
            url = url.decode('utf-8')
            url = url.encode('utf-8')
            try:
                numComprobaciones = numComprobaciones+1
                resultURL = urllib2.urlopen(url,None,timeout=timeOut)
                #if resultURL.code in (200, 401):
                #    print str(numComprobaciones) + " " + '[{0}]: '.format(url), "Up!"

            except urllib2.URLError,e:
                try:
                    if (e.reason):
                        razon = str(e.reason)
                        if str(e.reason) == "timed out":
                            razon= "TOUT"
                        if str(e.reason) == "[Errno -2] Name or service not known":
                            razon="NSNK"
                        if str(e.reason) == "no host given":
                            razon="NHG"
                        numErrores = numErrores +1
                        with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                            myfile.write(razon + "\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'].decode('utf-8') + "\t\t\t" + url.decode('utf-8') + "\n")

                except:
                    if e.code:
                        #print str(numComprobaciones) + " " + '[{0}]: '.format(url), "ERROR!"
                        numErrores = numErrores +1
                        with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                            myfile.write(str(e.code) + "\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'].decode('utf-8') + "\t\t\t" + url.decode('utf-8') + "\n")

            except:

                #print str(numComprobaciones) + " " + '[{0}]: '.format(url), "MAL!"
                numErrores = numErrores +1
                with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                    myfile.write("ERR\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'].decode('utf-8') + "\t\t\t" + url.decode('utf-8') + "\n")


        resources =  package_entity['resources']

        #Se comprueban todos los links de sus resources
        for resource in resources:
            urlResource = resource.get('url')
            urlResource = urlResource.encode('utf-8')



            try:
                numComprobaciones = numComprobaciones +1
                r = urllib2.urlopen(urlResource,None,timeout=timeOut)
                #if r.code in (200, 401):
                    #print str(numComprobaciones) + " " + str(r.code) + '[{0}]: '.format(urlResource), "Up!"

            except urllib2.URLError,e:
                try:
                    if (e.reason):
                        razon = str(e.reason)
                        if str(e.reason) == "timed out":
                            razon= "TOUT"
                        if str(e.reason) == "[Errno -2] Name or service not known":
                            razon="NSNK"
                        if str(e.reason) == "no host given":
                            razon="NHG"
                        numErrores = numErrores +1
                        with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                            myfile.write(razon + "\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'].decode('utf-8') + "\t\t\t" + urlResource.decode('utf-8') + "\n")

                except:
                    try:
                        if e.code:
                            #print str(numComprobaciones) + " " + '[{0}]: '.format(urlResource), "ERROR!"
                            numErrores = numErrores +1
                            with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                                myfile.write(str(e.code) + "\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'].decode('utf-8') + "\t\t\t" + urlResource.decode('utf-8') + "\n")
                    except:
                        numErrores = numErrores +1
                        with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                            myfile.write("ERR2\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'] + "\t\t\t" + urlResource.decode('utf-8') + "\n")

            except:
                #print str(numComprobaciones) + " " + '[{0}]: '.format(urlResource), "MAL!"
                numErrores = numErrores +1
                with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
                    myfile.write("ERR\t" + config.INDEX_LOCATION.split('index')[0] +package_entity['name'] + "\t\t\t" + urlResource + "\n")



    with codecs.open(config.UPLOAD_DOCUMENTS + 'erroresURL.txt', 'a', encoding='utf-8') as myfile:
        myfile.write("\nSe han encontrado {0} errores de {1} enlaces comprobados en {2} datasets\n\n".format(numErrores,numComprobaciones,len(package_list)))

        myfile.write("----------------------------------\n")
        myfile.write("Cod. comunes:\n\n")
        myfile.write("TOUT: Time Out. No se ha recibido respuesta tras un timeOut de: " + str(timeOut) + " segundos\n")
        myfile.write("NSNK: Nombre o servicio no conocido\n")
        myfile.write("NHG: No se ha especificado host\n")
        myfile.write("404: No encontrado\n")
        myfile.write("500: Error interno\n\n")
        myfile.write("Info cod. HTTP: http://es.wikipedia.org/wiki/Anexo:C%C3%B3digos_de_estado_HTTP")



main()
