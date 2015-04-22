 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psycopg2
import urllib2
import os
import re
#import config


DIR='/var/www/wolfcms/'
DIRSITEMAPS=DIR+'sitemaps/'
numURLs=0
URL="http://opendata.aragon.es/"
CATALOGO=URL+"catalogo/"
PORTAL=URL+"portal/"
ARAGOPEDIA=URL+"aragopedia/"
PAGINA_ARAGOPEDIA=ARAGOPEDIA+"index.php/"
BASEDATOS=CATALOGO+'base-datos/'
TEMA=CATALOGO+'group/'
ORGANIZACION=CATALOGO+'organization/'
TAGS=CATALOGO+'?tags='
URLDIRSITEMAPS=URL+"sitemaps/"
#CSV=open(DIR+"caidos.csv","w")
#fichero_sitemap=open(DIR+"ur-sitemaps.txt","w")
#url_200=open(DIR+"urlsSinComprobar.txt","w")

#Método que modifica caracteres por los suyos de escape
# expilcacion:Su archivo de Sitemap debe tener codificación UTF-8; habitualmente puede establecerlo así al guardar el archivo. Al igual que con los archivos XML, los valores de datos (incluidas las URL) deben utilizar caracteres de escape de entidad para los caracteres de la tabla que encontrará más abajo.
#Carácter	Código de caracteres de escape
#Símbolo de unión	&	&amp;
#Comillas simples	'	&apos;
#Comillas	"	&quot;
#Mayor que	>	&gt;
#Menor que	<	&lt;
def modificaCaracteresEscape(url):
	url=url.replace("&","&amp;")
	url=url.replace("'","&apos;")
	url=url.replace("\"","&quot;")
	url=url.replace(">","&gt;")
	url=url.replace("<","&lt;")
	return url

#Método que genera una sentencia del fichero siteMap dado unos parámetros
#El modo puede ser index o url, segun que sea el tipo de sitem que sea, si con indices o con ur
#Fecha tendra el formato yyyy-MM-dd
#frecuencia tiene los valores always, hourly, daily, weekly, monthly, yearly, never
#No comprobamos la url debido que en google webmaster tool tan sólo permite que sean urls de nuestro mismo dominio
def generaSentenciaSiteMap(url, modo, fecha=None, frecuencia=None, prioridad=None):
	
	global numURLs
#	global CSV
	devolver=''
	if (str(modo).lower() =='index') or (str(modo).lower()=='url'):
		if is_http_url(url):
			
			if url.endswith('.xml'):
				ret =200
			elif 'showVista?id=' in url:
				ret=404
			elif 'http://opendata.aragon.es' in url:
#				ret = comprobaURL(url)
				ret = 200
			else:
				ret=404
			if ret==200:
				if str(modo).lower() =='index':
					devolver='\t<sitemap>\n\t\t<loc>'+modificaCaracteresEscape(url)+'</loc>\n'
				elif str(modo).lower()=='url':
					devolver='\t<url>\n\t\t<loc>'+modificaCaracteresEscape(url)+'</loc>\n'
				if fecha is not None:
					if fecha != '':
						devolver+='\t\t<lastmod>'+fecha+'</lastmod>\n'
				if frecuencia is not None :
					if frecuencia != '':
						devolver+='\t\t<changefreq>'+frecuencia+'</changefreq>\n'
				if prioridad is not None and str(modo).lower()=='url':
					if prioridad != '':
						devolver+='\t\t<priority>'+prioridad+'</priority>\n'
				if str(modo).lower() =='index':
					devolver+='\t</sitemap>\n'
				elif str(modo).lower()=='url':
					devolver+='\t</url>\n'
				numURLs+=1
#				url_200.write(url+"\n")
#			else:
				#print 'Error en la url '+url+' '+str(ret)
#				if dataset is not None:
#					CSV.write('\"'+url+'\";\"'+str(ret)+'\";\"'+str(dataset)+'\"\n')
#				else:
#					CSV.write('\"'+url+'\";\"'+str(ret)+'\"\n')
#		else:
#			if dataset is not None:
#				CSV.write('\"'+url+'\";\"MALFORMADA\";\"'+str(dataset)+'\"\n')
#			else:
#				CSV.write('\"'+url+'\";\"MALFORMADA\"\n')
	return devolver

#Método dada la frecuencias como aparecen en la BBDD y devuelve la frecuencia para un sitemap
def devuelveFrecuenciaSiteMap(frecuency):
	
	if str(frecuency.lower())=='instantánea': 
		frecuencia='always'
		return frecuencia
	if str(frecuency.lower())=='horaria':
		frecuencia='hourly'
		return frecuencia
	elif str(frecuency.lower())=='diaria':
		frecuencia='daily'
		return frecuencia
	elif str(frecuency.lower())=='trisemanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='bisemanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='semanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='trimensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='quincenal':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='bimensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='mensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='bimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='trimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='cuatrimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='semestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='anual':
		frecuencia='yearly'
		return frecuencia
	else:
		frecuencia=''
		return frecuencia


#Método para comparar dos fechas, las fechas son yyyy-MM-dd
#devolvera  1  si la fecha primera el mayor, -1 si es menor y 0 si es igual
def comparaFecha(fecha1, fecha2):
	arrFecha1 = fecha1.split('-')
	arrFecha2 = fecha2.split('-')
	if arrFecha1[0]==arrFecha2[0]:
		if arrFecha1[1]==arrFecha2[1]:
			if arrFecha1[2]==arrFecha2[2]:
				return 0
			elif arrFecha1[2]>arrFecha2[2]:
				return 1
			else:
				return -1
		elif arrFecha1[1]>arrFecha2[1]:
			return 1
		else:
			return -1
	elif arrFecha1[0]>arrFecha2[0]:
		return 1
	else:
		return -1
		
#Método que devuelve la fecha más actualice
def fechaMasActual(fecha1, fecha2):
	aux = comparaFecha(str(fecha1), str(fecha2))
	if aux>0:
		return str(fecha1)
	else:
		return str(fecha2)

#Método que da la frecuencia para un dataset, si no tiene devuelve ''
def conseguirFrecuenciaDataset(dataset, conexion):
	cursor=conexion.cursor()
	consulta="SELECT package_extra_revision.value FROM public.package_revision, public.package_extra_revision WHERE package_extra_revision.package_id = package_revision.id AND package_revision.type='dataset' AND package_extra_revision.current ='t' AND package_extra_revision.key = 'Frequency' AND package_revision.current ='t' AND  package_revision.name='"+str(dataset)+"';"
	dev=''
	q=cursor.execute(consulta)
	resultados = cursor.fetchall()
	if resultados is not None:
		for frecuencia in resultados:
			frecuency=str(frecuencia[0])
			dev=devuelveFrecuenciaSiteMap(frecuency)
	cursor.close()
	return str(dev)


#Método que crea el sitemap propio para los recursos de un dataset propio
#dataset:	Nombre del dataset que se quiere obtener sus recursos
#tema_organizacion: El tema u organizacion del dataset en cuestión, se usa para generar el nombre del sitemap
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapRecursos(dataset, tema_organizacion, conexion):
#	global fichero_sitemap
	fechaMasNueva='0000-00-00'
	#Si el fichero correspndiete va a tener un path muy largo lo descartamos, ya que si no nos dará una excepcion
	if len(URLDIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml")<250:
		sitemap=open(DIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml","w")
		sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
		consulta="SELECT resource_revision.url, resource_revision.revision_timestamp, package_extra_revision.value FROM public.package_revision, public.package_extra_revision, public.resource_group_revision, public.resource_revision WHERE resource_group_revision.package_id = package_revision.id AND package_extra_revision.package_id = package_revision.id AND package_revision.type='dataset' AND package_extra_revision.current ='t' AND package_extra_revision.key = 'Frequency' AND resource_revision.resource_group_id = resource_group_revision.id AND package_revision.current ='t' AND resource_revision.current='t' AND resource_revision.state = 'active' AND package_revision.name='"+str(dataset)+"';"
		cursorRecurso=conexion.cursor()
		q = cursorRecurso.execute(consulta)
		resultados = cursorRecurso.fetchall()
		
	
		if resultados is not None:
			frecuencia=''
			for recurso in resultados:
				urlRecurso = str(recurso[0])
				fechaAux=recurso[1]
				fechaRecurso=str(fechaAux)[:10]
				frecuency=recurso[2]
				frecuencia=devuelveFrecuenciaSiteMap(frecuency)
				#sentencia = generaSentenciaSiteMap(urlRecurso,'url', fechaRecurso, frecuencia, '1' )
				sentencia = generaSentenciaSiteMap(urlRecurso,'url')
				sitemap.write(sentencia)
				fechaMasNueva=fechaMasActual(fechaMasNueva, fechaRecurso)
			#Hay que añadir el rdf que tendrá la fecha mayor de los recursos
			#sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+dataset+".rdf",'url', fechaMasNueva, frecuencia, '1' )
			sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+dataset+".rdf",'url', '', '', '')
			sitemap.write(sentencia)
			sitemap.write("</urlset>\n")
			sitemap.close()
		else:
			print 'No hay recursos'
		cursorRecurso.close()
	
		if fechaMasNueva == '0000-00-00':
			os.remove(DIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml")
#		else:
#			fichero_sitemap.write("sitemaps/"+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml\n")
	return fechaMasNueva
	
#Método que genera el sitemap de indice de los dataset y el sitemap de las url de los dataset. A su vez va generando los sitemap de sus correspondientes recursos
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapDataset(organizacion, conexion):
#	global fichero_sitemap
	print 'Se procede con la organizacion'+str(organizacion)
	sitemapURL=open(DIRSITEMAPS+"sitemapURLOrganizacion-"+str(organizacion)+".xml","w")
	sitemapIndex=open(DIRSITEMAPS+"sitemapIndexOrganizacion-"+str(organizacion)+".xml","w")
	sitemapURL.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	sitemapIndex.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	consulta="SELECT package_revision.name, package_revision.revision_timestamp FROM public.package_revision, public.group_revision WHERE group_revision.id = package_revision.owner_org AND package_revision.type='dataset' AND group_revision.name='"+str(organizacion)+"' AND package_revision.current ='t' ORDER BY package_revision.revision_timestamp DESC"
	cursorDataset=conexion.cursor()
#	print 'La consulta es ' +consulta
	q = cursorDataset.execute(consulta)
	resultados = cursorDataset.fetchall()
	fechaMasNueva='0000-00-00'
	if resultados is not None:
		for dataset in resultados:
			nameDataset=str(dataset[0])
			#Los dataset que vienen del elda no tienen recursos en la base de datos, pero hay que meterlos
			if 'datos-municipio' in nameDataset or 'datos-comarca' in nameDataset or 'datos-provincia' in nameDataset:
					fechaAux=dataset[1]
					fechaDataSet=str(fechaAux)[:10]
					#comparamos si la fecha de los recursos y la propia del dataset, nos quedamos con la más alta
					fechaDataSet=fechaMasActual(fechaDataSet,fechaRecursosDataSet)
					fechaMasNueva=fechaMasActual(fechaMasNueva, fechaDataSet)
					frecuencia=conseguirFrecuenciaDataset(nameDataset, conexion)
					#Ahora escribimos la sentencia del index y luego del de url
					urlIndiceDataset= "http://opendata.aragon.es/sitemaps/sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml"
					sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet, frecuencia, '0.9' )
					sitemapIndex.write(sentenciaIndice)
					sentenciaURL = generaSentenciaSiteMap(urlDataset,'url', fechaDataSet, frecuencia, '0.9' )
					sitemapURL.write(sentenciaURL)
					
					#Ahora añadimos su recursos a mano el rdf y la url (esto falta saber como meterla, ya que la url no se construye siempre igual)
					sitemapELDA=open(DIRSITEMAPS+"sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml","w")
					sitemapELDA.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
					sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+nameDataset+".rdf",'url' )
					sitemapELDA.write(sentencia)
					sitemapELDA.write("</urlset>")
					sitemapELDA.close()
#					print 'Se añade dataset de ELDA '+nameDataset
	
			else:
				fechaRecursosDataSet=generaSiteMapRecursos(nameDataset, organizacion, conexion)
				if comparaFecha(fechaRecursosDataSet,'0000-00-00' )>0:
					fechaAux=dataset[1]
					fechaDataSet=str(fechaAux)[:10]
					#comparamos si la fecha de los recursos y la propia del dataset, nos quedamos con la más alta
					fechaDataSet=fechaMasActual(fechaDataSet,fechaRecursosDataSet)
					fechaMasNueva=fechaMasActual(fechaMasNueva, fechaDataSet)
					frecuencia=conseguirFrecuenciaDataset(nameDataset, conexion)
					#Ahora escribimos la sentencia del index y luego del de url
					urlIndiceDataset= "http://opendata.aragon.es/sitemaps/sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml"
					#sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet, frecuencia, '0.9' )
					sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet )
					sitemapIndex.write(sentenciaIndice)
					urlDataset="http://opendata.aragon.es/catalogo/"+nameDataset
					sentenciaURL = generaSentenciaSiteMap(urlDataset,'url', fechaDataSet, frecuencia, '0.9' )
					sitemapURL.write(sentenciaURL)
					#print 'Se añade el dataset '+nameDataset
		sitemapURL.write("</urlset>\n")
		sitemapURL.close()
		sitemapIndex.write("</sitemapindex>")
		sitemapIndex.close()
		print "sitemapURLOrganizacion-"+str(organizacion)+".xml y "+"sitemapIndexOrganizacion-"+str(organizacion)+".xml"
	else:
		print "No hay datasets"
	cursorDataset.close()
	
