#!/usr/bin/python
URL_FILE="/usr/lib/ckan/default/src/ckan/ckan/ckanclient/url.properties"
DOWNLOAD_PATH="/xxxx"
DOWNLOAD_TEMPORAL="/xxxx"
UPLOAD_DOCUMENTS="/xxx/"
URL_VISTAS="http://opendata.aragon.es/catalogo/dataset/showVista?id="
URL_DOCUMENTS="http://opendata.aragon.es/catalogo/opendata/"

AST1_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx)))"
AST2_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx)))"
OPENDATA_CONEXION_BD="(DESCRIPTION=(LOAD_BALANCE=on)(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(ADDRESS=(PROTOCOL=TCP)(HOST=xxx.xxx.xx)(PORT=xxxx))(CONNECT_DATA=(SERVICE_NAME=xxx.xxx.xx)))"

OPENDATA_USR="xxxx"
OPENDATA_PASS="xxxx"

AST1_USR="xxxx"
AST1_PASS="xxxx"

AST2_USR="xxxx"
AST2_PASS="xxxx"

OPENDATA_POSTGRE_CONEXION_BD="host='xxx' dbname='ckan_ddbb'  port='xxxx' user='userckan' password='passckan'"

USR_ADMIN="xxxx"
API_KEY="xxxx"
BASE_LOCATION="http://opendata.aragon.es/catalogo/api"
INDEX_LOCATION="http://opendata.aragon.es/catalogo/dataset/index"
RSS_LOCATION="http://opendata.aragon.es/catalogo/feeds/dataset.atom"
DCAT_NAMESPACE = "http://www.w3.org/ns/dcat#"
DCT_NAMESPACE = "http://purl.org/dc/terms/"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
FOAF_NAMESPACE = "http://xmlns.com/foaf/0.1/"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
