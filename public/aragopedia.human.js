/*var prov = [
  {
    desc: "Huesca",
    label: "Huesca"
  },
  {
    desc: "Teruel",
    label: "Teruel"
  },
  {
    desc: "Zaragoza",
    label: "Zaragoza"
  }
];*/
var prov = ["Huesca", "Teruel", "Zaragoza"];

var formatList = ["csv", "ics", "xls", "xml"];

var comarca = [];
var aragopCom = new Array();
var munis = [];
var aragopMun = new Array();

function adM(nom, aragop) {
  var uriAragop = aragop;	
  if (aragop == "") {
    uriAragop = nom.replace(/ /g, '_');
  }
  //var aux = { desc: uriAragop, label: nom };
  //munis.push(aux);
  munis.push(nom);
  aragopMun[nom] = uriAragop;
}
function adC(nom) {
  var uriAragop = nom.replace(/ /g, '_');
  //var aux = { desc: uriAragop, label: nom };
  //comarca.push(aux);
  comarca.push(nom);
  aragopCom[nom] = uriAragop;
}
adC('Alto Gállego');
adC('Andorra-Sierra de Arcos');
adC('Aranda');
adC('Bajo Aragón');
adC('Bajo Aragón-Caspe/Baix Aragó-Casp');
adC('Bajo Cinca/Baix Cinca');
adC('Bajo Martín');
adC('Campo de Belchite');
adC('Campo de Borja');
adC('Campo de Cariñena');
adC('Campo de Daroca');
adC('Cinca Medio');
adC('Cinco Villas');
adC('Comunidad de Calatayud');
adC('Comunidad de Teruel');
adC('Cuencas Mineras');
adC('D.C. Zaragoza');
adC('Gúdar-Javalambre');
adC('Hoya de Huesca/Plana de Uesca');
adC('Jiloca');
adC('La Jacetania');
adC('La Litera/La Llitera');
adC('La Ribagorza');
adC('Los Monegros');
adC('Maestrazgo');
adC('Matarraña/Matarranya');
adC('Ribera Alta del Ebro');
adC('Ribera Baja del Ebro');
adC('Sierra de Albarracín');
adC('Sobrarbe');
adC('Somontano de Barbastro');
adC('Tarazona y el Moncayo');
adC('Valdejalón');

adM('Lascellas Ponzano','Lascellas-Ponzano');
adM('Monflorite Lascasas','Monflorite-Lascasas');
adM('Puente La Reina de Jaca','Puente_la_Reina_de_Jaca');

