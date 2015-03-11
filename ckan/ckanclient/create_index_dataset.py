#!/usr/bin/python
# coding=utf-8
import config
import ckanclient

ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)
index = {
        'title':'Catálogo de datos abiertos de Aragón Opendata',
        'name':'catalogo-opendata-real',
        'notes':'El catálogo de Aragón Open Data recoge el conjunto de datos recopilados por la iniciativa Aragón Open Data. Aragón Open Data es el repositorio estructurado de datos abiertos y en formatos reutilizables de Argón. Los datos se sirven para que puedan ser manipulados y enriquecidos por ciudanos en general y desarrolladores en particular. El catálogo de datos de Aragón Open Data se forma sobre el vocabulario DCAT, vocabulario reconocido por las principales organizaciones independientes que velan por la neutralidad e interoperabilidad tecnológica de internet en el largo plazo.',
        'metadata_created':'2013-05-02',
        'author':'D. G. de Nuevas Tecnologías',
        'maintainer':'D. G. de Nuevas Tecnologías',
        'url':"http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/IndustriaInnovacion/AreasTematicas/SociedadInformacion?channelSelected=870aa8aeb0c3a210VgnVCM100000450a15acRCRD",
        'license_id':'cc-by',
        'extras':[['Language', 'es'],
            ['Spatial','Aragón'],
            ['Temporal','1980-01-01T00:00:00Z/P100Y'],
            ['Granularity','base de datos'],
            ['Data Dictionary','http://opendata.aragon.es/catalogo/opendata/catalogo/catalogo_diccionario.pdf'],

            ]
}
'''Resources'''
resources = []
resource_description = 'El catálogo de Aragón Open Data recoge el conjunto de datos recopilados por la iniciativa Aragón Open Data. Aragón Open Data es el repositorio estructurado de datos abiertos y en formatos reutilizables de Argón. Los datos se sirven para que puedan ser manipulados y enriquecidos por ciudanos en general y desarrolladores en particular. El catálogo de datos de Aragón Open Data se forma sobre el vocabulario DCAT, vocabulario reconocido por las principales organizaciones independientes que velan por la neutralidad e interoperabilidad tecnológica de internet en el largo plazo.'
resources.append({
        'name':'Catálogo de datos abiertos de Aragón Opendata',
        'description':resource_description,
        'format':'XML',
        'type':'http://vocab.deri.ie/dcat#Download',
        'url':config.INDEX_LOCATION + '/catalogo_opendata.xml'
    })
resources.append({
        'name':'Catálogo de datos abiertos de Aragón Opendata',
        'description':resource_description,
        'format':'RSS',
        'type':'http://vocab.deri.ie/dcat#Download',
        'url':config.RSS_LOCATION
    })
resources.append({
        'name':'Catálogo de datos abiertos de Aragón Opendata',
        'description':resource_description,
        'format':'JSON',
        'type':'http://vocab.deri.ie/dcat#Download',
        'url':config.INDEX_LOCATION + '/catalogo_opendata.json'
    })
index['resources'] = resources
'''Tags'''
tags = ['Aragón',
        'Opendata',
        'Open',
        'Datos',
        'Data',
        'Abierto',
        'Gobierno Abierto',
        'Open Government',
        'Base de datos',
        'Dataset',
        'Conjunto de datos'
        ]
index['tags'] = tags

categoria = []
categoria.append({
     'id': 'e5035de7-0611-4cbd-9cfe-4cf1e3230095',
     'capacity':'public'
})



group = {
        'title':'Administración Pública',
        'name':'administracion-publica',
        'description':'Administración Pública',
        'id': 'e5035de7-0611-4cbd-9cfe-4cf1e3230095'
        }
index['groups'] = [group['id']]

try:
    ckan.group_register_post(group)
except ckanclient.CkanApiConflictError:
    print ("Group already created, skipping")
except Exception as e:
    print ("Error while uploading group")


try:
    ckan.package_register_post(index)
    print ("Index created")
except Exception as e:
    try:
        print(e)
        ckan.package_entity_put(index)
        print ("Index updated")
    except Exception as e:
        print ("Error while updating index %s" % e)
        print(e)