#	if fechaMasNueva == '0000-00-00':
#		os.remove(DIRSITEMAPS+"sitemapURL-"+organizacion+".xml")
#		os.remove(DIRSITEMAPS+"sitemapIndex-"+organizacion+".xml")
#	else:
#		fichero_sitemap.write("sitemaps/"+"sitemapURL-"+organizacion+".xml\n")
#		fichero_sitemap.write("sitemaps/"+"sitemapIndex-"+organizacion+".xml\n")
	return fechaMasNueva

#Método que genera el sitemap de los sitemap indice de las organizaciones y el sitemap de las url de los organizaciones. A su vez va generando los sitemap de los dataset correspondientes a sus datasets y cada uno a su correspondientes recursos
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapOrganizacion(conexion):
#	global fichero_sitemap
	sitemapURL=open(DIRSITEMAPS+"sitemapURL-Organizaciones.xml","w")
	sitemapIndex=open(DIRSITEMAPS+"sitemapIndex-Organizaciones.xml","w")
	sitemapURL.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	sitemapIndex.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	consulta="SELECT name FROM public.group_revision WHERE current='t' AND is_organization='t' AND state='active' "
	#print 'La consulta es '+consulta
	cursorOrganizacion=conexion.cursor()
	q = cursorOrganizacion.execute(consulta)
	resultados = cursorOrganizacion.fetchall()
	fechaMasNueva='0000-00-00'
	if resultados is not None:
		for organizacion in resultados:
			nameOrganizacion=str(organizacion[0])
			
			
			fechaOrganizacion=generaSiteMapDataset(nameOrganizacion, conexion)
			if comparaFecha(fechaOrganizacion,'0000-00-00' )>0:
				#comparamos la fecha más nueva de la organizacion con la de todas la organizaciones
				fechaMasNueva=fechaMasActual(fechaMasNueva, fechaOrganizacion)
				#Ahora escribimos la sentencia del index y luego del de url
				urlIndiceOrganizacion= "http://opendata.aragon.es/sitemaps/sitemapIndexOrganizacion-"+nameOrganizacion+".xml"
				#sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '', '1' )
				sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '','0.9')
				sitemapIndex.write(sentenciaIndice)
				urlOrganizacion=ORGANIZACION+nameOrganizacion
				sentenciaURL = generaSentenciaSiteMap(urlOrganizacion,'url', fechaOrganizacion, '', '0.9' )
				sitemapURL.write(sentenciaURL)
				urlIndiceOrganizacion= "http://opendata.aragon.es/sitemaps/sitemapURLOrganizacion-"+nameOrganizacion+".xml"
				sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '','0.9')
				sitemapIndex.write(sentenciaIndice)
				print 'Se añade la organizacion '+nameOrganizacion
		sitemapURL.write("</urlset>\n")
		sitemapURL.close()
		sitemapIndex.write("</sitemapindex>")
		sitemapIndex.close()
		print 'Se han generado los ficheros '+DIRSITEMAPS+'sitemapURL-Organizaciones.xml y '+DIRSITEMAPS+'sitemapIndex-Organizaciones.xml'
	else:
		print "No hay organizacion"
	cursorOrganizacion.close()
	
	if fechaMasNueva == '0000-00-00':
		os.remove(DIRSITEMAPS+"sitemapURL-Organizaciones.xml")
		os.remove(DIRSITEMAPS+"sitemapIndex-Organizaciones.xml")
#	else:
#		fichero_sitemap.write("sitemaps/"+"sitemapURL-Organizaciones.xml\n")
#		fichero_sitemap.write("sitemaps/"+"sitemapIndex-Organizaciones.xml\n")
	return fechaMasNueva
	

def is_http_url(s):
	"""
	Returns true if s is valid http url, else false 
	Arguments:
	- `s`:
	"""
	if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',s):
		return True
	else:
		return False
		
		
#Método que sirve para revisaruna URL
#Devuelve el código de estado de HTTP, 200 = Ok. http://es.wikipedia.org/wiki/Anexo:C%C3%B3digos_de_estado_HTTP
def comprobaURL(url):
	ret=0
	try:
		ret = urllib2.urlopen(url).code
	except urllib2.HTTPError, e:
		ret = e.code
	except urllib2.URLError, e:
		print e.args
		print 'La url que da cosas raras es '+url
	return ret
	
#Método que genera el siteMap del home, en un principio sólo tiene la  url de home, la home del catalogo y la aragopedia, ya  que el resto se meten en otros grupos
def generaSiteMapHome():
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemapHome.xml","w")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	urls = [URL, CATALOGO, CATALOGO+'catalogo.html', ARAGOPEDIA]
	for pagina in urls:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', '1' )
		sitemap.write(sentenciaURL)
	
	sitemap.write("</urlset>\n")
#	fichero_sitemap.write("sitemaps/"+"sitemapHome.xml\n")
	sitemap.close()
	
