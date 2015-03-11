#!/usr/bin/python
# -*- coding: utf-8 -*-


import config
import cx_Oracle
from time import time
from urllib import urlretrieve

import os

os.environ["NLS_LANG"] = ".UTF8"

def _download_xls_file(url):
    """ Download a xls with random name to hard disk"""
    dest = config.DOWNLOAD_TEMPORAL + "/" + str(int(time() * 100)) + ".xls"
    urlretrieve(url, dest)
    return dest

def descargar():
    return main()

def main():
    connection = cx_Oracle.connect(
    config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
    print  config.OPENDATA_CONEXION_BD
    cursor = connection.cursor()


    QUERY = "SELECT "
    QUERY = QUERY + "IAES.MET_DATASET.ID_DATASET AS IdDataset, "
    QUERY = QUERY + "IAES.MET_DATASET.NOMBRE_DS AS Titulo, "
    QUERY = QUERY + "IAES.MET_DATASET.URL_OPENDATA_PUBLICADO AS url_publicado, "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_ORGANISATION AS Autor, "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_EMAIL AS Email_autor, "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.DATA_DESCR, IAES.MET_OPERACION.DATA_DESCR) AS Descripcion, "
    QUERY = QUERY + "IAES.MET_DATASET.REF_AREA AS Spatial,  "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.CODIGO_COVERAGE_TIME, IAES.MET_PRODUCTO.COVERAGE_TIME) AS Temporal,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.FREQ_DISS AS Frecuencia, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ACCURACY AS Calidad, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.COMMENT_DSET, IAES.MET_PRODUCTO.DESCRIPCION_METOD) AS Notas_metodologicas, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.NIVEL_DETALLE, (IAES.MET_PRODUCTO.DATA_DESCR_VAR_ESTUDIO || '. ' || IAES.MET_PRODUCTO.DATA_DESCR_VAR_CLASIF || '. ' || IAES.MET_PRODUCTO.REF_PERIOD)) As Nivel_Detalle, "
    QUERY = QUERY + "IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA as Titulo_descarga,  "
    QUERY = QUERY + "IAES.MET_FICHEROS.URL_FICHERO_OPENDATA AS URL_descarga, "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.CODIGO_TEMA, IAES.MET_OPERACION.CODIGO_TEMA) || ' ' || NVL(IAES.MET_PRODUCTO.NOMBRE_TEMA, IAES.MET_OPERACION.NOMBRE_TEMA) AS Tema_estadistico,  "
    QUERY = QUERY + "IAES.MET_OPERACION.FUENTE AS Fuente, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_POP AS Poblacion_estadistica, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_UNIT AS Unidad_estadistica, "
    QUERY = QUERY + "IAES.MET_DATASET.UNIT_MEASURE AS Unidades_de_medida,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.BASE_PER AS Periodo_base, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.TIPO_OP AS Tipo_operacion, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.SOURCE_TYPE AS Tipologia_datos_origen, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_PROCESS AS Tratamiento_Estadistico, "
    QUERY = QUERY + "IAES.MET_OPERACION.LEGISLACION_UE AS Legislacion_UE, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ETIQUETAS AS Etiquetas,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.CATEGORIA_OPENDATA AS Categoria, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_CRE_DATOS AS Fecha_creacion, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_MOD_DATOS AS Fecha_modificacion,  "
    QUERY = QUERY + "IAES.MET_DATASET.IDIOMA AS Idioma, "
    QUERY = QUERY + "IAES.MET_DATASET.LICENCIA AS Licencia, "
    QUERY = QUERY + "IAES.MET_FICHEROS.FORMATO_FICHERO_OPENDATA AS Formato, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.FECHA_MOD_FICHA AS Fecha_cambio_metadatos "
    QUERY = QUERY + "FROM ((IAES.MET_FICHEROS RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_DATASET ON IAES.MET_FICHEROS.ID_DATASET=IAES.MET_DATASET.ID_DATASET) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_PRODUCTO ON IAES.MET_DATASET.ID_PRODUCTO=IAES.MET_PRODUCTO.ID_PRODUCTO) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_OPERACION ON IAES.MET_PRODUCTO.ID_OPERACION=IAES.MET_OPERACION.ID_OPERACION "
    QUERY = QUERY + "WHERE IAES.MET_DATASET.INCLUIR_OPENDATA='SI' " #and IAES.MET_DATASET.ID_DATASET=502  "
    QUERY = QUERY + "AND IAES.MET_PRODUCTO.CATEGORIA_OPENDATA is not null "
    QUERY = QUERY + "AND IAES.MET_DATASET.NOMBRE_DS is not null "
    QUERY = QUERY + "AND IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA is not null "
    print QUERY
    registros = cursor.execute(QUERY)
    lista = []

    # Cabecera del Fichero RDF
    fichero_RDF = "<?xml version=\"1.0\" encoding=\"utf-8\"?> <rdf:RDF xmlns:foaf=\"http://xmlns.com/foaf/0.1/\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:dcat=\"http://www.w3.org/ns/dcat#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:dct=\"http://purl.org/dc/terms/\">\n\n"

    fichero = fichero_RDF

    for r in registros:
        delete = False
        lista.append(r)

        idDataset = r[0]
        Titulo = r[1]
        url_publicado = r[2]
        autor = r[3]
        email_autor = r[4]
        Descripcion = r[5]
        Spatial = r[6]
        Temporal = r[7]
        Frecuencia = r[8]
        Calidad = r[9]
        Notas_metodologicas = r[10]
        Nivel_Detalle = r[11]
        Titulo_descarga = r[12]
        URL_descarga = r[13]
        Tema_estadistico = r[14]
        Fuente = r[15]
        Poblacion_estadistica = r[16]
        Unidad_estadistica = r[17]
        Unidades_de_medida = r[18]
        Periodo_base = r[19]
        Tipo_operacion = r[20]
        Tipologia_datos_origen = r[21]
        Tratamiento_Estadistico = r[22]
        Legislacion_UE = r[23]
        Etiquetas = r[24]
        Categoria = r[25]
        Fe_creacion = r[26]
        Fe_modificacion = r[27]
        Idioma = r[28]
        Licencia = r[29]
        Formato = r[30]
        F_cambio_metadatos = r[31]

        Formato_difusion=""

        #Dependen de parametro "organizacion"
        organizacion = "Instituto Aragonés de Estadística"
        organizacionUrl = "http://www.aragon.es/iaest"

        #Dependen del parÃ¡metro "frecuencia"
        if Frecuencia != None:
            if Frecuencia == "Diariamente":
                frecuenciaValue = "P1D"
                frecuenciaLabel = "Diaria"
            elif Frecuencia == "Mensualmente":
                frecuenciaValue = "P1M"
                frecuenciaLabel = "Mensual"
            else:
                frecuenciaValue = "P1Y"
                frecuenciaLabel = "Anual"
        else:
           frecuenciaValue = "P1Y"
           frecuenciaLabel = "Anual"

        #Dependen del parÃ¡metro "tema"
        tema = Categoria.replace(";", "")
        temaId = tema.lower().replace(" ", "-").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "")
        temaId = temaId.replace("-y-","-")
        temaId = temaId.replace("-e-","-")
        temaDes = Categoria.replace(";", "")


        if Nivel_Detalle != None:
            detalle = Nivel_Detalle
        else:
            detalle = ""

        if Notas_metodologicas != None:
            diccionario = Notas_metodologicas.strip()
        else:
            diccionario = ""

        if Calidad != None:
            calidad = Calidad.strip()
        else:
            calidad = ""

        if Idioma != None:
            idioma = Idioma.strip()
        else:
            idioma = ""

        if Licencia != None:
            licencia = Licencia.strip()
        else:
            licencia = ""

        if Fe_modificacion != None:
            fe_modificacion = Fe_modificacion
        else:
            fe_modificacion = ""

        if Fe_creacion != None:
            f_creacion = Fe_creacion
        else:
            f_creacion = ""


        #// Tipo ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        formato = Formato
        identificador = ""
        #// ID = Descripcion + nombre de archivo (sin tildes, espacios o signos de puntuación)
        if url_publicado !=None and url_publicado !="":
            if url_publicado.startswith("--"):
                url_publicado = url_publicado.lower().split("--")[1]
                delete =True
            identificador = url_publicado
        else:
            identificador = Titulo.decode('utf-8').encode('utf-8')
            identificador = identificador.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
            identificador = identificador.replace( "ú", "u").replace("%","")
            identificador = identificador.strip().lower().replace(":", "-").replace(")", "").replace(",", "").replace("'","")
            identificador = identificador.replace("(","").replace(".", "").replace(" ", "-")
            identificador = identificador.replace("--", "-").replace("ñ","ny").replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("º","")

        #// Se obtenian de la descripcion. Ahora tienen su propio campo
        if Etiquetas == None:
            tags = " "
        else:
            Etiquetas = Etiquetas.replace(";", ",")
            tags = Etiquetas.split(",")

        if URL_descarga == None:
            URL_descarga =" "

        aboutUrl = URL_descarga
        aboutUrl = aboutUrl.replace("&", "&amp;")
        title = Titulo
        description = Descripcion

        # Quitar los que no son solo zip y terminan en _d16 de COMARCA
        #if (!esquemas[r].equalsIgnoreCase("comarca") || (esquemas[r].equalsIgnoreCase("comarca") && (!identificador.endsWith("_d16") & & formato.equalsIgnoreCase(".zip"))))        {
        nombres = ""
        nombres = nombres + identificador + ".rdf\n"

        #fichero = fichero_RDF
        fichero = fichero + "\t<dcat:Dataset rdf:about=\"" + aboutUrl + "\">\n"
        fichero = fichero + "\t\t<dct:identifier>" + identificador[0:197]
        fichero = fichero + "</dct:identifier>\n" + "\t\t<dct:description>"
        fichero = fichero + description + "</dct:description>\n"

        for elemento in tags:
            if len(elemento) > 3:
                fichero = fichero + "\t\t<dcat:keyword xml:lang=\"es\">" + elemento.strip() + "</dcat:keyword>\n"


        # Fin del FOR
        fichero = fichero + "\t\t<dct:title>" + title + "</dct:title>\n"
        #fichero = fichero + "\t\t<dct:organization>" + "iaest" + "</dct:organization>\n"
        fichero = fichero + "\t\t<dct:modified>" + str(fe_modificacion) + "</dct:modified>\n"
        fichero = fichero + "\t\t<dct:organization>instituto_aragones_de_estadistica</dct:organization>\n"
        fichero = fichero + "\t\t<dct:issued>" + str(f_creacion) + "</dct:issued>\n"

        #// Publicador
        fichero = fichero + "\t\t<dcat:author_email>" + email_autor + "</dcat:author_email>\n"
        fichero = fichero + "\t\t<dct:publisher>\n"
        fichero = fichero + "\t\t\t<foaf:Organization>\n" + "\t\t\t\t<dct:title>"
        fichero = fichero + organizacion + "</dct:title>\n"
        fichero = fichero + "\t\t\t\t<foaf:homepage rdf:resource=\""
        fichero = fichero + organizacionUrl + "\"/>\n"
        fichero = fichero + "\t\t\t</foaf:Organization>\n" + "\t\t</dct:publisher>\n"
        #// Periodicidad
        fichero = fichero + "\t\t<dct:accrualPeriodicity>\n"
        fichero = fichero + "\t\t\t<dct:Frequency>\n" + "\t\t\t\t<rdf:value>"
        fichero = fichero + frecuenciaValue + "</rdf:value>\n"
        fichero = fichero + "\t\t\t\t<rdfs:label>" + frecuenciaLabel
        fichero = fichero + "</rdfs:label>\n" + "\t\t\t</dct:Frequency>\n"
        fichero = fichero + "\t\t</dct:accrualPeriodicity>\n"
        if detalle == "0":
            detalle = ""
        else:
            detalle = detalle
        if Spatial == None:
            Spatial = ""
        if Temporal == None:
            Temporal = ""
        if idioma == None:
            idioma=""
        if licencia == None:
            licencia = ""
        if detalle == None:
            detalle = ""
        if calidad == None:
            calidad = ""
        if diccionario == None:
            diccionario=""

        #forzamos a que elimine los datasets con formato pdf
        if formato != None and formato == 'pdf':
            delete = True
        diccionario = diccionario.replace("&","&amp;")

        fichero = fichero + "\t\t<dct:spatial>" + str(Spatial) + "</dct:spatial>\n"
        fichero = fichero + "\t\t<dct:temporal>" + str(Temporal) + "</dct:temporal>\n"
        fichero = fichero + "\t\t<dct:language>" + str(idioma) + "</dct:language>\n"
        fichero = fichero + "\t\t<dct:license rdf:resource=\"" + str(licencia) + "\"></dct:license>\n"
        fichero = fichero + "\t\t<dcat:granularity>" + str(detalle) + "</dcat:granularity>\n"
        fichero = fichero + "\t\t<dcat:dataQuality>" + str(calidad) + "</dcat:dataQuality>\n"
        fichero = fichero + "\t\t<dcat:dataDictionary>" + str(diccionario) + "</dcat:dataDictionary>\n"
        fichero = fichero + "\t\t<dct:status>" + str(delete) + "</dct:status>\n"


        if Tema_estadistico == None:
            Tema_estadistico =""
        if Unidad_estadistica == None:
            Unidad_estadistica =""
        if Poblacion_estadistica == None:
            Poblacion_estadistica =""
        if Unidades_de_medida == None:
            Unidades_de_medida =""

        if Spatial == None:
            Spatial = ""
        if Periodo_base == None:
            Periodo_base =""
        if Tipo_operacion == None:
            Tipo_operacion =""
        if Tipologia_datos_origen == None:
            Tipologia_datos_origen =""
        if Fuente == None:
            Fuente =""
        if Tratamiento_Estadistico == None:
            Tratamiento_Estadistico =""
        if Formato_difusion == None:
            Formato_difusion =""

        if Legislacion_UE == None:
            Legislacion_UE =""

        fichero = fichero + "\t\t<dcat:tema_estadistico>" + Tema_estadistico.strip() + "</dcat:tema_estadistico>\n"
        fichero = fichero + "\t\t<dcat:unidad_estadistica>" + Unidad_estadistica.strip() + "</dcat:unidad_estadistica>\n"
        fichero = fichero + "\t\t<dcat:poblacion_estadistica>" + Poblacion_estadistica.strip() + "</dcat:poblacion_estadistica>\n"
        fichero = fichero + "\t\t<dcat:unidad_medida>" + Unidades_de_medida.strip() + "</dcat:unidad_medida>\n"
        fichero = fichero + "\t\t<dcat:periodo_base>" + Periodo_base.strip() + "</dcat:periodo_base>\n"
        fichero = fichero + "\t\t<dcat:tipo_operacion>" + Tipo_operacion.strip() + "</dcat:tipo_operacion>\n"
        fichero = fichero + "\t\t<dcat:tipologia_datos_origen>" + Tipologia_datos_origen.strip() + "</dcat:tipologia_datos_origen>\n"
        fichero = fichero + "\t\t<dcat:fuente>" + Fuente.strip() + "</dcat:fuente>\n"
        fichero = fichero + "\t\t<dcat:tratamiento_estadistico>" + Tratamiento_Estadistico.strip() + "</dcat:tratamiento_estadistico>\n"
        fichero = fichero + "\t\t<dcat:formatos_difusion>" + Formato_difusion.strip() + "</dcat:formatos_difusion>\n"
        fichero = fichero + "\t\t<dcat:legislacion_ue>" + Legislacion_UE.strip() + "</dcat:legislacion_ue>\n"
        fichero = fichero + "\t\t<dcat:theme>\n"
        fichero = fichero + "\t\t\t<rdf:Description>\n" + "\t\t\t\t<rdfs:label>"
        fichero = fichero + tema + "</rdfs:label>\n" + "\t\t\t\t<dct:identifier>"
        fichero = fichero + temaId + "</dct:identifier>\n"
        fichero = fichero + "\t\t\t\t<dct:description>" + temaDes
        fichero = fichero + "</dct:description>\n" + "\t\t\t</rdf:Description>\n"
        fichero = fichero + "\t\t</dcat:theme>\n"

        accessURL = URL_descarga
        formatoValue = ""
        esPDF = 0
        if formato != None:
            if formato == "pdf":
                formatoValue = "application/pdf"
                esPDF = 1

            if formato == "shp.zip":
                formatoValue = "application/zip"

            if formato == "dwg.zip":
                formatoValue = "application/zip"

            if formato == "xml":
                formatoValue = "application/xml"

            if formato == "gml.zip":
                formatoValue = "application/zip"

            if formato == "kmz":
                formatoValue = "application/vnd.google-earth.kmz"

            if formato == "dxf.zip":
                formatoValue = "application/zip"


        if title == None:
            title = ""
        if description == None:
            description = ""
        if accessURL == None:
            accessURL = ""

        if formatoValue == None:
            formatoValue = ""
        if formato == None:
            formato = ""

        if (esPDF == 0):
            fichero = fichero + "\t\t<dcat:distribution>\n"
            fichero = fichero + "\t\t\t<dcat:Distribution>\n"
            fichero = fichero + "\t\t\t\t<rdfs:label>"
            fichero = fichero + title
            fichero = fichero + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t<dct:description>"
            fichero = fichero + description
            fichero = fichero + "</dct:description>\n"
            fichero = fichero + "\t\t\t\t<rdf:type rdf:resource=\"http://vocab.deri.ie/dcat#Download\"/>\n"
            fichero = fichero + "\t\t\t\t<dcat:accessURL rdf:resource=\""
            fichero = fichero + accessURL.replace("&","&amp;") + "\"></dcat:accessURL>\n"
            fichero = fichero + "\t\t\t\t<dcat:size>\n"
            fichero = fichero + "\t\t\t\t\t<rdf:Description>\n"
            fichero = fichero + "\t\t\t\t\t\t<dcat:bytes>"
            fichero = fichero + "</dcat:bytes>\n" + "\t\t\t\t\t\t <rdfs:label>"
            fichero = fichero + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t\t</rdf:Description>\n"
            fichero = fichero + "\t\t\t\t</dcat:size>\n"
            fichero = fichero + "\t\t\t\t<dct:format>\n"
            fichero = fichero + "\t\t\t\t\t<dct:IMT>\n"
            fichero = fichero + "\t\t\t\t\t\t<rdf:value>" + formatoValue
            fichero = fichero + "</rdf:value>\n" + "\t\t\t\t\t\t<rdfs:label>"
            fichero = fichero + formato + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t\t</dct:IMT>\n"
            fichero = fichero + "\t\t\t\t</dct:format>\n"
            fichero = fichero + "\t\t\t</dcat:Distribution>\n"
            fichero = fichero + "\t\t</dcat:distribution>\n"

        fichero = fichero + "\t</dcat:Dataset>\n"

        if (url_publicado == None or url_publicado == ""):
            updateCursor = connection.cursor()
            UPDATEQUERY = "UPDATE IAES.MET_DATASET SET URL_OPENDATA_PUBLICADO='" + str(identificador) + "' WHERE NOMBRE_DS= '" + r[1].replace("'","''") + "'"
            updateCursor.execute(UPDATEQUERY)
            connection.commit()
            updateCursor.close()

    fichero = fichero + "</rdf:RDF>\n"
    print fichero
    cursor.close()
    connection.close()

    # Copiar contenido a un fichero
    f = open(config.DOWNLOAD_PATH + "/downloadIaest.rdf","w")
    f.write(fichero)
    f.close()
    return fichero

main()
