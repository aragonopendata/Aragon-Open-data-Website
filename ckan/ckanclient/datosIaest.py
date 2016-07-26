#!/usr/bin/python
# -*- coding: utf-8 -*-


import config
import cx_Oracle
from time import time
from urllib import urlretrieve

import os

os.environ["NLS_LANG"] = ".UTF8"

#Esta funcion convierte los string que son fecha del iaest del tipo mm/aaaa o dd/mm/aaaa o aaaa
#Al formato que se guardan en el opendata. aaaa-mm o aaaa-mm-dd o aaaa
#Estos datos son los correspondientes a temporalUntil y temporarlFrom
def transformaTemporal(fechaIaest):
    troceado=str(fechaIaest).split('/')
    tam=len(troceado)
    if (tam==1):
        return troceado[0]
    elif (tam==2):
        return troceado[1]+'-'+troceado[0]
    elif (tam==3):
        return troceado[2]+'-'+troceado[1]+'-'+troceado[0]

def quitarParentesis(municipio):
  if " (" in municipio:
    splitres = municipio.split(" (");
    municipioReturn = splitres[1].split(")")[0] + " " + splitres[0];
    return municipioReturn
  else:
    return municipio
    
#Función que devuelve en un array los extras correspondientes a la Aragopedia [name_aragopedia, short_uri_aragopedia, type_aragopedia, uri_aragopedia]
def getEnlaceAragopedia(localidad):
  listado_comarcas =['Alto Gállego', 'Andorra-Sierra de Arcos', 'Aranda', 'Bajo Aragón', 'Bajo Aragón-Caspe/ Baix Aragó-Casp', 'Bajo Cinca/Baix Cinca', 'Bajo Martín', 'Campo de Belchite', 'Campo de Borja', 'Campo de Cariñena', 'Campo de Daroca', 'Cinca Medio', 'Cinco Villas', 'Comunidad de Calatayud', 'Comunidad de Teruel', 'Cuencas Mineras', 'D.C. Zaragoza', 'Gúdar-Javalambre', 'Hoya de Huesca/Plana de Uesca', 'Jiloca', 'La Jacetania', 'La Litera/La Llitera', 'La Ribagorza', 'Los Monegros', 'Maestrazgo', 'Matarraña/Matarranya', 'Ribera Alta del Ebro', 'Ribera Baja del Ebro', 'Sierra de Albarracín', 'Sobrarbe', 'Somontano de Barbastro', 'Tarazona y el Moncayo', 'Valdejalón']
  devolver=[]
  
  if localidad in 'Aragón':
    devolver.append(localidad)
    devolver.append(localidad)
    devolver.append(localidad)
    devolver.append('http://opendata.aragon.es/recurso/territorio/ComunidadAutonoma/Aragón')
    return devolver
  
  if localidad in listado_comarcas:
    devolver.append(localidad)
    devolver.append(localidad.replace(" ", "_"))
    devolver.append('Comarca')
    devolver.append('http://opendata.aragon.es/recurso/territorio/Comarca/'+localidad.replace(" ", "_"))
    return devolver
  
  listado_municipios =['Ababuj', 'Abanto', 'Abejuela', 'Abiego', 'Abizanda', 'Acered', 'Adahuesca', 'Agón', 'Aguarón', 'Aguatón', 'Aguaviva', 'Agüero', 'Aguilar del Alfambra', 'Aguilón', 'Aínsa-Sobrarbe', 'Ainzón', 'Aísa', 'Alacón', 'Aladrén', 'Alagón', 'Alarba', 'Alba', 'Albalate de Cinca', 'Albalate del Arzobispo', 'Albalatillo', 'Albarracín', 'Albelda', 'Albentosa', 'Alberite de San Juan', 'Albero Alto', 'Albero Bajo', 'Alberuela de Tubo', 'Albeta', 'Alborge', 'Alcaine', 'Alcalá de Ebro', 'Alcalá de Gurrea', 'Alcalá de la Selva', 'Alcalá de Moncayo', 'Alcalá del Obispo', 'Alcampell', 'Alcañiz', 'Alcolea de Cinca', 'Alconchel de Ariza', 'Alcorisa', 'Alcubierre', 'Aldehuela de Liestos', 'Alerre', 'Alfajarín', 'Alfambra', 'Alfamén', 'Alfántega', 'Alforque', 'Alhama de Aragón', 'Aliaga', 'Allepuz', 'Alloza', 'Allueva', 'Almochuel', 'Almohaja', 'Almolda (La)', 'Almonacid de la Cuba', 'Almonacid de la Sierra', 'Almudévar', 'Almunia de Doña Godina (La)', 'Almunia de San Juan', 'Almuniente', 'Alobras', 'Alpartir', 'Alpeñés', 'Alquézar', 'Altorricón', 'Ambel', 'Anadón', 'Andorra', 'Anento', 'Angüés', 'Aniñón', 'Añón de Moncayo', 'Ansó', 'Antillón', 'Aragüés del Puerto', 'Aranda de Moncayo', 'Arándiga', 'Arcos de las Salinas', 'Ardisa', 'Arén', 'Arens de Lledó', 'Argavieso', 'Argente', 'Arguis', 'Ariño', 'Ariza', 'Artieda', 'Asín', 'Atea', 'Ateca', 'Ayerbe', 'Azaila', 'Azanuy-Alins', 'Azara', 'Azlor', 'Azuara', 'Bádenas', 'Badules', 'Baells', 'Báguena', 'Bagüés', 'Bailo', 'Balconchán', 'Baldellou', 'Ballobar', 'Banastás', 'Bañón', 'Barbastro', 'Bárboles', 'Barbués', 'Barbuñales', 'Bárcabo', 'Bardallur', 'Barrachina', 'Bea', 'Beceite', 'Belchite', 'Bello', 'Belmonte de Gracián', 'Belmonte de San José', 'Belver de Cinca', 'Benabarre', 'Benasque', 'Beranuy', 'Berbegal', 'Berdejo', 'Berge', 'Berrueco', 'Bezas', 'Biel', 'Bielsa', 'Bierge', 'Biescas', 'Bijuesca', 'Binaced', 'Binéfar', 'Biota', 'Bisaurri', 'Biscarrués', 'Bisimbre', 'Blancas', 'Blecua y Torres', 'Blesa', 'Boltaña', 'Bonansa', 'Boquiñeni', 'Borau', 'Bordalba', 'Bordón', 'Borja', 'Botorrita', 'Brea de Aragón', 'Bronchales', 'Broto', 'Bubierca', 'Bueña', 'Bujaraloz', 'Bulbuente', 'Burbáguena', 'Bureta', 'Burgo de Ebro (El)', 'Buste (El)', 'Cabañas de Ebro', 'Cabolafuente', 'Cabra de Mora', 'Cadrete', 'Calaceite', 'Calamocha', 'Calanda', 'Calatayud', 'Calatorao', 'Calcena', 'Caldearenas', 'Calmarza', 'Calomarde', 'Camañas', 'Camarena de la Sierra', 'Camarillas', 'Caminreal', 'Campillo de Aragón', 'Campo', 'Camporrells', 'Cañada de Benatanduz', 'Cañada de Verich (La)', 'Cañada Vellida', 'Canal de Berdún', 'Candasnos', 'Canfranc', 'Cañizar del Olivar', 'Cantavieja', 'Capdesaso', 'Capella', 'Carenas', 'Cariñena', 'Casbas de Huesca', 'Cascante del Río', 'Caspe', 'Castejón de Alarba', 'Castejón de las Armas', 'Castejón de Monegros', 'Castejón de Sos', 'Castejón de Tornos', 'Castejón de Valdejasa', 'Castejón del Puente', 'Castel de Cabra', 'Castelflorite', 'Castellar (El)', 'Castellote', 'Castelnou', 'Castelserás', 'Castiello de Jaca', 'Castigaleu', 'Castiliscar', 'Castillazuelo', 'Castillonroy', 'Cedrillas', 'Celadas', 'Cella', 'Cerollera (La)', 'Cervera de la Cañada', 'Cerveruela', 'Cetina', 'Chalamera', 'Chía', 'Chimillas', 'Chiprana', 'Chodes', 'Cimballa', 'Cinco Olivas', 'Clarés de Ribota', 'Codo', 'Codoñera (La)', 'Codos', 'Colungo', 'Contamina', 'Corbalán', 'Cortes de Aragón', 'Cosa', 'Cosuenda', 'Cretas', 'Crivillén', 'Cuarte de Huerva', 'Cuba (La)', 'Cubel', 'Cubla', 'Cucalón', 'Cuerlas (Las)', 'Cuervo (El)', 'Cuevas de Almudén', 'Cuevas Labradas', 'Daroca', 'Ejea de los Caballeros', 'Ejulve', 'Embid de Ariza', 'Encinacorba', 'Épila', 'Erla', 'Escatrón', 'Escorihuela', 'Escucha', 'Esplús', 'Estada', 'Estadilla', 'Estercuel', 'Estopiñán del Castillo', 'Fabara', 'Fago', 'Fanlo', 'Farlete', 'Fayón', 'Fayos (Los)', 'Ferreruela de Huerva', 'Figueruelas', 'Fiscal', 'Fombuena', 'Fonfría', 'Fonz', 'Foradada del Toscar', 'Formiche Alto', 'Fórnoles', 'Fortanete', 'Foz-Calanda', 'Fraga', 'Frago (El)', 'Frasno (El)', 'Fréscano', 'Fresneda (La)', 'Frías de Albarracín', 'Fuendejalón', 'Fuendetodos', 'Fuenferrada', 'Fuentes Calientes', 'Fuentes Claras', 'Fuentes de Ebro', 'Fuentes de Jiloca', 'Fuentes de Rubielos', 'Fuentespalda', 'Fueva (La)', 'Gallocanta', 'Gallur', 'Galve', 'Gargallo', 'Gea de Albarracín', 'Gelsa', 'Ginebrosa (La)', 'Gistaín', 'Godojos', 'Gotor', 'Grado (El)', 'Grañén', 'Graus', 'Griegos', 'Grisel', 'Grisén', 'Guadalaviar', 'Gúdar', 'Gurrea de Gállego', 'Herrera de los Navarros', 'Híjar', 'Hinojosa de Jarque', 'Hoz de Jaca', 'Hoz de la Vieja (La)', 'Hoz y Costeán', 'Huerto', 'Huesa del Común', 'Huesca', 'Ibdes', 'Ibieca', 'Iglesuela del Cid (La)', 'Igriés', 'Ilche', 'Illueca', 'Isábena', 'Isuerre', 'Jabaloyas', 'Jaca', 'Jaraba', 'Jarque', 'Jarque de la Val', 'Jasa', 'Jatiel', 'Jaulín', 'Jorcas', 'Josa', 'Joyosa (La)', 'Labuerda', 'Lagata', 'Lagueruela', 'Laluenga', 'Lalueza', 'Lanaja', 'Langa del Castillo', 'Lanzuela', 'Laperdiguera', 'Lascellas-Ponzano', 'Lascuarre', 'Laspaúles', 'Laspuña', 'Layana', 'Lécera', 'Lechón', 'Leciñena', 'Letux', 'Libros', 'Lidón', 'Linares de Mora', 'Litago', 'Lituénigo', 'Lledó', 'Loarre', 'Lobera de Onsella', 'Longares', 'Longás', 'Loporzano', 'Loscorrales', 'Loscos', 'Lucena de Jalón', 'Luceni', 'Luesia', 'Luesma', 'Lumpiaque', 'Luna', 'Lupiñén-Ortilla', 'Maella', 'Magallón', 'Maicas', 'Mainar', 'Malanquilla', 'Maleján', 'Mallén', 'Malón', 'Maluenda', 'Manchones', 'Manzanera', 'Mara', 'María de Huerva', 'Marracos', 'Martín del Río', 'Mas de las Matas', 'Mata de los Olmos (La)', 'Mazaleón', 'Mediana de Aragón', 'Mequinenza', 'Mesones de Isuela', 'Mezalocha', 'Mezquita de Jarque', 'Mianos', 'Miedes de Aragón', 'Mirambel', 'Miravete de la Sierra', 'Molinos', 'Monegrillo', 'Monesma y Cajigar', 'Moneva', 'Monflorite-Lascasas', 'Monforte de Moyuela', 'Monreal de Ariza', 'Monreal del Campo', 'Monroyo', 'Montalbán', 'Montanuy', 'Monteagudo del Castillo', 'Monterde', 'Monterde de Albarracín', 'Montón', 'Monzón', 'Mora de Rubielos', 'Morata de Jalón', 'Morata de Jiloca', 'Morés', 'Moros', 'Moscardón', 'Mosqueruela', 'Moyuela', 'Mozota', 'Muel', 'Muela (La)', 'Munébrega', 'Muniesa', 'Murero', 'Murillo de Gállego', 'Naval', 'Navardún', 'Nigüella', 'Noguera de Albarracín', 'Nogueras', 'Nogueruelas', 'Nombrevilla', 'Nonaspe', 'Novales', 'Novallas', 'Novillas', 'Nueno', 'Nuévalos', 'Nuez de Ebro', 'Obón', 'Odón', 'Ojos Negros', 'Olba', 'Oliete', 'Olmos (Los)', 'Olvena', 'Olvés', 'Ontiñena', 'Orcajo', 'Orera', 'Orés', 'Orihuela del Tremedal', 'Orrios', 'Oseja', 'Osera de Ebro', 'Osso de Cinca', 'Palo', 'Palomar de Arroyos', 'Pancrudo', 'Paniza', 'Panticosa', 'Paracuellos de Jiloca', 'Paracuellos de la Ribera', 'Parras de Castellote (Las)', 'Pastriz', 'Pedrola', 'Pedrosas (Las)', 'Peñalba', 'Peñarroya de Tastavins', 'Peñas de Riglos (Las)', 'Peracense', 'Peralejos', 'Perales del Alfambra', 'Peralta de Alcofea', 'Peralta de Calasanz', 'Peraltilla', 'Perarrúa', 'Perdiguera', 'Pertusa', 'Piedratajada', 'Pina de Ebro', 'Pinseque', 'Pintanos (Los)', 'Piracés', 'Pitarque', 'Plan', 'Plasencia de Jalón', 'Pleitas', 'Plenas', 'Plou', 'Pobo (El)', 'Poleñino', 'Pomer', 'Portellada (La)', 'Pozán de Vero', 'Pozondón', 'Pozuel de Ariza', 'Pozuel del Campo', 'Pozuelo de Aragón', 'Pradilla de Ebro', 'Puebla de Albortón', 'Puebla de Alfindén (La)', 'Puebla de Castro (La)', 'Puebla de Híjar (La)', 'Puebla de Valverde (La)', 'Puendeluna', 'Puente de Montañana', 'Puente la Reina de Jaca', 'Puértolas', 'Puertomingalvo', 'Pueyo de Araguás (El)', 'Pueyo de Santa Cruz', 'Purujosa', 'Quicena', 'Quinto', 'Ráfales', 'Remolinos', 'Retascón', 'Ricla', 'Rillo', 'Riodeva', 'Robres', 'Ródenas', 'Romanos', 'Royuela', 'Rubiales', 'Rubielos de la Cérida', 'Rubielos de Mora', 'Rueda de Jalón', 'Ruesca', 'Sabiñánigo', 'Sádaba', 'Sahún', 'Salas Altas', 'Salas Bajas', 'Salcedillo', 'Saldón', 'Salillas', 'Salillas de Jalón', 'Sallent de Gállego', 'Salvatierra de Esca', 'Samper de Calanda', 'Samper del Salz', 'San Agustín', 'San Esteban de Litera', 'San Juan de Plan', 'San Martín de la Virgen de Moncayo', 'San Martín del Río', 'San Mateo de Gállego', 'San Miguel del Cinca', 'Sangarrén', 'Santa Cilia', 'Santa Cruz de Grío', 'Santa Cruz de la Serós', 'Santa Cruz de Moncayo', 'Santa Cruz de Nogueras', 'Santa Eulalia', 'Santa Eulalia de Gállego', 'Santa María de Dulcis', 'Santaliestra y San Quílez', 'Santed', 'Sariñena', 'Sarrión', 'Sástago', 'Saviñán', 'Secastilla', 'Sediles', 'Segura de los Baños', 'Seira', 'Sena', 'Senés de Alcubierre', 'Seno', 'Sesa', 'Sestrica', 'Sesué', 'Sierra de Luna', 'Siétamo', 'Sigüés', 'Singra', 'Sisamón', 'Sobradiel', 'Sopeira', 'Sos del Rey Católico', 'Sotonera (La)', 'Tabuenca', 'Talamantes', 'Tamarite de Litera', 'Tarazona', 'Tardienta', 'Tauste', 'Tella-Sin', 'Terrer', 'Terriente', 'Teruel', 'Tierga', 'Tierz', 'Tobed', 'Tolva', 'Toril y Masegoso', 'Torla-Ordesa', 'Tormón', 'Tornos', 'Torralba de Aragón', 'Torralba de los Frailes', 'Torralba de los Sisones', 'Torralba de Ribota', 'Torralbilla', 'Torre de Arcas', 'Torre de las Arcas', 'Torre del Compte', 'Torre la Ribera', 'Torre los Negros', 'Torrecilla de Alcañiz', 'Torrecilla del Rebollar', 'Torrehermosa', 'Torrelacárcel', 'Torrelapaja', 'Torrellas', 'Torremocha de Jiloca', 'Torrente de Cinca', 'Torres de Albarracín', 'Torres de Alcanadre', 'Torres de Barbués', 'Torres de Berrellén', 'Torrevelilla', 'Torrijas', 'Torrijo de la Cañada', 'Torrijo del Campo', 'Tosos', 'Tramacastiel', 'Tramacastilla', 'Tramaced', 'Trasmoz', 'Trasobares', 'Tronchón', 'Uncastillo', 'Undués de Lerda', 'Urrea de Gaén', 'Urrea de Jalón', 'Urriés', 'Used', 'Utebo', 'Utrillas', 'Val de San Martín', 'Valacloche', 'Valbona', 'Valdealgorfa', 'Valdecuenca', 'Valdehorna', 'Valdelinares', 'Valdeltormo', 'Valderrobres', 'Valfarta', 'Valjunquera', 'Valle de Bardají', 'Valle de Hecho', 'Valle de Lierp', 'Vallecillo (El)', 'Valmadrid', 'Valpalmas', 'Valtorres', 'Veguillas de la Sierra', 'Velilla de Cinca', 'Velilla de Ebro', 'Velilla de Jiloca', 'Vencillón', 'Vera de Moncayo', 'Viacamp y Litera', 'Vicién', 'Vierlas', 'Villadoz', 'Villafeliche', 'Villafranca de Ebro', 'Villafranca del Campo', 'Villahermosa del Campo', 'Villalba de Perejil', 'Villalengua', 'Villamayor de Gállego', 'Villanova', 'Villanúa', 'Villanueva de Gállego', 'Villanueva de Huerva', 'Villanueva de Jiloca', 'Villanueva de Sigena', 'Villanueva del Rebollar de la Sierra', 'Villar de los Navarros', 'Villar del Cobo', 'Villar del Salz', 'Villarluengo', 'Villarquemado', 'Villarreal de Huerva', 'Villarroya de la Sierra', 'Villarroya de los Pinares', 'Villarroya del Campo', 'Villastar', 'Villel', 'Vilueña (La)', 'Vinaceite', 'Visiedo', 'Vistabella', 'Vivel del Río Martín', 'Yebra de Basa', 'Yésero', 'Zaida (La)', 'Zaidín', 'Zaragoza', 'Zoma (La)', 'Zuera']
  
  if localidad in listado_municipios:
    devolver.append(quitarParentesis(localidad))
    devolver.append(localidad.replace(" ", "_"))
    devolver.append('Municipio')
    devolver.append('http://opendata.aragon.es/recurso/territorio/Municipio/'+localidad.replace(" ", "_"))
    return devolver
  else :
    devolver.append(localidad)
    devolver.append(localidad)
    devolver.append('Otro')
    devolver.append('')
    return devolver



