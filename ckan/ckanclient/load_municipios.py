#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import glob
import xml.etree.ElementTree as ET
import rdf_parser

def get_rdfs2():
    rdfs = []
    for rdf in glob.glob(config.DOWNLOAD_PATH + "/datosPignatelli_municipio.rdf"):
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

def quitarParentesis(municipio):
        if " (" in municipio:
            splitres = municipio.split(" (");
            municipioReturn = splitres[1].split(")")[0] + " " + splitres[0];
            return municipioReturn
        else:
            return municipio

def main():
    rdftotal = ""
    rdftotal = rdftotal  + '<?xml version="1.0" encoding="utf-8"?>'
    rdftotal = rdftotal  + '<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:owl="http://www.w3.org/2002/07/owl#"'
    rdftotal = rdftotal  + '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"'
    rdftotal = rdftotal  + '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"'
    rdftotal = rdftotal  + '  xmlns:dcat="http://www.w3.org/ns/dcat#"'
    rdftotal = rdftotal  + '  xmlns:dct="http://purl.org/dc/terms/">'


    listado_municipios =['Ababuj', 'Abanto', 'Abejuela', 'Abiego', 'Abizanda', 'Acered', 'Adahuesca', 'Agón', 'Aguarón', 'Aguatón', 'Aguaviva', 'Agüero', 'Aguilar del Alfambra', 'Aguilón', 'Aínsa-Sobrarbe', 'Ainzón', 'Aísa', 'Alacón', 'Aladrén', 'Alagón', 'Alarba', 'Alba', 'Albalate de Cinca', 'Albalate del Arzobispo', 'Albalatillo', 'Albarracín', 'Albelda', 'Albentosa', 'Alberite de San Juan', 'Albero Alto', 'Albero Bajo', 'Alberuela de Tubo', 'Albeta', 'Alborge', 'Alcaine', 'Alcalá de Ebro', 'Alcalá de Gurrea', 'Alcalá de la Selva', 'Alcalá de Moncayo', 'Alcalá del Obispo', 'Alcampell', 'Alcañiz', 'Alcolea de Cinca', 'Alconchel de Ariza', 'Alcorisa', 'Alcubierre', 'Aldehuela de Liestos', 'Alerre', 'Alfajarín', 'Alfambra', 'Alfamén', 'Alfántega', 'Alforque', 'Alhama de Aragón', 'Aliaga', 'Allepuz', 'Alloza', 'Allueva', 'Almochuel', 'Almohaja', 'Almolda (La)', 'Almonacid de la Cuba', 'Almonacid de la Sierra', 'Almudévar', 'Almunia de Doña Godina (La)', 'Almunia de San Juan', 'Almuniente', 'Alobras', 'Alpartir', 'Alpeñés', 'Alquézar', 'Altorricón', 'Ambel', 'Anadón', 'Andorra', 'Anento', 'Angüés', 'Aniñón', 'Añón de Moncayo', 'Ansó', 'Antillón', 'Aragüés del Puerto', 'Aranda de Moncayo', 'Arándiga', 'Arcos de las Salinas', 'Ardisa', 'Arén', 'Arens de Lledó', 'Argavieso', 'Argente', 'Arguis', 'Ariño', 'Ariza', 'Artieda', 'Asín', 'Atea', 'Ateca', 'Ayerbe', 'Azaila', 'Azanuy-Alins', 'Azara', 'Azlor', 'Azuara', 'Bádenas', 'Badules', 'Baells', 'Báguena', 'Bagüés', 'Bailo', 'Balconchán', 'Baldellou', 'Ballobar', 'Banastás', 'Bañón', 'Barbastro', 'Bárboles', 'Barbués', 'Barbuñales', 'Bárcabo', 'Bardallur', 'Barrachina', 'Bea', 'Beceite', 'Belchite', 'Bello', 'Belmonte de Gracián', 'Belmonte de San José', 'Belver de Cinca', 'Benabarre', 'Benasque', 'Beranuy', 'Berbegal', 'Berdejo', 'Berge', 'Berrueco', 'Bezas', 'Biel', 'Bielsa', 'Bierge', 'Biescas', 'Bijuesca', 'Binaced', 'Binéfar', 'Biota', 'Bisaurri', 'Biscarrués', 'Bisimbre', 'Blancas', 'Blecua y Torres', 'Blesa', 'Boltaña', 'Bonansa', 'Boquiñeni', 'Borau', 'Bordalba', 'Bordón', 'Borja', 'Botorrita', 'Brea de Aragón', 'Bronchales', 'Broto', 'Bubierca', 'Bueña', 'Bujaraloz', 'Bulbuente', 'Burbáguena', 'Bureta', 'Burgo de Ebro (El)', 'Buste (El)', 'Cabañas de Ebro', 'Cabolafuente', 'Cabra de Mora', 'Cadrete', 'Calaceite', 'Calamocha', 'Calanda', 'Calatayud', 'Calatorao', 'Calcena', 'Caldearenas', 'Calmarza', 'Calomarde', 'Camañas', 'Camarena de la Sierra', 'Camarillas', 'Caminreal', 'Campillo de Aragón', 'Campo', 'Camporrells', 'Cañada de Benatanduz', 'Cañada de Verich (La)', 'Cañada Vellida', 'Canal de Berdún', 'Candasnos', 'Canfranc', 'Cañizar del Olivar', 'Cantavieja', 'Capdesaso', 'Capella', 'Carenas', 'Cariñena', 'Casbas de Huesca', 'Cascante del Río', 'Caspe', 'Castejón de Alarba', 'Castejón de las Armas', 'Castejón de Monegros', 'Castejón de Sos', 'Castejón de Tornos', 'Castejón de Valdejasa', 'Castejón del Puente', 'Castel de Cabra', 'Castelflorite', 'Castellar (El)', 'Castellote', 'Castelnou', 'Castelserás', 'Castiello de Jaca', 'Castigaleu', 'Castiliscar', 'Castillazuelo', 'Castillonroy', 'Cedrillas', 'Celadas', 'Cella', 'Cerollera (La)', 'Cervera de la Cañada', 'Cerveruela', 'Cetina', 'Chalamera', 'Chía', 'Chimillas', 'Chiprana', 'Chodes', 'Cimballa', 'Cinco Olivas', 'Clarés de Ribota', 'Codo', 'Codoñera (La)', 'Codos', 'Colungo', 'Contamina', 'Corbalán', 'Cortes de Aragón', 'Cosa', 'Cosuenda', 'Cretas', 'Crivillén', 'Cuarte de Huerva', 'Cuba (La)', 'Cubel', 'Cubla', 'Cucalón', 'Cuerlas (Las)', 'Cuervo (El)', 'Cuevas de Almudén', 'Cuevas Labradas', 'Daroca', 'Ejea de los Caballeros', 'Ejulve', 'Embid de Ariza', 'Encinacorba', 'Épila', 'Erla', 'Escatrón', 'Escorihuela', 'Escucha', 'Esplús', 'Estada', 'Estadilla', 'Estercuel', 'Estopiñán del Castillo', 'Fabara', 'Fago', 'Fanlo', 'Farlete', 'Fayón', 'Fayos (Los)', 'Ferreruela de Huerva', 'Figueruelas', 'Fiscal', 'Fombuena', 'Fonfría', 'Fonz', 'Foradada del Toscar', 'Formiche Alto', 'Fórnoles', 'Fortanete', 'Foz-Calanda', 'Fraga', 'Frago (El)', 'Frasno (El)', 'Fréscano', 'Fresneda (La)', 'Frías de Albarracín', 'Fuendejalón', 'Fuendetodos', 'Fuenferrada', 'Fuentes Calientes', 'Fuentes Claras', 'Fuentes de Ebro', 'Fuentes de Jiloca', 'Fuentes de Rubielos', 'Fuentespalda', 'Fueva (La)', 'Gallocanta', 'Gallur', 'Galve', 'Gargallo', 'Gea de Albarracín', 'Gelsa', 'Ginebrosa (La)', 'Gistaín', 'Godojos', 'Gotor', 'Grado (El)', 'Grañén', 'Graus', 'Griegos', 'Grisel', 'Grisén', 'Guadalaviar', 'Gúdar', 'Gurrea de Gállego', 'Herrera de los Navarros', 'Híjar', 'Hinojosa de Jarque', 'Hoz de Jaca', 'Hoz de la Vieja (La)', 'Hoz y Costeán', 'Huerto', 'Huesa del Común', 'Huesca', 'Ibdes', 'Ibieca', 'Iglesuela del Cid (La)', 'Igriés', 'Ilche', 'Illueca', 'Isábena', 'Isuerre', 'Jabaloyas', 'Jaca', 'Jaraba', 'Jarque', 'Jarque de la Val', 'Jasa', 'Jatiel', 'Jaulín', 'Jorcas', 'Josa', 'Joyosa (La)', 'Labuerda', 'Lagata', 'Lagueruela', 'Laluenga', 'Lalueza', 'Lanaja', 'Langa del Castillo', 'Lanzuela', 'Laperdiguera', 'Lascellas-Ponzano', 'Lascuarre', 'Laspaúles', 'Laspuña', 'Layana', 'Lécera', 'Lechón', 'Leciñena', 'Letux', 'Libros', 'Lidón', 'Linares de Mora', 'Litago', 'Lituénigo', 'Lledó', 'Loarre', 'Lobera de Onsella', 'Longares', 'Longás', 'Loporzano', 'Loscorrales', 'Loscos', 'Lucena de Jalón', 'Luceni', 'Luesia', 'Luesma', 'Lumpiaque', 'Luna', 'Lupiñén-Ortilla', 'Maella', 'Magallón', 'Maicas', 'Mainar', 'Malanquilla', 'Maleján', 'Mallén', 'Malón', 'Maluenda', 'Manchones', 'Manzanera', 'Mara', 'María de Huerva', 'Marracos', 'Martín del Río', 'Mas de las Matas', 'Mata de los Olmos (La)', 'Mazaleón', 'Mediana de Aragón', 'Mequinenza', 'Mesones de Isuela', 'Mezalocha', 'Mezquita de Jarque', 'Mianos', 'Miedes de Aragón', 'Mirambel', 'Miravete de la Sierra', 'Molinos', 'Monegrillo', 'Monesma y Cajigar', 'Moneva', 'Monflorite-Lascasas', 'Monforte de Moyuela', 'Monreal de Ariza', 'Monreal del Campo', 'Monroyo', 'Montalbán', 'Montanuy', 'Monteagudo del Castillo', 'Monterde', 'Monterde de Albarracín', 'Montón', 'Monzón', 'Mora de Rubielos', 'Morata de Jalón', 'Morata de Jiloca', 'Morés', 'Moros', 'Moscardón', 'Mosqueruela', 'Moyuela', 'Mozota', 'Muel', 'Muela (La)', 'Munébrega', 'Muniesa', 'Murero', 'Murillo de Gállego', 'Naval', 'Navardún', 'Nigüella', 'Noguera de Albarracín', 'Nogueras', 'Nogueruelas', 'Nombrevilla', 'Nonaspe', 'Novales', 'Novallas', 'Novillas', 'Nueno', 'Nuévalos', 'Nuez de Ebro', 'Obón', 'Odón', 'Ojos Negros', 'Olba', 'Oliete', 'Olmos (Los)', 'Olvena', 'Olvés', 'Ontiñena', 'Orcajo', 'Orera', 'Orés', 'Orihuela del Tremedal', 'Orrios', 'Oseja', 'Osera de Ebro', 'Osso de Cinca', 'Palo', 'Palomar de Arroyos', 'Pancrudo', 'Paniza', 'Panticosa', 'Paracuellos de Jiloca', 'Paracuellos de la Ribera', 'Parras de Castellote (Las)', 'Pastriz', 'Pedrola', 'Pedrosas (Las)', 'Peñalba', 'Peñarroya de Tastavins', 'Peñas de Riglos (Las)', 'Peracense', 'Peralejos', 'Perales del Alfambra', 'Peralta de Alcofea', 'Peralta de Calasanz', 'Peraltilla', 'Perarrúa', 'Perdiguera', 'Pertusa', 'Piedratajada', 'Pina de Ebro', 'Pinseque', 'Pintanos (Los)', 'Piracés', 'Pitarque', 'Plan', 'Plasencia de Jalón', 'Pleitas', 'Plenas', 'Plou', 'Pobo (El)', 'Poleñino', 'Pomer', 'Portellada (La)', 'Pozán de Vero', 'Pozondón', 'Pozuel de Ariza', 'Pozuel del Campo', 'Pozuelo de Aragón', 'Pradilla de Ebro', 'Puebla de Albortón', 'Puebla de Alfindén (La)', 'Puebla de Castro (La)', 'Puebla de Híjar (La)', 'Puebla de Valverde (La)', 'Puendeluna', 'Puente de Montañana', 'Puente la Reina de Jaca', 'Puértolas', 'Puertomingalvo', 'Pueyo de Araguás (El)', 'Pueyo de Santa Cruz', 'Purujosa', 'Quicena', 'Quinto', 'Ráfales', 'Remolinos', 'Retascón', 'Ricla', 'Rillo', 'Riodeva', 'Robres', 'Ródenas', 'Romanos', 'Royuela', 'Rubiales', 'Rubielos de la Cérida', 'Rubielos de Mora', 'Rueda de Jalón', 'Ruesca', 'Sabiñánigo', 'Sádaba', 'Sahún', 'Salas Altas', 'Salas Bajas', 'Salcedillo', 'Saldón', 'Salillas', 'Salillas de Jalón', 'Sallent de Gállego', 'Salvatierra de Esca', 'Samper de Calanda', 'Samper del Salz', 'San Agustín', 'San Esteban de Litera', 'San Juan de Plan', 'San Martín de la Virgen de Moncayo', 'San Martín del Río', 'San Mateo de Gállego', 'San Miguel del Cinca', 'Sangarrén', 'Santa Cilia', 'Santa Cruz de Grío', 'Santa Cruz de la Serós', 'Santa Cruz de Moncayo', 'Santa Cruz de Nogueras', 'Santa Eulalia', 'Santa Eulalia de Gállego', 'Santa María de Dulcis', 'Santaliestra y San Quílez', 'Santed', 'Sariñena', 'Sarrión', 'Sástago', 'Saviñán', 'Secastilla', 'Sediles', 'Segura de los Baños', 'Seira', 'Sena', 'Senés de Alcubierre', 'Seno', 'Sesa', 'Sestrica', 'Sesué', 'Sierra de Luna', 'Siétamo', 'Sigüés', 'Singra', 'Sisamón', 'Sobradiel', 'Sopeira', 'Sos del Rey Católico', 'Sotonera (La)', 'Tabuenca', 'Talamantes', 'Tamarite de Litera', 'Tarazona', 'Tardienta', 'Tauste', 'Tella-Sin', 'Terrer', 'Terriente', 'Teruel', 'Tierga', 'Tierz', 'Tobed', 'Tolva', 'Toril y Masegoso', 'Torla-Ordesa', 'Tormón', 'Tornos', 'Torralba de Aragón', 'Torralba de los Frailes', 'Torralba de los Sisones', 'Torralba de Ribota', 'Torralbilla', 'Torre de Arcas', 'Torre de las Arcas', 'Torre del Compte', 'Torre la Ribera', 'Torre los Negros', 'Torrecilla de Alcañiz', 'Torrecilla del Rebollar', 'Torrehermosa', 'Torrelacárcel', 'Torrelapaja', 'Torrellas', 'Torremocha de Jiloca', 'Torrente de Cinca', 'Torres de Albarracín', 'Torres de Alcanadre', 'Torres de Barbués', 'Torres de Berrellén', 'Torrevelilla', 'Torrijas', 'Torrijo de la Cañada', 'Torrijo del Campo', 'Tosos', 'Tramacastiel', 'Tramacastilla', 'Tramaced', 'Trasmoz', 'Trasobares', 'Tronchón', 'Uncastillo', 'Undués de Lerda', 'Urrea de Gaén', 'Urrea de Jalón', 'Urriés', 'Used', 'Utebo', 'Utrillas', 'Val de San Martín', 'Valacloche', 'Valbona', 'Valdealgorfa', 'Valdecuenca', 'Valdehorna', 'Valdelinares', 'Valdeltormo', 'Valderrobres', 'Valfarta', 'Valjunquera', 'Valle de Bardají', 'Valle de Hecho', 'Valle de Lierp', 'Vallecillo (El)', 'Valmadrid', 'Valpalmas', 'Valtorres', 'Veguillas de la Sierra', 'Velilla de Cinca', 'Velilla de Ebro', 'Velilla de Jiloca', 'Vencillón', 'Vera de Moncayo', 'Viacamp y Litera', 'Vicién', 'Vierlas', 'Villadoz', 'Villafeliche', 'Villafranca de Ebro', 'Villafranca del Campo', 'Villahermosa del Campo', 'Villalba de Perejil', 'Villalengua', 'Villamayor de Gállego', 'Villanova', 'Villanúa', 'Villanueva de Gállego', 'Villanueva de Huerva', 'Villanueva de Jiloca', 'Villanueva de Sigena', 'Villanueva del Rebollar de la Sierra', 'Villar de los Navarros', 'Villar del Cobo', 'Villar del Salz', 'Villarluengo', 'Villarquemado', 'Villarreal de Huerva', 'Villarroya de la Sierra', 'Villarroya de los Pinares', 'Villarroya del Campo', 'Villastar', 'Villel', 'Vilueña (La)', 'Vinaceite', 'Visiedo', 'Vistabella', 'Vivel del Río Martín', 'Yebra de Basa', 'Yésero', 'Zaida (La)', 'Zaidín', 'Zaragoza', 'Zoma (La)', 'Zuera']

    print ("hay: " + str(len(listado_municipios)))
    
    index = 0
    

    for municipio in listado_municipios:
        print(municipio)
        rdftotal = rdftotal  + '	<dcat:Dataset rdf:about="http://opendata.aragon.es/aragopedia">\n'
        rdftotal = rdftotal  + '		<dct:identifier>datos-municipio-' + municipio.lower().replace('É', 'e').replace('(','').replace(')','').replace('ü','u').replace(" ", "-").replace('Ñ', 'n').replace('ñ', 'n').replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "") + '</dct:identifier>\n'
        rdftotal = rdftotal  + '		<dct:description>AragoPedia es una iniciativa de la Dirección General de Administración Electrónica y Sociedad de la Información para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos del municipio de ' + quitarParentesis(municipio) + '</dct:description>\n'

        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragón</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Demografía</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Nuevas tecnologías</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragopedia</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Municipio</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Ayuntamiento</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Local</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">' + quitarParentesis(municipio) + '</dcat:keyword>\n'

        rdftotal = rdftotal  + '<dct:title>Municipio: ' + quitarParentesis(municipio) +'</dct:title>\n'
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
        rdftotal = rdftotal  + '		<dct:spatial>' + quitarParentesis(municipio) +'</dct:spatial>\n'
        rdftotal = rdftotal  + '		<dct:temporalFrom>2000-01-01</dct:temporalFrom>\n'
        rdftotal = rdftotal  + '		<dct:language>ES</dct:language>\n'
        rdftotal = rdftotal  + '		<dct:license rdf:resource="http://www.opendefinition.org/licenses/cc-by"></dct:license>\n'
        rdftotal = rdftotal  + '		<dcat:granularity>Municipio</dcat:granularity>\n'
        rdftotal = rdftotal  + '		<dcat:dataQuality></dcat:dataQuality>\n'
        rdftotal = rdftotal  + '		<dcat:dataDictionary></dcat:dataDictionary>\n'
        #Se añade lo correspondiente a la aragopedia
        rdftotal = rdftotal  + '		<dcat:name_aragopedia>'+ quitarParentesis(municipio) + '</dcat:name_aragopedia>\n'
        index=index+1
        rdftotal = rdftotal  + '		<dcat:short_uri_aragopedia>'+ municipio.replace(" ", "_")+ '</dcat:short_uri_aragopedia>\n'
        rdftotal = rdftotal  + '		<dcat:type_aragopedia>Municipio</dcat:type_aragopedia>\n'
        rdftotal = rdftotal  + '		<dcat:uri_aragopedia>http://opendata.aragon.es/recurso/territorio/Municipio/'+ municipio.replace(" ", "_")+ '</dcat:uri_aragopedia>\n'
        
        rdftotal = rdftotal  + '		<dcat:theme>\n'
        rdftotal = rdftotal  + '			<rdf:Description>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Demografía</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:identifier>demografia</dct:identifier>\n'
        rdftotal = rdftotal  + '				<dct:description>Demografía</dct:description>\n'
        rdftotal = rdftotal  + '			</rdf:Description>\n'
        rdftotal = rdftotal  + '		</dcat:theme>\n'
        rdftotal = rdftotal  + '		<dcat:distribution>\n'
        rdftotal = rdftotal  + '			<dcat:Distribution>\n'
        rdftotal = rdftotal  + '				<rdfs:label>' + quitarParentesis(municipio) + '</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:description>AragoPedia es una iniciativa de la Dirección General de Administración Electrónica y Sociedad de la Información para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos del municipio de ' + quitarParentesis(municipio) + '</dct:description>\n'
        rdftotal = rdftotal  + '				<rdf:type rdf:resource="http://vocab.deri.ie/dcat#Download"/>\n'
        rdftotal = rdftotal  + '<dcat:accessURL rdf:resource="http://opendata.aragon.es/recurso/territorio/Municipio/' + municipio.replace(' ','_') +'?api_key=e103dc13eb276ad734e680f5855f20c6&amp;_view=completa"></dcat:accessURL>\n'
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
    f = open(config.DOWNLOAD_PATH + "/datosPignatelli_municipio.rdf","w")
    f.write(rdftotal)
    f.close()

    print(parse_rdfs2())

main()

