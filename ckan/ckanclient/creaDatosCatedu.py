#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Este script crea archivos .rdf correspondientes a DataSets.
Para ello necesita una estructura de carpetas y en cada una de ellas 3 archivos:
    {nombreCarpeta}plantilla.xls : Donde estarán los metadatos generales a esta sección
    UDs{nombreCarpeta}.csv : Información sobre las unidades
    PDs{nombreCarpeta}.csv : Información sobre los descargables de cada unidad.
Cada sección tendrá varias unidades.
A su vez cada unidad tendrá varias descargas.
Sección -> UDs -> PDs

Se creará un .rdf por cada UD {nombreCarpeta} .- UDs{nombreCarpeta} en :
/data/ckan_ficheros/opendata/catedu
"""

import config
import csv
import os
import urllib
import unicodedata
import itertools
from xlrd import open_workbook
from xlrd import open_workbook,cellname
from mmap import mmap,ACCESS_READ
import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

def transformar(cadena):
    cadena = cadena.decode('utf-8').encode('utf-8')
    cadena = cadena.lower()
    cadena = cadena.replace(" ","-")
    cadena = cadena.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
    cadena = cadena.replace( "ú", "u").replace("%","").replace("Ñ","ny")
    cadena = cadena.strip().lower().replace(":", "-").replace(")", "").replace(",", "").replace("'","")
    cadena = cadena.replace("(","").replace(".", "").replace(" ", "-").replace("¡","").replace("!","").replace("?","").replace("¿","")
    cadena = cadena.replace("/","-")
    cadena = cadena.replace("--", "-").replace("ñ","ny").replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("Ú","u").replace("º","")
    cadena = cadena.replace("è", "e").replace("à","a").replace("ì","i").replace("ò","o").replace("ù","u")
    cadena = cadena.replace("Ç", "c").replace("ç","c").replace("ü","u").replace(":","").replace("'","-").replace(";","-")
    cadena = cadena.replace("+", "").replace("`","-").replace("ê","e").replace("@","").replace(": ","")
    cadena = cadena.replace("\'","-").replace("´","").replace("\"","-")
    cadena = cadena.strip()
    cadena = strip_accents(cadena)
    cadena = cadena.lower()
    return cadena

def strip_accents(string):
    import unicodedata
    return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore')

def main():
    #Leemos las carpetas -> ficheros:
    total_creados = 0
    testCadena = ""
    path = config.UPLOAD_DOCUMENTS + "facilitamosOpenData"
    #Crea un array con el nombre de las carpetas bajo nuestra ruta.
    dir_list = os.walk(path).next()[1]
    #print dir_list
    for fil in dir_list:
        uds_fileName = "uds" + fil + "v2.csv"
        pds_fileName  = "pds" + fil + "v2.csv"
        plantilla_fileName = "plantilla" + fil + "v2.xls"
        #Leemos el excel
        debug_xls = 0
        excelfile= config.UPLOAD_DOCUMENTS + "facilitamosOpenData/" + fil + "/" + plantilla_fileName
        book = open_workbook(excelfile)
        sheet = book.sheet_by_index(0)
        columna = 3
        #url_publicado = sheet.cell(2,columna).value
        #Teniendo en cuenta que esta sea la URL para todos los DataSet
        url_publicado = "http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/EducacionUniversidadCulturaDeporte"
        descripcion_ud = sheet.cell(3,columna).value
        etiquetas = sheet.cell(4,columna).value
        titulo_general = sheet.cell(5,columna).value
        fe_modificacion = sheet.cell(6,columna).value
        fe_creacion = sheet.cell(7,columna).value
        #Fila 9 VACÍA
        organizacion = sheet.cell(9,columna).value
        organizacionURL = sheet.cell(10,columna).value
        frecuencia = sheet.cell(11,columna).value
        cobertura_espacial = sheet.cell(12,columna).value
        intervalo = sheet.cell(13,columna).value
        idioma = sheet.cell(14,columna).value
        #licencia = sheet.cell(15,columna).value
        #licencia = "Creative Commons-Reconocimiento CC-By 4.0"
        licencia = "http://www.opendefinition.org/licenses/cc-by"
        nivel_detalle = sheet.cell(16,columna).value
        calidad = sheet.cell(17,columna).value
        diccionario = sheet.cell(18,columna).value
        #File 20 VACÍA
        categoria_datos = sheet.cell(20,columna).value
        #descarga1
        titulo_descarga = sheet.cell(24,columna).value
        descripcion_descarga = sheet.cell(25,columna).value
        url_descarga = sheet.cell(26,columna).value
        tamanyo_descarga = sheet.cell(27,columna).value
        formato_descarga = sheet.cell(29,columna).value
        #descarga2
        titulo_descarga2 = sheet.cell(31,columna).value
        descripcion_descarga2 = sheet.cell(32,columna).value
        url_descarga2 = sheet.cell(33,columna).value
        tamanyo_descarga2 = sheet.cell(34,columna).value
        formato_descarga2 = sheet.cell(36,columna).value
        #descarga3
        titulo_descarga3 = sheet.cell(38,columna).value
        descripcion_descarga3 = sheet.cell(39,columna).value
        url_descarga3 = sheet.cell(40,columna).value
        tamanyo_descarga3 = sheet.cell(41,columna).value
        formato_descarga3 = sheet.cell(42,columna).value

        #Variables comunes a todos los DataSets
        mainteiner = "Dirección General de Planificación y Formación Profesional"
        author = "Dirección General de Planificación y Formación Profesional"
        organizacion_code  = "direccion_general_de_planificacion_y_formacion_profesional"
        organizacion = "Dirección General de Planificación y Formación Profesional"
        organizacionURL = "http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/EducacionUniversidadCulturaDeporte"

        # Cabecera del Fichero RDF
        fichero_RDF = "<rdf:RDF xmlns:foaf=\"http://xmlns.com/foaf/0.1/\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n"
        fichero_RDF = fichero_RDF + "  xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n"
        fichero_RDF = fichero_RDF + "  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"
        fichero_RDF = fichero_RDF + "  xmlns:dcat=\"http://www.w3.org/ns/dcat#\"\n"
        fichero_RDF = fichero_RDF + "  xmlns:dct=\"http://purl.org/dc/terms/\">\n\n"

        #frecuencia
        #Mensual(P1M) Diaria(P1D) Anual(P1Y)
        if frecuencia != None:
            if "diaria" in frecuencia.lower() or "p1d" in frecuencia.lower():
                frecuenciaValue = "Diaria"
                frecuenciaLabel = "Diaria"
            elif "mensual" in frecuencia.lower() or "p1m" in frecuencia.lower():
                frecuenciaValue = "Mensual"
                frecuenciaLabel = "Mensual"
            elif "anual" in frecuencia.lower() or "p1y" in frecuencia.lower():
                frecuenciaValue = "Anual"
                frecuenciaLabel = "Anual"
            else:
                frecuenciaValue = "Anual"
                frecuenciaLabel = "Anual"

        if(debug_xls == 1):
            print("--BEGIN--")
            print("url_publicado: " + url_publicado + "\n")
            print("descripcion: " + descripcion + "\n")
            print("etiquetas: " + etiquetas + "\n")
            print("titulo_general: " + titulo_general + "\n")
            print("fe_modificacion: " + fe_modificacion + "\n")
            print("fe_creacion: " + fe_creacion + "\n")
            print("organizacion: " + organizacion + "\n")
            print("organizacionURL: " + organizacionURL + "\n")
            print("frecuencia: " + frecuencia + "\n")
            print("cobertura_espacial: " + cobertura_espacial + "\n")
            print("intervalo: " + intervalo + "\n")
            print("idioma: " + idioma + "\n")
            print("licencia: " + licencia + "\n")
            print("nivel_detalle: " + nivel_detalle + "\n")
            print("calidad: " + calidad + "\n")
            print("diccionario: " + diccionario + "\n")
            print("categoria_datos: " + categoria_datos + "\n")
            print("titulo_descarga: " + titulo_descarga + "\n")
            print("descripcion_descarga: " + descripcion_descarga + "\n")
            print("url_descarga: " + url_descarga + "\n")
            print("tamanyo_descarga: " + tamanyo_descarga + "\n")
            print("formato_descarga: " + formato_descarga + "\n")
            print("titulo_descarga2: " + titulo_descarga2 + "\n")
            print("descripcion_descarga2: " + descripcion_descarga2 + "\n")
            print("url_descarga2: " + url_descarga2 + "\n")
            print("tamanyo_descarga2: " + tamanyo_descarga2 + "\n")
            print("formato_descarga2: " + formato_descarga2 + "\n")
            print("titulo_descarga3: " + titulo_descarga3 + "\n")
            print("descripcion_descarga3: " + descripcion_descarga3 + "\n")
            print("url_descarga3: " + url_descarga3 + "\n")
            print("tamanyo_descarga3: " + tamanyo_descarga3 + "\n")
            print("formato_descarga3: " + formato_descarga3 + "\n")
            print("---END---")

        #Leemos el CSV "UDs..."
        debug_uds = 0
        csvfile= config.UPLOAD_DOCUMENTS + "facilitamosOpenData/" + fil + "/" + uds_fileName
        with open(csvfile, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                identificador = row[0]
                descripcion = row[1]
                titulo = row[2]
                UDsID = row[3]
                if(debug_uds == 1):
                    print("--BEGIN--")
                    print("identificador: " + identificador)
                    print("descripcion: " + descripcion)
                    print("titulo: " + titulo)
                    print("---END---")

                #Uds
                ficheroDataSet = fichero_RDF
                ficheroDataSet = ficheroDataSet + "\t<dcat:Dataset rdf:about=\"" + url_publicado + "\">\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:identifier>recurso-educativo-" + transformar(fil) + "-"  +transformar(titulo) + "</dct:identifier>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:description>" + descripcion + "</dct:description>\n"

                #Sacamos cada una de las etiquetas, que nos las pasan en una línea separadas por comas.
                for elemento in etiquetas.split(","):
                    if len(elemento) > 3:
                        ficheroDataSet = ficheroDataSet + "\t\t<dcat:keyword xml:lang=\"es\">" + elemento.strip() + "</dcat:keyword>\n"

                #ficheroDataSet = ficheroDataSet + "\t\t<dct:title>" + titulo + "</dct:title>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:title>Recurso Educativo - " + titulo_general + " - " + titulo + "</dct:title>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:modified>" + str(fe_modificacion) + "</dct:modified>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:organization>"+organizacion_code+"</dct:organization>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:issued>" + str(fe_creacion) + "</dct:issued>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:author_email>" + author + "</dcat:author_email>\n"

                #Publisher
                ficheroDataSet = ficheroDataSet + "\t\t<dct:publisher>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t<foaf:Organization>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<dct:title>"+ mainteiner +"</dct:title>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<foaf:homepage rdf:resource=\""+organizacionURL+"\"/>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t</foaf:Organization>\n"
                ficheroDataSet = ficheroDataSet + "\t\t</dct:publisher>\n"


                #Periodicidad
                ficheroDataSet = ficheroDataSet + "\t\t<dct:accrualPeriodicity>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t<dct:Frequency>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<rdfs:label>"+ frecuenciaLabel + "</rdfs:label>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<rdf:value>" + frecuenciaValue + "</rdf:value>\n"
                ficheroDataSet = ficheroDataSet  + "\t\t\t</dct:Frequency>\n"
                ficheroDataSet = ficheroDataSet + "\t\t</dct:accrualPeriodicity>\n"

                #Groups
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:theme>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t<rdf:Description>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<rdfs:label>Educación</rdfs:label>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<dct:description>Educación</dct:description>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t\t<dct:identifier>educacion</dct:identifier>\n"
                ficheroDataSet = ficheroDataSet  + "\t\t\t</rdf:Description>\n"
                ficheroDataSet = ficheroDataSet + "\t\t</dcat:theme>\n"

                ficheroDataSet = ficheroDataSet + "\t\t<dct:spatial>"+ cobertura_espacial +"</dct:spatial>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:temporal>" + str(intervalo) + "</dct:temporal>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:language>" + str(idioma).upper() + "</dct:language>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dct:license rdf:resource=\"" + str(licencia) + "\"></dct:license>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:granularity>" + nivel_detalle + "</dcat:granularity>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:dataQuality>" + str(calidad) + "</dcat:dataQuality>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:dataDictionary>" + str(calidad) + "</dcat:dataDictionary>\n"
                
                #Aragopedia, tienen todos el valor por defecto que es aragon
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:name_aragopedia>Aragón</dcat:name_aragopedia>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:short_uri_aragopedia>Aragón</dcat:short_uri_aragopedia>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:type_aragopedia>Aragón</dcat:type_aragopedia>\n"
                ficheroDataSet = ficheroDataSet + "\t\t<dcat:uri_aragopedia>http://opendata.aragon.es/recurso/territorio/ComunidadAutonoma/Aragón</dcat:uri_aragopedia>\n"
                
                #ficheroDataSet = ficheroDataSet + "\t\t<dct:status></dct:status>\n"

                '''
                ficheroDataSet = ficheroDataSet + "\t\t<dct:contributor>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t<rdf:Description>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t<foaf:name>"+mainteiner+"</foaf:name>\n"
                ficheroDataSet = ficheroDataSet + "\t\t\t</rdf:Description>\n"
                ficheroDataSet = ficheroDataSet + "\t\t</dct:contributor>\n"
                '''

                ficheroUDs = ficheroDataSet
                #ficheroUDs = ficheroUDs + "\t\t<dct:title>"+titulo+"</dct:title>\n"
                #ficheroUDs = ficheroUDs + "\t\t<dct:description>" + descripcion + "</dct:description>\n"
                #ficheroUDs = ficheroUDs + "\t\t<dct:identifier>" + identificador + "</dct:identifier>\n"

                titulo_propuesta_array = []
                #Leemos el CSV "PDs..."
                debug_pds = 0
                csvfile_PDs= config.UPLOAD_DOCUMENTS + "facilitamosOpenData/" + fil + "/" + pds_fileName
                with open(csvfile_PDs, 'rb') as csvfile_PDs:
                    spamreader_PDs = csv.reader(csvfile_PDs, delimiter=',')
                    fichero = ficheroUDs
                    #fichero = fichero + "\t\t<dcat:distribution>\n"
                    #Sacamos solo las que coincida un campo que previamente hemos creado en csv, excel, para relacionar
                    #UDs con PDs
                    #for row2 in itertools.islice(spamreader_PDs,fila,fila+5):
                    num = 0
                    for row2 in spamreader_PDs:
                        num = num + 1
                        titulo_propuesta = row2[0]
                        id = row2[1]
                        campo = row2[2]
                        valor = row2[3]

                        if valor == "" or not valor or valor is None:
                            valor = "#"
                        tamanyo =""
                        if row2[4] != "":
                            tamanyo = row2[4]
                        PDsID = row2[6]
                        formato = ""
                        if campo == "wpcf-actividades-zip":
                            formato = "ZIP"
                            formato_text = "HTML"
                        if campo == "wpcf-actividades-elp":
                            formato = ""
                            formato_text = "ELP"
                        if campo == "wpcf-actividades-scorm":
                            formato = ""
                            formato_text = "SCORM"
                        if(debug_pds == 1):
                            print("\t\t--BEGIN--")
                            print("\t\t titulo_propuesta: " + titulo_propuesta)
                            print("\t\t id: " + id)
                            print("\t\t campo: " + campo)
                            print("\t\t valor: " + valor)
                            print("\t\t tamanyo: " + tamanyo)
                            print("\t\t ---END---")

                        #Descargables
                        if UDsID == PDsID:
                            #Si es la 1º vez que leemos este titulo añadimos los metadatos generales
                            #if titulo_propuesta not in titulo_propuesta_array:
                                #fichero = fichero + "\t\t\t<dcat:Distribution>\n"

                            desc = ""
                            if campo == "wpcf-texto-descriptivo":
                                desc =  "\t\t\t\t<dct:description>"+valor+"</dct:description>\n"
                            elif campo == "_wpcf_belongs_unidad-didactica_id":
                                fichero = fichero
                            else:
                                fichero = fichero + "\t\t\t<dcat:Distribution>\n"
                                fichero = fichero + "\t\t\t\t<dct:title>"+titulo_propuesta+"</dct:title>\n"
                                #print titulo_general
                                #print titulo_propuesta
                                #testCadena = testCadena + titulo_general + ".-" + titulo_propuesta + "\n"
                                fichero = fichero + desc
                                titulo_propuesta_array.append(titulo_propuesta)
                                #fichero = fichero + "\t\t\t\t<dcat:label>"+campo+"</dcat:label>\n"
                                fichero = fichero + "\t\t\t\t<dcat:accessURL rdf:resource='"+valor+"'></dcat:accessURL>\n"
                                fichero = fichero + "\t\t\t\t<dcat:size>\n"
                                fichero = fichero + "\t\t\t\t\t<rdf:Description>\n"
                                fichero = fichero + "\t\t\t\t\t\t<dcat:bytes>" + tamanyo + "</dcat:bytes>\n"
                                fichero = fichero + "\t\t\t\t\t\t<rdfs:label>bytes</rdfs:label>\n"
                                fichero = fichero + "\t\t\t\t\t</rdf:Description>\n"
                                fichero = fichero + "\t\t\t\t</dcat:size>\n"
                                fichero = fichero + "\t\t\t\t<dct:format>\n"
                                fichero = fichero + "\t\t\t\t\t<dct:IMT>\n"
                                fichero = fichero + "\t\t\t\t\t\t<rdf:value>" + formato + "</rdf:value>\n"
                                fichero = fichero + "\t\t\t\t\t\t<rdfs:label>" + formato_text + "</rdfs:label>\n"
                                fichero = fichero + "\t\t\t\t\t</dct:IMT>\n"
                                fichero = fichero + "\t\t\t\t</dct:format>\n"
                                fichero = fichero + "\t\t\t</dcat:Distribution>\n"
                            #Cerramos cada 5 filas.
                            #if num%5 == 0:
                                #print "CIERRA"
                                #fichero = fichero + "\t\t\t</dcat:Distribution>\n"

                #fichero = fichero + "\t\t</dcat:distribution>\n"
                fichero = fichero + "\t</dcat:Dataset>\n"
                fichero = fichero + "</rdf:RDF>\n"

                # Copiar contenido a un fichero
                titulo_rdf = transformar(titulo_general)+ " .- " +transformar(titulo)
                f = open(config.UPLOAD_DOCUMENTS + "catedu/"+ titulo_rdf +".rdf","w")
                #f2 = open(config.UPLOAD_DOCUMENTS + "catedu/testCadena.txt","w")
                fichero = fichero.replace("&aacute;","á").replace("&eacute;","é").replace("&iacute;","í").replace("&oacute;","ó").replace("&uacute;","ú").replace("&nbsp;","").replace("\"","'").replace("&ldquo;","").replace("&rdquo;","").replace("&ntilde;","ñ").replace("&Aacute;","Á").replace("&Eacute;","É").replace("&Iacute;","Í)").replace("&Oacute;","Ó").replace("&Uacute;","Ú").replace("\&iexcl;","!").replace("\&iquest;","¿").replace("ldquo;"," ").replace("rdquo;"," ")
                fichero = fichero.replace("&","and")
                f.write(fichero)
                #f2.write(testCadena)
                total_creados +=  1
                #print("Se ha creado el ficehro" + config.UPLOAD_DOCUMENTS + "catedu/" + titulo_rdf +".rdf")
                f.close()

    print("Se han creado " + str(total_creados) + " ficheros en " + config.UPLOAD_DOCUMENTS + "catedu/ ")

main()
