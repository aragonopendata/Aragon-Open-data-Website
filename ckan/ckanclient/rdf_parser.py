#!/usr/bin/python
# coding=utf-8
import glob
import xml.etree.ElementTree as ET
import re
import ckanclient
import datetime
import sys
import config
import cx_Oracle
import psycopg2
import config

def clean_tag(tag):
    res = tag.encode('utf-8')
    res= re.sub(":","-", res)
    res= re.sub("/","-", res)

    if " (" in res:
        splitres = res.split(" (");
        res = splitres[1].split(")")[0] + " " + splitres[0];
    #res= re.sub("\\(","\\(", res)
    #res= re.sub("\\)","\\)", res)
    #res = re.sub("[^-\\\.\wñáéíóú]", "_", res)
    return res

def clean_url(url):
    res = url.encode('utf-8').lower()
    res = re.sub("á", "a", res)
    res = re.sub("é", "e", res)
    res = re.sub("í", "i", res)
    res = re.sub("ó", "o", res)
    res = re.sub("ú", "u", res)
    res = re.sub("[^-\\\.\/:\w]", "_", res)
    return res

def diffDatasets(ckan, dataset):

    datasetBD = ckan.package_entity_get(dataset['name'])

    #Compruebo datos simples
    datosARevisar = ['notes','title','author','owner_org','name', 'maintainer'];
    datosARevisarLista = ['extras','tags','resources'];

    coinciden=True;

    for datoARevisar in datosARevisar:
#        print 'Se va a comparar ', dataset.get(datoARevisar),'con',datasetBD.get(datoARevisar).encode('utf-8')
        if (datoARevisar == 'owner_org'):
            if (dataset.get(datoARevisar) is not None and dataset.get(datoARevisar) != datasetBD.get(datoARevisar) is not  None):
                 if (dataset.get(datoARevisar) != datasetBD.get(datoARevisar).encode('utf-8')):
                    coinciden=False;

        else:
            if (dataset.get(datoARevisar) != datasetBD.get(datoARevisar).encode('utf-8')):
                coinciden=False;


    #Compruebo datos complejos
    for datoARevisarLista in datosARevisarLista:
        if coinciden:
            #REVISO LOS EXTRAS
            if datoARevisarLista == 'extras':
                # Extras a revisar
                #sublista = ['Frequency','Spatial','Temporal','Language','Granularity','References','Data Quality','Data Dictionary']
                sublista = ['Frequency','Spatial','TemporalFrom', 'TemporalUntil','LangEs','Granularity','References','Data Quality', 'Data Quality URL0','Data Dictionary', 'Data Dictionary URL0', 'nameAragopedia', 'shortUriAragopedia', 'typeAragopedia', 'uriAragopedia']

                #Conversion a dictionary
                listaDict = dict((x[0], x[1]) for x in dataset.get(datoARevisarLista)[0:])


                for itemSubLista in sublista:

                    if listaDict.get(itemSubLista) != None:
                        if datasetBD.get(datoARevisarLista).get(itemSubLista)!= None:
                            if (datasetBD.get(datoARevisarLista).get(itemSubLista).encode('utf-8') != listaDict.get(itemSubLista)):
                                coinciden=False;
                        else:
                            coinciden = False # Hay q actualizar
                    #else: #viene sin el
                    #     if datasetBD.get(datoARevisarLista).get(itemSubLista)!= None:
                    #         print "en BD SI existia: " + itemSubLista
                    #         coinciden = False # Hay q actualizar

                # EXTRAS de IAEST
                if coinciden:
                    subListaIAEST = ['01_IAEST_Tema estadístico','02_IAEST_Unidad Estadística','03_IAEST_Población estadística','04_IAEST_Unidad de medida','05_IAEST_Cobertura temporal','06_IAEST_Periodo base','07_IAEST_Tipo de operación','08_IAEST_Tipología de datos de origen','09_IAEST_Fuente','11_IAEST_Tratamiento estadístico', '12_IAEST_Formatos de difusión','15_IAEST_Legislación UE']

                   # Obtenemos la info de BD en DICT
                    listaDictIAESTBD={}
                    for item in datasetBD.get('extrasIAEST'):
                        listaDictIAESTBD[item.get('key')] = item.get('value');

                    for itemSubLista in subListaIAEST:
                        if listaDict.get(itemSubLista) != None:
                            if listaDictIAESTBD.get(itemSubLista.decode('utf-8'))!= None:
                                if (listaDictIAESTBD.get(itemSubLista.decode('utf-8')).encode('utf-8') != listaDict.get(itemSubLista)):
                                    coinciden=False;
                            else:
                                coinciden = False # Hay q actualizar
                        #else: #viene sin el
                        #     if listaDictIAESTBD.get(itemSubLista.decode('utf-8'))!= None:
                        #         print "en BD SI existia: " + itemSubLista
                        #         coinciden = False # Hay q actualizar

            if datoARevisarLista == 'tags':
                tagsNuevos = dataset.get(datoARevisarLista)
                tagsAntiguos = datasetBD.get(datoARevisarLista)

                if (len(tagsAntiguos) != len(tagsNuevos)):
                    coinciden = False;

                #SI hay mas o menos ya no coinciden...
                if coinciden:
                    tagsAntiguosClean = []
                    for tagOld in tagsAntiguos:
                        tagsAntiguosClean.append(tagOld.encode('utf-8'))


                    for tagNuevo in tagsNuevos:
                        if tagsAntiguosClean.index(tagNuevo) == -1:
                            coinciden=False;

            if datoARevisarLista == 'resources':

                resourcesNuevos = dataset.get(datoARevisarLista)
                resourcesAntiguos = datasetBD.get(datoARevisarLista)

                # Si no coinciden en numero...
                if (len(resourcesNuevos) != len(resourcesAntiguos)):
                    coinciden = False;


                #Comprobamos cada resource
                if coinciden:
                    sublista = ['name','description','type','mimetype','format','mimetype_inner','size','url']
                    #sublista = ['name','description','type','mimetype','format','size','url']
                    for resource in resourcesNuevos:
                        encontradoResource = False
                        for resourceOld in resourcesAntiguos:
                            # Los comparamos con la URL

                            if resourceOld.get(sublista[7]).encode('utf-8') == resource.get(sublista[7]):
                                encontradoResource = True;
                                #Comprobamos los campos. Teniendo en cuenta si es None
                                for itemSubLista in sublista:
                                    if resourceOld.get(itemSubLista) is None:
                                        if resource.get(itemSubLista) !='':
                                            coinciden= False
                                    else:
                                        if itemSubLista == 'format':
                                            if resourceOld.get(itemSubLista).encode('utf-8').lower() != resource.get(itemSubLista).lower():
                                                coinciden = False;
                                        elif itemSubLista == 'size':
                                            if int(resourceOld.get(itemSubLista))!= int(resource.get(itemSubLista)):
                                                coinciden = False;
                                        else:
                                            if resourceOld.get(itemSubLista).encode('utf-8') != resource.get(itemSubLista):
                                                coinciden = False;

                        if not encontradoResource:
                            coinciden = False;

    print 'Los dataset coinciden ', coinciden
    return coinciden;



def upload_dataset(dataset, script=None):
    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    try:

        try:
            coinciden = diffDatasets(ckan, dataset);
        except Exception as e:
            coinciden = False;
            print ("Ha fallado el diff de datasets")
            print(e)


        #Solo se actualiza si hay cambios
        if not coinciden or dataset['state']=='deleted':
            ckan.package_entity_put(dataset)
            print ("Dataset {0} updated".format(dataset['name']))
            #guardo el log con los actualizados
            if script:
		          with open("uploads" + str(script) + ".log","a+") as f:
		              f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Dataset {0} updated".format(dataset['name']))
		              f.write("\n");
		          f.close()

    except ckanclient.CkanApiNotFoundError:
        try:
            ckan.package_register_post(dataset)
            print ("Dataset {0} created".format(dataset['name']))
            if script:
		          with open("uploads" + str(script) + ".log","a+") as f:
		              f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " NUEVO - Dataset {0} created".format(dataset['name']))
		              f.write("\n");
		          f.close()
        except Exception as e:
            print ("Error while creating {0}:".format(dataset['name']))
            if script:
		          with open("uploads" + str(script) + ".log","a+") as f:
		              f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Error while creating {0}:".format(dataset['name']))
		              f.write("\n");
		          f.close()
            print e
    except Exception as e:
        print ("Error while updating {0}:".format(dataset['name']))
        if script:
		      with open("uploads" + str(script) + ".log","a+") as f:
		          f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Error while updating {0}:".format(dataset['name']))
		          f.write("\n");
		      f.close()
        print e