#método para generar el sitemap de la aragopedia: Estos estaran divididos en en 5  secciones. Comunidad autonoma, provincias, comarcas, municipios y varios (aqui meteremos los articulos diferentes por ejemplo el prontuario (cuando este el articulo))
def generaSiteMapAragopedia():
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"Aragopedia.xml","w")
#	fichero_sitemap.write("sitemaps/"+"Aragopedia.xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	
	#ComunidadAutonoma
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComunidadAutonoma.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComunidadAutonoma.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaComunidadAutonomaURL = ['Aragón']
	generaSiteMapArticulosAragopedia('AragopediaComunidadAutonoma', paginaAragopediaComunidadAutonomaURL)
	
	#Provincias
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaProvincias.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaProvincias.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaProvinciasURL = ['Huesca_(provincia)', 'Teruel_(provincia)', 'Zaragoza_(provincia)']
	generaSiteMapArticulosAragopedia('AragopediaProvincias', paginaAragopediaProvinciasURL)
	
	
	#Comarcas
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComarcas.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComarcas.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaComarcasURL = ['Alto_Gállego', 'Andorra-Sierra_de_Arcos', 'Aranda', 'Bajo_Aragón', 'Bajo_Aragón-Caspe/_Baix_Aragó-Casp', 'Bajo_Cinca/Baix_Cinca', 'Bajo_Martín', 'Campo_de_Belchite', 'Campo_de_Borja', 'Campo_de_Cariñena', 'Campo_de_Daroca', 'Cinca_Medio', 'Cinco_Villas', 'Comunidad_de_Calatayud', 'Comunidad_de_Teruel', 'Cuencas_Mineras', 'D.C._Zaragoza', 'Gúdar-Javalambre', 'Hoya_de_Huesca/Plana_de_Uesca', 'Jiloca', 'La_Jacetania', 'La_Litera/La_Llitera', 'La_Ribagorza', 'Los_Monegros', 'Maestrazgo', 'Matarraña/Matarranya', 'Ribera_Alta_del_Ebro', 'Ribera_Baja_del_Ebro', 'Sierra_de_Albarracín', 'Sobrarbe', 'Somontano_de_Barbastro', 'Tarazona_y_el_Moncayo', 'Valdejalón']
	generaSiteMapArticulosAragopedia('AragopediaComarcas', paginaAragopediaComarcasURL)
	
	#municipios
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaMunicipios.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaMunicipios.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaMunicipiosURL = ['Abiego', 'Abizanda', 'Adahuesca', 'Agüero', 'Aísa', 'Albalate_de_Cinca', 'Albalatillo', 'Albelda', 'Albero_Alto', 'Albero_Bajo', 'Alberuela_de_Tubo', 'Alcalá_de_Gurrea', 'Alcalá_del_Obispo', 'Alcampell', 'Alcolea_de_Cinca', 'Alcubierre', 'Alerre', 'Alfántega', 'Almudévar', 'Almunia_de_San_Juan', 'Almuniente', 'Alquézar', 'Altorricón', 'Angüés', 'Ansó', 'Antillón', 'Aragüés_del_Puerto', 'Arén', 'Argavieso', 'Arguis', 'Ayerbe', 'Azanuy-Alins', 'Azara', 'Azlor', 'Baells', 'Bailo', 'Baldellou', 'Ballobar', 'Banastás', 'Barbastro', 'Barbués', 'Barbuñales', 'Bárcabo', 'Belver_de_Cinca', 'Benabarre', 'Benasque', 'Berbegal', 'Bielsa', 'Bierge', 'Biescas', 'Binaced', 'Binéfar', 'Bisaurri', 'Biscarrués', 'Blecua_y_Torres', 'Boltaña', 'Bonansa', 'Borau', 'Broto', 'Caldearenas', 'Campo', 'Camporrells', 'Canal_de_Berdún', 'Candasnos', 'Canfranc', 'Capdesaso', 'Capella', 'Casbas_de_Huesca', 'Castejón_del_Puente', 'Castejón_de_Monegros', 'Castejón_de_Sos', 'Castelflorite', 'Castiello_de_Jaca', 'Castigaleu', 'Castillazuelo', 'Castillonroy', 'Colungo', 'Chalamera', 'Chía', 'Chimillas', 'Esplús', 'Estada', 'Estadilla', 'Estopiñán_del_Castillo', 'Fago', 'Fanlo', 'Fiscal', 'Fonz', 'Foradada_del_Toscar', 'Fraga', 'Fueva_(La)', 'Gistaín', 'Grado_(El)', 'Grañén', 'Graus', 'Gurrea_de_Gállego', 'Hoz_de_Jaca', 'Huerto', 'Huesca', 'Ibieca', 'Igriés', 'Ilche', 'Isábena', 'Jaca', 'Jasa', 'Labuerda', 'Laluenga', 'Lalueza', 'Lanaja', 'Laperdiguera', 'Lascellas-Ponzano', 'Lascuarre', 'Laspaúles', 'Laspuña', 'Loarre', 'Loporzano', 'Loscorrales', 'Monesma_y_Cajigar', 'Monflorite-Lascasas', 'Montanuy', 'Monzón', 'Naval', 'Novales', 'Nueno', 'Olvena', 'Ontiñena', 'Osso_de_Cinca', 'Palo', 'Panticosa', 'Peñalba', 'Peñas_de_Riglos_(Las)', 'Peralta_de_Alcofea', 'Peralta_de_Calasanz', 'Peraltilla', 'Perarrúa', 'Pertusa', 'Piracés', 'Plan', 'Poleñino', 'Pozán_de_Vero', 'Puebla_de_Castro_(La)', 'Puente_de_Montañana', 'Puértolas', 'Pueyo_de_Araguás_(El)', 'Pueyo_de_Santa_Cruz', 'Quicena', 'Robres', 'Sabiñánigo', 'Sahún', 'Salas_Altas', 'Salas_Bajas', 'Salillas', 'Sallent_de_Gállego', 'San_Esteban_de_Litera', 'Sangarrén', 'San_Juan_de_Plan', 'Santa_Cilia', 'Santa_Cruz_de_la_Serós', 'Santaliestra_y_San_Quílez', 'Sariñena', 'Secastilla', 'Seira', 'Sena', 'Senés_de_Alcubierre', 'Sesa', 'Sesué', 'Siétamo', 'Sopeira', 'Tamarite_de_Litera', 'Tardienta', 'Tella-Sin', 'Tierz', 'Tolva', 'Torla-Ordesa', 'Torralba_de_Aragón', 'Torre_la_Ribera', 'Torrente_de_Cinca', 'Torres_de_Alcanadre', 'Torres_de_Barbués', 'Tramaced', 'Valfarta', 'Valle_de_Bardají', 'Valle_de_Lierp', 'Velilla_de_Cinca', 'Beranuy', 'Viacamp_y_Litera', 'Vicién', 'Villanova', 'Villanúa', 'Villanueva_de_Sigena', 'Yebra_de_Basa', 'Yésero', 'Zaidín', 'Valle_de_Hecho', 'Puente_la_Reina_de_Jaca', 'San_Miguel_del_Cinca', 'Sotonera_(La)', 'Lupiñén-Ortilla', 'Santa_María_de_Dulcis', 'Aínsa-Sobrarbe', 'Hoz_y_Costeán', 'Vencillón', 'Ababuj', 'Abejuela', 'Aguatón', 'Aguaviva', 'Aguilar_del_Alfambra', 'Alacón', 'Alba', 'Albalate_del_Arzobispo', 'Albarracín', 'Albentosa', 'Alcaine', 'Alcalá_de_la_Selva', 'Alcañiz', 'Alcorisa', 'Alfambra', 'Aliaga', 'Almohaja', 'Alobras', 'Alpeñés', 'Allepuz', 'Alloza', 'Allueva', 'Anadón', 'Andorra', 'Arcos_de_las_Salinas', 'Arens_de_Lledó', 'Argente', 'Ariño', 'Azaila', 'Bádenas', 'Báguena', 'Bañón', 'Barrachina', 'Bea', 'Beceite', 'Belmonte_de_San_José', 'Bello', 'Berge', 'Bezas', 'Blancas', 'Blesa', 'Bordón', 'Bronchales', 'Bueña', 'Burbáguena', 'Cabra_de_Mora', 'Calaceite', 'Calamocha', 'Calanda', 'Calomarde', 'Camañas', 'Camarena_de_la_Sierra', 'Camarillas', 'Caminreal', 'Cantavieja', 'Cañada_de_Benatanduz', 'Cañada_de_Verich_(La)', 'Cañada_Vellida', 'Cañizar_del_Olivar', 'Cascante_del_Río', 'Castejón_de_Tornos', 'Castel_de_Cabra', 'Castelnou', 'Castelserás', 'Castellar_(El)', 'Castellote', 'Cedrillas', 'Celadas', 'Cella', 'Cerollera_(La)', 'Codoñera_(La)', 'Corbalán', 'Cortes_de_Aragón', 'Cosa', 'Cretas', 'Crivillén', 'Cuba_(La)', 'Cubla', 'Cucalón', 'Cuervo_(El)', 'Cuevas_de_Almudén', 'Cuevas_Labradas', 'Ejulve', 'Escorihuela', 'Escucha', 'Estercuel', 'Ferreruela_de_Huerva', 'Fonfría', 'Formiche_Alto', 'Fórnoles', 'Fortanete', 'Foz-Calanda', 'Fresneda_(La)', 'Frías_de_Albarracín', 'Fuenferrada', 'Fuentes_Calientes', 'Fuentes_Claras', 'Fuentes_de_Rubielos', 'Fuentespalda', 'Galve', 'Gargallo', 'Gea_de_Albarracín', 'Ginebrosa_(La)', 'Griegos', 'Guadalaviar', 'Gúdar', 'Híjar', 'Hinojosa_de_Jarque', 'Hoz_de_la_Vieja_(La)', 'Huesa_del_Común', 'Iglesuela_del_Cid_(La)', 'Jabaloyas', 'Jarque_de_la_Val', 'Jatiel', 'Jorcas', 'Josa', 'Lagueruela', 'Lanzuela', 'Libros', 'Lidón', 'Linares_de_Mora', 'Loscos', 'Lledó', 'Maicas', 'Manzanera', 'Martín_del_Río', 'Mas_de_las_Matas', 'Mata_de_los_Olmos_(La)', 'Mazaleón', 'Mezquita_de_Jarque', 'Mirambel', 'Miravete_de_la_Sierra', 'Molinos', 'Monforte_de_Moyuela', 'Monreal_del_Campo', 'Monroyo', 'Montalbán', 'Monteagudo_del_Castillo', 'Monterde_de_Albarracín', 'Mora_de_Rubielos', 'Moscardón', 'Mosqueruela', 'Muniesa', 'Noguera_de_Albarracín', 'Nogueras', 'Nogueruelas', 'Obón', 'Odón', 'Ojos_Negros', 'Olba', 'Oliete', 'Olmos_(Los)', 'Orihuela_del_Tremedal', 'Orrios', 'Palomar_de_Arroyos', 'Pancrudo', 'Parras_de_Castellote_(Las)', 'Peñarroya_de_Tastavins', 'Peracense', 'Peralejos', 'Perales_del_Alfambra', 'Pitarque', 'Plou', 'Pobo_(El)', 'Portellada_(La)', 'Pozondón', 'Pozuel_del_Campo', 'Puebla_de_Híjar_(La)', 'Puebla_de_Valverde_(La)', 'Puertomingalvo', 'Ráfales', 'Rillo', 'Riodeva', 'Ródenas', 'Royuela', 'Rubiales', 'Rubielos_de_la_Cérida', 'Rubielos_de_Mora', 'Salcedillo', 'Saldón', 'Samper_de_Calanda', 'San_Agustín', 'San_Martín_del_Río', 'Santa_Cruz_de_Nogueras', 'Santa_Eulalia', 'Sarrión', 'Segura_de_los_Baños', 'Seno', 'Singra', 'Terriente', 'Teruel', 'Toril_y_Masegoso', 'Tormón', 'Tornos', 'Torralba_de_los_Sisones', 'Torrecilla_de_Alcañiz', 'Torrecilla_del_Rebollar', 'Torre_de_Arcas', 'Torre_de_las_Arcas', 'Torre_del_Compte', 'Torrelacárcel', 'Torre_los_Negros', 'Torremocha_de_Jiloca', 'Torres_de_Albarracín', 'Torrevelilla', 'Torrijas', 'Torrijo_del_Campo', 'Tramacastiel', 'Tramacastilla', 'Tronchón', 'Urrea_de_Gaén', 'Utrillas', 'Valacloche', 'Valbona', 'Valdealgorfa', 'Valdecuenca', 'Valdelinares', 'Valdeltormo', 'Valderrobres', 'Valjunquera', 'Vallecillo_(El)', 'Veguillas_de_la_Sierra', 'Villafranca_del_Campo', 'Villahermosa_del_Campo', 'Villanueva_del_Rebollar_de_la_Sierra', 'Villar_del_Cobo', 'Villar_del_Salz', 'Villarluengo', 'Villarquemado', 'Villarroya_de_los_Pinares', 'Villastar', 'Villel', 'Vinaceite', 'Visiedo', 'Vivel_del_Río_Martín', 'Zoma_(La)', 'Abanto', 'Acered', 'Agón', 'Aguarón', 'Aguilón', 'Ainzón', 'Aladrén', 'Alagón', 'Alarba', 'Alberite_de_San_Juan', 'Albeta', 'Alborge', 'Alcalá_de_Ebro', 'Alcalá_de_Moncayo', 'Alconchel_de_Ariza', 'Aldehuela_de_Liestos', 'Alfajarín', 'Alfamén', 'Alforque', 'Alhama_de_Aragón', 'Almochuel', 'Almolda_(La)', 'Almonacid_de_la_Cuba', 'Almonacid_de_la_Sierra', 'Almunia_de_Doña_Godina_(La)', 'Alpartir', 'Ambel', 'Anento', 'Aniñón', 'Añón_de_Moncayo', 'Aranda_de_Moncayo', 'Arándiga', 'Ardisa', 'Ariza', 'Artieda', 'Asín', 'Atea', 'Ateca', 'Azuara', 'Badules', 'Bagüés', 'Balconchán', 'Bárboles', 'Bardallur', 'Belchite', 'Belmonte_de_Gracián', 'Berdejo', 'Berrueco', 'Bijuesca', 'Biota', 'Bisimbre', 'Boquiñeni', 'Bordalba', 'Borja', 'Botorrita', 'Brea_de_Aragón', 'Bubierca', 'Bujaraloz', 'Bulbuente', 'Bureta', 'Burgo_de_Ebro_(El)', 'Buste_(El)', 'Cabañas_de_Ebro', 'Cabolafuente', 'Cadrete', 'Calatayud', 'Calatorao', 'Calcena', 'Calmarza', 'Campillo_de_Aragón', 'Carenas', 'Cariñena', 'Caspe', 'Castejón_de_Alarba', 'Castejón_de_las_Armas', 'Castejón_de_Valdejasa', 'Castiliscar', 'Cervera_de_la_Cañada', 'Cerveruela', 'Cetina', 'Cimballa', 'Cinco_Olivas', 'Clarés_de_Ribota', 'Codo', 'Codos', 'Contamina', 'Cosuenda', 'Cuarte_de_Huerva', 'Cubel', 'Cuerlas_(Las)', 'Chiprana', 'Chodes', 'Daroca', 'Ejea_de_los_Caballeros', 'Embid_de_Ariza', 'Encinacorba', 'Épila', 'Erla', 'Escatrón', 'Fabara', 'Farlete', 'Fayón', 'Fayos_(Los)', 'Figueruelas', 'Fombuena', 'Frago_(El)', 'Frasno_(El)', 'Fréscano', 'Fuendejalón', 'Fuendetodos', 'Fuentes_de_Ebro', 'Fuentes_de_Jiloca', 'Gallocanta', 'Gallur', 'Gelsa', 'Godojos', 'Gotor', 'Grisel', 'Grisén', 'Herrera_de_los_Navarros', 'Ibdes', 'Illueca', 'Isuerre', 'Jaraba', 'Jarque', 'Jaulín', 'Joyosa_(La)', 'Lagata', 'Langa_del_Castillo', 'Layana', 'Lécera', 'Leciñena', 'Lechón', 'Letux', 'Litago', 'Lituénigo', 'Lobera_de_Onsella', 'Longares', 'Longás', 'Lucena_de_Jalón', 'Luceni', 'Luesia', 'Luesma', 'Lumpiaque', 'Luna', 'Maella', 'Magallón', 'Mainar', 'Malanquilla', 'Maleján', 'Malón', 'Maluenda', 'Mallén', 'Manchones', 'Mara', 'María_de_Huerva', 'Mediana_de_Aragón', 'Mequinenza', 'Mesones_de_Isuela', 'Mezalocha', 'Mianos', 'Miedes_de_Aragón', 'Monegrillo', 'Moneva', 'Monreal_de_Ariza', 'Monterde', 'Montón', 'Morata_de_Jalón', 'Morata_de_Jiloca', 'Morés', 'Moros', 'Moyuela', 'Mozota', 'Muel', 'Muela_(La)', 'Munébrega', 'Murero', 'Murillo_de_Gállego', 'Navardún', 'Nigüella', 'Nombrevilla', 'Nonaspe', 'Novallas', 'Novillas', 'Nuévalos', 'Nuez_de_Ebro', 'Olvés', 'Orcajo', 'Orera', 'Orés', 'Oseja', 'Osera_de_Ebro', 'Paniza', 'Paracuellos_de_Jiloca', 'Paracuellos_de_la_Ribera', 'Pastriz', 'Pedrola', 'Pedrosas_(Las)', 'Perdiguera', 'Piedratajada', 'Pina_de_Ebro', 'Pinseque', 'Pintanos_(Los)', 'Plasencia_de_Jalón', 'Pleitas', 'Plenas', 'Pomer', 'Pozuel_de_Ariza', 'Pozuelo_de_Aragón', 'Pradilla_de_Ebro', 'Puebla_de_Albortón', 'Puebla_de_Alfindén_(La)', 'Puendeluna', 'Purujosa', 'Quinto', 'Remolinos', 'Retascón', 'Ricla', 'Romanos', 'Rueda_de_Jalón', 'Ruesca', 'Sádaba', 'Salillas_de_Jalón', 'Salvatierra_de_Esca', 'Samper_del_Salz', 'San_Martín_de_la_Virgen_de_Moncayo', 'San_Mateo_de_Gállego', 'Santa_Cruz_de_Grío', 'Santa_Cruz_de_Moncayo', 'Santa_Eulalia_de_Gállego', 'Santed', 'Sástago', 'Saviñán', 'Sediles', 'Sestrica', 'Sierra_de_Luna', 'Sigüés', 'Sisamón', 'Sobradiel', 'Sos_del_Rey_Católico', 'Tabuenca', 'Talamantes', 'Tarazona', 'Tauste', 'Terrer', 'Tierga', 'Tobed', 'Torralba_de_los_Frailes', 'Torralba_de_Ribota', 'Torralbilla', 'Torrehermosa', 'Torrelapaja', 'Torrellas', 'Torres_de_Berrellén', 'Torrijo_de_la_Cañada', 'Tosos', 'Trasmoz', 'Trasobares', 'Uncastillo', 'Undués_de_Lerda', 'Urrea_de_Jalón', 'Urriés', 'Used', 'Utebo', 'Valdehorna', 'Val_de_San_Martín', 'Valmadrid', 'Valpalmas', 'Valtorres', 'Velilla_de_Ebro', 'Velilla_de_Jiloca', 'Vera_de_Moncayo', 'Vierlas', 'Vilueña_(La)', 'Villadoz', 'Villafeliche', 'Villafranca_de_Ebro', 'Villalba_de_Perejil', 'Villalengua', 'Villanueva_de_Gállego', 'Villanueva_de_Jiloca', 'Villanueva_de_Huerva', 'Villar_de_los_Navarros', 'Villarreal_de_Huerva', 'Villarroya_de_la_Sierra', 'Villarroya_del_Campo', 'Vistabella', 'Zaida_(La)', 'Zaragoza', 'Zuera', 'Biel', 'Marracos', 'Villamayor_de_Gállego']
	generaSiteMapArticulosAragopedia('AragopediaMunicipios', paginaAragopediaMunicipiosURL)
	
	#Varios
#	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaVarios.xml','index', '', '', '0.9' )
#	sitemap.write(sentenciaURL)
#	paginaAragopediaComunidadAutonomaurl = []
	
	
	sitemap.write("</sitemapindex>\n")
	sitemap.close()
	
#Método que sirve genera el sitemap de articulos de la aragopedia
#Los articulos se le meten en un array
def generaSiteMapArticulosAragopedia(nombre, arrayPaginas):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+nombre+".xml","w")
#	fichero_sitemap.write("sitemaps/"+nombre+".xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	
	for pagina in arrayPaginas:
		sentenciaURL = generaSentenciaSiteMap(PAGINA_ARAGOPEDIA+pagina,'url', '', '', '0.8' )
		sitemap.write(sentenciaURL)
	sitemap.write("</urlset>\n")
	sitemap.close()
	

#Método que sirve para generar el sitemap de nombre.
def generaSiteMapURL(nombre, arrayURLs, prioridad):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemap"+nombre+".xml","w")
#	fichero_sitemap.write("sitemaps/sitemap"+nombre+".xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	for pagina in arrayURLs:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', prioridad )
		sitemap.write(sentenciaURL)
	sitemap.write("</urlset>\n")
	sitemap.close()
	
	
#Método para generar el sitemap de  varios. Este contiene las búsquedas, los temas.... y luego finalmente los tags de los dataset de ckan
def generaSiteMapVarios(arrayVarios, conexion):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemapVarios.xml","w")
#	fichero_sitemap.write("sitemaps/sitemapVarios.xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
		#Añadimos los temas
	consulta="SELECT name FROM public.group_revision WHERE current='t' AND is_organization='f'"
	cursor =conexion.cursor()
	q = cursor.execute(consulta)
	resultados = cursor.fetchall()
	
	if resultados is not None:
		for tema in resultados:
			sentencia = generaSentenciaSiteMap(TEMA+tema[0],'url', '', '', '0.2' )
			sitemap.write(sentencia)
	else:
		print 'No hay temas'
	
	
	for pagina in arrayVarios:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', '0.2' )
		sitemap.write(sentenciaURL)
	#Añadimos los tags
	consulta="SELECT  name FROM public.tag"
	
	q = cursor.execute(consulta)
	resultados = cursor.fetchall()
	
	if resultados is not None:
		for tag in resultados:
			sentencia = generaSentenciaSiteMap(TAGS+tag[0],'url', '', '', '0.2' )
			sitemap.write(sentencia)
	else:
		print 'No hay tags'
	cursor.close()
	
	sitemap.write("</urlset>\n")
	sitemap.close()
	