def _download_xls_file(url):
    """ Download a xls with random name to hard disk"""
    dest = config.DOWNLOAD_TEMPORAL + "/" + str(int(time() * 100)) + ".xls"
    urlretrieve(url, dest)
    return dest

def descargar():
    return main()

def main():
    connection = cx_Oracle.connect(
    config.OPENDATA_USR + "/" + config.OPENDATA_PASS + "@" + config.OPENDATA_CONEXION_BD)
    print  config.OPENDATA_CONEXION_BD
    cursor = connection.cursor()


    QUERY = "SELECT "
    QUERY = QUERY + "IAES.MET_DATASET.ID_DATASET AS IdDataset, "
    QUERY = QUERY + "IAES.MET_DATASET.NOMBRE_DS AS Titulo, "
    QUERY = QUERY + "IAES.MET_DATASET.URL_OPENDATA_PUBLICADO AS url_publicado, "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_ORGANISATION AS Autor, "
    QUERY = QUERY + "IAES.MET_OPERACION.CONTACT_EMAIL AS Email_autor, "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.DATA_DESCR, IAES.MET_OPERACION.DATA_DESCR) AS Descripcion, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.REF_AREA, IAES.MET_PRODUCTO.REF_AREA) AS Spatial,   "
#    QUERY = QUERY + "NVL(IAES.MET_DATASET.CODIGO_COVERAGE_TIME, IAES.MET_PRODUCTO.COVERAGE_TIME) AS Temporal,  "

    QUERY = QUERY + "NVL(IAES.MET_DATASET.TIME_FROM, IAES.MET_PRODUCTO.COVERAGE_TIME_FROM) AS Temporal_from, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.TIME_TO, IAES.MET_PRODUCTO.COVERAGE_TIME_TO) AS Temporal_to, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.CODIGO_COVERAGE_TIME, IAES.MET_PRODUCTO.COVERAGE_TIME) AS Temporal_alternativo, "
    
    QUERY = QUERY + "IAES.MET_PRODUCTO.FREQ_DISS AS Frecuencia, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ACCURACY AS Calidad, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.URL_ACCURACY AS url_calidad,"
    
    QUERY = QUERY + "NVL(IAES.MET_DATASET.COMMENT_DSET, IAES.MET_PRODUCTO.DESCRIPCION_METOD) AS Notas_metodologicas, "
    QUERY = QUERY + "NVL(IAES.MET_DATASET.URL_COMMENT, IAES.MET_PRODUCTO.URL_METOD) AS url_metodologia, "
    
    QUERY = QUERY + "NVL(IAES.MET_DATASET.NIVEL_DETALLE, (IAES.MET_PRODUCTO.DATA_DESCR_VAR_ESTUDIO || '. ' || IAES.MET_PRODUCTO.DATA_DESCR_VAR_CLASIF || '. ' || IAES.MET_PRODUCTO.REF_PERIOD)) As Nivel_Detalle, "
    QUERY = QUERY + "IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA as Titulo_descarga,  "
    QUERY = QUERY + "IAES.MET_FICHEROS.URL_FICHERO_OPENDATA AS URL_descarga, "
    QUERY = QUERY + "NVL(IAES.MET_PRODUCTO.CODIGO_TEMA, IAES.MET_OPERACION.CODIGO_TEMA) || ' ' || NVL(IAES.MET_PRODUCTO.NOMBRE_TEMA, IAES.MET_OPERACION.NOMBRE_TEMA) AS Tema_estadistico,  "
    QUERY = QUERY + "IAES.MET_OPERACION.FUENTE AS Fuente, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_POP AS Poblacion_estadistica, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_UNIT AS Unidad_estadistica, "
    QUERY = QUERY + "IAES.MET_DATASET.UNIT_MEASURE AS Unidades_de_medida,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.BASE_PER AS Periodo_base, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.TIPO_OP AS Tipo_operacion, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.SOURCE_TYPE AS Tipologia_datos_origen, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.STAT_PROCESS AS Tratamiento_Estadistico, "
    QUERY = QUERY + "IAES.MET_OPERACION.LEGISLACION_UE AS Legislacion_UE, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.ETIQUETAS AS Etiquetas,  "
    QUERY = QUERY + "IAES.MET_PRODUCTO.CATEGORIA_OPENDATA AS Categoria, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_CRE_DATOS AS Fecha_creacion, "
    QUERY = QUERY + "IAES.MET_DATASET.FECHA_MOD_DATOS AS Fecha_modificacion,  "
    QUERY = QUERY + "IAES.MET_DATASET.IDIOMA AS Idioma, "
    QUERY = QUERY + "IAES.MET_DATASET.LICENCIA AS Licencia, "
    QUERY = QUERY + "IAES.MET_FICHEROS.FORMATO_FICHERO_OPENDATA AS Formato, "
    QUERY = QUERY + "IAES.MET_FICHEROS.FORMATO_ACCESO_FICHERO AS Formato_acceso, "
    QUERY = QUERY + "IAES.MET_PRODUCTO.FECHA_MOD_FICHA AS Fecha_cambio_metadatos "
    QUERY = QUERY + "FROM ((IAES.MET_FICHEROS RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_DATASET ON IAES.MET_FICHEROS.ID_DATASET=IAES.MET_DATASET.ID_DATASET) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_PRODUCTO ON IAES.MET_DATASET.ID_PRODUCTO=IAES.MET_PRODUCTO.ID_PRODUCTO) RIGHT JOIN  "
    QUERY = QUERY + "IAES.MET_OPERACION ON IAES.MET_PRODUCTO.ID_OPERACION=IAES.MET_OPERACION.ID_OPERACION "
    QUERY = QUERY + "WHERE IAES.MET_DATASET.INCLUIR_OPENDATA='SI' " #and IAES.MET_DATASET.ID_DATASET=502  "
    QUERY = QUERY + "AND IAES.MET_PRODUCTO.CATEGORIA_OPENDATA is not null "
    QUERY = QUERY + "AND IAES.MET_DATASET.NOMBRE_DS is not null "
    QUERY = QUERY + "AND IAES.MET_FICHEROS.NOMBRE_FICHERO_OPENDATA is not null "
    print QUERY
    registros = cursor.execute(QUERY)
    lista = []

    # Cabecera del Fichero RDF
    fichero_RDF = "<?xml version=\"1.0\" encoding=\"utf-8\"?> <rdf:RDF xmlns:foaf=\"http://xmlns.com/foaf/0.1/\" xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:dcat=\"http://www.w3.org/ns/dcat#\"\n"
    fichero_RDF = fichero_RDF + "  xmlns:dct=\"http://purl.org/dc/terms/\">\n\n"

    fichero = fichero_RDF

    for r in registros:
        delete = False
        lista.append(r)

        idDataset = r[0]
        Titulo = r[1]
        url_publicado = r[2]
        autor = r[3]
        email_autor = r[4]
        Descripcion = r[5]
        Spatial = r[6]
        Temporal_from = r[7]
        Temporal_to = r[8]
        Temporal_alternativo = r[9]
        Frecuencia = r[10]
        Calidad = r[11]
        URL_calidad = r[12]
        Notas_metodologicas = r[13]
        URL_metodologia = r[14]
        Nivel_Detalle = r[15]
        Titulo_descarga = r[16]
        URL_descarga = r[17]
        Tema_estadistico = r[18]
        Fuente = r[19]
        Poblacion_estadistica = r[20]
        Unidad_estadistica = r[21]
        Unidades_de_medida = r[22]
        Periodo_base = r[23]
        Tipo_operacion = r[24]
        Tipologia_datos_origen = r[25]
        Tratamiento_Estadistico = r[26]
        Legislacion_UE = r[27]
        Etiquetas = r[28]
        Categoria = r[29]
        Fe_creacion = r[30]
        Fe_modificacion = r[31]
        Idioma = r[32]
        Licencia = r[33]
        Formato = r[34]
        Formato_acceso = r[35]
        F_cambio_metadatos = r[36]
        
        

        Formato_difusion=""

        #Dependen de parametro "organizacion"
        organizacion = "Instituto Aragonés de Estadística"
        organizacionUrl = "http://www.aragon.es/iaest"

        #Dependen del parÃ¡metro "frecuencia"
        if Frecuencia != None:
            if Frecuencia == "Decenal":
                frecuenciaValue = "Decenal"
                frecuenciaLabel = "Decenal"
            elif Frecuencia == "Quinquenal":
                frecuenciaValue = "Quinquenal"
                frecuenciaLabel = "Quinquenal"
            elif Frecuencia == "Cuatrienal":
                frecuenciaValue = "Cada 4 años"
                frecuenciaLabel = "Cada 4 años"
            elif Frecuencia == "Bienal":
                frecuenciaValue = "Bienal"
                frecuenciaLabel = "Bienal"
            elif Frecuencia == "Anual":
                frecuenciaValue = "Anual"
                frecuenciaLabel = "Anual"
            elif Frecuencia == "Semestral":
                frecuenciaValue = "Semestral"
                frecuenciaLabel = "Semestral"
            elif Frecuencia == "Cuatrimestral":
                frecuenciaValue = "Cuatrimestral"
                frecuenciaLabel = "Cuatrimestral"
            elif Frecuencia == "Trimestral":
                frecuenciaValue = "Trimestral"
                frecuenciaLabel = "Trimestral"
            elif Frecuencia == "Bimestral":
                frecuenciaValue = "Bimestral"
                frecuenciaLabel = "Bimestral"
            elif Frecuencia == "Mensual":
                frecuenciaValue = "Mensual"
                frecuenciaLabel = "Mensual"
            elif Frecuencia == "Bimensual":
                frecuenciaValue = "Bimensual"
                frecuenciaLabel = "Bimensual"
            elif Frecuencia == "Quincenal":
                frecuenciaValue = "Quincenal"
                frecuenciaLabel = "Quincenal"
            elif Frecuencia == "Trimensual":
                frecuenciaValue = "Trimensual"
                frecuenciaLabel = "Trimensual"
            elif Frecuencia == "Semanal":
                frecuenciaValue = "Semanal"
                frecuenciaLabel = "Semanal"
            elif Frecuencia == "Bisemanal":
                frecuenciaValue = "Bisemanal"
                frecuenciaLabel = "Bisemanal"
            elif Frecuencia == "Trisemanal":
                frecuenciaValue = "Trisemanal"
                frecuenciaLabel = "Trisemanal"
            elif Frecuencia == "Diaria":
                frecuenciaValue = "Diaria"
                frecuenciaLabel = "Diaria"
            elif Frecuencia == "Horaria":
                frecuenciaValue = "Horaria"
                frecuenciaLabel = "Horaria"
            elif Frecuencia == "Instantánea":
                frecuenciaValue = "Instantánea"
                frecuenciaLabel = "Instantánea"
            else:#Desconocida
                frecuenciaValue = ""
                frecuenciaLabel = ""
        else:#Si no tiene lo ponemos como desconocida que es vacio
           frecuenciaValue = ""
           frecuenciaLabel = ""


        #Dependen del parÃ¡metro "tema"
        tema = Categoria.replace(";", "")
        temaId = tema.lower().replace(" ", "-").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "")
        temaId = temaId.replace("-y-","-")
        temaId = temaId.replace("-e-","-")
        temaDes = Categoria.replace(";", "")


        if Nivel_Detalle != None:
            detalle = Nivel_Detalle
        else:
            detalle = ""

        if Notas_metodologicas != None:
            diccionario = Notas_metodologicas.strip()
        else:
            diccionario = ""
            
        if URL_metodologia != None:
            url_diccionario = URL_metodologia.strip()
        else:
            url_diccionario = ""

        if Calidad != None:
            calidad = Calidad.strip()
        else:
            calidad = ""
            
        if URL_calidad != None:
            url_calidad = URL_calidad.strip()
        else:
            url_calidad = ""

        if Idioma != None:
            idioma = Idioma.strip()
        else:
            idioma = ""

        if Licencia != None:
            licencia = Licencia.strip()
        else:
            licencia = ""

        if Fe_modificacion != None:
            fe_modificacion = Fe_modificacion
        else:
            fe_modificacion = ""

        if Fe_creacion != None:
            f_creacion = Fe_creacion
        else:
            f_creacion = ""