def upload_group(group):
    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    try: 
        ckan.group_register_post(group)
    except ckanclient.CkanApiConflictError:
        print ("Group {0} already created, skipping".format(group['name']))
    except Exception as e:
        print ("Error while uploading group {0}:".format(group['name']))
        print e


def dcat_tag(tag):
    return str(ET.QName(config.DCAT_NAMESPACE, tag))

def dct_tag(tag):
    return str(ET.QName(config.DCT_NAMESPACE, tag))

def rdfs_tag(tag):
    return str(ET.QName(config.RDFS_NAMESPACE, tag))

def foaf_tag(tag):
    return str(ET.QName(config.FOAF_NAMESPACE, tag))

def rdf_tag(tag):
    return str(ET.QName(config.RDF_NAMESPACE, tag))

def get_tag_text(xml, tag):
    record = xml.find(tag)
    if record is not None and record.text is not None:
        return record.text.replace('/','-').encode('utf-8')
    else:
        return ""

def get_tag_text_basic(xml, tag):
    record = xml.find(tag)
    if record is not None and record.text is not None:
        return record.text.encode('utf-8')
    else:
        return ""


#Esta funcion se le mete el formato. Devuelve  mimetype_inner
def correctMimetypeInner(formato):
	devolver=''
	print 'El formato es ', formato
	formatValueList_inner = {
		'CSV': 'text/csv', 
		'DGN': 'image/vnd.dgn',
		'DWG': 'image/vnd.dwg',
		'DXF': 'application/dxf',
		'ELP': 'application/elp',
		'GEOJSON': 'application/vnd.geo+json',
		'GML': 'application/gml+xml',
		'HTML': 'text/html',
		'ICS': 'text/calendar',
		'JPG': 'image/jpeg',
		'JSON': 'application/json',
		'KMZ': 'application/vnd.google-earth.kmz',
		'ODS': 'application/vnd.oasis.opendocument.spreadsheet',
		'PNG': 'image/png',
		'PX': 'text/pc-axis',
		'RSS': 'application/rss+xml',
		'SCORM': 'application/scorm',
		'SHP': 'application/x-zipped-shp',
		'SIG': 'application/pgp-signature',
		'TXT': 'text/plain',
		'URL': 'text/uri-list',
		'XLS': 'application/vnd.ms-excel',
		'XLSX': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		'XML': 'application/xml',
		'XSLX': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		'ZIP': 'application/zip'
	}
	
	if formato.upper() in formatValueList_inner:
		devolver=formatValueList_inner[formato.upper()]
	else:
		print 'Error con el mimetype_inner el formato es ', formato 
	
	return devolver

#Esta funcion se le mete el modo de acceso. Devuelve  mimetype
def correctMimetype(formato):
	devolver=''
	print 'El modo de acceso es ', formato
	formatValueList = {
		'HTML': 'text/html',
		'SHP': 'application/zip',
		'ZIP': 'application/zip',
		'APPLICATION/ZIP' : 'application/zip',
		'':'',
		'APPLICATION-ZIP' : 'application/zip'
		
	}
	
	if formato.upper() in formatValueList:
		devolver=formatValueList[formato.upper()]
	else:
		print 'Error con el modo de acceso el formato es ', formato
	
	return devolver