#Método que sirve para limpiar directorio que contiene los sitempas
def limpiaXml():
	filelist = [ f for f in os.listdir(DIRSITEMAPS) if f.endswith(".xml") ]
	for f in filelist:
		os.remove(DIRSITEMAPS+f)

def main():
	##PostgreSQL
	CONEXION_BD = "host='localhost' dbname='ckan_default' port='9999' user='ckan_default' password='ckan_default'"
	
	"""CONEXION_BD = config.OPENDATA_POSTGRE_CONEXION_BD"""
	URL="http://opendata.aragon.es/"
	CATALOGO=URL+"catalogo/"
	PORTAL=URL+"portal/"
	ARAGOPEDIA=URL+"aragopedia/"
	PAGINA_ARAGOPEDIA=ARAGOPEDIA+"index.php/"
	BASEDATOS=CATALOGO+'base-datos/'
	TEMA=CATALOGO+'group/'
	ORGANIZACION=CATALOGO+'organization/'
	TAGS=CATALOGO+'?tags='
	
	
	limpiaXml()
	sitemap=open(DIR+"sitemap.xml","w")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapHome.xml",'index', '', '', '' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de HOME'
	generaSiteMapHome()
	#Nos conectamos a la base de datos
	connection = psycopg2.connect(CONEXION_BD)
	
	fecha=generaSiteMapDataset('direccion_general_de_patrimonio_cultural', connection)
	print 'Comenzamos a generar el sitemap de los datasets'
	fecha=generaSiteMapOrganizacion(connection)
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapURL-Organizaciones.xml",'index', fecha, '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapURL-Organizaciones.xml",'index', fecha)
	sitemap.write(sentenciaURL)
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapIndex-Organizaciones.xml",'index', fecha, '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapIndex-Organizaciones.xml",'index', fecha)
	sitemap.write(sentenciaURL)
	#Aragopedia
	generaSiteMapAragopedia()
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"Aragopedia.xml",'index', '', '', '0.8' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"Aragopedia.xml",'index' )
	sitemap.write(sentenciaURL)
	#Socialdata
	print 'Comenzamos a generar el sitemap de social-data'
	generaSiteMapURL('Socialdata', [URL+'portal/social-data', URL+'condiciones-utilizacion-social-data'], '0.7')
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapSocialdata.xml",'index' )
	sitemap.write(sentenciaURL)
	#Colabora
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapColabora.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de colabora'
	generaSiteMapURL('Colabora', [URL+'portal/colabora'], '0.4')
	#Aplicaciones
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapAplicaciones.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de las aplicaciones'
	aplicaciones=['http://opendata.aragon.es/portal/aplicaciones', 'http://opendata.aragon.es/aragopedia', 'http://presupuesto.aragon.es/', 'http://opendata.aragon.es/portal/social-data', 'http://www.boa.aragon.es/EBOA/opendata.htm', 'http://www.arcgis.com/apps/StorytellingTextLegend/index.html?appid=3f1d252c1db64140817ab84f0a03524c', 'http://www.marianistas.net/', 'http://dondevanmisimpuestos.es/', 'http://www.ebolets.com/es/index.html', 'http://vps147.cesvima.upm.es/jacathon_2014/index.html', 'https://github.com/aragonopendata/DEVTA','http://laboratorio.diariodenavarra.es/jacathon/', 'https://github.com/aragonopendata/DNlab', 'https://github.com/aragonopendata/Huracan', 'http://crasaragon.com/','https://github.com/aragonopendata/JodoCoders', 'http://neru.me/', 'https://github.com/aragonopendata/Manata', 'https://play.google.com/store/apps/details?id=noteam.conocesaragon', 'https://github.com/aragonopendata/NOTEAM', 'http://visual-aragopedia.visualizados.com/', 'https://github.com/aragonopendata/Poolparty', 'http://opendata.aragon.es/portal/envio-aplicaciones'] #Falta , 'http://aot.rbel.co/' que no va
	generaSiteMapURL('Aplicaciones', aplicaciones, '0.3')
	
	#Info open data
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapInfoOpenData.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de info open data'
	infoOpenData=[ PORTAL+'aragon-open-data', PORTAL+'multimedia/videos', PORTAL+'multimedia/imagenes', PORTAL+'multimedia/presentaciones', PORTAL+'documentacion', PORTAL+'desarrolladores/resumen', PORTAL+'desarrolladores/api-ckan', PORTAL+'desarrolladores/api-social-data', PORTAL+'desarrolladores/api-aragopedia', PORTAL+'desarrolladores/api-aragodbpedia', PORTAL+'desarrolladores/punto-sparql', URL+'def/Aragopedia.html', PORTAL+'cliente-sparql', PORTAL+'jacathon']
	generaSiteMapURL('InfoOpenData', infoOpenData, '0.6')
	
	#Terminos
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapTerminos.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de terminos de uso'
	terminos = [URL+'terminos']
	generaSiteMapURL('Terminos', terminos, '0.5')
	
	#Varios
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapVarios.xml",'index')
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap varios'
	urlBusqueda = [CATALOGO+'ciencia-tecnologia',CATALOGO+'comercio',CATALOGO+'cultura-ocio',CATALOGO+'demografia',CATALOGO+'deporte',CATALOGO+'economia',CATALOGO+'educacion',CATALOGO+'empleo',CATALOGO+'energia',CATALOGO+'hacienda',CATALOGO+'industria',CATALOGO+'legislacion-justicia',CATALOGO+'medio-ambiente',CATALOGO+'medio-rural-pesca',CATALOGO+'salud',CATALOGO+'sector-publico',CATALOGO+'seguridad',CATALOGO+'sociedad-bienestar',CATALOGO+'transporte',CATALOGO+'turismo',CATALOGO+'urbanismo-infraestructuras',CATALOGO+'vivienda',CATALOGO+'ciencia-tecnologia'+'/hojas-de-calculo',CATALOGO+'comercio'+'/hojas-de-calculo',CATALOGO+'cultura-ocio'+'/hojas-de-calculo',CATALOGO+'demografia'+'/hojas-de-calculo',CATALOGO+'deporte'+'/hojas-de-calculo',CATALOGO+'economia'+'/hojas-de-calculo',CATALOGO+'educacion'+'/hojas-de-calculo',CATALOGO+'empleo'+'/hojas-de-calculo',CATALOGO+'energia'+'/hojas-de-calculo',CATALOGO+'hacienda'+'/hojas-de-calculo',CATALOGO+'industria'+'/hojas-de-calculo',CATALOGO+'legislacion-justicia'+'/hojas-de-calculo',CATALOGO+'medio-ambiente'+'/hojas-de-calculo',CATALOGO+'medio-rural-pesca'+'/hojas-de-calculo',CATALOGO+'salud'+'/hojas-de-calculo',CATALOGO+'sector-publico'+'/hojas-de-calculo',CATALOGO+'seguridad'+'/hojas-de-calculo',CATALOGO+'sociedad-bienestar'+'/hojas-de-calculo',CATALOGO+'transporte'+'/hojas-de-calculo',CATALOGO+'turismo'+'/hojas-de-calculo',CATALOGO+'urbanismo-infraestructuras'+'/hojas-de-calculo',CATALOGO+'vivienda'+'/hojas-de-calculo',CATALOGO+'ciencia-tecnologia'+'/texto-plano',CATALOGO+'comercio'+'/texto-plano',CATALOGO+'cultura-ocio'+'/texto-plano',CATALOGO+'demografia'+'/texto-plano',CATALOGO+'deporte'+'/texto-plano',CATALOGO+'economia'+'/texto-plano',CATALOGO+'educacion'+'/texto-plano',CATALOGO+'empleo'+'/texto-plano',CATALOGO+'energia'+'/texto-plano',CATALOGO+'hacienda'+'/texto-plano',CATALOGO+'industria'+'/texto-plano',CATALOGO+'legislacion-justicia'+'/texto-plano',CATALOGO+'medio-ambiente'+'/texto-plano',CATALOGO+'medio-rural-pesca'+'/texto-plano',CATALOGO+'salud'+'/texto-plano',CATALOGO+'sector-publico'+'/texto-plano',CATALOGO+'seguridad'+'/texto-plano',CATALOGO+'sociedad-bienestar'+'/texto-plano',CATALOGO+'transporte'+'/texto-plano',CATALOGO+'turismo'+'/texto-plano',CATALOGO+'urbanismo-infraestructuras'+'/texto-plano',CATALOGO+'vivienda'+'/texto-plano',CATALOGO+'ciencia-tecnologia'+'/mapas',CATALOGO+'comercio'+'/mapas',CATALOGO+'cultura-ocio'+'/mapas',CATALOGO+'demografia'+'/mapas',CATALOGO+'deporte'+'/mapas',CATALOGO+'economia'+'/mapas',CATALOGO+'educacion'+'/mapas',CATALOGO+'empleo'+'/mapas',CATALOGO+'energia'+'/mapas',CATALOGO+'hacienda'+'/mapas',CATALOGO+'industria'+'/mapas',CATALOGO+'legislacion-justicia'+'/mapas',CATALOGO+'medio-ambiente'+'/mapas',CATALOGO+'medio-rural-pesca'+'/mapas',CATALOGO+'salud'+'/mapas',CATALOGO+'sector-publico'+'/mapas',CATALOGO+'seguridad'+'/mapas',CATALOGO+'sociedad-bienestar'+'/mapas',CATALOGO+'transporte'+'/mapas',CATALOGO+'turismo'+'/mapas',CATALOGO+'urbanismo-infraestructuras'+'/mapas',CATALOGO+'vivienda'+'/mapas',CATALOGO+'ciencia-tecnologia'+' ',CATALOGO+'comercio'+'/fotos',CATALOGO+'cultura-ocio'+'/fotos',CATALOGO+'demografia'+'/fotos',CATALOGO+'deporte'+'/fotos',CATALOGO+'economia'+'/fotos',CATALOGO+'educacion'+'/fotos',CATALOGO+'empleo'+'/fotos',CATALOGO+'energia'+'/fotos',CATALOGO+'hacienda'+'/fotos',CATALOGO+'industria'+'/fotos',CATALOGO+'legislacion-justicia'+'/fotos',CATALOGO+'medio-ambiente'+'/fotos',CATALOGO+'medio-rural-pesca'+'/fotos',CATALOGO+'salud'+'/fotos',CATALOGO+'sector-publico'+'/fotos',CATALOGO+'seguridad'+'/fotos',CATALOGO+'sociedad-bienestar'+'/fotos',CATALOGO+'transporte'+'/fotos',CATALOGO+'turismo'+'/fotos',CATALOGO+'urbanismo-infraestructuras'+'/fotos',CATALOGO+'vivienda'+'/fotos',CATALOGO+'ciencia-tecnologia'+'/rss',CATALOGO+'comercio'+'/rss',CATALOGO+'cultura-ocio'+'/rss',CATALOGO+'demografia'+'/rss',CATALOGO+'deporte'+'/rss',CATALOGO+'economia'+'/rss',CATALOGO+'educacion'+'/rss',CATALOGO+'empleo'+'/rss',CATALOGO+'energia'+'/rss',CATALOGO+'hacienda'+'/rss',CATALOGO+'industria'+'/rss',CATALOGO+'legislacion-justicia'+'/rss',CATALOGO+'medio-ambiente'+'/rss',CATALOGO+'medio-rural-pesca'+'/rss',CATALOGO+'salud'+'/rss',CATALOGO+'sector-publico'+'/rss',CATALOGO+'seguridad'+'/rss',CATALOGO+'sociedad-bienestar'+'/rss',CATALOGO+'transporte'+'/rss',CATALOGO+'turismo'+'/rss',CATALOGO+'urbanismo-infraestructuras'+'/rss',CATALOGO+'vivienda'+'/rss', CATALOGO+'busqueda-libre',CATALOGO+'base-datos',BASEDATOS+'ciencia-tecnologia',BASEDATOS+'comercio',BASEDATOS+'cultura-ocio',BASEDATOS+'demografia',BASEDATOS+'deporte',BASEDATOS+'economia',BASEDATOS+'educacion',BASEDATOS+'empleo',BASEDATOS+'energia',BASEDATOS+'hacienda',BASEDATOS+'industria',BASEDATOS+'legislacion-justicia',BASEDATOS+'medio-ambiente',BASEDATOS+'medio-rural-pesca',BASEDATOS+'salud',BASEDATOS+'sector-publico',BASEDATOS+'seguridad',BASEDATOS+'sociedad-bienestar',BASEDATOS+'transporte',BASEDATOS+'turismo',BASEDATOS+'urbanismo-infraestructuras',BASEDATOS+'vivienda']
	generaSiteMapVarios(urlBusqueda, connection)
	sitemap.write("</sitemapindex>\n")
	sitemap.close()
#	fichero_sitemap.close()
	
	print "La fecha más nueva es "+fecha
	
	
#	url_200.close()
	print 'Se han añadido '+str(numURLs)+' urls en el sitemaps'
	print 'Fin'

main() #!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psycopg2
import urllib2
import os
import re
#import config


DIR='/var/www/wolfcms/'
DIRSITEMAPS=DIR+'sitemaps/'
numURLs=0
URL="http://opendata.aragon.es/"
CATALOGO=URL+"catalogo/"
PORTAL=URL+"portal/"
ARAGOPEDIA=URL+"aragopedia/"
PAGINA_ARAGOPEDIA=ARAGOPEDIA+"index.php/"
BASEDATOS=CATALOGO+'base-datos/'
TEMA=CATALOGO+'group/'
ORGANIZACION=CATALOGO+'organization/'
TAGS=CATALOGO+'?tags='
URLDIRSITEMAPS=URL+"sitemaps/"
#CSV=open(DIR+"caidos.csv","w")
#fichero_sitemap=open(DIR+"ur-sitemaps.txt","w")
#url_200=open(DIR+"urlsSinComprobar.txt","w")