#        Si no tien titulo de descarga le ponemos el del dataset
        if Titulo_descarga!= None:
            titulo_descarga = Titulo_descarga
        else:
            titulo_descarga=Titulo


        #// Tipo ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
        formato = Formato
        formato_acceso = Formato_acceso
        identificador = ""
        #// ID = Descripcion + nombre de archivo (sin tildes, espacios o signos de puntuación)
        if url_publicado !=None and url_publicado !="":
            if url_publicado.startswith("--"):
                url_publicado = url_publicado.lower().split("--")[1]
                delete =True
            identificador = url_publicado
            identificador = identificador.replace("ü", "u").replace("Ü", "u")
        else:
            identificador = Titulo.decode('utf-8').encode('utf-8')
            identificador = identificador.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
            identificador = identificador.replace( "ú", "u").replace("%","")
            identificador = identificador.strip().lower().replace(":", "-").replace(")", "").replace(",", "").replace("'","")
            identificador = identificador.replace("(","").replace(".", "").replace(" ", "-")
            identificador = identificador.replace("--", "-").replace("ñ","ny").replace("Á","a").replace("É","e").replace("Í","i").replace("Ó","o").replace("º","")

        #// Se obtenian de la descripcion. Ahora tienen su propio campo
        if Etiquetas == None:
            tags = " "
        else:
            Etiquetas = Etiquetas.replace(";", ",")
            tags = Etiquetas.split(",")

        if URL_descarga == None:
            URL_descarga =" "

        aboutUrl = URL_descarga
        aboutUrl = aboutUrl.replace("&", "&amp;")
        title = Titulo
        description = Descripcion

        # Quitar los que no son solo zip y terminan en _d16 de COMARCA
        #if (!esquemas[r].equalsIgnoreCase("comarca") || (esquemas[r].equalsIgnoreCase("comarca") && (!identificador.endsWith("_d16") & & formato.equalsIgnoreCase(".zip"))))        {
        nombres = ""
        nombres = nombres + identificador + ".rdf\n"

        #fichero = fichero_RDF
        fichero = fichero + "\t<dcat:Dataset rdf:about=\"" + aboutUrl + "\">\n"
        fichero = fichero + "\t\t<dct:identifier>" + identificador[0:197]
        fichero = fichero + "</dct:identifier>\n" + "\t\t<dct:description>"
        fichero = fichero + description + "</dct:description>\n"

        for elemento in tags:
            if len(elemento) > 3:
                fichero = fichero + "\t\t<dcat:keyword xml:lang=\"es\">" + elemento.strip() + "</dcat:keyword>\n"


        # Fin del FOR
        fichero = fichero + "\t\t<dct:title>" + title + "</dct:title>\n"
        #fichero = fichero + "\t\t<dct:organization>" + "iaest" + "</dct:organization>\n"
        fichero = fichero + "\t\t<dct:modified>" + str(fe_modificacion) + "</dct:modified>\n"
        fichero = fichero + "\t\t<dct:organization>instituto_aragones_de_estadistica</dct:organization>\n"
        fichero = fichero + "\t\t<dct:issued>" + str(f_creacion) + "</dct:issued>\n"

        #// Publicador
        fichero = fichero + "\t\t<dcat:author_email>" + str(email_autor) + "</dcat:author_email>\n"
        fichero = fichero + "\t\t<dct:publisher>\n"
        fichero = fichero + "\t\t\t<foaf:Organization>\n" + "\t\t\t\t<dct:title>"
        fichero = fichero + organizacion + "</dct:title>\n"
        fichero = fichero + "\t\t\t\t<foaf:homepage rdf:resource=\""
        fichero = fichero + organizacionUrl + "\"/>\n"
        fichero = fichero + "\t\t\t</foaf:Organization>\n" + "\t\t</dct:publisher>\n"
        #// Periodicidad
        fichero = fichero + "\t\t<dct:accrualPeriodicity>\n"
        fichero = fichero + "\t\t\t<dct:Frequency>\n" + "\t\t\t\t<rdf:value>"
        fichero = fichero + frecuenciaValue + "</rdf:value>\n"
        fichero = fichero + "\t\t\t\t<rdfs:label>" + frecuenciaLabel
        fichero = fichero + "</rdfs:label>\n" + "\t\t\t</dct:Frequency>\n"
        fichero = fichero + "\t\t</dct:accrualPeriodicity>\n"
        if detalle == "0":
            detalle = ""
        else:
            detalle = detalle
        if Spatial == None:
            Spatial = ""