def create_resources(distributions_xml, title):
    resources = []
    for resources_xml in distributions_xml:
        for resource_xml in resources_xml:
            resource = {}
            # resource name
            name= get_tag_text(resource_xml, dct_tag('title'))
            if (name==None) | (name==''):
              resource['name'] = title
            else:
              resource['name'] = get_tag_text(resource_xml, dct_tag('title'))
            # resource description
            resource['description'] = get_tag_text(resource_xml, dct_tag('description'))
            # resource type
            type_xml = resource_xml.find(rdf_tag('type'))
            if type_xml is not None:
                resource['type'] = type_xml.get(rdf_tag('resource'))
            # resource mime type
            format_xml = resource_xml.find(dct_tag('format'))
            if format_xml is not None:
                
                value_tag = '{0}//{1}'.format(dct_tag('IMT'), rdf_tag('value'))
                modoAcceso = get_tag_text(format_xml, value_tag)
                resource['mimetype'] = correctMimetype(modoAcceso)
                label_tag = '{0}//{1}'.format(dct_tag('IMT'), rdfs_tag('label'))
                formato = get_tag_text(format_xml, label_tag)
                resource['format'] = formato
                resource['mimetype_inner'] = correctMimetypeInner(formato)
                #print '+++El modo de acceso es', modoAcceso, 'y el formato es ', formato, ' en el datase de nombre', resource['name']
#                resource['format'] = get_tag_text(format_xml, label_tag)
            # resource size
#            size_tag = '{0}//{1}//{2}'.format(
#                    dcat_tag('size'),
#                    rdf_tag('Description'),
#                    dcat_tag('bytes'))
#            size_xml = resource_xml.find(size_tag)
#            if size_xml is not None and size_xml.text is not None and  size_xml.text !=" ":
#                if "Mb" in size_xml.text:
#                    size_xml.text=str(float(size_xml.text.split("Mb")[0])* 1024 *1024)
#                resource['size'] = int(round(float(size_xml.text.replace(',','.'))))
#            else:
            
            resource['size'] = ""
            # resource url
            access_url_xml = resource_xml.find(dcat_tag('accessURL'))
            #resource['url'] = clean_url(access_url_xml.get(rdf_tag('resource')))
            resource['url'] = access_url_xml.get(rdf_tag('resource'))
            resources.append(resource)
    return resources

def create_groups(groups_xml):
    groups = []
    for group_xml in groups_xml:
        group = {}
        description_xml = group_xml.find(rdf_tag('Description'))
        group['title'] = get_tag_text(description_xml, rdfs_tag('label'))
        group['name'] = clean_url(get_tag_text(description_xml, dct_tag('identifier')))
        group['description'] = get_tag_text(description_xml, dct_tag('description'))
        upload_group(group)
        groups.append(group['name'])
    return groups
    dataset['groups'] = groups

def create_dataset(xml):
    dataset = {}
    extras = []
    resources = []
    # name
