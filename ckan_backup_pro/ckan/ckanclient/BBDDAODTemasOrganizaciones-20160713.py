# -*- coding: utf-8 -*-

import config as configuracion


from modelsAODTemasOrganizaciones import *


#Método que devuelve El string en el que modificamos los caracteres "raros" por (pseudo)etiquetas de HTML
def meteEtiquetaHTML(frase_cambiar):
	devolver =frase_cambiar.replace('á', '&aacute;').replace('é', '&eacute;').replace('í', '&iacute;').replace('ó', '&oacute;').replace('ú', '&uacute;').replace('Á', '&Aacute;').replace('É', '&Eacute;').replace('Í', '&Iacute;').replace('Ó', '&Oacute;').replace('Ú', '&Uacute;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace('¿', '&iquest;').replace('¡', '&iexcl;').replace('Ñ', '&Ntilde;').replace('ñ', '&ntilde;').replace('º', '&ordm;').replace('ª', '&ordf;').replace('#', '&almohadilla;').replace('ü', '&uuml;').replace('Ü', '&Uuml;')
	return devolver
	

def home(tipo):
	conexionBBDD=configuracion.conexion('opendata-postgre')
	cursor= conexionBBDD.cursor()
	if tipo=='tema':
		consulta= "SELECT group_revision.title, group_revision.name, group_revision.description, COUNT(package_revision.*), group_revision.image_url FROM public.group_revision, public.member_revision, public.package_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.is_organization = FALSE AND   group_revision.current=TRUE AND member_revision.current=TRUE AND package_revision.current=TRUE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND package_revision.state='active' GROUP BY  group_revision.title, group_revision.name,  group_revision.description, group_revision.image_url ORDER BY group_revision.title ASC;"
	elif tipo=='organizacion':
		consulta= "SELECT group_revision.title, group_revision.name, group_revision.description, COUNT(package_revision.*), group_revision.image_url FROM public.group_revision, public.package_revision, public.\"user\" WHERE group_revision.id = package_revision.owner_org AND package_revision.current=TRUE AND package_revision.state='active' AND public.group_revision.title = \"user\".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE GROUP BY  group_revision.title, group_revision.name,  group_revision.description, group_revision.image_url ORDER BY group_revision.title ASC;"
	else:
		cursor.close()
		conexionBBDD.close()
		return []
	q=cursor.execute(consulta)
	resultados = cursor.fetchall()
	devolver = []
	if resultados is not None:
			for resultado in resultados:
				objeto_home = ObjectHome (resultado[1] ,meteEtiquetaHTML(resultado[0]), meteEtiquetaHTML(resultado[2]), resultado[3], resultado[4])
				devolver.append(objeto_home)
	cursor.close()
	conexionBBDD.close()
	return devolver

#Tipo sera tema o organizacion. En valor estará su valor
def __datasets(tipo, valor, cursor):
	if tipo =='organizacion':
		consulta= "SELECT package_revision.title, package_revision.name, tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY'), tracking_summary.recent_views FROM public.package_revision, public.group_revision, public.tracking_summary WHERE group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = \"tracking_summary\".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = '"+valor.strip()+"' ORDER BY package_revision.revision_timestamp DESC;"
	elif tipo =='tema':
		consulta= "SELECT package_revision.title, package_revision.name, tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY'), tracking_summary.recent_views FROM public.package_revision, public.group_revision, public.tracking_summary, public.member_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND   package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = \"tracking_summary\".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = '"+valor.strip()+"'  ORDER BY package_revision.revision_timestamp DESC;"
	else:
		return []
	q=cursor.execute(consulta)
	datasets = cursor.fetchall()
	devolver = []
	if datasets is not None:
			for dataset in datasets:
				datasets_json = ConjuntoDato(meteEtiquetaHTML(dataset[0]), dataset[1], dataset[2], dataset[3], dataset[4])
				devolver.append(datasets_json)
	return devolver
	
def obtenOrganizacion(organizacion):
	conexionBBDD=configuracion.conexion('opendata-postgre')
	cursor= conexionBBDD.cursor()
	devolver =[]
	consulta1="SELECT group_revision.title, group_revision.description, \"user\".email, COUNT (package_revision.*) FROM public.group_revision, public.\"user\", public.package_revision WHERE group_revision.id = package_revision.owner_org AND public.group_revision.title = \"user\".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND public.group_revision.name ='"+organizacion.strip()+"' GROUP BY group_revision.title, group_revision.description, \"user\".email;"
	q=cursor.execute(consulta1)
	resultado1 = cursor.fetchone()
	if resultado1 is not None:
		consulta2 = "SELECT group_extra_revision.key, group_extra_revision.value FROM public.group_extra_revision, public.group_revision WHERE group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND group_extra_revision.state='active' AND group_extra_revision.current=TRUE AND (group_extra_revision.key = 'webpage' OR group_extra_revision.key = 'address' OR group_extra_revision.key = 'person') AND group_extra_revision.group_id = group_revision.id AND group_revision.name = '"+organizacion.strip()+"' ;";
		urlOrganizacion=''
		direccionOrganizacion=''
		responsableOrganizacion=''
		q=cursor.execute(consulta2)
		extras = cursor.fetchall()
		if extras is not None:
			for extra in extras:
				if extra[0]=='webpage':
					urlOrganizacion=extra[1]
				elif extra[0]=='person':
					responsableOrganizacion=extra[1]
				elif extra[0]=='address':
					direccionOrganizacion=extra[1]
		datasets=[]
		datasets =__datasets('organizacion', organizacion, cursor)
		devolver = Organizacion(organizacion, meteEtiquetaHTML(resultado1[0]), urlOrganizacion, meteEtiquetaHTML(resultado1[1]), meteEtiquetaHTML(responsableOrganizacion), meteEtiquetaHTML(resultado1[2]), meteEtiquetaHTML(direccionOrganizacion), resultado1[3], datasets)
		
		
	cursor.close()
	conexionBBDD.close()
	return devolver

def obtenTema(tema):
	conexionBBDD=configuracion.conexion('opendata-postgre')
	cursor= conexionBBDD.cursor()
	consulta="SELECT group_revision.title, group_revision.description, COUNT (package_revision.*) FROM public.package_revision, public.group_revision, public.member_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND group_revision.name = '"+tema.strip()+"' GROUP BY group_revision.title, group_revision.description;"
	q=cursor.execute(consulta)
	eltema = cursor.fetchone()
	if eltema is not None:
		datasets=[]
		datasets = __datasets('tema', tema, cursor)
		devolver = Tema(tema, meteEtiquetaHTML(eltema[0]), meteEtiquetaHTML(eltema[1]), eltema[2], datasets)
	cursor.close()
	conexionBBDD.close()
	return devolver

