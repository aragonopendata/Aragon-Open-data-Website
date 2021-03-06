#!/usr/bin/python
# coding=utf-8
"""
Crea un JSON extrayendo los datos ficheros .rdf
Usa la API de CKAN para crear los DataSets
"""
import glob
import xml.etree.ElementTree as ET
import re
import ckanclient
import datetime
import sys
import config
import urllib
import json


debug = False

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
    #Cuidado porque hay archivos con el nombre en mayúsculas y en este caso las URL son case-sensitive
    #res = url.encode('utf-8').lower()
    res = url.encode('utf-8')
    res = res.lower()
    res = re.sub("á", "a", res)
    res = re.sub("é", "e", res)
    res = re.sub("í", "i", res)
    res = re.sub("ó", "o", res)
    res = re.sub("ú", "u", res)
    res = re.sub("ñ", "ny", res)
    res = re.sub("Á", "a", res)
    res = re.sub("É", "e", res)
    res = re.sub("Í", "i", res)
    res = re.sub("Ó", "o", res)
    res = re.sub("Ú", "u", res)
    res = re.sub("Ñ", "ny", res)
    res = re.sub("[^-\\\.\/:\w]", "_", res)
    res = urllib.quote_plus(res)
    return res

def diffDatasets(ckan, dataset):
    coinciden = False

    return coinciden



def upload_dataset(dataset, script):
    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)

    try:

        #dataset = json.loads(str(dataset))
        #if(debug == True):
            #print("ckan.package_register_post("+str(dataset)+") BEGIN")
        ckan.package_register_post(dataset)
        #if(debug == True):
            #print("ckan.package_register_post("+str(dataset)+") END")
        fil = open(config.UPLOAD_DOCUMENTS + "/datasets.txt","w")
        fil.write(str(dataset))
        print ("[INFO] Dataset {0} created".format(dataset['name']))
        with open("uploads" + str(script) + ".log","a+") as f:
            f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " NUEVO - Dataset {0} created".format(dataset['name']))
            f.write("\n");
        f.close()

    except Exception as e:

        try:
            fil = open(config.UPLOAD_DOCUMENTS + "/datasets.txt","w")
            fil.write(str(dataset))
            ckan.package_entity_put(dataset)
            print ("[INFO] Dataset {0} updated".format(dataset['name']))
            #guardo el log con los actualizados
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Dataset {0} updated".format(dataset['name']))
                f.write("\n");
            f.close()

        except Exception as e:
            print ("[INFO] Error while creating {0}:".format(dataset['name']))
            with open("uploads" + str(script) + ".log","a+") as f:
                f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + " Error while creating {0}:".format(dataset['name']))
                f.write("\n");
            f.close()
            print e


def upload_group(group):
    ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
    try: 
        ckan.group_register_post(group)
    except ckanclient.CkanApiConflictError:
        if debug == True:
            print ("[INFO] Group {0} already created, skipping".format(group['name']))
    except Exception as e:
        print ("[INFO] Error while uploading group {0}:".format(group['name']))
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
    for resource_xml in distributions_xml:
        resource = {}
        # resource name
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
                size_xml.text=str(float(size_xml.text.split("Mb")[0])* 1024 *1024)
                resource['size'] = int(round(float(size_xml.text.replace(',','.'))))
            else:
                resource['size'] = get_tag_text(resource_xml, size_tag)

        #resource URL
        access_url_xml = resource_xml.find(dcat_tag('accessURL'))
        #resource['url'] = clean_url(access_url_xml.get(rdf_tag('resource')))
        resource['url'] = access_url_xml.get(rdf_tag('resource'))
        if(debug == True):
            print "resource['url']" + str(resource['url'])

        resources.append(resource)
    return resources

def create_groups(groups_xml):
    if(debug == True):
        print("create_groups(groups_xml)) BEGIN")
    groups = []
    for group_xml in groups_xml:
        group = {}
        description_xml = group_xml.find(rdf_tag('Description'))
        group['title'] = get_tag_text(description_xml, rdfs_tag('label'))
        group['name'] = get_tag_text(description_xml, dct_tag('identifier'))
        group['description'] = get_tag_text(description_xml, dct_tag('description'))
        upload_group(group)
        groups.append(group['name'])
    return groups
    dataset['groups'] = groups

def create_dataset(xml):
    if(debug == True):
        print("create_dataset(xml) BEGIN")
    dataset = {}
    extras = []
    resources = []
    # name
    dataset['name'] = get_tag_text(xml, dct_tag('identifier')).replace("ñ","ny")
    if(debug == True):
        print("-------------------->dataset['name']:" + dataset['name']);
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
    # temporal No tienen valores
#    extra = ['Temporal', get_tag_text_basic(xml, dct_tag('temporal'))]
#    if (extra[1] != ""): extras.append(extra)
    # language
    extra = ['LangES', get_tag_text(xml, dct_tag('language'))]
    if (extra[1] != ""): extras.append(extra)
    # references
    #extra = ['References', get_tag_text(xml, dct_tag('references'))]
    #if (extra[1] != ""): extras.append(extra)
    # granularity
    extra = ['Granularity', get_tag_text_basic(xml, dcat_tag('granularity'))]
    if (extra[1] != ""): extras.append(extra)
    # data quality
    extra = ['Data Quality', get_tag_text(xml, dcat_tag('dataQuality')).replace('/','-')]
    if (extra[1] != ""): extras.append(extra)
    # data dictionary
    extra = ['Data Dictionary', get_tag_text_basic(xml, dcat_tag('dataDictionary'))]
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


    tags = []
    for tag_xml in xml.findall(dcat_tag('keyword')):
        tags.append(clean_tag(tag_xml.text))

     # resources
    distributions = []
    #for distributions_xml in xml.findall(dcat_tag('Distribution')):
        #distributions.append(distributions_xml)
    distributions = xml.findall(dcat_tag('Distribution'))
    if debug == True:
        print "- distributions START- "
        for t in distributions:
            print str(t)
        print "- distributions END - "
    resources = create_resources(distributions)
    # groups / themes
    groups_xml = xml.findall(dcat_tag('theme'))
    groups = create_groups(groups_xml)

    dataset['resources'] = resources
    dataset['extras'] = extras
    dataset['groups'] = groups
    if(debug == True):
        print("create_dataset(xml) END")
    return dataset

def get_rdfs():
    rdfs = []
    if debug == True:
        test_path = "/data/ckan_ficheros/opendata/rdfTestCatedu"
    elif debug == False:
        test_path = "/data/ckan_ficheros/opendata/catedu"
    for rdf in glob.glob(test_path + "/*.rdf"):
        rdfs.append(rdf)
        '''
        print(rdf)
        print("---")
        break
        '''
    return rdfs

def parse_rdfs():
    rdfs = get_rdfs()
    datasets = []
    dataset_tag = str(ET.QName(config.DCAT_NAMESPACE, 'Dataset'))
    for rdf in rdfs:
        script="CATEDU"
        tree = ET.parse(rdf)
        contador = 0;
        for dataset in tree.findall(dataset_tag):
            contador = contador +1
            datasets.append(dataset)
            ds = create_dataset(dataset)
            upload_dataset(ds,script)

