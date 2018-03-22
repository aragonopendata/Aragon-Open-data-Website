#!/usr/bin/python
# coding=utf-8
import config
import ckanclient

ckan = ckanclient.CkanClient(base_location=config.BASE_LOCATION, api_key=config.API_KEY)

try:
    datasetsComarca = ckan.tag_entity_get("Comarca")
    datasetsMunicipio = ckan.tag_entity_get("Municipio")

    for datasetComarca in datasetsComarca:
        print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-alto--gallego"):
            print("SI")
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-bajo-aragon-caspe-baix-arago-casp"):
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-comunidad-de-teuel"):
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-bajo-cina-baix-cinca"):
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-zaagoza"):
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))
        if str(datasetComarca)==("datos-comarca-zaragoza"):
            ckan.package_entity_delete(datasetComarca)
            print(str(datasetComarca))

            datasetsComarca = ckan.tag_entity_get("Comarca")


    for datasetMunicipio in datasetsMunicipio:
        if str(datasetMunicipio)==("datos-municipio-sabinan"):
            ckan.package_entity_delete(datasetMunicipio)
            print(str(datasetMunicipio))


except ckanclient.CkanApiConflictError:
    print ("Error")
except Exception as e:
    print (e)