#Método que modifica caracteres por los suyos de escape
# expilcacion:Su archivo de Sitemap debe tener codificación UTF-8; habitualmente puede establecerlo así al guardar el archivo. Al igual que con los archivos XML, los valores de datos (incluidas las URL) deben utilizar caracteres de escape de entidad para los caracteres de la tabla que encontrará más abajo.
#Carácter	Código de caracteres de escape
#Símbolo de unión	&	&amp;
#Comillas simples	'	&apos;
#Comillas	"	&quot;
#Mayor que	>	&gt;
#Menor que	<	&lt;
def modificaCaracteresEscape(url):
	url=url.replace("&","&amp;")
	url=url.replace("'","&apos;")
	url=url.replace("\"","&quot;")
	url=url.replace(">","&gt;")
	url=url.replace("<","&lt;")
	return url

#Método que genera una sentencia del fichero siteMap dado unos parámetros
#El modo puede ser index o url, segun que sea el tipo de sitem que sea, si con indices o con ur
#Fecha tendra el formato yyyy-MM-dd
#frecuencia tiene los valores always, hourly, daily, weekly, monthly, yearly, never
#No comprobamos la url debido que en google webmaster tool tan sólo permite que sean urls de nuestro mismo dominio
def generaSentenciaSiteMap(url, modo, fecha=None, frecuencia=None, prioridad=None):
	
	global numURLs
#	global CSV
	devolver=''
	if (str(modo).lower() =='index') or (str(modo).lower()=='url'):
		if is_http_url(url):
			
			if url.endswith('.xml'):
				ret =200
			elif 'showVista?id=' in url:
				ret=404
			elif 'http://opendata.aragon.es' in url:
#				ret = comprobaURL(url)
				ret = 200
			else:
				ret=404
			if ret==200:
				if str(modo).lower() =='index':
					devolver='\t<sitemap>\n\t\t<loc>'+modificaCaracteresEscape(url)+'</loc>\n'
				elif str(modo).lower()=='url':
					devolver='\t<url>\n\t\t<loc>'+modificaCaracteresEscape(url)+'</loc>\n'
				if fecha is not None:
					if fecha != '':
						devolver+='\t\t<lastmod>'+fecha+'</lastmod>\n'
				if frecuencia is not None :
					if frecuencia != '':
						devolver+='\t\t<changefreq>'+frecuencia+'</changefreq>\n'
				if prioridad is not None and str(modo).lower()=='url':
					if prioridad != '':
						devolver+='\t\t<priority>'+prioridad+'</priority>\n'
				if str(modo).lower() =='index':
					devolver+='\t</sitemap>\n'
				elif str(modo).lower()=='url':
					devolver+='\t</url>\n'
				numURLs+=1
#				url_200.write(url+"\n")
#			else:
				#print 'Error en la url '+url+' '+str(ret)
#				if dataset is not None:
#					CSV.write('\"'+url+'\";\"'+str(ret)+'\";\"'+str(dataset)+'\"\n')
#				else:
#					CSV.write('\"'+url+'\";\"'+str(ret)+'\"\n')
#		else:
#			if dataset is not None:
#				CSV.write('\"'+url+'\";\"MALFORMADA\";\"'+str(dataset)+'\"\n')
#			else:
#				CSV.write('\"'+url+'\";\"MALFORMADA\"\n')
	return devolver

#Método dada la frecuencias como aparecen en la BBDD y devuelve la frecuencia para un sitemap
def devuelveFrecuenciaSiteMap(frecuency):
	
	if str(frecuency.lower())=='instantánea': 
		frecuencia='always'
		return frecuencia
	if str(frecuency.lower())=='horaria':
		frecuencia='hourly'
		return frecuencia
	elif str(frecuency.lower())=='diaria':
		frecuencia='daily'
		return frecuencia
	elif str(frecuency.lower())=='trisemanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='bisemanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='semanal':
		frecuencia='weekly'
		return frecuencia
	elif str(frecuency.lower())=='trimensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='quincenal':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='bimensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='mensual':
		frecuencia='monthly'
		return frecuencia
	elif str(frecuency.lower())=='bimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='trimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='cuatrimestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='semestral':
		frecuencia='yearly'
		return frecuencia
	elif str(frecuency.lower())=='anual':
		frecuencia='yearly'
		return frecuencia
	else:
		frecuencia=''
		return frecuencia


#Método para comparar dos fechas, las fechas son yyyy-MM-dd
#devolvera  1  si la fecha primera el mayor, -1 si es menor y 0 si es igual
def comparaFecha(fecha1, fecha2):
	arrFecha1 = fecha1.split('-')
	arrFecha2 = fecha2.split('-')
	if arrFecha1[0]==arrFecha2[0]:
		if arrFecha1[1]==arrFecha2[1]:
			if arrFecha1[2]==arrFecha2[2]:
				return 0
			elif arrFecha1[2]>arrFecha2[2]:
				return 1
			else:
				return -1
		elif arrFecha1[1]>arrFecha2[1]:
			return 1
		else:
			return -1
	elif arrFecha1[0]>arrFecha2[0]:
		return 1
	else:
		return -1
		
#Método que devuelve la fecha más actualice
def fechaMasActual(fecha1, fecha2):
	aux = comparaFecha(str(fecha1), str(fecha2))
	if aux>0:
		return str(fecha1)
	else:
		return str(fecha2)

#Método que da la frecuencia para un dataset, si no tiene devuelve ''
def conseguirFrecuenciaDataset(dataset, conexion):
	cursor=conexion.cursor()
	consulta="SELECT package_extra_revision.value FROM public.package_revision, public.package_extra_revision WHERE package_extra_revision.package_id = package_revision.id AND package_revision.type='dataset' AND package_extra_revision.current ='t' AND package_extra_revision.key = 'Frequency' AND package_revision.current ='t' AND  package_revision.name='"+str(dataset)+"';"
	dev=''
	q=cursor.execute(consulta)
	resultados = cursor.fetchall()
	if resultados is not None:
		for frecuencia in resultados:
			frecuency=str(frecuencia[0])
			dev=devuelveFrecuenciaSiteMap(frecuency)
	cursor.close()
	return str(dev)


#Método que crea el sitemap propio para los recursos de un dataset propio
#dataset:	Nombre del dataset que se quiere obtener sus recursos
#tema_organizacion: El tema u organizacion del dataset en cuestión, se usa para generar el nombre del sitemap
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapRecursos(dataset, tema_organizacion, conexion):
#	global fichero_sitemap
	fechaMasNueva='0000-00-00'
	#Si el fichero correspndiete va a tener un path muy largo lo descartamos, ya que si no nos dará una excepcion
	if len(URLDIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml")<250:
		sitemap=open(DIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml","w")
		sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
		consulta="SELECT resource_revision.url, resource_revision.revision_timestamp, package_extra_revision.value FROM public.package_revision, public.package_extra_revision, public.resource_group_revision, public.resource_revision WHERE resource_group_revision.package_id = package_revision.id AND package_extra_revision.package_id = package_revision.id AND package_revision.type='dataset' AND package_extra_revision.current ='t' AND package_extra_revision.key = 'Frequency' AND resource_revision.resource_group_id = resource_group_revision.id AND package_revision.current ='t' AND resource_revision.current='t' AND resource_revision.state = 'active' AND package_revision.name='"+str(dataset)+"';"
		cursorRecurso=conexion.cursor()
		q = cursorRecurso.execute(consulta)
		resultados = cursorRecurso.fetchall()
		
	
		if resultados is not None:
			frecuencia=''
			for recurso in resultados:
				urlRecurso = str(recurso[0])
				fechaAux=recurso[1]
				fechaRecurso=str(fechaAux)[:10]
				frecuency=recurso[2]
				frecuencia=devuelveFrecuenciaSiteMap(frecuency)
				#sentencia = generaSentenciaSiteMap(urlRecurso,'url', fechaRecurso, frecuencia, '1' )
				sentencia = generaSentenciaSiteMap(urlRecurso,'url')
				sitemap.write(sentencia)
				fechaMasNueva=fechaMasActual(fechaMasNueva, fechaRecurso)
			#Hay que añadir el rdf que tendrá la fecha mayor de los recursos
			#sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+dataset+".rdf",'url', fechaMasNueva, frecuencia, '1' )
			sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+dataset+".rdf",'url', '', '', '', dataset)
			sitemap.write(sentencia)
			sitemap.write("</urlset>\n")
			sitemap.close()
		else:
			print 'No hay recursos'
		cursorRecurso.close()
	
		if fechaMasNueva == '0000-00-00':
			os.remove(DIRSITEMAPS+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml")
#		else:
#			fichero_sitemap.write("sitemaps/"+"sitemapRecursos-"+tema_organizacion+"-DataSet-"+dataset+".xml\n")
	return fechaMasNueva
	
#Método que genera el sitemap de indice de los dataset y el sitemap de las url de los dataset. A su vez va generando los sitemap de sus correspondientes recursos
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapDataset(organizacion, conexion):
#	global fichero_sitemap
	print 'Se procede con la organizacion'+str(organizacion)
	sitemapURL=open(DIRSITEMAPS+"sitemapURLOrganizacion-"+str(organizacion)+".xml","w")
	sitemapIndex=open(DIRSITEMAPS+"sitemapIndexOrganizacion-"+str(organizacion)+".xml","w")
	sitemapURL.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	sitemapIndex.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	consulta="SELECT package_revision.name, package_revision.revision_timestamp FROM public.package_revision, public.group_revision WHERE group_revision.id = package_revision.owner_org AND package_revision.type='dataset' AND group_revision.name='"+str(organizacion)+"' AND package_revision.current ='t' ORDER BY package_revision.revision_timestamp DESC"
	cursorDataset=conexion.cursor()
#	print 'La consulta es ' +consulta
	q = cursorDataset.execute(consulta)
	resultados = cursorDataset.fetchall()
	fechaMasNueva='0000-00-00'
	if resultados is not None:
		for dataset in resultados:
			nameDataset=str(dataset[0])
			#Los dataset que vienen del elda no tienen recursos en la base de datos, pero hay que meterlos
			if 'datos-municipio' in nameDataset or 'datos-comarca' in nameDataset or 'datos-provincia' in nameDataset:
					fechaAux=dataset[1]
					fechaDataSet=str(fechaAux)[:10]
					#comparamos si la fecha de los recursos y la propia del dataset, nos quedamos con la más alta
					fechaDataSet=fechaMasActual(fechaDataSet,fechaRecursosDataSet)
					fechaMasNueva=fechaMasActual(fechaMasNueva, fechaDataSet)
					frecuencia=conseguirFrecuenciaDataset(nameDataset, conexion)
					#Ahora escribimos la sentencia del index y luego del de url
					urlIndiceDataset= "http://opendata.aragon.es/sitemaps/sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml"
					sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet, frecuencia, '0.9' )
					sitemapIndex.write(sentenciaIndice)
					sentenciaURL = generaSentenciaSiteMap(urlDataset,'url', fechaDataSet, frecuencia, '0.9' )
					sitemapURL.write(sentenciaURL)
					
					#Ahora añadimos su recursos a mano el rdf y la url (esto falta saber como meterla, ya que la url no se construye siempre igual)
					sitemapELDA=open(DIRSITEMAPS+"sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml","w")
					sitemapELDA.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
					sentencia = generaSentenciaSiteMap("http://opendata.aragon.es/catalogo/"+nameDataset+".rdf",'url' )
					sitemapELDA.write(sentencia)
					sitemapELDA.write("</urlset>")
					sitemapELDA.close()
#					print 'Se añade dataset de ELDA '+nameDataset
	
			else:
				fechaRecursosDataSet=generaSiteMapRecursos(nameDataset, organizacion, conexion)
				if comparaFecha(fechaRecursosDataSet,'0000-00-00' )>0:
					fechaAux=dataset[1]
					fechaDataSet=str(fechaAux)[:10]
					#comparamos si la fecha de los recursos y la propia del dataset, nos quedamos con la más alta
					fechaDataSet=fechaMasActual(fechaDataSet,fechaRecursosDataSet)
					fechaMasNueva=fechaMasActual(fechaMasNueva, fechaDataSet)
					frecuencia=conseguirFrecuenciaDataset(nameDataset, conexion)
					#Ahora escribimos la sentencia del index y luego del de url
					urlIndiceDataset= "http://opendata.aragon.es/sitemaps/sitemapRecursos-"+organizacion+"-DataSet-"+nameDataset+".xml"
					#sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet, frecuencia, '0.9' )
					sentenciaIndice = generaSentenciaSiteMap(urlIndiceDataset,'index', fechaDataSet )
					sitemapIndex.write(sentenciaIndice)
					urlDataset="http://opendata.aragon.es/catalogo/"+nameDataset
					sentenciaURL = generaSentenciaSiteMap(urlDataset,'url', fechaDataSet, frecuencia, '0.9' )
					sitemapURL.write(sentenciaURL)
					#print 'Se añade el dataset '+nameDataset
		sitemapURL.write("</urlset>\n")
		sitemapURL.close()
		sitemapIndex.write("</sitemapindex>")
		sitemapIndex.close()
		print "sitemapURLOrganizacion-"+str(organizacion)+".xml y "+"sitemapIndexOrganizacion-"+str(organizacion)+".xml"
	else:
		print "No hay datasets"
	cursorDataset.close()
	
#	if fechaMasNueva == '0000-00-00':
#		os.remove(DIRSITEMAPS+"sitemapURL-"+organizacion+".xml")
#		os.remove(DIRSITEMAPS+"sitemapIndex-"+organizacion+".xml")
#	else:
#		fichero_sitemap.write("sitemaps/"+"sitemapURL-"+organizacion+".xml\n")
#		fichero_sitemap.write("sitemaps/"+"sitemapIndex-"+organizacion+".xml\n")
	return fechaMasNueva

#Método que genera el sitemap de los sitemap indice de las organizaciones y el sitemap de las url de los organizaciones. A su vez va generando los sitemap de los dataset correspondientes a sus datasets y cada uno a su correspondientes recursos
#devuelve la fecha del dataset para luego ver cual es el más actual ya de este modo actualice en cascada los datasets a los que pertenece
#Si devuelve 0000-00-00 es que todo los recursos estan caído, con lo que no habría que añadir 
def generaSiteMapOrganizacion(conexion):
#	global fichero_sitemap
	sitemapURL=open(DIRSITEMAPS+"sitemapURL-Organizaciones.xml","w")
	sitemapIndex=open(DIRSITEMAPS+"sitemapIndex-Organizaciones.xml","w")
	sitemapURL.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	sitemapIndex.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	consulta="SELECT name FROM public.group_revision WHERE current='t' AND is_organization='t' AND state='active' "
	#print 'La consulta es '+consulta
	cursorOrganizacion=conexion.cursor()
	q = cursorOrganizacion.execute(consulta)
	resultados = cursorOrganizacion.fetchall()
	fechaMasNueva='0000-00-00'
	if resultados is not None:
		for organizacion in resultados:
			nameOrganizacion=str(organizacion[0])
			
			
			fechaOrganizacion=generaSiteMapDataset(nameOrganizacion, conexion)
			if comparaFecha(fechaOrganizacion,'0000-00-00' )>0:
				#comparamos la fecha más nueva de la organizacion con la de todas la organizaciones
				fechaMasNueva=fechaMasActual(fechaMasNueva, fechaOrganizacion)
				#Ahora escribimos la sentencia del index y luego del de url
				urlIndiceOrganizacion= "http://opendata.aragon.es/sitemaps/sitemapIndexOrganizacion-"+nameOrganizacion+".xml"
				#sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '', '1' )
				sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '','0.9')
				sitemapIndex.write(sentenciaIndice)
				urlOrganizacion=ORGANIZACION+nameOrganizacion
				sentenciaURL = generaSentenciaSiteMap(urlOrganizacion,'url', fechaOrganizacion, '', '0.9' )
				sitemapURL.write(sentenciaURL)
				urlIndiceOrganizacion= "http://opendata.aragon.es/sitemaps/sitemapURLOrganizacion-"+nameOrganizacion+".xml"
				sentenciaIndice = generaSentenciaSiteMap(urlIndiceOrganizacion,'index', fechaOrganizacion, '','0.9')
				sitemapIndex.write(sentenciaIndice)
				print 'Se añade la organizacion '+nameOrganizacion
		sitemapURL.write("</urlset>\n")
		sitemapURL.close()
		sitemapIndex.write("</sitemapindex>")
		sitemapIndex.close()
		print 'Se han generado los ficheros '+DIRSITEMAPS+'sitemapURL-Organizaciones.xml y '+DIRSITEMAPS+'sitemapIndex-Organizaciones.xml'
	else:
		print "No hay organizacion"
	cursorOrganizacion.close()
	
	if fechaMasNueva == '0000-00-00':
		os.remove(DIRSITEMAPS+"sitemapURL-Organizaciones.xml")
		os.remove(DIRSITEMAPS+"sitemapIndex-Organizaciones.xml")
