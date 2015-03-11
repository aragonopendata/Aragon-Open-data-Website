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

def main():
    rdftotal = ""
    rdftotal = rdftotal  + '<?xml version="1.0" encoding="utf-8"?>'
    rdftotal = rdftotal  + '<rdf:RDF xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:owl="http://www.w3.org/2002/07/owl#"'
    rdftotal = rdftotal  + '  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"'
    rdftotal = rdftotal  + '  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"'
    rdftotal = rdftotal  + '  xmlns:dcat="http://www.w3.org/ns/dcat#"'
    rdftotal = rdftotal  + '  xmlns:dct="http://purl.org/dc/terms/">'


    listado_municipios ={'Abiego', 'Abizanda', 'Adahuesca', 'Agüero', 'Aisa', 'Albalate de Cinca', 'Albalatillo', 'Albelda', 'Albero Alto', 'Albero Bajo', 'Alberuela de Tubo', 'Alcalá de Gurrea', 'Alcalá del Obispo', 'Alcampell', 'Alcolea de Cinca', 'Alcubierre', 'Alerre', 'Alfántega', 'Almudévar', 'Almunia de San Juan', 'Almuniente', 'Alquézar', 'Altorricón', 'Angüés', 'Ansó', 'Antillón', 'Aragüés del Puerto', 'Arén', 'Argavieso', 'Arguis', 'Ayerbe', 'Azanuy-Alins', 'Azara', 'Azlor', 'Baélls', 'Bailo', 'Baldellou', 'Ballobar', 'Banastás', 'Barbastro', 'Barbués', 'Barbuñales', 'Bárcabo', 'Belver de Cinca', 'Benabarre', 'Benasque', 'Berbegal', 'Bielsa', 'Bierge', 'Biescas', 'Binaced', 'Binéfar', 'Bisaurri', 'Biscarrués', 'Blecua y Torres', 'Boltaña', 'Bonansa', 'Borau', 'Broto', 'Caldearenas', 'Campo', 'Camporrélls', 'Canal de Berdún', 'Candasnos', 'Canfranc', 'Capdesaso', 'Capella', 'Casbas de Huesca', 'Castejón del Puente', 'Castejón de Monegros', 'Castejón de Sos', 'Castelflorite', 'Castiello de Jaca', 'Castigaleu', 'Castillazuelo', 'Castillonroy', 'Colungo', 'Chalamera', 'Chía', 'Chimillas', 'Esplús', 'Estada', 'Estadilla', 'Estopiñán del Castillo', 'Fago', 'Fanlo', 'Fiscal', 'Fonz', 'Foradada del Toscar', 'Fraga', 'Fueva (La)', 'Gistaín', 'Grado (El)', 'Grañén', 'Graus', 'Gurrea de Gállego', 'Hoz de Jaca', 'Huerto', 'Huesca', 'Ibieca', 'Igriés', 'Ilche', 'Isábena', 'Jaca', 'Jasa', 'Labuerda', 'Laluenga', 'Lalueza', 'Lanaja', 'Laperdiguera', 'Lascellas-Ponzano', 'Lascuarre', 'Laspaúles', 'Laspuña', 'Loarre', 'Loporzano', 'Loscorrales', 'Monesma y Cajigar', 'Monflorite-Lascasas', 'Montanuy', 'Monzón', 'Naval', 'Novales', 'Nueno', 'Olvena', 'Ontiñena', 'Osso de Cinca', 'Palo', 'Panticosa', 'Peñalba', 'Peñas de Riglos (Las)', 'Peralta de Alcofea', 'Peralta de Calasanz', 'Peraltilla', 'Perarrúa', 'Pertusa', 'Piracés', 'Plan', 'Poleñino', 'Pozán de Vero', 'Puebla de Castro (La)', 'Puente de Montañana', 'Puértolas', 'Pueyo de Araguás (El)', 'Pueyo de Santa Cruz', 'Quicena', 'Robres', 'Sabiñánigo', 'Sahún', 'Salas Altas', 'Salas Bajas', 'Salillas', 'Sallent de Gállego', 'San Esteban de Litera', 'Sangarrén', 'San Juan de Plan', 'Santa Cilia', 'Santa Cruz de la Serós', 'Santaliestra y San Quílez', 'Sariñena', 'Secastilla', 'Seira', 'Sena', 'Senés de Alcubierre', 'Sesa', 'Sesué', 'Siétamo', 'Sopeira', 'Tamarite de Litera', 'Tardienta', 'Tella-Sin', 'Tierz', 'Tolva', 'Torla', 'Torralba de Aragón', 'Torre la Ribera', 'Torrente de Cinca', 'Torres de Alcanadre', 'Torres de Barbués', 'Tramaced', 'Valfarta', 'Valle de Bardají', 'Valle de Lierp', 'Velilla de Cinca', 'Beranuy', 'Viacamp y Litera', 'Vicién', 'Villanova', 'Villanúa', 'Villanueva de Sigena', 'Yebra de Basa', 'Yésero', 'Zaidín', 'Valle de Hecho', 'Puente la Reina de Jaca', 'San Miguel del Cinca', 'Sotonera (La)', 'Lupiñén-Ortilla', 'Santa María de Dulcis', 'Aínsa-Sobrarbe', 'Hoz y Costean', 'Vencillón', 'Ababuj', 'Abejuela', 'Aguatón', 'Aguaviva', 'Aguilar del Alfambra', 'Alacón', 'Alba', 'Albalate del Arzobispo', 'Albarracín', 'Albentosa', 'Alcaine', 'Alcalá de la Selva', 'Alcañiz', 'Alcorisa', 'Alfambra', 'Aliaga', 'Almohaja', 'Alobras', 'Alpeñés', 'Allepuz', 'Alloza', 'Allueva', 'Anadón', 'Andorra', 'Arcos de las Salinas', 'Arens de Lledó', 'Argente', 'Ariño', 'Azaila', 'Bádenas', 'Báguena', 'Bañón', 'Barrachina', 'Bea', 'Beceite', 'Belmonte de San José', 'Bello', 'Berge', 'Bezas', 'Blancas', 'Blesa', 'Bordón', 'Bronchales', 'Bueña', 'Burbáguena', 'Cabra de Mora', 'Calaceite', 'Calamocha', 'Calanda', 'Calomarde', 'Camañas', 'Camarena de la Sierra', 'Camarillas', 'Caminreal', 'Cantavieja', 'Cañada de Benatanduz', 'Cañada de Verich (La)', 'Cañada Vellida', 'Cañizar del Olivar', 'Cascante del Río', 'Castejón de Tornos', 'Castel de Cabra', 'Castelnou', 'Castelserás', 'Castellar (El)', 'Castellote', 'Cedrillas', 'Celadas', 'Cella', 'Cerollera (La)', 'Codoñera (La)', 'Corbalán', 'Cortes de Aragón', 'Cosa', 'Cretas', 'Crivillén', 'Cuba (La)', 'Cubla', 'Cucalón', 'Cuervo (El)', 'Cuevas de Almudén', 'Cuevas Labradas', 'Ejulve', 'Escorihuela', 'Escucha', 'Estercuel', 'Ferreruela de Huerva', 'Fonfría', 'Formiche Alto', 'Fórnoles', 'Fortanete', 'Foz-Calanda', 'Fresneda (La)', 'Frías de Albarracín', 'Fuenferrada', 'Fuentes Calientes', 'Fuentes Claras', 'Fuentes de Rubielos', 'Fuentespalda', 'Galve', 'Gargallo', 'Gea de Albarracín', 'Ginebrosa (La)', 'Griegos', 'Guadalaviar', 'Gúdar', 'Híjar', 'Hinojosa de Jarque', 'Hoz de la Vieja (La)', 'Huesa del Común', 'Iglesuela del Cid (La)', 'Jabaloyas', 'Jarque de la Val', 'Jatiel', 'Jorcas', 'Josa', 'Lagueruela', 'Lanzuela', 'Libros', 'Lidón', 'Linares de Mora', 'Loscos', 'Lledó', 'Maicas', 'Manzanera', 'Martín del Río', 'Mas de las Matas', 'Mata de los Olmos (La)', 'Mazaleón', 'Mezquita de Jarque', 'Mirambel', 'Miravete de la Sierra', 'Molinos', 'Monforte de Moyuela', 'Monreal del Campo', 'Monroyo', 'Montalbán', 'Monteagudo del Castillo', 'Monterde de Albarracín', 'Mora de Rubielos', 'Moscardón', 'Mosqueruela', 'Muniesa', 'Noguera de Albarracín', 'Nogueras', 'Nogueruelas', 'Obón', 'Odón', 'Ojos Negros', 'Olba', 'Oliete', 'Olmos (Los)', 'Orihuela del Tremedal', 'Orrios', 'Palomar de Arroyos', 'Pancrudo', 'Parras de Castellote (Las)', 'Peñarroya de Tastavins', 'Peracense', 'Peralejos', 'Perales del Alfambra', 'Pitarque', 'Plou', 'Pobo (El)', 'Portellada (La)', 'Pozondón', 'Pozuel del Campo', 'Puebla de Híjar (La)', 'Puebla de Valverde (La)', 'Puertomingalvo', 'Ráfales', 'Rillo', 'Riodeva', 'Ródenas', 'Royuela', 'Rubiales', 'Rubielos de la Cérida', 'Rubielos de Mora', 'Salcedillo', 'Saldón', 'Samper de Calanda', 'San Agustín', 'San Martín del Río', 'Santa Cruz de Nogueras', 'Santa Eulalia', 'Sarrión', 'Segura de los Baños', 'Seno', 'Singra', 'Terriente', 'Teruel', 'Toril y Masegoso', 'Tormón', 'Tornos', 'Torralba de los Sisones', 'Torrecilla de Alcañiz', 'Torrecilla del Rebollar', 'Torre de Arcas', 'Torre de las Arcas', 'Torre del Compte', 'Torrelacárcel', 'Torre los Negros', 'Torremocha de Jiloca', 'Torres de Albarracín', 'Torrevelilla', 'Torrijas', 'Torrijo del Campo', 'Tramacastiel', 'Tramacastilla', 'Tronchón', 'Urrea de Gaén', 'Utrillas', 'Valacloche', 'Valbona', 'Valdealgorfa', 'Valdecuenca', 'Valdelinares', 'Valdeltormo', 'Valderrobres', 'Valjunquera', 'Vallecillo (El)', 'Veguillas de la Sierra', 'Villafranca del Campo', 'Villahermosa del Campo', 'Villanueva del Rebollar de la Sierra', 'Villar del Cobo', 'Villar del Salz', 'Villarluengo', 'Villarquemado', 'Villarroya de los Pinares', 'Villastar', 'Villel', 'Vinaceite', 'Visiedo', 'Vivel del Río Martín', 'Zoma (La)', 'Abanto', 'Acered', 'Agón', 'Aguarón', 'Aguilón', 'Ainzón', 'Aladrén', 'Alagón', 'Alarba', 'Alberite de San Juan', 'Albeta', 'Alborge', 'Alcalá de Ebro', 'Alcalá de Moncayo', 'Alconchel de Ariza', 'Aldehuela de Liestos', 'Alfajarín', 'Alfamén', 'Alforque', 'Alhama de Aragón', 'Almochuel', 'Almolda (La)', 'Almonacid de la Cuba', 'Almonacid de la Sierra', 'Almunia de Doña Godina (La)', 'Alpartir', 'Ambel', 'Anento', 'Aniñón', 'Añón de Moncayo', 'Aranda de Moncayo', 'Arándiga', 'Ardisa', 'Ariza', 'Artieda', 'Asín', 'Atea', 'Ateca', 'Azuara', 'Badules', 'Bagüés', 'Balconchán', 'Bárboles', 'Bardallur', 'Belchite', 'Belmonte de Gracián', 'Berdejo', 'Berrueco', 'Bijuesca', 'Biota', 'Bisimbre', 'Boquiñeni', 'Bordalba', 'Borja', 'Botorrita', 'Brea de Aragón', 'Bubierca', 'Bujaraloz', 'Bulbuente', 'Bureta', 'Burgo de Ebro (El)', 'Buste (El)', 'Cabañas de Ebro', 'Cabolafuente', 'Cadrete', 'Calatayud', 'Calatorao', 'Calcena', 'Calmarza', 'Campillo de Aragón', 'Carenas', 'Cariñena', 'Caspe', 'Castejón de Alarba', 'Castejón de las Armas', 'Castejón de Valdejasa', 'Castiliscar', 'Cervera de la Cañada', 'Cerveruela', 'Cetina', 'Cimballa', 'Cinco Olivas', 'Clarés de Ribota', 'Codo', 'Codos', 'Contamina', 'Cosuenda', 'Cuarte de Huerva', 'Cubel', 'Cuerlas (Las)', 'Chiprana', 'Chodes', 'Daroca', 'Ejea de los Caballeros', 'Embid de Ariza', 'Encinacorba', 'Épila', 'Erla', 'Escatrón', 'Fabara', 'Farlete', 'Fayón', 'Fayos (Los)', 'Figueruelas', 'Fombuena', 'Frago (El)', 'Frasno (El)', 'Fréscano', 'Fuendejalón', 'Fuendetodos', 'Fuentes de Ebro', 'Fuentes de Jiloca', 'Gallocanta', 'Gallur', 'Gelsa', 'Godojos', 'Gotor', 'Grisel', 'Grisén', 'Herrera de los Navarros', 'Ibdes', 'Illueca', 'Isuerre', 'Jaraba', 'Jarque', 'Jaulín', 'Joyosa (La)', 'Lagata', 'Langa del Castillo', 'Layana', 'Lécera', 'Leciñena', 'Lechón', 'Letux', 'Litago', 'Lituénigo', 'Lobera de Onsella', 'Longares', 'Longás', 'Lucena de Jalón', 'Luceni', 'Luesia', 'Luesma', 'Lumpiaque', 'Luna', 'Maella', 'Magallón', 'Mainar', 'Malanquilla', 'Maleján', 'Malón', 'Maluenda', 'Mallén', 'Manchones', 'Mara', 'María de Huerva', 'Mediana de Aragón', 'Mequinenza', 'Mesones de Isuela', 'Mezalocha', 'Mianos', 'Miedes de Aragón', 'Monegrillo', 'Moneva', 'Monreal de Ariza', 'Monterde', 'Montón', 'Morata de Jalón', 'Morata de Jiloca', 'Morés', 'Moros', 'Moyuela', 'Mozota', 'Muel', 'Muela (La)', 'Munébrega', 'Murero', 'Murillo de Gállego', 'Navardún', 'Nigüella', 'Nombrevilla', 'Nonaspe', 'Novallas', 'Novillas', 'Nuévalos', 'Nuez de Ebro', 'Olvés', 'Orcajo', 'Orera', 'Orés', 'Oseja', 'Osera de Ebro', 'Paniza', 'Paracuellos de Jiloca', 'Paracuellos de la Ribera', 'Pastriz', 'Pedrola', 'Pedrosas (Las)', 'Perdiguera', 'Piedratajada', 'Pina de Ebro', 'Pinseque', 'Pintanos (Los)', 'Plasencia de Jalón', 'Pleitas', 'Plenas', 'Pomer', 'Pozuel de Ariza', 'Pozuelo de Aragón', 'Pradilla de Ebro', 'Puebla de Albortón', 'Puebla de Alfindén (La)', 'Puendeluna', 'Purujosa', 'Quinto', 'Remolinos', 'Retascón', 'Ricla', 'Romanos', 'Rueda de Jalón', 'Ruesca', 'Sádaba', 'Salillas de Jalón', 'Salvatierra de Esca', 'Samper del Salz', 'San Martín de la Virgen de Moncayo', 'San Mateo de Gállego', 'Santa Cruz de Grío', 'Santa Cruz de Moncayo', 'Santa Eulalia de Gállego', 'Santed', 'Sástago', 'Sabiñán', 'Sediles', 'Sestrica', 'Sierra de Luna', 'Sisamón', 'Sobradiel', 'Sos del Rey Católico', 'Tabuenca', 'Talamantes', 'Tarazona', 'Tauste', 'Terrer', 'Tierga', 'Tobed', 'Torralba de los Frailes', 'Torralba de Ribota', 'Torralbilla', 'Torrehermosa', 'Torrelapaja', 'Torrellas', 'Torres de Berrellén', 'Torrijo de la Cañada', 'Tosos', 'Trasmoz', 'Trasobares', 'Uncastillo', 'Undués de Lerda', 'Urrea de Jalón', 'Urriés', 'Used', 'Utebo', 'Valdehorna', 'Val de San Martín', 'Valmadrid', 'Valpalmas', 'Valtorres', 'Velilla de Ebro', 'Velilla de Jiloca', 'Vera de Moncayo', 'Vierlas', 'Vilueña (La)', 'Villadoz', 'Villafeliche', 'Villafranca de Ebro', 'Villalba de Perejil', 'Villalengua', 'Villanueva de Gállego', 'Villanueva de Jiloca', 'Villanueva de Huerva', 'Villar de los Navarros', 'Villarreal de Huerva', 'Villarroya de la Sierra', 'Villarroya del Campo', 'Vistabella', 'Zaida (La)', 'Zaragoza', 'Zuera', 'Biel', 'Marracos', 'Villamayor de Gállego', 'Sigüés'}

    for municipio in listado_municipios:

        print(municipio)
        rdftotal = rdftotal  + '	<dcat:Dataset rdf:about="http://opendata.aragon.es/aragopedia">\n'
        rdftotal = rdftotal  + '		<dct:identifier>datos-municipio-' + municipio.lower().replace('É', 'E').replace('(','').replace(')','').replace('ü','u').replace(" ", "-").replace('Ñ', 'n').replace('ñ', 'n').replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "") + '</dct:identifier>\n'
        rdftotal = rdftotal  + '		<dct:description>AragoPedia es una iniciativa de la Dirección General de Nuevas Tecnologías para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos del municipio de ' + municipio + '</dct:description>\n'

        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragón</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Demografía</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Nuevas tecnologías</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Aragopedia</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Municipio</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Ayuntamiento</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">Local</dcat:keyword>\n'
        rdftotal = rdftotal  + '		<dcat:keyword xml:lang="es">' + municipio.replace('É', 'E').replace('(','').replace(')','').replace('ü','u').replace(" ", "-").replace('Ñ', 'n').replace('ñ', 'n').replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace(";", "") + '</dcat:keyword>\n'

        rdftotal = rdftotal  + '<dct:title>Municipio: ' + municipio+'</dct:title>\n'
        rdftotal = rdftotal  + '		<dct:modified>2014-02-05</dct:modified>\n'
        rdftotal = rdftotal  + '		<dct:issued>2014-02-05</dct:issued>\n'
        rdftotal = rdftotal  + '		<dct:publisher>\n'
        rdftotal = rdftotal  + '			<foaf:Organization>\n'
        rdftotal = rdftotal  + '				<dct:title>Dirección General de Nuevas Tecnologías</dct:title>\n'
        rdftotal = rdftotal  + '				<foaf:homepage rdf:resource="http://www.aragon.es/DepartamentosOrganismosPublicos/Departamentos/IndustriaInnovacion/AreasTematicas/SociedadInformacion?channelSelected=870aa8aeb0c3a210VgnVCM100000450a15acRCRD"/>\n'
        rdftotal = rdftotal  + '			</foaf:Organization>\n'
        rdftotal = rdftotal  + '		</dct:publisher>\n'
        rdftotal = rdftotal  + '		<dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '			<dct:frequency>\n'
        rdftotal = rdftotal  + '				<rdf:value>P1M</rdf:value>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Mensual</rdfs:label>\n'
        rdftotal = rdftotal  + '		    </dct:frequency>\n'
        rdftotal = rdftotal  + '		</dct:accrualPeriodicity>\n'
        rdftotal = rdftotal  + '		<dct:spatial>' + municipio +'</dct:spatial>\n'
        rdftotal = rdftotal  + '		<dct:temporal>2000-01-01 a actualidad</dct:temporal>\n'
        rdftotal = rdftotal  + '		<dct:language>es</dct:language>\n'
        rdftotal = rdftotal  + '		<dct:license rdf:resource="Creative Commons-Reconocimiento CC-By 3.0"></dct:license>\n'
        rdftotal = rdftotal  + '		<dcat:granularity>Municipio</dcat:granularity>\n'
        rdftotal = rdftotal  + '		<dcat:dataQuality></dcat:dataQuality>\n'
        rdftotal = rdftotal  + '		<dcat:dataDictionary></dcat:dataDictionary>\n'
        rdftotal = rdftotal  + '		<dcat:theme>\n'
        rdftotal = rdftotal  + '			<rdf:Description>\n'
        rdftotal = rdftotal  + '				<rdfs:label>Demografía</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:identifier>demografia</dct:identifier>\n'
        rdftotal = rdftotal  + '				<dct:description>Demografía</dct:description>\n'
        rdftotal = rdftotal  + '			</rdf:Description>\n'
        rdftotal = rdftotal  + '		</dcat:theme>\n'
        rdftotal = rdftotal  + '		<dcat:distribution>\n'
        rdftotal = rdftotal  + '			<dcat:Distribution>\n'
        rdftotal = rdftotal  + '				<rdfs:label>' + municipio + '</rdfs:label>\n'
        rdftotal = rdftotal  + '				<dct:description>AragoPedia es una iniciativa de la Dirección General de Nuevas Tecnologías para que todos los municipios de Aragón puedan contar con una página de Datos Abiertos. Se han explotado los conjuntos de datos de Aragón Open Data para extraer los datos geolocalizados. Los datos geolocalizados se han ordenados según las entidades locales a las que les pertenecen, generando una cobertura open data para el 100% del territorio aragonés. AragoPedia está desarrollada sobre software libre, en concreto se ha realizado con MediaWiki, el software utilizado para desarrollar la WikiPedia. En este caso, se ofrecen los datos abiertos del municipio de ' + municipio + '</dct:description>\n'
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

    print rdftotal
    f = open(config.DOWNLOAD_PATH + "/datosPignatelli_municipio.rdf","w")
    f.write(rdftotal)
    f.close()

    print(parse_rdfs2())





main()

