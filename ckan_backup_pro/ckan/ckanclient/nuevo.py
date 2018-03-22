#!/usr/bin/python
# coding=utf-8
import glob
import xml.etree.ElementTree as ET
import re
import ckanclient
import sys
import config    


def main():
    QUERY = "SELECT "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_ORGANISATION AS Autor, "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_EMAIL AS Email_autor, "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.CODIGO_TEMA, IAES.MET_OPERACION.CODIGO_TEMA) || ' ' || NVL(IAES.MET_PRODUCTO.NOMBRE_TEMA, IAES.MET_OPERACION.NOMBRE_TEMA) AS Tema_estadistico,  "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.DATA_DESCR, IAES.MET_OPERACION.DATA_DESCR) AS Descripcion, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_UNIT AS Unidad_estadistica, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_POP AS Poblacion_estadistica, "
    QUERY = QUERY + "IAES.MET_DATASET.UNIT_MEASURE AS Unidades_de_medida,  "
    QUERY = QUERY + "IAES.MET_DATASET.REF_AREA AS Spatial,  "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.CODIGO_COVERAGE_TIME, IAES.MET_PRODUCTO.COVERAGE_TIME) AS Cobertura_temporal,  "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.CODIGO_COVERAGE_TIME, IAES.MET_PRODUCTO.COVERAGE_TIME) AS Temporal,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.BASE_PER AS Periodo_base, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.TIPO_OP AS Tipo_operacion, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.FREQ_DISS AS Frecuencia, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.SOURCE_TYPE AS Tipologia_datos_origen, "
    QUERY = QUERY + "IAES.MET_OPERACION.FUENTE AS Fuente, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_PROCESS AS Tratamiento_Estadistico, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ACCURACY AS Calidad, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_COM, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_PUB, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_DBA, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_BD, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_BD_SECA, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_BD_DWH, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_BD_PCAXIS, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_MICRO, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.DISS_FOR_OTROS, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.COMMENT_DSET, IAES.MET_PRODUCTO.DESCRIPCION_METOD) AS Notas_metodologicas, "
    QUERY = QUERY + "IAES.MET_OPERACION.CODIGO_PEN2013 AS Codigo_PEN2013, "
    QUERY = QUERY + "IAES.MET_OPERACION.NOMBRE_PEN2013 AS Nombre_PEN2013, "
    QUERY = QUERY + "IAES.MET_OPERACION.LEGISLACION_UE AS Legislacion_UE, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ETIQUETAS AS Etiquetas,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.CATEGORIA_OPENDATA AS Categoria, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_CRE_DATOS AS Fecha_creacion, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_MOD_DATOS AS Fecha_modificacion,  "
    QUERY = QUERY + "IAES.MET_DATASET.IDIOMA AS Idioma, "
    QUERY = QUERY + "IAES.MET_DATASET.LICENCIA AS Licencia, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.NIVEL_DETALLE, (IAES.MET_PRODUCTO.DATA_DESCR_VAR_ESTUDIO || '. ' || IAES.MET_PRODUCTO.DATA_DESCR_VAR_CLASIF || '. ' || IAES.MET_PRODUCTO.REF_PERIOD)) As Nivel_Detalle, "
    QUERY = QUERY + "IAES.MET_DATASET.NOMBRE_DS AS Titulo, "
    QUERY = QUERY + "IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA as Titulo_descarga,  "
    QUERY = QUERY + "IAES.MET_FICHEROS.URL_FICHERO_OPENDATA AS URL_descarga, "
    QUERY = QUERY + "IAES.MET_FICHEROS.SIZE_FICHERO_OPENDATA AS Tamanyo, "
    QUERY = QUERY + "IAES.MET_FICHEROS.FORMATO_FICHERO_OPENDATA AS Formato, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.FECHA_MOD_FICHA AS Fecha_cambio_metadatos, "
    QUERY = QUERY + "IAES.MET_OPERACION.FUENTE_FORMATO AS Formato_fuente, "
    QUERY = QUERY + "IAES.MET_DATASET.URL_OPENDATA_PUBLICADO AS url_publicado "
    QUERY = QUERY + "FROM ((IAES.MET_FICHEROS RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_DATASET ON IAES.MET_FICHEROS.ID_DATASET=IAES.MET_DATASET.ID_DATASET) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_PRODUCTO ON IAES.MET_DATASET.ID_PRODUCTO=IAES.MET_PRODUCTO.ID_PRODUCTO) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_OPERACION ON IAES.MET_PRODUCTO.ID_OPERACION=IAES.MET_OPERACION.ID_OPERACION "
    QUERY = QUERY + "WHERE IAES.MET_DATASET.INCLUIR_OPENDATA='SI' "
    QUERY = QUERY + "AND IAES.MET_PRODUCTO.CATEGORIA_OPENDATA is not null "
    QUERY = QUERY + "AND IAES.MET_DATASET.NOMBRE_DS is not null "
    QUERY = QUERY + "AND IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA is not null "
    print QUERY

main()