#	else:
#		fichero_sitemap.write("sitemaps/"+"sitemapURL-Organizaciones.xml\n")
#		fichero_sitemap.write("sitemaps/"+"sitemapIndex-Organizaciones.xml\n")
	return fechaMasNueva
	

def is_http_url(s):
	"""
	Returns true if s is valid http url, else false 
	Arguments:
	- `s`:
	"""
	if re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',s):
		return True
	else:
		return False
		
		
#Método que sirve para revisaruna URL
#Devuelve el código de estado de HTTP, 200 = Ok. http://es.wikipedia.org/wiki/Anexo:C%C3%B3digos_de_estado_HTTP
def comprobaURL(url):
	ret=0
	try:
		ret = urllib2.urlopen(url).code
	except urllib2.HTTPError, e:
		ret = e.code
	except urllib2.URLError, e:
		print e.args
		print 'La url que da cosas raras es '+url
	return ret
	
#Método que genera el siteMap del home, en un principio sólo tiene la  url de home, la home del catalogo y la aragopedia, ya  que el resto se meten en otros grupos
def generaSiteMapHome():
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemapHome.xml","w")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	urls = [URL, CATALOGO, CATALOGO+'catalogo.html', ARAGOPEDIA]
	for pagina in urls:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', '1' )
		sitemap.write(sentenciaURL)
	
	sitemap.write("</urlset>\n")
#	fichero_sitemap.write("sitemaps/"+"sitemapHome.xml\n")
	sitemap.close()
	
