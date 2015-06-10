var idHomer = "";

function parseInitialHomerParams() {
	var currentUrl = window.location.toString();

	var urlListParamPrev  = new Array();
	var urlListParam  = new Array();
	urlListParamPrev = currentUrl.split("/");

	if (urlListParamPrev.length >= 5) {
		if (urlListParamPrev[4] == "detallesHOMER") {
			idHomer = urlListParamPrev[5];
		}
	}
}

function doQueryHomer() {
	parseInitialHomerParams();
//	toggleZonaAvanzada();
	toggleZona('zonaHOMER');
	$("#tipoBusquedaFilter")[0].selectedIndex = 3;
	$("#tipoBusquedaFilter").trigger('chosen:updated');


  var queryHomer = '/proxyHomer?q=package_id%3A' + idHomer;

	//tryToSelectItem($("#langHOMERFilter")[0], urlListParam[2]);

	$.ajax({
		url: queryHomer,
		dataType: "xml",
		success: function (data) {

			var textHTML = "";

			var homerCount = $(data).find("result").attr("numFound");

			if (homerCount < 1) {
				textHTML = "Error accediendo a los detalles del conjunto de datos en HOMER";
			} else if (homerCount > 1) {
				tituloHTML = "Encontrados " + homerCount + " resultados en HOMER con este criterio. No es posible mostrar los detalles.";
			} else {

				$(data).find('doc').each(function() {
					textHTML += '<div class="metadataZone">';
					textHTML += '<section class="additional-info">';
					textHTML += '  <h3>PROPIEDADES DE LOS METADATOS</h3>';

					var titulo = "-";
					var portal = "-";
					var enlace = "";
					var langu = "-";
					var tagList = "";
					var fCreac = "";
					var fModif = "";
					var fValidTo = "";
					var conceptList = "";
					var topicList = "";
					var source = "";
					var metadata_origin = "";
					var license_id = "";
					var update_rate = "";
					var package_type = "";

					$(this).find("arr").each(function() {
            if ($(this).attr("name") == "author") {
							author = $(this).text();
						}
            if ($(this).attr("name") == "tag") {
							tagList += '<section class="tags"><ul class="tag-list well">';
							$(this).find("str").each(function() {
								tagList += "<li class='tag recuadroRedondeado'>" + ($(this).text()) + "</li>";
							});
							tagList += "</ul></section>";
						}
            if ($(this).attr("name") == "concept") {
							conceptList += '<section><ul>';
							$(this).find("str").each(function() {
								conceptList += "<li>" + ($(this).text()) + "</li>";
							});
							conceptList += "</ul></section>";
						}
            if ($(this).attr("name") == "topic") {
							topicList += '<section><ul>';
							$(this).find("str").each(function() {
								topicList += "<li>" + ($(this).text()) + "</li>";
							});
							topicList += "</ul></section>";
						}
					});
					$(this).find("str").each(function() {
             if ($(this).attr("name") == "description") {
							descript = $(this).text();
						}
            if ($(this).attr("name") == "title") {
							title = $(this).text();
						}
            if ($(this).attr("name") == "portal") {
							portal = $(this).text();
						}
            if ($(this).attr("name") == "language") {
							langu = $(this).text();
						}
            if ($(this).attr("name") == "url") {
							enlace = $(this).text();
						}
            if ($(this).attr("name") == "source") {
							source = $(this).text();
						}
            if ($(this).attr("name") == "metadata_origin") {
							metadata_origin = $(this).text();
						}
            if ($(this).attr("name") == "license_id") {
							license_id = $(this).text();
						}
            if ($(this).attr("name") == "update_rate") {
							update_rate = $(this).text();
						}
            if ($(this).attr("name") == "package_type") {
							package_type = $(this).text();
						}
					});
					$(this).find("date").each(function() {
            if ($(this).attr("name") == "package_created") {
							aux = $(this).text().split("T");
							fCreac = aux[0];
						}
            if ($(this).attr("name") == "package_modified") {
							aux = $(this).text().split("T");
							fModif = aux[0];
						}
            if ($(this).attr("name") == "valid_to") {
							aux = $(this).text().split("T");
							fValidTo = aux[0];
						}
					});

					textHTML += getKeyValueHTML("T&iacute;tulo", title);
					textHTML += getKeyValueHTML("Descripci&oacute;n", descript);
//Categor&iacute;a
					textHTML += getKeyValueHTML("Palabra clave / etiqueta", tagList);
					textHTML += getKeyValueHTML("Fecha de actualizaci&oacute;n / modificaci&oacute;n", fModif);
					textHTML += getKeyValueHTML("Fecha de creaci&oacute;n", fCreac);
					textHTML += getKeyValueHTML("Publicador", author);
					textHTML += getKeyValueHTML("Frecuencia de actualizaci&oacute;n", update_rate);
					textHTML += getKeyValueHTML("Idioma", langu);
					textHTML += getKeyValueHTML("Fecha de validez", fValidTo);
					textHTML += getKeyValueHTML("Licencia", license_id);
					//textHTML += getKeyValueHTML("Conceptos", conceptList);
					textHTML += getKeyValueHTML("Temas", topicList);
					textHTML += getKeyValueHTML("Tipo de dato", package_type);
					textHTML += getKeyValueHTML("Portal", portal);
					textHTML += getKeyValueHTML("Fuente", source);

					textHTML += "</section>";
					textHTML += "</div>";
					textHTML += '<div class="resourceZone">';
					textHTML += ' <section class="resources" id="dataset-resources">';
					textHTML += '  <h3>DESCARGAS</h3>';
					textHTML += '  <div class="negrita">Metadato original</div>';
					textHTML += '  <div>';
					textHTML += '   <ul><li><a href="' + metadata_origin + '" title="Metadato original" class="recuadroNoResaltado">Metadato</a></li></ul>';
					textHTML += '  </div>';
					textHTML += '  <div class="negrita">Dato</div>';
					textHTML += '  <div>';
					textHTML += '    <ul>';
					textHTML += '      <li><a title="Descarga" href="' + enlace + '" class="recuadroNoResaltado">';
					textHTML += '      <span class="format-label">Descarga</span>';
					textHTML += '      </a></li>';         
					textHTML += '    </ul>';
					textHTML += '   </div>';
					textHTML += ' </section>';
					textHTML += '</div>';
				});
			}

			$("#homerResults").html(textHTML);

		},
		error: function (data,textStatus,  errorThrown) {
			$("#homerResults").html("No se ha podido obtener los detalles de HOMER");
		}
	});
}

function getKeyValueHTML(key, value) {
	var auxHTML = '';
	if (value != "") {
		auxHTML += '<div class="fieldName">' + key + '</div>'
		auxHTML += '<div class="fieldValue">' + value + '</div>';
	}
	return auxHTML;
}
