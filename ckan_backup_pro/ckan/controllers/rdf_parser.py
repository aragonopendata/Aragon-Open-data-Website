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

    print "************************************ DATASET ************************************"
    print dataset
    print "************************************ BASE DE DATOS ************************************"
    print datasetBD
    #Compruebo datos simples
    datosARevisar = ['notes','title','author','owner_org','name', 'maintainer'];
    datosARevisarLista = ['extras','tags','resources'];

    coinciden=True;

    for datoARevisar in datosARevisar:
        print dataset.get(datoARevisar);
        print datasetBD.get(datoARevisar);
        if (datoARevisar == 'owner_org'):
            if (dataset.get(datoARevisar) is not None and dataset.get(datoARevisar) != datasetBD.get(datoARevisar) is not  None):
                 if (dataset.get(datoARevisar) != datasetBD.get(datoARevisar).encode('utf-8')):
                    print("NO COINCIDEN")
                    coinciden=False;


        else:
            if (dataset.get(datoARevisar) != datasetBD.get(datoARevisar).encode('utf-8')):
                print("NO COINCIDEN")
                coinciden=False;


    #Compruebo datos complejos
    for datoARevisarLista in datosARevisarLista:
        if coinciden:
            print("********************** " + datoARevisarLista);
            #REVISO LOS EXTRAS
            if datoARevisarLista == 'extras':
                # Extras a revisar
                sublista = ['Frequency','Spatial','Temporal','Language','Granularity','References','Data Quality','Data Dictionary']

                #Conversion a dictionary
                listaDict = dict((x[0], x[1]) for x in dataset.get(datoARevisarLista)[0:])

                print "DE BASE DE DATOS:"
                print datasetBD.get(datoARevisarLista)
                print "EL QUE LLEGA:"
                print(dataset.get(datoARevisarLista))
                print listaDict
                for itemSubLista in sublista:
                    print "NO TIENE" if (datasetBD.get(datoARevisarLista).get(itemSubLista)==None) else datasetBD.get(datoARevisarLista).get(itemSubLista).encode('utf-8');
                    print listaDict.get(itemSubLista)
                    if listaDict.get(itemSubLista) != None:
                        if datasetBD.get(datoARevisarLista).get(itemSubLista)!= None:
                            if (datasetBD.get(datoARevisarLista).get(itemSubLista).encode('utf-8') != listaDict.get(itemSubLista)):
                                print("NO COINCIDEN");
                                coinciden=False;
                        else:
                            print "en BD no existe: " + itemSubLista
                            coinciden = False # Hay q actualizar
                    #else: #viene sin el
                    #     if datasetBD.get(datoARevisarLista).get(itemSubLista)!= None:
                    #         print "en BD SI existia: " + itemSubLista
                    #         coinciden = False # Hay q actualizar

                # EXTRAS de IAEST
                if coinciden:
                    print "Comprobando IAEST..........."
                    subListaIAEST = ['01_IAEST_Tema estadístico','02_IAEST_Unidad Estadística','03_IAEST_Población estadística','04_IAEST_Unidad de medida','05_IAEST_Cobertura temporal','06_IAEST_Periodo base','07_IAEST_Tipo de operación','08_IAEST_Tipología de datos de origen','09_IAEST_Fuente','11_IAEST_Tratamiento estadístico', '12_IAEST_Formatos de difusión','15_IAEST_Legislación UE']

                   # Obtenemos la info de BD en DICT
                    listaDictIAESTBD={}
                    for item in datasetBD.get('extrasIAEST'):
                        listaDictIAESTBD[item.get('key')] = item.get('value');

                    for itemSubLista in subListaIAEST:
                        print "mirando: " + itemSubLista
                        if listaDict.get(itemSubLista) != None:
                            if listaDictIAESTBD.get(itemSubLista.decode('utf-8'))!= None:
                                print("esta en los 2")
                                if (listaDictIAESTBD.get(itemSubLista.decode('utf-8')).encode('utf-8') != listaDict.get(itemSubLista)):
                                    print("NO COINCIDEN");
                                    coinciden=False;
                            else:
                                print "en BD no existe: " + itemSubLista
                                coinciden = False # Hay q actualizar
                        #else: #viene sin el
                        #     if listaDictIAESTBD.get(itemSubLista.decode('utf-8'))!= None:
                        #         print "en BD SI existia: " + itemSubLista
                        #         coinciden = False # Hay q actualizar

            if datoARevisarLista == 'tags':
                tagsNuevos = dataset.get(datoARevisarLista)
                tagsAntiguos = datasetBD.get(datoARevisarLista)

                if (len(tagsAntiguos) != len(tagsNuevos)):
                    print("No hay el mismo numero");
                    coinciden = False;

                #SI hay mas o menos ya no coinciden...
                if coinciden:
                    tagsAntiguosClean = []
                    for tagOld in tagsAntiguos:
                        tagsAntiguosClean.append(tagOld.encode('utf-8'))

                    print("DEL DATASET:")
                    print(tagsNuevos)
                    print("DE BD:")
                    print(tagsAntiguosClean)

                    for tagNuevo in tagsNuevos:
                        print(tagsAntiguosClean.index(tagNuevo))
                        if tagsAntiguosClean.index(tagNuevo) != -1:
                            print ("ya existía")
                        else:
                            coinciden=False;

            if datoARevisarLista == 'resources':

                resourcesNuevos = dataset.get(datoARevisarLista)
                resourcesAntiguos = datasetBD.get(datoARevisarLista)

                # Si no coinciden en numero...
                if (len(resourcesNuevos) != len(resourcesAntiguos)):
                    print("no coinciden en numero")
                    coinciden = False;

                print ("Miramos mas....")
                print(coinciden)
                #Comprobamos cada resource
                if coinciden:
                    sublista = ['name','description','type','mimetype','format','size','url']
                    for resource in resourcesNuevos:
                        print("miro un resource...")
                        encontradoResource = False
                        for resourceOld in resourcesAntiguos:
                            print("miro de los viejos...")
                            # Los comparamos con la URL
                            print ("SON IGUALES.....????")
                            print(resourceOld.get(sublista[6]).encode('utf-8'))
                            print(resource.get(sublista[6]))
                            if resourceOld.get(sublista[6]).encode('utf-8') == resource.get(sublista[6]):
                                print("encontrado el resource...")
                                encontradoResource = True;
                                #Comprobamos los campos. Teniendo en cuenta si es None
                                for itemSubLista in sublista:
                                    print("compruebo: " + itemSubLista)
                                    if resourceOld.get(itemSubLista) is None:
                                        if resource.get(itemSubLista) !='':
                                            coinciden= False
                                    else:
                                        print(resourceOld.get(itemSubLista).encode('utf-8'))
                                        print(resource.get(itemSubLista))
                                        if itemSubLista == 'format':
                                            if resourceOld.get(itemSubLista).encode('utf-8').lower() != resource.get(itemSubLista).lower():
                                                print("no coinciden")
                                                coinciden = False;
                                        elif itemSubLista == 'size':
                                            if int(resourceOld.get(itemSubLista))!= int(resource.get(itemSubLista)):
                                                print("no coinciden en tamanio: ")
                                                print(resourceOld.get(itemSubLista))
                                                print(resource.get(itemSubLista))
                                                coinciden = False;
                                        else:
                                            if resourceOld.get(itemSubLista).encode('utf-8') != resource.get(itemSubLista):
                                                print("no coinciden")
                                                coinciden = False;

                        if not encontradoResource:
                            print("no he encontrado el resource")
                            coinciden = False;

    return coinciden;



