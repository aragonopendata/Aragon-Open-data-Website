#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

import config
import glob
import xml.etree.ElementTree as ET
import rdf_parser

def get_rdfs2():
    rdfs = []
    for rdf in glob.glob(config.DOWNLOAD_PATH + "/datosPignatelli_comarcas.rdf"):
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


    listado_comarcas ={'Alto Gállego', 'Andorra-Sierra de Arcos', 'Aranda', 'Bajo Aragón', 'Bajo Aragón-Caspe/ Baix Aragó-Casp', 'Bajo Cinca/Baix Cinca', 'Bajo Martín', 'Campo de Belchite', 'Campo de Borja', 'Campo de Cariñena', 'Campo de Daroca', 'Cinca Medio', 'Cinco Villas', 'Comunidad de Calatayud', 'Comunidad de Teruel', 'Cuencas Mineras', 'D.C. Zaragoza', 'Gúdar-Javalambre', 'Hoya de Huesca/Plana de Uesca', 'Jiloca', 'La Jacetania', 'La Litera/La Llitera', 'La Ribagorza', 'Los Monegros', 'Maestrazgo', 'Matarraña/Matarranya', 'Ribera Alta del Ebro', 'Ribera Baja del Ebro', 'Sierra de Albarracín', 'Sobrarbe', 'Somontano de Barbastro', 'Tarazona y el Moncayo', 'Valdejalón'}

    print ("hay: " + str(len(listado_comarcas)))
    for comarca in listado_comarcas:

        print (comarca)
        rdftotal = rdftotal  + '	<dcat:Dataset rdf:about="http://opendata.aragon.es/aragopedia">\n'
        rdftotal = rdftotal  + '		<dct:identifier>datos-comarca-' + comarca.lower().replace('/','-').replace('ü','u').replace(" ", "-").replace('Ñ', 'n').replace('ñ', 'n').replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "").replace(".", "-") + '</dct:identifier>\n'
        rdftotal = rdftotal  + '		<dct:description>AragoPedia es una iniciativa de la Dirección General de Administración Electrónica y Sociedad de la Información para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos de la comarca de ' + comarca + '</dct:description>\n'

        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragón</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Demografía</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Nuevas tecnologías</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragopedia</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Comarca</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">' + comarca + '</dcat:keyword>\n'

        rdftotal = rdftotal  + '<dct:title>Comarca: ' + comarca +'</dct:title>\n'
        rdftotal = rdftotal  + '		<dct:modified>2014-02-05</dct:modified>\n'
        rdftotal = rdftotal  + '		<dct:issued>2014-02-05</dct:issued>\n'
        rdftotal = rdftotal  + "		<dct:organization>direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion</dct:organization>\n"
        rdftotal = rdftotal  + '		<dct:publisher>\n'
        rdftotal = rdftotal  + '			<foaf:Organization>\n'
        rdftotal = rdftotal  + '				<dct:title>Dirección General de Administración Electrónica y Sociedad de la Información</dct:title>\n'
        rdftotal = rdftotal  + '				<foaf:homepage rdf:resource="http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/IndustriaInnovacion/AreasTematicas/SociedadInformacion?channelSelected=870aa8aeb0c3a210VgnVCM100000450a15acRCRD"/>\n'
        rdftotal = rdftotal  + '			</foaf:Organization>\n'
        rdftotal = rdftotal  + '		</dct:publisher>\n'
        rdftotal = rdftotal  + '		<dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '			<dct:frequency>\n'
        rdftotal = rdftotal  + '				<rdf:value>Mensual</rdf:value>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Mensual</rdfs:label>\n'
        rdftotal = rdftotal  + '		    </dct:frequency>\n'
        rdftotal = rdftotal  + '		</dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '		<dct:spatial>' + comarca +'</dct:spatial>\n'
        rdftotal = rdftotal  + '		<dct:temporalFrom>2000-01-01</dct:temporalFrom>\n'
        
        rdftotal = rdftotal  + '		<dct:language>ES</dct:language>\n'
        rdftotal = rdftotal  + '		<dct:license rdf:resource="http://www.opendefinition.org/licenses/cc-by"></dct:license>\n'
        rdftotal = rdftotal  + '		<dcat:granularity>Comarca</dcat:granularity>\n'
        rdftotal = rdftotal  + '		<dcat:dataQuality></dcat:dataQuality>\n'
        rdftotal = rdftotal  + '		<dcat:dataDictionary></dcat:dataDictionary>\n'
        
        #Se añade lo correspondiente a la aragopedia
        rdftotal = rdftotal  + '		<dcat:name_aragopedia>'+ comarca+ '</dcat:name_aragopedia>\n'
        rdftotal = rdftotal  + '		<dcat:short_uri_aragopedia>'+ comarca.replace(" ", "_")+ '</dcat:short_uri_aragopedia>\n'
        rdftotal = rdftotal  + '		<dcat:type_aragopedia>Comarca</dcat:type_aragopedia>\n'
        rdftotal = rdftotal  + '		<dcat:uri_aragopedia>http://opendata.aragon.es/recurso/territorio/Comarca/'+ comarca.replace(" ", "_")+ '</dcat:uri_aragopedia>\n'
        
        rdftotal = rdftotal  + '		<dcat:theme>\n'
        rdftotal = rdftotal  + '			<rdf:Description>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Demografía</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:identifier>demografia</dct:identifier>\n'
        rdftotal = rdftotal  + '				<dct:description>Demografía</dct:description>\n'
        rdftotal = rdftotal  + '			</rdf:Description>\n'
        rdftotal = rdftotal  + '		</dcat:theme>\n'
        rdftotal = rdftotal  + '		<dcat:distribution>\n'
        rdftotal = rdftotal  + '			<dcat:Distribution>\n'
        rdftotal = rdftotal  + '				<rdfs:label>' + comarca + '</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:description>AragoPedia es una iniciativa de la Dirección General de Administración Electrónica y Sociedad de la Información para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos de la comarca de ' + comarca + '</dct:description>\n'
        rdftotal = rdftotal  + '				<rdf:type rdf:resource="http://vocab.deri.ie/dcat#Download"/>\n'
        rdftotal = rdftotal  + '<dcat:accessURL rdf:resource="http://opendata.aragon.es/recurso/territorio/Comarca/' + comarca.replace(' ','_') +'?api_key=e103dc13eb276ad734e680f5855f20c6&amp;_view=completa"></dcat:accessURL>\n'
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
    f = open(config.DOWNLOAD_PATH + "/datosPignatelli_comarcas.rdf","w")
    f.write(rdftotal)
    f.close()

    print(parse_rdfs2())



main()

