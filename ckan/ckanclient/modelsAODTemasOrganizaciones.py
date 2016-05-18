# -*- coding: utf-8 -*-

class ConjuntoDato:
	'Conjunto de datos '
	def __init__(self, titulo, name, numeroAccesos, ultimaActualizacion, visitasRecientes):
		self.titulo=titulo
		self.name=name
		self.numeroAccesos=numeroAccesos
		self.ultimaActualizacion=ultimaActualizacion
		self.visitasRecientes=visitasRecientes

class ObjectHome:
	'Objeto de la home, puede ser para una organizacion o un tema'
	def __init__(self, name, titulo, descripcion, numeroDatasets, urlImagen):
		self.name=name
		self.titulo=titulo
		self.descripcion=descripcion
		self.numeroDatasets=numeroDatasets
		self.urlImagen=urlImagen

class Tema:
	'Objeto Tema'
	def __init__(self, name,titulo, descripcion, totalConjuntosDeDatos, conjuntosDeDatos):
		self.name=name
		self.titulo=titulo
		self.descripcion=descripcion
		self.totalConjuntosDeDatos=totalConjuntosDeDatos
		self.conjuntosDeDatos=conjuntosDeDatos

class Organizacion:
	'Objeto organizacion'
	def __init__(self, name, titulo, url, descripcion, responsable, email, direccion, totalConjuntosDeDatos, conjuntosDeDatos):
		self.name=name
		self.titulo=titulo
		self.url=url
		self.descripcion=descripcion
		self.responsable=responsable
		self.email=email
		self.direccion=direccion
		self.totalConjuntosDeDatos=totalConjuntosDeDatos
		self.conjuntosDeDatos=conjuntosDeDatos