#método para generar el sitemap de la aragopedia: Estos estaran divididos en en 5  secciones. Comunidad autonoma, provincias, comarcas, municipios y varios (aqui meteremos los articulos diferentes por ejemplo el prontuario (cuando este el articulo))
def generaSiteMapAragopedia():
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"Aragopedia.xml","w")
#	fichero_sitemap.write("sitemaps/"+"Aragopedia.xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	
	#ComunidadAutonoma
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComunidadAutonoma.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComunidadAutonoma.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaComunidadAutonomaURL = ['Aragón']
	generaSiteMapArticulosAragopedia('AragopediaComunidadAutonoma', paginaAragopediaComunidadAutonomaURL)
	
	#Provincias
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaProvincias.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaProvincias.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaProvinciasURL = ['Huesca_(provincia)', 'Teruel_(provincia)', 'Zaragoza_(provincia)']
	generaSiteMapArticulosAragopedia('AragopediaProvincias', paginaAragopediaProvinciasURL)
	
	
	#Comarcas
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComarcas.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaComarcas.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaComarcasURL = ['Alto_Gállego', 'Andorra-Sierra_de_Arcos', 'Aranda', 'Bajo_Aragón', 'Bajo_Aragón-Caspe/_Baix_Aragó-Casp', 'Bajo_Cinca/Baix_Cinca', 'Bajo_Martín', 'Campo_de_Belchite', 'Campo_de_Borja', 'Campo_de_Cariñena', 'Campo_de_Daroca', 'Cinca_Medio', 'Cinco_Villas', 'Comunidad_de_Calatayud', 'Comunidad_de_Teruel', 'Cuencas_Mineras', 'D.C._Zaragoza', 'Gúdar-Javalambre', 'Hoya_de_Huesca/Plana_de_Uesca', 'Jiloca', 'La_Jacetania', 'La_Litera/La_Llitera', 'La_Ribagorza', 'Los_Monegros', 'Maestrazgo', 'Matarraña/Matarranya', 'Ribera_Alta_del_Ebro', 'Ribera_Baja_del_Ebro', 'Sierra_de_Albarracín', 'Sobrarbe', 'Somontano_de_Barbastro', 'Tarazona_y_el_Moncayo', 'Valdejalón']
	generaSiteMapArticulosAragopedia('AragopediaComarcas', paginaAragopediaComarcasURL)
	
	#municipios
	#sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaMunicipios.xml','index', '', '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaMunicipios.xml','index')
	sitemap.write(sentenciaURL)
	paginaAragopediaMunicipiosURL = ['Abiego', 'Abizanda', 'Adahuesca', 'Agüero', 'Aísa', 'Albalate_de_Cinca', 'Albalatillo', 'Albelda', 'Albero_Alto', 'Albero_Bajo', 'Alberuela_de_Tubo', 'Alcalá_de_Gurrea', 'Alcalá_del_Obispo', 'Alcampell', 'Alcolea_de_Cinca', 'Alcubierre', 'Alerre', 'Alfántega', 'Almudévar', 'Almunia_de_San_Juan', 'Almuniente', 'Alquézar', 'Altorricón', 'Angüés', 'Ansó', 'Antillón', 'Aragüés_del_Puerto', 'Arén', 'Argavieso', 'Arguis', 'Ayerbe', 'Azanuy-Alins', 'Azara', 'Azlor', 'Baells', 'Bailo', 'Baldellou', 'Ballobar', 'Banastás', 'Barbastro', 'Barbués', 'Barbuñales', 'Bárcabo', 'Belver_de_Cinca', 'Benabarre', 'Benasque', 'Berbegal', 'Bielsa', 'Bierge', 'Biescas', 'Binaced', 'Binéfar', 'Bisaurri', 'Biscarrués', 'Blecua_y_Torres', 'Boltaña', 'Bonansa', 'Borau', 'Broto', 'Caldearenas', 'Campo', 'Camporrells', 'Canal_de_Berdún', 'Candasnos', 'Canfranc', 'Capdesaso', 'Capella', 'Casbas_de_Huesca', 'Castejón_del_Puente', 'Castejón_de_Monegros', 'Castejón_de_Sos', 'Castelflorite', 'Castiello_de_Jaca', 'Castigaleu', 'Castillazuelo', 'Castillonroy', 'Colungo', 'Chalamera', 'Chía', 'Chimillas', 'Esplús', 'Estada', 'Estadilla', 'Estopiñán_del_Castillo', 'Fago', 'Fanlo', 'Fiscal', 'Fonz', 'Foradada_del_Toscar', 'Fraga', 'Fueva_(La)', 'Gistaín', 'Grado_(El)', 'Grañén', 'Graus', 'Gurrea_de_Gállego', 'Hoz_de_Jaca', 'Huerto', 'Huesca', 'Ibieca', 'Igriés', 'Ilche', 'Isábena', 'Jaca', 'Jasa', 'Labuerda', 'Laluenga', 'Lalueza', 'Lanaja', 'Laperdiguera', 'Lascellas-Ponzano', 'Lascuarre', 'Laspaúles', 'Laspuña', 'Loarre', 'Loporzano', 'Loscorrales', 'Monesma_y_Cajigar', 'Monflorite-Lascasas', 'Montanuy', 'Monzón', 'Naval', 'Novales', 'Nueno', 'Olvena', 'Ontiñena', 'Osso_de_Cinca', 'Palo', 'Panticosa', 'Peñalba', 'Peñas_de_Riglos_(Las)', 'Peralta_de_Alcofea', 'Peralta_de_Calasanz', 'Peraltilla', 'Perarrúa', 'Pertusa', 'Piracés', 'Plan', 'Poleñino', 'Pozán_de_Vero', 'Puebla_de_Castro_(La)', 'Puente_de_Montañana', 'Puértolas', 'Pueyo_de_Araguás_(El)', 'Pueyo_de_Santa_Cruz', 'Quicena', 'Robres', 'Sabiñánigo', 'Sahún', 'Salas_Altas', 'Salas_Bajas', 'Salillas', 'Sallent_de_Gállego', 'San_Esteban_de_Litera', 'Sangarrén', 'San_Juan_de_Plan', 'Santa_Cilia', 'Santa_Cruz_de_la_Serós', 'Santaliestra_y_San_Quílez', 'Sariñena', 'Secastilla', 'Seira', 'Sena', 'Senés_de_Alcubierre', 'Sesa', 'Sesué', 'Siétamo', 'Sopeira', 'Tamarite_de_Litera', 'Tardienta', 'Tella-Sin', 'Tierz', 'Tolva', 'Torla-Ordesa', 'Torralba_de_Aragón', 'Torre_la_Ribera', 'Torrente_de_Cinca', 'Torres_de_Alcanadre', 'Torres_de_Barbués', 'Tramaced', 'Valfarta', 'Valle_de_Bardají', 'Valle_de_Lierp', 'Velilla_de_Cinca', 'Beranuy', 'Viacamp_y_Litera', 'Vicién', 'Villanova', 'Villanúa', 'Villanueva_de_Sigena', 'Yebra_de_Basa', 'Yésero', 'Zaidín', 'Valle_de_Hecho', 'Puente_la_Reina_de_Jaca', 'San_Miguel_del_Cinca', 'Sotonera_(La)', 'Lupiñén-Ortilla', 'Santa_María_de_Dulcis', 'Aínsa-Sobrarbe', 'Hoz_y_Costeán', 'Vencillón', 'Ababuj', 'Abejuela', 'Aguatón', 'Aguaviva', 'Aguilar_del_Alfambra', 'Alacón', 'Alba', 'Albalate_del_Arzobispo', 'Albarracín', 'Albentosa', 'Alcaine', 'Alcalá_de_la_Selva', 'Alcañiz', 'Alcorisa', 'Alfambra', 'Aliaga', 'Almohaja', 'Alobras', 'Alpeñés', 'Allepuz', 'Alloza', 'Allueva', 'Anadón', 'Andorra', 'Arcos_de_las_Salinas', 'Arens_de_Lledó', 'Argente', 'Ariño', 'Azaila', 'Bádenas', 'Báguena', 'Bañón', 'Barrachina', 'Bea', 'Beceite', 'Belmonte_de_San_José', 'Bello', 'Berge', 'Bezas', 'Blancas', 'Blesa', 'Bordón', 'Bronchales', 'Bueña', 'Burbáguena', 'Cabra_de_Mora', 'Calaceite', 'Calamocha', 'Calanda', 'Calomarde', 'Camañas', 'Camarena_de_la_Sierra', 'Camarillas', 'Caminreal', 'Cantavieja', 'Cañada_de_Benatanduz', 'Cañada_de_Verich_(La)', 'Cañada_Vellida', 'Cañizar_del_Olivar', 'Cascante_del_Río', 'Castejón_de_Tornos', 'Castel_de_Cabra', 'Castelnou', 'Castelserás', 'Castellar_(El)', 'Castellote', 'Cedrillas', 'Celadas', 'Cella', 'Cerollera_(La)', 'Codoñera_(La)', 'Corbalán', 'Cortes_de_Aragón', 'Cosa', 'Cretas', 'Crivillén', 'Cuba_(La)', 'Cubla', 'Cucalón', 'Cuervo_(El)', 'Cuevas_de_Almudén', 'Cuevas_Labradas', 'Ejulve', 'Escorihuela', 'Escucha', 'Estercuel', 'Ferreruela_de_Huerva', 'Fonfría', 'Formiche_Alto', 'Fórnoles', 'Fortanete', 'Foz-Calanda', 'Fresneda_(La)', 'Frías_de_Albarracín', 'Fuenferrada', 'Fuentes_Calientes', 'Fuentes_Claras', 'Fuentes_de_Rubielos', 'Fuentespalda', 'Galve', 'Gargallo', 'Gea_de_Albarracín', 'Ginebrosa_(La)', 'Griegos', 'Guadalaviar', 'Gúdar', 'Híjar', 'Hinojosa_de_Jarque', 'Hoz_de_la_Vieja_(La)', 'Huesa_del_Común', 'Iglesuela_del_Cid_(La)', 'Jabaloyas', 'Jarque_de_la_Val', 'Jatiel', 'Jorcas', 'Josa', 'Lagueruela', 'Lanzuela', 'Libros', 'Lidón', 'Linares_de_Mora', 'Loscos', 'Lledó', 'Maicas', 'Manzanera', 'Martín_del_Río', 'Mas_de_las_Matas', 'Mata_de_los_Olmos_(La)', 'Mazaleón', 'Mezquita_de_Jarque', 'Mirambel', 'Miravete_de_la_Sierra', 'Molinos', 'Monforte_de_Moyuela', 'Monreal_del_Campo', 'Monroyo', 'Montalbán', 'Monteagudo_del_Castillo', 'Monterde_de_Albarracín', 'Mora_de_Rubielos', 'Moscardón', 'Mosqueruela', 'Muniesa', 'Noguera_de_Albarracín', 'Nogueras', 'Nogueruelas', 'Obón', 'Odón', 'Ojos_Negros', 'Olba', 'Oliete', 'Olmos_(Los)', 'Orihuela_del_Tremedal', 'Orrios', 'Palomar_de_Arroyos', 'Pancrudo', 'Parras_de_Castellote_(Las)', 'Peñarroya_de_Tastavins', 'Peracense', 'Peralejos', 'Perales_del_Alfambra', 'Pitarque', 'Plou', 'Pobo_(El)', 'Portellada_(La)', 'Pozondón', 'Pozuel_del_Campo', 'Puebla_de_Híjar_(La)', 'Puebla_de_Valverde_(La)', 'Puertomingalvo', 'Ráfales', 'Rillo', 'Riodeva', 'Ródenas', 'Royuela', 'Rubiales', 'Rubielos_de_la_Cérida', 'Rubielos_de_Mora', 'Salcedillo', 'Saldón', 'Samper_de_Calanda', 'San_Agustín', 'San_Martín_del_Río', 'Santa_Cruz_de_Nogueras', 'Santa_Eulalia', 'Sarrión', 'Segura_de_los_Baños', 'Seno', 'Singra', 'Terriente', 'Teruel', 'Toril_y_Masegoso', 'Tormón', 'Tornos', 'Torralba_de_los_Sisones', 'Torrecilla_de_Alcañiz', 'Torrecilla_del_Rebollar', 'Torre_de_Arcas', 'Torre_de_las_Arcas', 'Torre_del_Compte', 'Torrelacárcel', 'Torre_los_Negros', 'Torremocha_de_Jiloca', 'Torres_de_Albarracín', 'Torrevelilla', 'Torrijas', 'Torrijo_del_Campo', 'Tramacastiel', 'Tramacastilla', 'Tronchón', 'Urrea_de_Gaén', 'Utrillas', 'Valacloche', 'Valbona', 'Valdealgorfa', 'Valdecuenca', 'Valdelinares', 'Valdeltormo', 'Valderrobres', 'Valjunquera', 'Vallecillo_(El)', 'Veguillas_de_la_Sierra', 'Villafranca_del_Campo', 'Villahermosa_del_Campo', 'Villanueva_del_Rebollar_de_la_Sierra', 'Villar_del_Cobo', 'Villar_del_Salz', 'Villarluengo', 'Villarquemado', 'Villarroya_de_los_Pinares', 'Villastar', 'Villel', 'Vinaceite', 'Visiedo', 'Vivel_del_Río_Martín', 'Zoma_(La)', 'Abanto', 'Acered', 'Agón', 'Aguarón', 'Aguilón', 'Ainzón', 'Aladrén', 'Alagón', 'Alarba', 'Alberite_de_San_Juan', 'Albeta', 'Alborge', 'Alcalá_de_Ebro', 'Alcalá_de_Moncayo', 'Alconchel_de_Ariza', 'Aldehuela_de_Liestos', 'Alfajarín', 'Alfamén', 'Alforque', 'Alhama_de_Aragón', 'Almochuel', 'Almolda_(La)', 'Almonacid_de_la_Cuba', 'Almonacid_de_la_Sierra', 'Almunia_de_Doña_Godina_(La)', 'Alpartir', 'Ambel', 'Anento', 'Aniñón', 'Añón_de_Moncayo', 'Aranda_de_Moncayo', 'Arándiga', 'Ardisa', 'Ariza', 'Artieda', 'Asín', 'Atea', 'Ateca', 'Azuara', 'Badules', 'Bagüés', 'Balconchán', 'Bárboles', 'Bardallur', 'Belchite', 'Belmonte_de_Gracián', 'Berdejo', 'Berrueco', 'Bijuesca', 'Biota', 'Bisimbre', 'Boquiñeni', 'Bordalba', 'Borja', 'Botorrita', 'Brea_de_Aragón', 'Bubierca', 'Bujaraloz', 'Bulbuente', 'Bureta', 'Burgo_de_Ebro_(El)', 'Buste_(El)', 'Cabañas_de_Ebro', 'Cabolafuente', 'Cadrete', 'Calatayud', 'Calatorao', 'Calcena', 'Calmarza', 'Campillo_de_Aragón', 'Carenas', 'Cariñena', 'Caspe', 'Castejón_de_Alarba', 'Castejón_de_las_Armas', 'Castejón_de_Valdejasa', 'Castiliscar', 'Cervera_de_la_Cañada', 'Cerveruela', 'Cetina', 'Cimballa', 'Cinco_Olivas', 'Clarés_de_Ribota', 'Codo', 'Codos', 'Contamina', 'Cosuenda', 'Cuarte_de_Huerva', 'Cubel', 'Cuerlas_(Las)', 'Chiprana', 'Chodes', 'Daroca', 'Ejea_de_los_Caballeros', 'Embid_de_Ariza', 'Encinacorba', 'Épila', 'Erla', 'Escatrón', 'Fabara', 'Farlete', 'Fayón', 'Fayos_(Los)', 'Figueruelas', 'Fombuena', 'Frago_(El)', 'Frasno_(El)', 'Fréscano', 'Fuendejalón', 'Fuendetodos', 'Fuentes_de_Ebro', 'Fuentes_de_Jiloca', 'Gallocanta', 'Gallur', 'Gelsa', 'Godojos', 'Gotor', 'Grisel', 'Grisén', 'Herrera_de_los_Navarros', 'Ibdes', 'Illueca', 'Isuerre', 'Jaraba', 'Jarque', 'Jaulín', 'Joyosa_(La)', 'Lagata', 'Langa_del_Castillo', 'Layana', 'Lécera', 'Leciñena', 'Lechón', 'Letux', 'Litago', 'Lituénigo', 'Lobera_de_Onsella', 'Longares', 'Longás', 'Lucena_de_Jalón', 'Luceni', 'Luesia', 'Luesma', 'Lumpiaque', 'Luna', 'Maella', 'Magallón', 'Mainar', 'Malanquilla', 'Maleján', 'Malón', 'Maluenda', 'Mallén', 'Manchones', 'Mara', 'María_de_Huerva', 'Mediana_de_Aragón', 'Mequinenza', 'Mesones_de_Isuela', 'Mezalocha', 'Mianos', 'Miedes_de_Aragón', 'Monegrillo', 'Moneva', 'Monreal_de_Ariza', 'Monterde', 'Montón', 'Morata_de_Jalón', 'Morata_de_Jiloca', 'Morés', 'Moros', 'Moyuela', 'Mozota', 'Muel', 'Muela_(La)', 'Munébrega', 'Murero', 'Murillo_de_Gállego', 'Navardún', 'Nigüella', 'Nombrevilla', 'Nonaspe', 'Novallas', 'Novillas', 'Nuévalos', 'Nuez_de_Ebro', 'Olvés', 'Orcajo', 'Orera', 'Orés', 'Oseja', 'Osera_de_Ebro', 'Paniza', 'Paracuellos_de_Jiloca', 'Paracuellos_de_la_Ribera', 'Pastriz', 'Pedrola', 'Pedrosas_(Las)', 'Perdiguera', 'Piedratajada', 'Pina_de_Ebro', 'Pinseque', 'Pintanos_(Los)', 'Plasencia_de_Jalón', 'Pleitas', 'Plenas', 'Pomer', 'Pozuel_de_Ariza', 'Pozuelo_de_Aragón', 'Pradilla_de_Ebro', 'Puebla_de_Albortón', 'Puebla_de_Alfindén_(La)', 'Puendeluna', 'Purujosa', 'Quinto', 'Remolinos', 'Retascón', 'Ricla', 'Romanos', 'Rueda_de_Jalón', 'Ruesca', 'Sádaba', 'Salillas_de_Jalón', 'Salvatierra_de_Esca', 'Samper_del_Salz', 'San_Martín_de_la_Virgen_de_Moncayo', 'San_Mateo_de_Gállego', 'Santa_Cruz_de_Grío', 'Santa_Cruz_de_Moncayo', 'Santa_Eulalia_de_Gállego', 'Santed', 'Sástago', 'Saviñán', 'Sediles', 'Sestrica', 'Sierra_de_Luna', 'Sigüés', 'Sisamón', 'Sobradiel', 'Sos_del_Rey_Católico', 'Tabuenca', 'Talamantes', 'Tarazona', 'Tauste', 'Terrer', 'Tierga', 'Tobed', 'Torralba_de_los_Frailes', 'Torralba_de_Ribota', 'Torralbilla', 'Torrehermosa', 'Torrelapaja', 'Torrellas', 'Torres_de_Berrellén', 'Torrijo_de_la_Cañada', 'Tosos', 'Trasmoz', 'Trasobares', 'Uncastillo', 'Undués_de_Lerda', 'Urrea_de_Jalón', 'Urriés', 'Used', 'Utebo', 'Valdehorna', 'Val_de_San_Martín', 'Valmadrid', 'Valpalmas', 'Valtorres', 'Velilla_de_Ebro', 'Velilla_de_Jiloca', 'Vera_de_Moncayo', 'Vierlas', 'Vilueña_(La)', 'Villadoz', 'Villafeliche', 'Villafranca_de_Ebro', 'Villalba_de_Perejil', 'Villalengua', 'Villanueva_de_Gállego', 'Villanueva_de_Jiloca', 'Villanueva_de_Huerva', 'Villar_de_los_Navarros', 'Villarreal_de_Huerva', 'Villarroya_de_la_Sierra', 'Villarroya_del_Campo', 'Vistabella', 'Zaida_(La)', 'Zaragoza', 'Zuera', 'Biel', 'Marracos', 'Villamayor_de_Gállego']
	generaSiteMapArticulosAragopedia('AragopediaMunicipios', paginaAragopediaMunicipiosURL)
	
	#Varios
#	sentenciaURL = generaSentenciaSiteMap('http://opendata.aragon.es/sitemaps/'+'AragopediaVarios.xml','index', '', '', '0.9' )
#	sitemap.write(sentenciaURL)
#	paginaAragopediaComunidadAutonomaurl = []
	
	
	sitemap.write("</sitemapindex>\n")
	sitemap.close()
	
#Método que sirve genera el sitemap de articulos de la aragopedia
#Los articulos se le meten en un array
def generaSiteMapArticulosAragopedia(nombre, arrayPaginas):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+nombre+".xml","w")
#	fichero_sitemap.write("sitemaps/"+nombre+".xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	
	for pagina in arrayPaginas:
		sentenciaURL = generaSentenciaSiteMap(PAGINA_ARAGOPEDIA+pagina,'url', '', '', '0.8' )
		sitemap.write(sentenciaURL)
	sitemap.write("</urlset>\n")
	sitemap.close()
	

#Método que sirve para generar el sitemap de nombre.
def generaSiteMapURL(nombre, arrayURLs, prioridad):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemap"+nombre+".xml","w")
#	fichero_sitemap.write("sitemaps/sitemap"+nombre+".xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
	for pagina in arrayURLs:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', prioridad )
		sitemap.write(sentenciaURL)
	sitemap.write("</urlset>\n")
	sitemap.close()
	
	
#Método para generar el sitemap de  varios. Este contiene las búsquedas, los temas.... y luego finalmente los tags de los dataset de ckan
def generaSiteMapVarios(arrayVarios, conexion):
#	global fichero_sitemap
	sitemap=open(DIRSITEMAPS+"sitemapVarios.xml","w")
#	fichero_sitemap.write("sitemaps/sitemapVarios.xml\n")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")
		#Añadimos los temas
	consulta="SELECT name FROM public.group_revision WHERE current='t' AND is_organization='f'"
	cursor =conexion.cursor()
	q = cursor.execute(consulta)
	resultados = cursor.fetchall()
	
	if resultados is not None:
		for tema in resultados:
			sentencia = generaSentenciaSiteMap(TEMA+tema[0],'url', '', '', '0.2' )
			sitemap.write(sentencia)
	else:
		print 'No hay temas'
	
	
	for pagina in arrayVarios:
		sentenciaURL = generaSentenciaSiteMap(pagina,'url', '', '', '0.2' )
		sitemap.write(sentenciaURL)
	#Añadimos los tags
	consulta="SELECT  name FROM public.tag"
	
	q = cursor.execute(consulta)
	resultados = cursor.fetchall()
	
	if resultados is not None:
		for tag in resultados:
			sentencia = generaSentenciaSiteMap(TAGS+tag[0],'url', '', '', '0.2' )
			sitemap.write(sentencia)
	else:
		print 'No hay tags'
	cursor.close()
	
	sitemap.write("</urlset>\n")
	sitemap.close()
	