#        if Temporal == None:
#            Temporal = ""
        if Temporal_from == None:
            Temporal_from=""
        if Temporal_to == None:
            Temporal_to=""
        if Temporal_alternativo == None:
            Temporal_alternativo=""
            
        if idioma == None:
            idioma=""
        if licencia == None:
            licencia = ""
        if detalle == None:
            detalle = ""
        if calidad == None:
            calidad = ""
        if url_calidad == None:
            url_calidad = ""
        if diccionario == None:
            diccionario=""
        if url_diccionario == None:
            url_diccionario=""

        #forzamos a que elimine los datasets con formato pdf
        if formato != None and formato == 'pdf':
            delete = True
        #forzamos a que elimine los datasets con formato pdf
        if formato_acceso != None and formato_acceso == 'pdf':
            delete = True
        diccionario = diccionario.replace("&","&amp;")
        url_diccionario = url_diccionario.replace("&","&amp;")

#        fichero = fichero + "\t\t<dct:spatial>" + str(Spatial) + "</dct:spatial>\n"
        
#        fichero = fichero + "\t\t<dct:temporal>" + str(Temporal) + "</dct:temporal>\n"
        fichero = fichero + "\t\t<dct:temporalFrom>" + transformaTemporal(Temporal_from) + "</dct:temporalFrom>\n"
        fichero = fichero + "\t\t<dct:temporalUntil>" + transformaTemporal(Temporal_to) + "</dct:temporalUntil>\n"
        

        
        fichero = fichero + "\t\t<dct:language>" + str(idioma).upper() + "</dct:language>\n"
        fichero = fichero + "\t\t<dct:license rdf:resource=\"" + str(licencia) + "\"></dct:license>\n"
        fichero = fichero + "\t\t<dcat:granularity>" + str(detalle) + "</dcat:granularity>\n"
        if ((str(calidad)=="") &&(str(url_calidad)!="")):
          fichero = fichero + "\t\t<dcat:dataQuality>La calidad de datos se encuentra en la siguiente url</dcat:dataQuality>\n"
        else:
          fichero = fichero + "\t\t<dcat:dataQuality>" + str(calidad) + "</dcat:dataQuality>\n"
        fichero = fichero + "\t\t<dcat:urlQuality>" + str(url_calidad) + "</dcat:urlQuality>\n"
        if ((str(diccionario)=="") &&(str(url_diccionario)!="")):
          fichero = fichero + "\t\t<dcat:dataDictionary>El diccionario del dato se encuentra en la siguiente url</dcat:dataDictionary>\n";
        else:
          fichero = fichero + "\t\t<dcat:dataDictionary>" + str(diccionario) + "</dcat:dataDictionary>\n"
        fichero = fichero + "\t\t<dcat:urlDictionary>" + str(url_diccionario) + "</dcat:urlDictionary>\n"
        
        #Aragopedia
        enlacesAragopegia= getEnlaceAragopedia(str(Spatial))
        fichero = fichero + "\t\t<dcat:name_aragopedia>"+enlacesAragopegia[0]+"</dcat:name_aragopedia>\n"
        fichero = fichero + "\t\t<dcat:short_uri_aragopedia>"+enlacesAragopegia[1]+"</dcat:short_uri_aragopedia>\n"
        fichero = fichero + "\t\t<dcat:type_aragopedia>"+enlacesAragopegia[2]+"</dcat:type_aragopedia>\n"
        fichero = fichero + "\t\t<dcat:uri_aragopedia>"+enlacesAragopegia[3]+"</dcat:uri_aragopedia>\n"
        
        
        fichero = fichero + "\t\t<dct:status>" + str(delete) + "</dct:status>\n"


        if Tema_estadistico == None:
            Tema_estadistico =""
        if Unidad_estadistica == None:
            Unidad_estadistica =""
        if Poblacion_estadistica == None:
            Poblacion_estadistica =""
        if Unidades_de_medida == None:
            Unidades_de_medida =""

        if Spatial == None:
            Spatial = ""
        if Periodo_base == None:
            Periodo_base =""
        if Tipo_operacion == None:
            Tipo_operacion =""
        if Tipologia_datos_origen == None:
            Tipologia_datos_origen =""
        if Fuente == None:
            Fuente =""
        if Tratamiento_Estadistico == None:
            Tratamiento_Estadistico =""
        if Formato_difusion == None:
            Formato_difusion =""

        if Legislacion_UE == None:
            Legislacion_UE =""

        fichero = fichero + "\t\t<dcat:tema_estadistico>" + Tema_estadistico.strip() + "</dcat:tema_estadistico>\n"
        fichero = fichero + "\t\t<dcat:unidad_estadistica>" + Unidad_estadistica.strip() + "</dcat:unidad_estadistica>\n"
        fichero = fichero + "\t\t<dcat:poblacion_estadistica>" + Poblacion_estadistica.strip() + "</dcat:poblacion_estadistica>\n"
        fichero = fichero + "\t\t<dcat:unidad_medida>" + Unidades_de_medida.strip() + "</dcat:unidad_medida>\n"
        fichero = fichero + "\t\t<dcat:periodo_base>" + Periodo_base.strip() + "</dcat:periodo_base>\n"
        fichero = fichero + "\t\t<dcat:tipo_operacion>" + Tipo_operacion.strip() + "</dcat:tipo_operacion>\n"
        fichero = fichero + "\t\t<dcat:tipologia_datos_origen>" + Tipologia_datos_origen.strip() + "</dcat:tipologia_datos_origen>\n"
        fichero = fichero + "\t\t<dcat:fuente>" + Fuente.strip() + "</dcat:fuente>\n"
        fichero = fichero + "\t\t<dcat:tratamiento_estadistico>" + Tratamiento_Estadistico.strip() + "</dcat:tratamiento_estadistico>\n"
        fichero = fichero + "\t\t<dcat:formatos_difusion>" + Formato_difusion.strip() + "</dcat:formatos_difusion>\n"
        fichero = fichero + "\t\t<dcat:legislacion_ue>" + Legislacion_UE.strip().replace('&','$amp;').replace('<','&lt;').replace('>','&gt;') + "</dcat:legislacion_ue>\n"
        fichero = fichero + "\t\t<dcat:theme>\n"
        fichero = fichero + "\t\t\t<rdf:Description>\n" + "\t\t\t\t<rdfs:label>"
        fichero = fichero + tema + "</rdfs:label>\n" + "\t\t\t\t<dct:identifier>"
        fichero = fichero + temaId + "</dct:identifier>\n"
        fichero = fichero + "\t\t\t\t<dct:description>" + temaDes
        fichero = fichero + "</dct:description>\n" + "\t\t\t</rdf:Description>\n"
        fichero = fichero + "\t\t</dcat:theme>\n"

        accessURL = URL_descarga
        formatoValue = ""
        esPDF = 0
        if formato != None:
            if formato == "pdf":
                formatoValue = "application/pdf"
                esPDF = 1

            if formato == "shp.zip":
                formatoValue = "application/zip"

            if formato == "dwg.zip":
                formatoValue = "application/zip"

            if formato == "xml":
                formatoValue = "application/xml"

            if formato == "gml.zip":
                formatoValue = "application/zip"

            if formato == "kmz":
                formatoValue = "application/vnd.google-earth.kmz"

            if formato == "dxf.zip":
                formatoValue = "application/zip"


        if title == None:
            title = ""
        if description == None:
            description = ""
        if accessURL == None:
            accessURL = ""

        if formatoValue == None:
            formatoValue = ""
        if formato == None:
            formato = ""

        if (esPDF == 0):
            fichero = fichero + "\t\t<dcat:distribution>\n"
            fichero = fichero + "\t\t\t<dcat:Distribution>\n"
            fichero = fichero + "\t\t\t\t<dct:title>" +titulo_descarga+"</dct:title>\n"