adM('Aísa','');
adM('Ababuj','');
adM('Abanto','');
adM('Abejuela','');
adM('Abiego','');
adM('Abizanda','');
adM('Acered','');
adM('Adahuesca','');
adM('Agón','');
adM('Aguarón','');
adM('Aguatón','');
adM('Aguaviva','');
adM('Agüero','');
adM('Aguilar del Alfambra','');
adM('Aguilón','');
adM('Aínsa-Sobrarbe','');
adM('Ainzón','');
adM('Alacón','');
adM('Aladrén','');
adM('Alagón','');
adM('Alarba','');
adM('Alba','');
adM('Albalate de Cinca','');
adM('Albalate del Arzobispo','');
adM('Albalatillo','');
adM('Albarracín','');
adM('Albelda','');
adM('Albentosa','');
adM('Alberite de San Juan','');
adM('Albero Alto','');
adM('Albero Bajo','');
adM('Alberuela de Tubo','');
adM('Albeta','');
adM('Alborge','');
adM('Alcaine','');
adM('Alcalá de Ebro','');
adM('Alcalá de Gurrea','');
adM('Alcalá de la Selva','');
adM('Alcalá de Moncayo','');
adM('Alcalá del Obispo','');
adM('Alcampell','');
adM('Alcañiz','');
adM('Alcolea de Cinca','');
adM('Alconchel de Ariza','');
adM('Alcorisa','');
adM('Alcubierre','');
adM('Aldehuela de Liestos','');
adM('Alerre','');
adM('Alfajarín','');
adM('Alfambra','');
adM('Alfamén','');
adM('Alfántega','');
adM('Alforque','');
adM('Alhama de Aragón','');
adM('Aliaga','');
adM('Allepuz','');
adM('Alloza','');
adM('Allueva','');
adM('Almochuel','');
adM('Almohaja','');
adM('Almonacid de la Cuba','');
adM('Almonacid de la Sierra','');
adM('Almudévar','');
adM('Almunia de San Juan','');
adM('Almuniente','');
adM('Alobras','');
adM('Alpartir','');
adM('Alpeñés','');
adM('Alquézar','');
adM('Altorricón','');
adM('Ambel','');
adM('Anadón','');
adM('Andorra','');
adM('Anento','');
adM('Angüés','');
adM('Aniñón','');
adM('Ansó','');
adM('Antillón','');
adM('Añón de Moncayo','');
adM('Aragüés del Puerto','');
adM('Aranda de Moncayo','');
adM('Arándiga','');
adM('Arcos de las Salinas','');
adM('Ardisa','');
adM('Arén','');
adM('Arens de Lledó','');
adM('Argavieso','');
adM('Argente','');
adM('Arguis','');
adM('Ariño','');
adM('Ariza','');
adM('Artieda','');
adM('Asín','');
adM('Atea','');
adM('Ateca','');
adM('Ayerbe','');
adM('Azaila','');
adM('Azanuy-Alins','');
adM('Azara','');
adM('Azlor','');
adM('Azuara','');
adM('Bádenas','');
adM('Badules','');
adM('Baélls','Baells');
adM('Báguena','');
adM('Bagüés','');
adM('Bailo','');
adM('Balconchán','');
adM('Baldellou','');
adM('Ballobar','');
adM('Banastás','');
adM('Bañón','');
adM('Barbastro','');
adM('Bárboles','');
adM('Barbués','');
adM('Barbuñales','');
adM('Bárcabo','');
adM('Bardallur','');
adM('Barrachina','');
adM('Bea','');
adM('Beceite','');
adM('Belchite','');
adM('Bello','');
adM('Belmonte de Gracián','');
adM('Belmonte de San José','');
adM('Belver de Cinca','');
adM('Benabarre','');
adM('Benasque','');
adM('Beranuy','Veracruz');
adM('Berbegal','');
adM('Berdejo','');
adM('Berge','');
adM('Berrueco','');
adM('Bezas','');
adM('Biel','');
adM('Bielsa','');
adM('Bierge','');
adM('Biescas','');
adM('Bijuesca','');
adM('Binaced','');
adM('Binéfar','');
adM('Biota','');
adM('Bisaurri','');
adM('Biscarrués','');
adM('Bisimbre','');
adM('Blancas','');
adM('Blecua y Torres','');
adM('Blesa','');
adM('Boltaña','');
adM('Bonansa','');
adM('Boquiñeni','');
adM('Borau','');
adM('Bordalba','');
adM('Bordón','');
adM('Borja','');
adM('Botorrita','');
adM('Brea de Aragón','');
adM('Bronchales','');
adM('Broto','');
adM('Bubierca','');
adM('Bueña','');
adM('Bujaraloz','');
adM('Bulbuente','');
adM('Burbáguena','');
adM('Bureta','');
adM('Cabañas de Ebro','');
adM('Cabolafuente','');
adM('Cabra de Mora','');
adM('Cadrete','');
adM('Calaceite','');
adM('Calamocha','');
adM('Calanda','');
adM('Calatayud','');
adM('Calatorao','');
adM('Calcena','');
adM('Caldearenas','');
adM('Calmarza','');
adM('Calomarde','');
adM('Camañas','');
adM('Camarena de la Sierra','');
adM('Camarillas','');
adM('Caminreal','');
adM('Campillo de Aragón','');
adM('Campo','');
adM('Camporrélls','Camporrells');
adM('Canal de Berdún','');
adM('Candasnos','');
adM('Canfranc','');
adM('Cantavieja','');
adM('Cañada de Benatanduz','');
adM('Cañada Vellida','');
adM('Cañizar del Olivar','');
adM('Capdesaso','');
adM('Capella','');
adM('Carenas','');
adM('Cariñena','');
adM('Casbas de Huesca','');
adM('Cascante del Río','');
adM('Caspe','');
adM('Castejón de Alarba','');
adM('Castejón de las Armas','');
adM('Castejón de Monegros','');
adM('Castejón de Sos','');
adM('Castejón de Tornos','');
adM('Castejón de Valdejasa','');
adM('Castejón del Puente','');
adM('Castel de Cabra','');
adM('Castelflorite','');
adM('Castellote','');
adM('Castelnou','');
adM('Castelserás','');
adM('Castiello de Jaca','');
adM('Castigaleu','');
adM('Castiliscar','');
adM('Castillazuelo','');
adM('Castillonroy','');
adM('Cedrillas','');
adM('Celadas','');
adM('Cella','');
adM('Cervera de la Cañada','');
adM('Cerveruela','');
adM('Cetina','');
adM('Chalamera','');
adM('Chía','');
adM('Chimillas','');
adM('Chiprana','');
adM('Chodes','');
adM('Cimballa','');
adM('Cinco Olivas','');
adM('Clarés de Ribota','');
adM('Codo','');
adM('Codos','');
adM('Colungo','');
adM('Contamina','');
adM('Corbalán','');
adM('Cortes de Aragón','');
adM('Cosa','');
adM('Cosuenda','');
adM('Cretas','');
adM('Crivillén','');
adM('Cuarte de Huerva','');
adM('Cubel','');
adM('Cubla','');
adM('Cucalón','');
adM('Cuevas de Almudén','');
adM('Cuevas Labradas','');
adM('Daroca','');
adM('Ejea de los Caballeros','');
adM('Ejulve','');
adM('El Burgo de Ebro','Burgo_de_Ebro_(El)');
adM('El Buste','Buste_(El)');
adM('El Castellar','Castellar_(El)');
adM('El Cuervo','Cuervo_(El)');
adM('El Frago','Frago_(El)');
adM('El Frasno','Frasno_(El)');
adM('El Grado','Grado_(El)');
adM('El Pobo','Pobo_(El)');
adM('El Pueyo de Araguás','Pueyo_de_Araguás_(El)');
adM('El Vallecillo','Vallecillo_(El)');
adM('Embid de Ariza','');
adM('Encinacorba','');
adM('Épila','');
adM('Erla','');
adM('Escatrón','');
adM('Escorihuela','');
adM('Escucha','');
adM('Esplús','');
adM('Estada','');
adM('Estadilla','');
adM('Estercuel','');
adM('Estopiñán del Castillo','');
adM('Fabara','');
adM('Fago','');
adM('Fanlo','');
adM('Farlete','');
adM('Fayón','');
adM('Ferreruela de Huerva','');
adM('Figueruelas','');
adM('Fiscal','');
adM('Fombuena','');
adM('Fonfría','');
adM('Fonz','');
adM('Foradada del Toscar','');
adM('Formiche Alto','');
adM('Fórnoles','');
adM('Fortanete','');
adM('Foz-Calanda','');
adM('Fraga','');
adM('Fréscano','');
adM('Frías de Albarracín','');
adM('Fuendejalón','');
adM('Fuendetodos','');
adM('Fuenferrada','');
adM('Fuentes Calientes','');
adM('Fuentes Claras','');
adM('Fuentes de Ebro','');
adM('Fuentes de Jiloca','');
adM('Fuentes de Rubielos','');
adM('Fuentespalda','');
adM('Gallocanta','');
adM('Gallur','');
adM('Galve','');
adM('Gargallo','');
adM('Gea de Albarracín','');
adM('Gelsa','');
adM('Gistaín','');
adM('Godojos','');
adM('Gotor','');
adM('Grañén','');
adM('Graus','');
adM('Griegos','');
adM('Grisel','');
adM('Grisén','');
adM('Guadalaviar','');
adM('Gúdar','');
adM('Gurrea de Gállego','');
adM('Herrera de los Navarros','');
adM('Híjar','');
adM('Hinojosa de Jarque','');
adM('Hoz de Jaca','');
adM('Hoz y Costeán','');
adM('Huerto','');
adM('Huesa del Común','');
adM('Huesca','');
adM('Ibdes','');
adM('Ibieca','');
adM('Igriés','');
adM('Ilche','');
adM('Illueca','');
adM('Isábena','');
adM('Isuerre','');
adM('Jabaloyas','');
adM('Jaca','');
adM('Jaraba','');
adM('Jarque','');
adM('Jarque de la Val','');
adM('Jasa','');
adM('Jatiel','');
adM('Jaulín','');
adM('Jorcas','');
adM('Josa','');
adM('La Almolda','Almolda_(La)');
adM('La Almunia de Doña Godina','Almunia_de_Doña_Godina_(La)');
adM('La Cañada de Verich','Cañada_de_Verich_(La)');
adM('La Cerollera','Cerollera_(La)');
adM('La Codoñera','Codoñera_(La)');
adM('La Cuba','Cuba_(La)');
adM('La Fresneda','Fresneda_(La)');
adM('La Fueva','Fueva_(La)');
adM('La Ginebrosa','Ginebrosa_(La)');
adM('La Hoz de la Vieja','Hoz_de_la_Vieja_(La)');
adM('La Iglesuela del Cid','Iglesuela_del_Cid_(La)');
adM('La Joyosa','Joyosa_(La)');
adM('La Mata de los Olmos','Mata_de_los_Olmos_(La)');
adM('La Muela','Muela_(La)');
adM('La Portellada','Portellada_(La)');
adM('La Puebla de Alfindén','Puebla_de_Alfindén_(La)');
adM('La Puebla de Castro','Puebla_de_Castro_(La)');
adM('La Puebla de Híjar','Puebla_de_Híjar_(La)');
adM('La Puebla de Valverde','Puebla_de_Valverde_(La)');
adM('La Sotonera','Sotonera_(La)');
adM('La Vilueña','Vilueña_(La)');
adM('La Zaida','Zaida_(La)');
adM('La Zoma','Zoma_(La)');
adM('Labuerda','');
adM('Lagata','');
adM('Lagueruela','');
adM('Laluenga','');
adM('Lalueza','');
adM('Lanaja','');
adM('Langa del Castillo','');
adM('Lanzuela','');
adM('Laperdiguera','');
adM('Las Cuerlas','Cuerlas_(Las)');
adM('Las Parras de Castellote','Parras_de_Castellote_(Las)');
adM('Las Pedrosas','Pedrosas_(Las)');
adM('Las Peñas de Riglos','Peñas_de_Riglos_(Las)');
adM('Lascuarre','');
adM('Laspaúles','');
adM('Laspuña','');
adM('Layana','');
adM('Lécera','');
adM('Lechón','');
adM('Leciñena','');
adM('Letux','');
adM('Libros','');
adM('Lidón','');
adM('Linares de Mora','');
adM('Litago','');
adM('Lituénigo','');
adM('Lledó','');
adM('Loarre','');
adM('Lobera de Onsella','');
adM('Longares','');
adM('Longás','');
adM('Loporzano','');
adM('Los Olmos','Olmos_(Los)');
adM('Los Fayos','Fayos_(Los)');
adM('Los Pintanos','Pintanos_(Los)');
adM('Loscorrales','');
adM('Loscos','');
adM('Lucena de Jalón','');
adM('Luceni','');
adM('Luesia','');
adM('Luesma','');
adM('Lumpiaque','');
adM('Luna','');
adM('Lupiñén-Ortilla','');
adM('Maella','');
adM('Magallón','');
adM('Maicas','');
adM('Mainar','');
adM('Malanquilla','');
adM('Maleján','');
adM('Mallén','');
adM('Malón','');
adM('Maluenda','');
adM('Manchones','');
adM('Manzanera','');
adM('Mara','');
adM('María de Huerva','');
adM('Marracos','');
adM('Martín del Río','');
adM('Mas de las Matas','');
adM('Mazaleón','');
adM('Mediana de Aragón','');
adM('Mequinenza','');
adM('Mesones de Isuela','');
adM('Mezalocha','');
adM('Mezquita de Jarque','');
adM('Mianos','');
adM('Miedes de Aragón','');
adM('Mirambel','');
adM('Miravete de la Sierra','');
adM('Molinos','');
adM('Monegrillo','');
adM('Monesma y Cajigar','');
adM('Moneva','');
adM('Monforte de Moyuela','');
adM('Monreal de Ariza','');
adM('Monreal del Campo','');
adM('Monroyo','');
adM('Montalbán','');
adM('Montanuy','');
adM('Monteagudo del Castillo','');
adM('Monterde','');
adM('Monterde de Albarracín','');
adM('Montón','');
adM('Monzón','');
adM('Mora de Rubielos','');
adM('Morata de Jalón','');
adM('Morata de Jiloca','');
adM('Morés','');
adM('Moros','');
adM('Moscardón','');
adM('Mosqueruela','');
adM('Moyuela','');
adM('Mozota','');
adM('Muel','');
adM('Munébrega','');
adM('Muniesa','');
adM('Murero','');
adM('Murillo de Gállego','');
adM('Naval','');
adM('Navardún','');
adM('Nigüella','');
adM('Noguera de Albarracín','');
adM('Nogueras','');
adM('Nogueruelas','');
adM('Nombrevilla','');
adM('Nonaspe','');
adM('Novales','');
adM('Novallas','');
adM('Novillas','');
adM('Nueno','');
adM('Nuévalos','');
adM('Nuez de Ebro','');
adM('Obón','');
adM('Odón','');
adM('Ojos Negros','');
adM('Olba','');
adM('Oliete','');
adM('Olvena','');
adM('Olvés','');
adM('Ontiñena','');
adM('Orcajo','');
adM('Orera','');
adM('Orés','');
adM('Orihuela del Tremedal','');
adM('Orrios','');
adM('Oseja','');
adM('Osera de Ebro','');
adM('Osso de Cinca','');
adM('Palo','');
adM('Palomar de Arroyos','');
adM('Pancrudo','');
adM('Paniza','');
adM('Panticosa','');
adM('Paracuellos de Jiloca','');
adM('Paracuellos de la Ribera','');
adM('Pastriz','');
adM('Pedrola','');
adM('Peñalba','');
adM('Peñarroya de Tastavins','');
adM('Peracense','');
adM('Peralejos','');
adM('Perales del Alfambra','');
adM('Peralta de Alcofea','');
adM('Peralta de Calasanz','');
adM('Peraltilla','');
adM('Perarrúa','');
adM('Perdiguera','');
adM('Pertusa','');
adM('Piedratajada','');
adM('Pina de Ebro','');
adM('Pinseque','');
adM('Piracés','');
adM('Pitarque','');
adM('Plan','');
adM('Plasencia de Jalón','');
adM('Pleitas','');
adM('Plenas','');
adM('Plou','');
adM('Poleñino','');
adM('Pomer','');
adM('Pozán de Vero','');
adM('Pozondón','');
adM('Pozuel de Ariza','');
adM('Pozuel del Campo','');
adM('Pozuelo de Aragón','');
adM('Pradilla de Ebro','');
adM('Puebla de Albortón','');
adM('Puendeluna','');
adM('Puente de Montañana','');
adM('Puértolas','');
adM('Puertomingalvo','');
adM('Pueyo de Santa Cruz','');
adM('Purujosa','');
adM('Quicena','');
adM('Quinto','');
adM('Ráfales','');
adM('Remolinos','');
adM('Retascón','');
adM('Ricla','');
adM('Rillo','');
adM('Riodeva','');
adM('Robres','');
adM('Ródenas','');
adM('Romanos','');
adM('Royuela','');
adM('Rubiales','');
adM('Rubielos de la Cérida','');
adM('Rubielos de Mora','');
adM('Rueda de Jalón','');
adM('Ruesca','');
adM('Sabiñán','Saviñán');
adM('Sabiñánigo','');
adM('Sádaba','');
adM('Sahún','');
adM('Salas Altas','');
adM('Salas Bajas','');
adM('Salcedillo','');
adM('Saldón','');
adM('Salillas','');
adM('Salillas de Jalón','');
adM('Sallent de Gállego','');
adM('Salvatierra de Esca','');
adM('Samper de Calanda','');
adM('Samper del Salz','');
adM('San Agustín','');
adM('San Esteban de Litera','');
adM('San Juan de Plan','');
adM('San Martín de la Virgen de Moncayo','');
adM('San Martín del Río','');
adM('San Mateo de Gállego','');
adM('San Miguel del Cinca','');
adM('Sangarrén','');
adM('Santa Cilia','');
adM('Santa Cruz de Grío','');
adM('Santa Cruz de la Serós','');
adM('Santa Cruz de Moncayo','');
adM('Santa Cruz de Nogueras','');
adM('Santa Eulalia','');
adM('Santa Eulalia de Gállego','');
adM('Santa María de Dulcis','');
adM('Santaliestra y San Quílez','');
adM('Santed','');
adM('Sariñena','');
adM('Sarrión','');
adM('Sástago','');
adM('Secastilla','');
adM('Sediles','');
adM('Segura de los Baños','');
adM('Seira','');
adM('Sena','');
adM('Senés de Alcubierre','');
adM('Seno','');
adM('Sesa','');
adM('Sestrica','');
adM('Sesué','');
adM('Sierra de Luna','');
adM('Siétamo','');
adM('Sigüés','');
adM('Singra','');
adM('Sisamón','');
adM('Sobradiel','');
adM('Sopeira','');
adM('Sos del Rey Católico','');
adM('Tabuenca','');
adM('Talamantes','');
adM('Tamarite de Litera','');
adM('Tarazona','');
adM('Tardienta','');
adM('Tauste','');
adM('Tella-Sin','');
adM('Terrer','');
adM('Terriente','');
adM('Teruel','');
adM('Tierga','');
adM('Tierz','');
adM('Tobed','');
adM('Tolva','');
adM('Toril y Masegoso','');
adM('Torla','');
adM('Tormón','');
adM('Tornos','');
adM('Torralba de Aragón','');
adM('Torralba de los Frailes','');
adM('Torralba de los Sisones','');
adM('Torralba de Ribota','');
adM('Torralbilla','');
adM('Torre de Arcas','');
adM('Torre de las Arcas','');
adM('Torre del Compte','');
adM('Torre la Ribera','');
adM('Torre los Negros','');
adM('Torrecilla de Alcañiz','');
adM('Torrecilla del Rebollar','');
adM('Torrehermosa','');
adM('Torrelacárcel','');
adM('Torrelapaja','');
adM('Torrellas','');
adM('Torremocha de Jiloca','');
adM('Torrente de Cinca','');
adM('Torres de Albarracín','');
adM('Torres de Alcanadre','');
adM('Torres de Barbués','');
adM('Torres de Berrellén','');
adM('Torrevelilla','');
adM('Torrijas','');
adM('Torrijo de la Cañada','');
adM('Torrijo del Campo','');
adM('Tosos','');
adM('Tramacastiel','');
adM('Tramacastilla','');
adM('Tramaced','');
adM('Trasmoz','');
adM('Trasobares','');
adM('Tronchón','');
adM('Uncastillo','');
adM('Undués de Lerda','');
adM('Urrea de Gaén','');
adM('Urrea de Jalón','');
adM('Urriés','');
adM('Used','');
adM('Utebo','');
adM('Utrillas','');
adM('Val de San Martín','');
adM('Valacloche','');
adM('Valbona','');
adM('Valdealgorfa','');
adM('Valdecuenca','');
adM('Valdehorna','');
adM('Valdelinares','');
adM('Valdeltormo','');
adM('Valderrobres','');
adM('Valfarta','');
adM('Valjunquera','');
adM('Valle de Bardají','');
adM('Valle de Hecho','');
adM('Valle de Lierp','');
adM('Valmadrid','');
adM('Valpalmas','');
adM('Valtorres','');
adM('Veguillas de la Sierra','');
adM('Velilla de Cinca','');
adM('Velilla de Ebro','');
adM('Velilla de Jiloca','');
adM('Vencillón','');
adM('Vera de Moncayo','');
adM('Viacamp y Litera','');
adM('Vicién','');
adM('Vierlas','');
adM('Villadoz','');
adM('Villafeliche','');
adM('Villafranca de Ebro','');
adM('Villafranca del Campo','');
adM('Villahermosa del Campo','');
adM('Villalba de Perejil','');
adM('Villalengua','');
adM('Villamayor de Gállego','');
adM('Villanova','');
adM('Villanúa','');
adM('Villanueva de Gállego','');
adM('Villanueva de Huerva','');
adM('Villanueva de Jiloca','');
adM('Villanueva de Sigena','');
adM('Villanueva del Rebollar de la Sierra','');
adM('Villar de los Navarros','');
adM('Villar del Cobo','');
adM('Villar del Salz','');
adM('Villarluengo','');
adM('Villarquemado','');
adM('Villarreal de Huerva','');
adM('Villarroya de la Sierra','');
adM('Villarroya de los Pinares','');
adM('Villarroya del Campo','');
adM('Villastar','');
adM('Villel','');
adM('Vinaceite','');
adM('Visiedo','');
adM('Vistabella','');
adM('Vivel del Río Martín','');
adM('Yebra de Basa','');
adM('Yésero','');
adM('Zaidín','');
adM('Zaragoza','');
adM('Zuera','');