#Método que sirve para limpiar directorio que contiene los sitempas
def limpiaXml():
	filelist = [ f for f in os.listdir(DIRSITEMAPS) if f.endswith(".xml") ]
	for f in filelist:
		os.remove(DIRSITEMAPS+f)

def main():
	##PostgreSQL
	CONEXION_BD = "host='localhost' dbname='ckan_default' port='9999' user='ckan_default' password='ckan_default'"
	
	"""CONEXION_BD = config.OPENDATA_POSTGRE_CONEXION_BD"""
	URL="http://opendata.aragon.es/"
	CATALOGO=URL+"catalogo/"
	PORTAL=URL+"portal/"
	ARAGOPEDIA=URL+"aragopedia/"
	PAGINA_ARAGOPEDIA=ARAGOPEDIA+"index.php/"
	BASEDATOS=CATALOGO+'base-datos/'
	TEMA=CATALOGO+'group/'
	ORGANIZACION=CATALOGO+'organization/'
	TAGS=CATALOGO+'?tags='
	
	
	limpiaXml()
	sitemap=open(DIR+"sitemap.xml","w")
	sitemap.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<sitemapindex\n\txmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n\txmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\txsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9\n\t\thttp://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd\">\n")
	
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapHome.xml",'index', '', '', '' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de HOME'
	generaSiteMapHome()
	#Nos conectamos a la base de datos
	connection = psycopg2.connect(CONEXION_BD)
	
	fecha=generaSiteMapDataset('direccion_general_de_patrimonio_cultural', connection)
	print 'Comenzamos a generar el sitemap de los datasets'
	fecha=generaSiteMapOrganizacion(connection)
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapURL-Organizaciones.xml",'index', fecha, '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapURL-Organizaciones.xml",'index', fecha)
	sitemap.write(sentenciaURL)
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapIndex-Organizaciones.xml",'index', fecha, '', '0.9' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapIndex-Organizaciones.xml",'index', fecha)
	sitemap.write(sentenciaURL)
	#Aragopedia
	generaSiteMapAragopedia()
	#sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"Aragopedia.xml",'index', '', '', '0.8' )
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"Aragopedia.xml",'index' )
	sitemap.write(sentenciaURL)
	#Socialdata
	print 'Comenzamos a generar el sitemap de social-data'
	generaSiteMapURL('Socialdata', [URL+'portal/social-data', URL+'condiciones-utilizacion-social-data'], '0.7')
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapSocialdata.xml",'index' )
	sitemap.write(sentenciaURL)
	#Colabora
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapColabora.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de colabora'
	generaSiteMapURL('Colabora', [URL+'portal/colabora'], '0.4')
	#Aplicaciones
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapAplicaciones.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de las aplicaciones'
	aplicaciones=['http://opendata.aragon.es/portal/aplicaciones', 'http://opendata.aragon.es/aragopedia', 'http://presupuesto.aragon.es/', 'http://opendata.aragon.es/portal/social-data', 'http://www.boa.aragon.es/EBOA/opendata.htm', 'http://www.arcgis.com/apps/StorytellingTextLegend/index.html?appid=3f1d252c1db64140817ab84f0a03524c', 'http://www.marianistas.net/', 'http://dondevanmisimpuestos.es/', 'http://www.ebolets.com/es/index.html', 'http://vps147.cesvima.upm.es/jacathon_2014/index.html', 'https://github.com/aragonopendata/DEVTA','http://laboratorio.diariodenavarra.es/jacathon/', 'https://github.com/aragonopendata/DNlab', 'https://github.com/aragonopendata/Huracan', 'http://crasaragon.com/','https://github.com/aragonopendata/JodoCoders', 'http://neru.me/', 'https://github.com/aragonopendata/Manata', 'https://play.google.com/store/apps/details?id=noteam.conocesaragon', 'https://github.com/aragonopendata/NOTEAM', 'http://visual-aragopedia.visualizados.com/', 'https://github.com/aragonopendata/Poolparty', 'http://opendata.aragon.es/portal/envio-aplicaciones'] #Falta , 'http://aot.rbel.co/' que no va
	generaSiteMapURL('Aplicaciones', aplicaciones, '0.3')
	
	#Info open data
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapInfoOpenData.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de info open data'
	infoOpenData=[ PORTAL+'aragon-open-data', PORTAL+'multimedia/videos', PORTAL+'multimedia/imagenes', PORTAL+'multimedia/presentaciones', PORTAL+'documentacion', PORTAL+'desarrolladores/resumen', PORTAL+'desarrolladores/api-ckan', PORTAL+'desarrolladores/api-social-data', PORTAL+'desarrolladores/api-aragopedia', PORTAL+'desarrolladores/api-aragodbpedia', PORTAL+'desarrolladores/punto-sparql', URL+'def/Aragopedia.html', PORTAL+'cliente-sparql', PORTAL+'jacathon']
	generaSiteMapURL('InfoOpenData', infoOpenData, '0.6')
	
	#Terminos
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapTerminos.xml",'index' )
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap de terminos de uso'
	terminos = [URL+'terminos']
	generaSiteMapURL('Terminos', terminos, '0.5')
	
	#Varios
	sentenciaURL = generaSentenciaSiteMap(URLDIRSITEMAPS+"sitemapVarios.xml",'index')
	sitemap.write(sentenciaURL)
	print 'Comenzamos a generar el sitemap varios'
	urlBusqueda = [CATALOGO+'ciencia-tecnologia',CATALOGO+'comercio',CATALOGO+'cultura-ocio',CATALOGO+'demografia',CATALOGO+'deporte',CATALOGO+'economia',CATALOGO+'educacion',CATALOGO+'empleo',CATALOGO+'energia',CATALOGO+'hacienda',CATALOGO+'industria',CATALOGO+'legislacion-justicia',CATALOGO+'medio-ambiente',CATALOGO+'medio-rural-pesca',CATALOGO+'salud',CATALOGO+'sector-publico',CATALOGO+'seguridad',CATALOGO+'sociedad-bienestar',CATALOGO+'transporte',CATALOGO+'turismo',CATALOGO+'urbanismo-infraestructuras',CATALOGO+'vivienda',CATALOGO+'ciencia-tecnologia'+'/hojas-de-calculo',CATALOGO+'comercio'+'/hojas-de-calculo',CATALOGO+'cultura-ocio'+'/hojas-de-calculo',CATALOGO+'demografia'+'/hojas-de-calculo',CATALOGO+'deporte'+'/hojas-de-calculo',CATALOGO+'economia'+'/hojas-de-calculo',CATALOGO+'educacion'+'/hojas-de-calculo',CATALOGO+'empleo'+'/hojas-de-calculo',CATALOGO+'energia'+'/hojas-de-calculo',CATALOGO+'hacienda'+'/hojas-de-calculo',CATALOGO+'industria'+'/hojas-de-calculo',CATALOGO+'legislacion-justicia'+'/hojas-de-calculo',CATALOGO+'medio-ambiente'+'/hojas-de-calculo',CATALOGO+'medio-rural-pesca'+'/hojas-de-calculo',CATALOGO+'salud'+'/hojas-de-calculo',CATALOGO+'sector-publico'+'/hojas-de-calculo',CATALOGO+'seguridad'+'/hojas-de-calculo',CATALOGO+'sociedad-bienestar'+'/hojas-de-calculo',CATALOGO+'transporte'+'/hojas-de-calculo',CATALOGO+'turismo'+'/hojas-de-calculo',CATALOGO+'urbanismo-infraestructuras'+'/hojas-de-calculo',CATALOGO+'vivienda'+'/hojas-de-calculo',CATALOGO+'ciencia-tecnologia'+'/texto-plano',CATALOGO+'comercio'+'/texto-plano',CATALOGO+'cultura-ocio'+'/texto-plano',CATALOGO+'demografia'+'/texto-plano',CATALOGO+'deporte'+'/texto-plano',CATALOGO+'economia'+'/texto-plano',CATALOGO+'educacion'+'/texto-plano',CATALOGO+'empleo'+'/texto-plano',CATALOGO+'energia'+'/texto-plano',CATALOGO+'hacienda'+'/texto-plano',CATALOGO+'industria'+'/texto-plano',CATALOGO+'legislacion-justicia'+'/texto-plano',CATALOGO+'medio-ambiente'+'/texto-plano',CATALOGO+'medio-rural-pesca'+'/texto-plano',CATALOGO+'salud'+'/texto-plano',CATALOGO+'sector-publico'+'/texto-plano',CATALOGO+'seguridad'+'/texto-plano',CATALOGO+'sociedad-bienestar'+'/texto-plano',CATALOGO+'transporte'+'/texto-plano',CATALOGO+'turismo'+'/texto-plano',CATALOGO+'urbanismo-infraestructuras'+'/texto-plano',CATALOGO+'vivienda'+'/texto-plano',CATALOGO+'ciencia-tecnologia'+'/mapas',CATALOGO+'comercio'+'/mapas',CATALOGO+'cultura-ocio'+'/mapas',CATALOGO+'demografia'+'/mapas',CATALOGO+'deporte'+'/mapas',CATALOGO+'economia'+'/mapas',CATALOGO+'educacion'+'/mapas',CATALOGO+'empleo'+'/mapas',CATALOGO+'energia'+'/mapas',CATALOGO+'hacienda'+'/mapas',CATALOGO+'industria'+'/mapas',CATALOGO+'legislacion-justicia'+'/mapas',CATALOGO+'medio-ambiente'+'/mapas',CATALOGO+'medio-rural-pesca'+'/mapas',CATALOGO+'salud'+'/mapas',CATALOGO+'sector-publico'+'/mapas',CATALOGO+'seguridad'+'/mapas',CATALOGO+'sociedad-bienestar'+'/mapas',CATALOGO+'transporte'+'/mapas',CATALOGO+'turismo'+'/mapas',CATALOGO+'urbanismo-infraestructuras'+'/mapas',CATALOGO+'vivienda'+'/mapas',CATALOGO+'ciencia-tecnologia'+' ',CATALOGO+'comercio'+'/fotos',CATALOGO+'cultura-ocio'+'/fotos',CATALOGO+'demografia'+'/fotos',CATALOGO+'deporte'+'/fotos',CATALOGO+'economia'+'/fotos',CATALOGO+'educacion'+'/fotos',CATALOGO+'empleo'+'/fotos',CATALOGO+'energia'+'/fotos',CATALOGO+'hacienda'+'/fotos',CATALOGO+'industria'+'/fotos',CATALOGO+'legislacion-justicia'+'/fotos',CATALOGO+'medio-ambiente'+'/fotos',CATALOGO+'medio-rural-pesca'+'/fotos',CATALOGO+'salud'+'/fotos',CATALOGO+'sector-publico'+'/fotos',CATALOGO+'seguridad'+'/fotos',CATALOGO+'sociedad-bienestar'+'/fotos',CATALOGO+'transporte'+'/fotos',CATALOGO+'turismo'+'/fotos',CATALOGO+'urbanismo-infraestructuras'+'/fotos',CATALOGO+'vivienda'+'/fotos',CATALOGO+'ciencia-tecnologia'+'/rss',CATALOGO+'comercio'+'/rss',CATALOGO+'cultura-ocio'+'/rss',CATALOGO+'demografia'+'/rss',CATALOGO+'deporte'+'/rss',CATALOGO+'economia'+'/rss',CATALOGO+'educacion'+'/rss',CATALOGO+'empleo'+'/rss',CATALOGO+'energia'+'/rss',CATALOGO+'hacienda'+'/rss',CATALOGO+'industria'+'/rss',CATALOGO+'legislacion-justicia'+'/rss',CATALOGO+'medio-ambiente'+'/rss',CATALOGO+'medio-rural-pesca'+'/rss',CATALOGO+'salud'+'/rss',CATALOGO+'sector-publico'+'/rss',CATALOGO+'seguridad'+'/rss',CATALOGO+'sociedad-bienestar'+'/rss',CATALOGO+'transporte'+'/rss',CATALOGO+'turismo'+'/rss',CATALOGO+'urbanismo-infraestructuras'+'/rss',CATALOGO+'vivienda'+'/rss', CATALOGO+'busqueda-libre',CATALOGO+'base-datos',BASEDATOS+'ciencia-tecnologia',BASEDATOS+'comercio',BASEDATOS+'cultura-ocio',BASEDATOS+'demografia',BASEDATOS+'deporte',BASEDATOS+'economia',BASEDATOS+'educacion',BASEDATOS+'empleo',BASEDATOS+'energia',BASEDATOS+'hacienda',BASEDATOS+'industria',BASEDATOS+'legislacion-justicia',BASEDATOS+'medio-ambiente',BASEDATOS+'medio-rural-pesca',BASEDATOS+'salud',BASEDATOS+'sector-publico',BASEDATOS+'seguridad',BASEDATOS+'sociedad-bienestar',BASEDATOS+'transporte',BASEDATOS+'turismo',BASEDATOS+'urbanismo-infraestructuras',BASEDATOS+'vivienda']
	generaSiteMapVarios(urlBusqueda, connection)
	sitemap.write("</sitemapindex>\n")
	sitemap.close()
#	fichero_sitemap.close()
	
	print "La fecha más nueva es "+fecha
	
	
#	url_200.close()
	print 'Se han añadido '+str(numURLs)+' urls en el sitemaps'
	print 'Fin'

main()
