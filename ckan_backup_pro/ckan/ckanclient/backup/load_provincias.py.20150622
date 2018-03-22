#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import glob
import xml.etree.ElementTree as ET
import rdf_parser

def get_rdfs2():
    rdfs = []
    for rdf in glob.glob(config.DOWNLOAD_PATH + "/datosPignatelli.rdf"):
        rdfs.append(rdf)
    return rdfs

def parse_rdfs2():
    rdfs = get_rdfs2()
    datasets = []
    dataset_tag = str(ET.QName(config.DCAT_NAMESPACE, 'Dataset'))
    for rdf in rdfs:
        tree = ET.parse(rdf)
        for dataset in tree.findall(dataset_tag):
          	datasets.append(dataset)
            	ds = rdf_parser.create_dataset(dataset)
            	rdf_parser.upload_dataset(ds)

def main():
    rdftotal = ""
    rdftotal = rdftotal  + '<?xml version="1.0" encoding="utf-8"?>'
    rdftotal = rdftotal  + '<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:owl="http://www.w3.org/2002/07/owl#"'
    rdftotal = rdftotal  + '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"'
    rdftotal = rdftotal  + '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"'
    rdftotal = rdftotal  + '  xmlns:dcat="http://www.w3.org/ns/dcat#"'
    rdftotal = rdftotal  + '  xmlns:dct="http://purl.org/dc/terms/">'


    listado_provincias ={'Huesca','Zaragoza','Teruel'}
    print ("hay: " + str(len(listado_provincias)))


    for provincia in listado_provincias:

        print(provincia)
        rdftotal = rdftotal  + '	<dcat:Dataset rdf:about="http://opendata.aragon.es/aragopedia">\n'
        rdftotal = rdftotal  + '		<dct:identifier>datos-provincia-' + provincia.lower() + '</dct:identifier>\n'
        rdftotal = rdftotal  + '		<dct:description>AragoPedia es una iniciativa de la Dirección General de Nuevas Tecnologías para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos de la provincia de ' + provincia + '</dct:description>\n'

        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragón</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Demografía</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Nuevas tecnologías</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragopedia</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Provincia</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">' + provincia + '</dcat:keyword>\n'

        rdftotal = rdftotal  + '<dct:title>Provincia de ' + provincia +'</dct:title>\n'
        rdftotal = rdftotal  + '		<dct:modified>2014-02-05</dct:modified>\n'
        rdftotal = rdftotal  + '		<dct:issued>2014-02-05</dct:issued>\n'
        rdftotal = rdftotal  + '		<dct:publisher>\n'
        rdftotal = rdftotal  + '			<foaf:Organization>\n'
        rdftotal = rdftotal  + '				<dct:title>Dirección General de Nuevas Tecnologías</dct:title>\n'
        rdftotal = rdftotal  + '				<foaf:homepage rdf:resource="http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/IndustriaInnovacion/AreasTematicas/SociedadInformacion?channelSelected=870aa8aeb0c3a210VgnVCM100000450a15acRCRD"/>\n'
        rdftotal = rdftotal  + '			</foaf:Organization>\n'
        rdftotal = rdftotal  + '		</dct:publisher>\n'
        rdftotal = rdftotal  + '		<dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '			<dct:frequency>\n'
        rdftotal = rdftotal  + '				<rdf:value>P1M</rdf:value>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Mensual</rdfs:label>\n'
        rdftotal = rdftotal  + '		    </dct:frequency>\n'
        rdftotal = rdftotal  + '		</dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '		<dct:spatial>' + provincia +'</dct:spatial>\n'
        rdftotal = rdftotal  + '		<dct:temporal>2000-01-01 a actualidad</dct:temporal>\n'
        rdftotal = rdftotal  + '		<dct:language>es</dct:language>\n'
        rdftotal = rdftotal  + '		<dct:license rdf:resource="Creative Commons-Reconocimiento CC-By 3.0"></dct:license>\n'
        rdftotal = rdftotal  + '		<dcat:granularity>Provincia</dcat:granularity>\n'
        rdftotal = rdftotal  + '		<dcat:dataQuality></dcat:dataQuality>\n'
        rdftotal = rdftotal  + '		<dcat:dataDictionary></dcat:dataDictionary>\n'
        rdftotal = rdftotal  + '		<dcat:theme>\n'
        rdftotal = rdftotal  + '			<rdf:Description>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Demografía</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:identifier>demografia</dct:identifier>\n'
        rdftotal = rdftotal  + '				<dct:description>Demografía</dct:description>\n'
        rdftotal = rdftotal  + '			</rdf:Description>\n'
        rdftotal = rdftotal  + '		</dcat:theme>\n'
        rdftotal = rdftotal  + '		<dcat:distribution>\n'
        rdftotal = rdftotal  + '			<dcat:Distribution>\n'
        rdftotal = rdftotal  + '				<rdfs:label>' + provincia + '</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:description>AragoPedia es una iniciativa de la Dirección General de Nuevas Tecnologías para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos de la provincia de ' +provincia + '</dct:description>\n'
        rdftotal = rdftotal  + '				<rdf:type rdf:resource="http://vocab.deri.ie/dcat#Download"/>\n'
        rdftotal = rdftotal  + '<dcat:accessURL rdf:resource="http://opendata.aragon.es/recurso/territorio/Provincia/' + provincia +'?api_key=e103dc13eb276ad734e680f5855f20c6&amp;_view=completa"></dcat:accessURL>\n'
        rdftotal = rdftotal  + '				<dcat:size>\n'
        rdftotal = rdftotal  + '					<rdf:Description>\n'
        rdftotal = rdftotal  + '						<dcat:bytes></dcat:bytes>\n'
        rdftotal = rdftotal  + '						 <rdfs:label></rdfs:label>\n'
        rdftotal = rdftotal  + '					</rdf:Description>\n'
        rdftotal = rdftotal  + '				</dcat:size>\n'
        rdftotal = rdftotal  + '				<dct:format>\n'
        rdftotal = rdftotal  + '					<dct:IMT>\n'
        rdftotal = rdftotal  + '						<rdf:value>URL</rdf:value>\n'
        rdftotal = rdftotal  + '						<rdfs:label>URL</rdfs:label>\n'
        rdftotal = rdftotal  + '					</dct:IMT>\n'
        rdftotal = rdftotal  + '				</dct:format>\n'
        rdftotal = rdftotal  + '			</dcat:Distribution>\n'
        rdftotal = rdftotal  + '		</dcat:distribution>\n'
        rdftotal = rdftotal  + '	</dcat:Dataset>\n'
    rdftotal = rdftotal  + '</rdf:RDF>\n'

    #print rdftotal
    f = open(config.DOWNLOAD_PATH + "/datosPignatelli.rdf","w")
    f.write(rdftotal)
    f.close()

    print(parse_rdfs2())


main()