#            fichero = fichero + "\t\t\t\t<rdfs:label>" + title + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t<dct:description>" + description + "</dct:description>\n"
            fichero = fichero + "\t\t\t\t<rdf:type rdf:resource=\"http://vocab.deri.ie/dcat#Download\"/>\n"
            fichero = fichero + "\t\t\t\t<dcat:accessURL rdf:resource=\"" + accessURL.replace("&","&amp;") + "\"></dcat:accessURL>\n"
            fichero = fichero + "\t\t\t\t<dcat:size>\n"
            fichero = fichero + "\t\t\t\t\t<rdf:Description>\n"
            fichero = fichero + "\t\t\t\t\t\t<dcat:bytes>"
            fichero = fichero + "</dcat:bytes>\n" + "\t\t\t\t\t\t <rdfs:label>"
            fichero = fichero + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t\t</rdf:Description>\n"
            fichero = fichero + "\t\t\t\t</dcat:size>\n"
            fichero = fichero + "\t\t\t\t<dct:format>\n"
            fichero = fichero + "\t\t\t\t\t<dct:IMT>\n"
            if (formato_acceso!=None):
                fichero = fichero + "\t\t\t\t\t\t<rdf:value>" + formato_acceso.upper() + "</rdf:value>\n"
#            fichero = fichero + "\t\t\t\t\t\t<rdf:value>" + formatoValue + "</rdf:value>\n"
            fichero = fichero + "\t\t\t\t\t\t<rdfs:label>" + formato + "</rdfs:label>\n"
            fichero = fichero + "\t\t\t\t\t</dct:IMT>\n"
            fichero = fichero + "\t\t\t\t</dct:format>\n"
            fichero = fichero + "\t\t\t</dcat:Distribution>\n"
            fichero = fichero + "\t\t</dcat:distribution>\n"

        fichero = fichero + "\t</dcat:Dataset>\n"

        if (url_publicado == None or url_publicado == ""):
            updateCursor = connection.cursor()
            UPDATEQUERY = "UPDATE IAES.MET_DATASET SET URL_OPENDATA_PUBLICADO='" + str(identificador) + "' WHERE NOMBRE_DS= '" + r[1].replace("'","''") + "'"
            updateCursor.execute(UPDATEQUERY)
            connection.commit()
            updateCursor.close()

    fichero = fichero + "</rdf:RDF>\n"
    print fichero
    cursor.close()
    connection.close()

    # Copiar contenido a un fichero
    f = open(config.DOWNLOAD_PATH + "/downloadIaest.rdf","w")
    f.write(fichero)
    f.close()
    return fichero

main()
