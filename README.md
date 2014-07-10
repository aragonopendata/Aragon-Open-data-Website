
<img src="http://presupuesto.aragon.es/static/assets/logo-gobierno-aragon.png" height="28px" /><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>![Logo Aragón Open Data](logoAragonOpenData.png)

##Catálogo de datos abiertos de Aragón Open Data

Este repositorio contiene el código de la aplicación de [Catálogo de datos abiertos][1], desarrollada como parte del proyecto [Aragón Open Data][2].

### Introducción
El catálogo de Aragón Open Data recoge el conjunto de datos recopilados por la iniciativa Aragón Open Data.

Aragón Open Data es el repositorio estructurado de datos abiertos y en formatos reutilizables de Aragón. Los datos se sirven para que puedan ser manipulados y enriquecidos por ciudanos en general y desarrolladores en particular. El catálogo de datos de Aragón Open Data se forma sobre el vocabulario DCAT, vocabulario reconocido por las principales organizaciones independientes que velan por la neutralidad e interoperabilidad tecnológica de internet en el largo plazo. 

Este catálogo se basa en la versión 2.1.1 del software de código abierto [CKAN][3] (Comprehensive Knowledge Archive Network), desarrollado por la [Open Knowledge Foundation (OKFN)][4]. Entre los principales argumentos que han motivado la utilización de CKAN destacan: 
* Es la solución adoptada por muchas iniciativas similares a nivel internacional.
* Incluye un amplio conjunto de funcionalidades por defecto.
* Proporciona un API de acceso a sus contenidos.
* Tiene posibilidad de ser ampliado mediante extensiones.
* Ofrece amplia documentación para su instalación y desarrollo.
* Dispone de una activa comunidad de desarrolladores. 
* Su coste de licencias es cero.

En los últimos meses se ha realizado un notable esfuerzo para cumplir el objetivo permanente de incorporar continuamente nuevos conjuntos de datos abiertos. Pero además, se han realizado las modificaciones necesarias para adecuar este catálogo a la [Norma Técnica de Interoperabilidad de Reutilización de recursos de la información (NTI)][5], aprobada mediante Resolución de 19 de febrero de 2013.

Para más información sobre la adecuación a la NTI puede consultarse el siguiente [informe][6] y su [anexo][7].
Para más información sobre la utilización del API de CKAN puede consultarse la [zona de desarrolladores del portal][8].

[1]: http://opendata.aragon.es/catalogo
[2]: http://opendata.aragon.es/
[3]: http://ckan.org
[4]: https://okfn.org/
[5]: http://www.boe.es/boe/dias/2013/03/04/pdfs/BOE-A-2013-2380.pdf
[6]: http://opendata.aragon.es/public/documentos/Informe_NTI_Aragon_OpenData_v31-01-14.pdf
[7]: http://opendata.aragon.es/public/documentos/AnexoI_Analisis_Metadatos_Aragon_OpenData_v31-01-14.pdf
[8]: http://opendata.aragon.es/portal/desarrolladores/api-ckan


### Instalando en local

Para instalar la aplicación en local es necesario seguir los siguientes pasos:

* Instalar ckan 2.1.1 en local. Seguir los pasos de la guía oficial (sirve tanto la instalación por paquete como la instalación con código fuente).

* Instalar módulo xlrd para poder acceder a datos en Microsoft Excel.

        (default)$ pip install xlrd

* Tener en cuenta que el catálogo está pensado que se incluya en un portal con más contenidos (hojas de estilo, imágenes, etc.) gestionados por un CMS. El catálogo está previsto que se ubique bajo la ruta http://host/catalogo (por lo que debes configurar el servidor web para que CKAN cuelgue a partir de esa ruta). Si se utiliza apache con wsgi esta configuración quedaría similar a:

        WSGIScriptAlias /catalogo /etc/ckan/default/apache.wsgi

* Incluir los ficheros existentes en este repositorio.  Incluir los nuevos y reemplazar los existentes. Mantener los permisos de los ficheros iguales que los originales.

* En caso de que se desee utilizar el acceso al API por línea de comandos, configurar los parámetros del fichero ckan/ckanclient/config.py

* Hay un desarrollo específico para obtener datos desde tablas de datos oracle a través del módulo cx_Oracle. En general, dado que esto no será de tu interés, debes comentar la línea import cx_Oracle dentro del fichero /ckan/controllers/package.py

* Arrancar el servidor web (se muestra apache)

        $ sudo service apache restart

Para más información, consulta la [documentación técnica de CKAN](http://docs.ckan.org/en/ckan-2.1.1/installing.html).

###Licencia

El Gobierno de Aragón a través de Aragón Open Data pone a disposición de usuarios, desarrolladores y comunidad en general la aplicación denominada “Catálogo de datos abiertos de Aragón Open Data” bajo la Licencia Pública de la Unión Europea “European Union Public Licence – EUPL”. Esta licencia, desarrollada en el seno de la Unión Europea, nació con la intención de ser la licencia bajo la cuál se liberasen los programas y aplicaciones desarrolladas por la Administración Pública y con la característica específica de ser compatible con otras licencias denominadas libres, como la GNU General Public License (GNU/GPL). Estas características dotan, a las aplicaciones así liberadas, de mayor seguridad jurídica y fomentan la interoperabilidad de los servicios de la Administración Electrónica.

Que el código de esta aplicación esté publicado bajo la licencia abierta [EUPL 1.1][2] (European Union Public License 1.1), significa que puedes reutilizarlo, modificarlo y adaptarlo a tus necesidades de forma totalmente libre. Si utilizas el código, a modo de reconocimiento a Aragón Open Data incluye en tu proyecto nuestro logo en el cabecero o en el pie de página, te lo agradeceremos!

![Logo Aragón Open Data](logoAragonOpenData.png)

[2]: https://joinup.ec.europa.eu/software/page/eupl