def upload_dataset(dataset, script):
    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    try:

        try:
            coinciden = diffDatasets(ckan, dataset);
        except Exception as e:
            coinciden = False;
            print ("Ha fallado el diff de datasets")
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " HA FALLADO {0} ".format(dataset['name']))
                f.write("\n");
            f.close()
            print(e)

        print("COINCIDEN?: " + str(coinciden));

        #Solo se actualiza si hay cambios
        if not coinciden:
            ckan.package_entity_put(dataset)
            print ("Dataset {0} updated".format(dataset['name']))
            #guardo el log con los actualizados
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Dataset {0} updated".format(dataset['name']))
                f.write("\n");
            f.close()

    except ckanclient.CkanApiNotFoundError:
        try:
            print ("PRUEBO A CREARLO")
            ckan.package_register_post(dataset)
            print ("Dataset {0} created".format(dataset['name']))
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Dataset {0} created".format(dataset['name']))
                f.write("\n");
            f.close()
        except Exception as e:
            print ("Error while creating {0}:".format(dataset['name']))
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Error while creating {0}:".format(dataset['name']))
                f.write("\n");
            f.close()
            print e
    except Exception as e:
        print ("Error while updating {0}:".format(dataset['name']))
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

def create_resources(distributions_xml):
    resources = []
    for resources_xml in distributions_xml:
        for resource_xml in resources_xml:
            resource = {}
            # resource name
            resource['name'] = get_tag_text(resource_xml, rdfs_tag('label'))
            # resource description
            resource['description'] = get_tag_text(resource_xml, dct_tag('description'))
            resource['description'] = "ESTA ES LA DESCRIPCION" #quitarrrrrrrr
            # resource type
            type_xml = resource_xml.find(rdf_tag('type'))
            if type_xml is not None:
                resource['type'] = type_xml.get(rdf_tag('resource'))
            # resource mime type
            format_xml = resource_xml.find(dct_tag('format'))
            if format_xml is not None:
                value_tag = '{0}//{1}'.format(dct_tag('IMT'), rdf_tag('value'))
                resource['mimetype'] = get_tag_text(format_xml, value_tag)
                label_tag = '{0}//{1}'.format(dct_tag('IMT'), rdfs_tag('label'))
                resource['format'] = get_tag_text(format_xml, label_tag)
            # resource size
            size_tag = '{0}//{1}//{2}'.format(
                    dcat_tag('size'),
                    rdf_tag('Description'),
                    dcat_tag('bytes'))
            size_xml = resource_xml.find(size_tag)
            if size_xml is not None and size_xml.text is not None and  size_xml.text !=" ":
                if "Mb" in size_xml.text:
                    print(size_xml.text)
                    size_xml.text=str(float(size_xml.text.split("Mb")[0])* 1024 *1024)
                resource['size'] = int(round(float(size_xml.text.replace(',','.'))))
            else:
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
    print "CREATE - CREATE - CREATE "
    dataset = {}
    extras = []
    resources = []
    # name
    dataset['name'] = get_tag_text(xml, dct_tag('identifier')).replace("ñ","ny")

    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)

    organizacion =""
    try:
        organizacion = ckan.group_entity_get(get_tag_text(xml, dct_tag('organization')))
        if (organizacion != ""):
            dataset['owner_org'] = organizacion.get('id')

    except Exception:
         organizacion = ""
         print("no existe la organizacion")

    #print("********************** ORGANIZACION ************************: " + dataset['owner_org'])
    # description
    dataset['notes'] = get_tag_text(xml, dct_tag('description'))
    # title
    dataset['title'] = get_tag_text(xml, dct_tag('title'))

    dataset['author_email'] = get_tag_text(xml, dct_tag('author_email'))
    # tags
    tags = []
    for tag_xml in xml.findall(dcat_tag('keyword')):
        tags.append(clean_tag(tag_xml.text))
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
    # temporal
    extra = ['Temporal', get_tag_text_basic(xml, dct_tag('temporal'))]
    if (extra[1] != ""): extras.append(extra)
    # language
    extra = ['Language', get_tag_text(xml, dct_tag('language'))]
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
    # data dictionary
    extra = ['Data Dictionary', get_tag_text_basic(xml, dcat_tag('dataDictionary'))]
    if (extra[1] != ""): extras.append(extra)


    if (organizacion != "" and "org-iaest" == organizacion.get('name')):
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
        extra = ['15_IAEST_Legislación UE', get_tag_text(xml, dcat_tag('legislacion_ue'))]
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
    resources = create_resources(distributions_xml)
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
    rdfs = get_rdfs()
    datasets = []
    dataset_tag = str(ET.QName(config.DCAT_NAMESPACE, 'Dataset'))
    for rdf in rdfs:
        script = "";
        if "IAEST" in rdf.upper():
            script = "IAEST";
        else:
            script="CINTA";

        print("SCRIPT: " + script)


        if script == "CINTA":
            #connection = cx_Oracle.connect(config.OPENDATA_USR + "/" + config.OPENDATA_PASS  + "@" + config.OPENDATA_CONEXION_BD)
            print ("OPENDATA/OPENDATA@" + config.OPENDATA_CONEXION_BD_DES);
            connection = cx_Oracle.connect("OPENDATA/OPENDATA@" + config.OPENDATA_CONEXION_BD_DES)
            cursor = connection.cursor()
            registros = cursor.execute(
                "SELECT * FROM OPENDATA_V_REGIAEST_ACTIVOS")
            print("HECHO")
            datasetsEnBD = {}

            for r in registros:
                #rellenar HashMap
                print ("Registro: ")
                datasetsEnBD[r[0]] = "0"
                print(r);
                print  datasetsEnBD
                #check si esta en el hashmap. Si esta: 1 si no esta: 2
                #upload_dataset(ds,script)


        tree = ET.parse(rdf)
        contador = 0;
        for dataset in tree.findall(dataset_tag):
            contador = contador +1;
            datasets.append(dataset)
            ds = create_dataset(dataset)
            if script == "CINTA":
            #Si el script es de CINTA gestionar los repetidos...

                print(ds.get('name'))
                if datasetsEnBD.get(ds.get('name')) is None:
                     datasetsEnBD[ds.get('name')] = "2" #NO ENCONTRADO
                     #upload_dataset(ds,script)
                else:
                    datasetsEnBD[ds.get('name')] = "1" #ENCONTRADO
                    #upload_dataset(ds,script)
                print datasetsEnBD
            else:
                upload_dataset(ds,script)

        print ("------------------------- HABIA: " + str(contador))

        #datasetsEnBD['mapa-topografico_mapatopografico'] = "0"; #QUITARRRRRRRRRR
        #Cuando termine si es de CINTA
        if script == "CINTA":
            for key,value in datasetsEnBD.items():
                if (value == "2"):
                    print("*************** AÑADO: " + key);
                    cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_ADD', [key, 'NUEVO',None])
                    connection.commit()
                if (value == "0"): #HAY QUE BORRARLO
                    print("************ MARCO COMO BORRADO: " + key)
                    cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_REGISTRO_IAEST_UPD', [key, 'BORRAR', datetime.datetime.now()])
                    #ds['state'] = 'deleted';
                    #upload_dataset(ds,script)

        cursor.close()
        connection.close()