#    dataset['name'] = get_tag_text(xml, dct_tag('identifier')).replace("ñ","ny").
    dataset['name'] = get_tag_text(xml, dct_tag('identifier')).replace("ñ","ny").replace(":","")

    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)

    organizacion =""
    
    try:
        #print "Organization_: "+str(get_tag_text(xml, dct_tag('organization')))
        #print "xml:"+str(xml)
        #print "prueba2: "+str(ckan.group_entity_get(get_tag_text(xml, dct_tag('organization'))))
        organizacion = ckan.group_entity_get(get_tag_text(xml, dct_tag('organization')))
        #print str(organizacion)
        
        if (organizacion != ""):
            dataset['owner_org'] = organizacion.get('id')

    except Exception:
         organizacion = ""
         print("no existe la organizacion")

    print("********************** ORGANIZACION ************************: " + dataset['name'])
    # description
    dataset['notes'] = get_tag_text(xml, dct_tag('description'))
    #print dataset['notes']
    # title
    dataset['title'] = get_tag_text(xml, dct_tag('title'))
    #print dataset['title']

    dataset['author_email'] = get_tag_text(xml, dct_tag('author_email'))
    # tags
    tags = []
    for tag_xml in xml.findall(dcat_tag('keyword')):
        if clean_tag(tag_xml.text).isupper():
            tags.append(clean_tag(tag_xml.text))
        else:
            tags.append(clean_tag(tag_xml.text).capitalize())
    dataset['tags'] = tags
    # modified
    dataset['metadata_modified'] = get_tag_text(xml, dct_tag('modified'))
    # created
    dataset['metadata_created'] = get_tag_text(xml, dct_tag('issued'))
    # frequency 
    frequency_tag = '{0}//{1}//{2}'.format(dct_tag('accrualPeriodicity'), 
            dct_tag('Frequency'),
            rdfs_tag('label'))
    extra = ['Frequency', get_tag_text(xml, frequency_tag)]
    if (extra[1] != ""): extras.append(extra)
    # spatial
    extra = ['Spatial', get_tag_text(xml, dct_tag('spatial'))]
    if (extra[1] != ""): extras.append(extra)
    # Temporal_from
    extra = ['TemporalFrom', get_tag_text_basic(xml, dct_tag('temporalFrom'))]
    if (extra[1] != ""): extras.append(extra)
    # Temporal_until
    extra = ['TemporalUntil', get_tag_text_basic(xml, dct_tag('temporalUntil'))]
    if (extra[1] != ""): extras.append(extra)
    # language
    extra = ['LangES', get_tag_text(xml, dct_tag('language'))]
    if (extra[1] != ""): extras.append(extra)
    # references
    extra = ['References', get_tag_text(xml, dct_tag('references'))]
    if (extra[1] != ""): extras.append(extra)
    # granularity
    extra = ['Granularity', get_tag_text_basic(xml, dcat_tag('granularity'))]
    if (extra[1] != ""): extras.append(extra)
    # data quality
    extra = ['Data Quality', get_tag_text(xml, dcat_tag('dataQuality')).replace('/','-')]
    if (extra[1] != ""): extras.append(extra)
    # data quality URL
    extra = ['Data Quality URL0', get_tag_text_basic(xml, dcat_tag('urlQuality'))]
    if (extra[1] != ""): extras.append(extra)
    # data dictionary
    extra = ['Data Dictionary', get_tag_text_basic(xml, dcat_tag('dataDictionary'))]
    if (extra[1] != ""): extras.append(extra)
    # data dictionary URL
    extra = ['Data Dictionary URL0', get_tag_text_basic(xml, dcat_tag('urlDictionary'))]
    if (extra[1] != ""): extras.append(extra)
    
    #Extras de Aragopedia
    # nameAragopedia
    extra = ['nameAragopedia', get_tag_text(xml, dcat_tag('name_aragopedia'))]
    if (extra[1] != ""): extras.append(extra)
    # shortUriAragopedia
    extra = ['shortUriAragopedia', get_tag_text(xml, dcat_tag('short_uri_aragopedia'))]
    if (extra[1] != ""): extras.append(extra)
    # typeAragopedia
    extra = ['typeAragopedia', get_tag_text(xml, dcat_tag('type_aragopedia'))]
    if (extra[1] != ""): extras.append(extra)
    # uriAragopedia
    extra = ['uriAragopedia', get_tag_text_basic(xml, dcat_tag('uri_aragopedia'))]
    if (extra[1] != ""): extras.append(extra)


    if (organizacion != "" and "instituto-aragones-estadistica" == organizacion.get('name')):
        extra = ['01_IAEST_Tema estadístico', get_tag_text(xml, dcat_tag('tema_estadistico'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['02_IAEST_Unidad Estadística', get_tag_text(xml, dcat_tag('unidad_estadistica'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['03_IAEST_Población estadística', get_tag_text(xml, dcat_tag('poblacion_estadistica'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['04_IAEST_Unidad de medida', get_tag_text(xml, dcat_tag('unidad_medida'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['05_IAEST_Cobertura temporal', get_tag_text(xml, dcat_tag('cobertura_temporal'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['06_IAEST_Periodo base', get_tag_text(xml, dcat_tag('periodo_base'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['07_IAEST_Tipo de operación', get_tag_text(xml, dcat_tag('tipo_operacion'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['08_IAEST_Tipología de datos de origen', get_tag_text(xml, dcat_tag('tipologia_datos_origen'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['09_IAEST_Fuente', get_tag_text(xml, dcat_tag('fuente'))]
        if (extra[1] != ""): extras.append(extra)
        #extra = ['10_IAEST_Formato de la fuente', get_tag_text(xml, dcat_tag('formato_fuente'))]
        #if (extra[1] != ""): extras.append(extra)
        extra = ['11_IAEST_Tratamiento estadístico', get_tag_text(xml, dcat_tag('tratamiento_estadistico'))]
        if (extra[1] != ""): extras.append(extra)
        extra = ['12_IAEST_Formatos de difusión', get_tag_text(xml, dcat_tag('formatos_difusion'))]
        if (extra[1] != ""): extras.append(extra)
        #extra = ['13_IAEST_Nombre de la operación en el PEN 2013-2016', get_tag_text(xml, dcat_tag('nombre_op_pen'))]
        #if (extra[1] != ""): extras.append(extra)
        #extra = ['14_IAEST_Código de la operación en el PEN 2013-2016', get_tag_text(xml, dcat_tag('cod_op_pen'))]
        #if (extra[1] != ""): extras.append(extra)
        print "\n\n\nLegalizacion\n"
        print get_tag_text_basic(xml, dcat_tag('legislacion_ue'))
        extra = ['15_IAEST_Legislación UE', get_tag_text_basic(xml, dcat_tag('legislacion_ue'))]
        if (extra[1] != ""): extras.append(extra)

    # author
    author_tag = '{0}//{1}//{2}'.format(dct_tag('publisher'), 
            foaf_tag('Organization'),
            dct_tag('title'))
    dataset['author'] = get_tag_text(xml, author_tag)
    dataset['maintainer'] = get_tag_text(xml, author_tag)
	
    if get_tag_text(xml, dct_tag('status')).lower() == 'true':
        dataset['state'] = 'deleted'
    else:
        dataset['state'] = 'active'
    # url
    homepage_tag = '{0}//{1}//{2}'.format(dct_tag('publisher'), 
            foaf_tag('Organization'),
            foaf_tag('homepage'))
    homepage_xml = xml.find(homepage_tag)
    dataset['url'] = homepage_xml.get(rdf_tag('resource'))
    # license
    license_xml = xml.find(dct_tag('license'))
    license = license_xml.get(rdf_tag('resource'))
    if re.match(".*[Cc][Cc]-[Bb][Yy]", license):
        dataset['license_id'] = "cc-by"

    # resources
    distributions_xml = xml.findall(dcat_tag('distribution')) 
    resources = create_resources(distributions_xml, dataset['title'])
    # groups / themes
    groups_xml = xml.findall(dcat_tag('theme'))
    groups = create_groups(groups_xml)

    dataset['resources'] = resources
    dataset['extras'] = extras
    dataset['groups'] = groups
    return dataset

def get_rdfs():
    rdfs = []
    for rdf in glob.glob(config.DOWNLOAD_PATH + "/*.rdf"):
        rdfs.append(rdf)
    return rdfs

def parse_rdfs():
    print "red_parser"
    rdfs = get_rdfs()
    print 'Hay ', len(rdfs), 'datasets '
    datasets = []
    dataset_tag = str(ET.QName(config.DCAT_NAMESPACE, 'Dataset'))
    
    for rdf in rdfs:
        script = "";
        if "IAEST" in rdf.upper():
            script = "IAEST";
        else:
            script="CINTA";

        if script == "CINTA":
            #connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS  + "@" + config.OPENDATA_CONEXION_BD)
            #connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS  + "@" + config.OPENDATA_CONEXION_BD_PRE)
            #connection = cx_Oracle.connect("OPENDATA/OPENDATA@" + config.OPENDATA_CONEXION_BD_DES)
            #connection =  config.conexion('opendata-postgre')
            
            #connection = psycopg2.connect(config.OPENDATA_POSTGRE_CONEXION_BD)
            connection = config.conexion('opendata-postgre')
            cursor = connection.cursor()
            consulta="SELECT package_revision.name, group_revision.name FROM public.package_revision, public.group_revision WHERE  package_revision.owner_org = group_revision.id AND package_revision.state = 'active' AND package_revision.current = 't' AND (group_revision.name='instituto-geografico-aragon' OR group_revision.name='instituto-aragones-gestion-ambiental' OR group_revision.name='direccion-general-urbanismo') AND package_revision.name NOT IN ('servicio-descarga-cartografica-e-1-1000-localidad', 'servicio-descarga-cartografica-e-1-1000-municipios', 'servicio-descarga-cartografica-e-1-5000-y-e-1-10000', 'expedientes-de-modificaciones-de-planeamiento-de-desarrollo-de-aragon-de-la-direccion-general-de-urbanismo', 'expedientes-de-planeamiento-de-desarrollo-de-aragon-de-la-direccion-general-de-urbanismo', 'expedientes-de-planeamiento-general-de-aragon-de-la-direccion-general-de-urbanismo', 'expedientes-de-modificaciones-de-planeamiento-general-y-de-modificaciones-de-delimitaciones-de-suelo-urbano-de-aragon-de-la-direccion-general-de-urbanismo') ORDER BY group_revision.name ASC"
            q=cursor.execute(consulta)
            
            
            #registros = cursor.execute(
                #"SELECT * FROM OPENDATA_V_REGIAEST_ACTIVOS")
            datasetsEnBD = {}
            contadorDict = 0;
            registros = cursor.fetchall()
            if registros is not None:
              for r in registros:
                  contadorDict =contadorDict +1;
                  #rellenar HashMap
                  datasetsEnBD[r[0]] = "0"
                  #check si esta en el hashmap. Si esta: 1 si no esta: 2
                  #upload_dataset(ds,script)
              print 'Dataset eEn BD es ', str(datasetsEnBD), 'y tiene ',len(datasetsEnBD)
            else:
              print 'No hay recursos'

        print "El script es "+script+" y el fichero con el rdf esta en "+rdf

        
        parser = ET.XMLParser()
        tree = ET.parse(rdf,parser)
        print tree;
        contador = 0;
        for dataset in tree.findall(dataset_tag):
            contador = contador +1;
            datasets.append(dataset)
            ds = create_dataset(dataset)
            if script == "CINTA":
            #Si el script es de CINTA gestionar los repetidos...

                
                if datasetsEnBD.get(ds.get('name')) is None:
                     datasetsEnBD[ds.get('name')] = "2" #NO ENCONTRADO
                     upload_dataset(ds,script)
                else:
                    datasetsEnBD[ds.get('name')] = "1" #ENCONTRADO
                    upload_dataset(ds,script)
            else:
                upload_dataset(ds,script)


        #Cuando termine si es de CINTA
        if script == "CINTA":
            for key,value in datasetsEnBD.items():
                
                print 'La key es ', str(key), ' y el value es', str(value)
                
                if (value == "2"):
                    print 'Se va a insertar '+str(key)
                    #cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [key, 'ACTIVO',None])
                    with open("uploads" + str(script) + ".log","a+") as f:
                        f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Añado como borrado :" + key)
                        f.write("\n");
                    f.close()
                    connection.commit()
                if (value == "0"): #HAY QUE BORRARLO
                    #cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_UPD', [key, 'BORRAR', datetime.datetime.now()])

                    with open("uploads" + str(script) + ".log","a+") as f:
                        f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Marco como borrado :" + key)
                        f.write("\n");
                    f.close()

                    
                    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
                    datasetABorrar = ckan.package_entity_get(key)
                    datasetABorrar['state'] = 'deleted';
                    upload_dataset(datasetABorrar,script)

            cursor.close()
            connection.close()
