var txtHomer = "*";
var langHomer = "es";
var startHomer = 0;
var rowsHomer = 20;
var sortHomer = "portal";
var sortTypeHomer = "asc";

function parseInitialHomerParams() {
	var currentUrl = window.location.toString();

	var urlListParamPrev  = new Array();
	var urlListParam  = new Array();
	urlListParamPrev = currentUrl.split("?");

	if (urlListParamPrev.length > 1) {

		urlListParam = urlListParamPrev[1].split("&");

		for (var i = 0; i < urlListParam.length; i++) {
			var keyValue = urlListParam[i].split("=");
			switch (keyValue[0]) {
				case 'txtHOMER': (keyValue[1] ? txtHomer = decodeURI(decodeURI(keyValue[1])).replace(/\+/g, " ") : j=0); break;
				case 'langHOMERFilter': (keyValue[1] ? langHomer = keyValue[1] : j=0); break;
				case 'startHOMER': (keyValue[1] ? startHomer = keyValue[1] : j=0); break;
				case 'rowsHOMER': (keyValue[1] ? rowsHomer = keyValue[1] : j=0); break;
				case 'sortHOMER': (keyValue[1] ? sortHomer = keyValue[1] : j=0); break;
				case 'sortTypeHOMER': (keyValue[1] ? sortTypeHomer = keyValue[1] : j=0); break;
			}
		}
	}
}

function getPaginationHomer(totalResults) {
	var htmlCode = '';

	var urlbase = '/catalogo/searchHOMER?txtHOMER=' + txtHomer + '&langHOMERFilter=' + langHomer;
	urlbase += '&sortHOMER=' + sortHomer + '&sortTypeHOMER=' + sortTypeHomer + '&startHOMER=';
	var currentPage = Math.floor(startHomer / rowsHomer) + 1;
	var totalPages = Math.ceil(totalResults / rowsHomer);

	if (totalPages > 1) {
		var prevIndex = Math.max(1, currentPage-2);
		var postIndex = Math.min(totalPages, currentPage+2);

		htmlCode += '<div class="pagination pagination-centered"><ul>';

		if (currentPage > 1) {
			htmlCode += '<li><a href="' + urlbase + ((currentPage-2)*rowsHomer) + '">«</a></li>';
		}
		if (prevIndex == 2) {
			htmlCode += '<li><a href="' + urlbase + '0">1</a></li>';
		}

		if (prevIndex >= 3) {
			htmlCode += '<li><a href="' + urlbase + '0">1</a></li>';
			htmlCode += '<li class="disabled"><a href="#">...</a></li>';
		}

		for (var jj = prevIndex; jj <= postIndex; jj++) {
			htmlCode += '<li';
			if (jj == currentPage) {
				htmlCode += ' class="active"';
			}
			htmlCode += '><a href="' + urlbase + ((jj-1)*rowsHomer) + '">' + jj + '</a></li>';
		}

		if (postIndex == totalPages-1) {
			htmlCode += '<li><a href="' + urlbase + ((totalPages-1)*rowsHomer) + '">' + totalPages+ '</a></li>';
		}

		if (postIndex < totalPages-1) {
			htmlCode += '<li class="disabled"><a href="#">...</a></li>';
			htmlCode += '<li><a href="' + urlbase + ((totalPages-1)*rowsHomer) + '">' + totalPages+ '</a></li>';
		}

		if (currentPage < totalPages) {
			htmlCode += '<li><a href="' + urlbase + ((currentPage)*rowsHomer) + '">»</a></li>';
		}

		htmlCode += '</ul></div>';
	}
	return htmlCode;
}

function changeOrderHomer(newOrderType, newSortType) {
	var urlbase = '/catalogo/searchHOMER?txtHOMER=' + txtHomer + '&langHOMERFilter=' + langHomer;
	urlbase += '&sortHOMER=' + newOrderType + '&sortTypeHOMER=' + newSortType + '&startHOMER=' + startHomer;
	window.location = urlbase;
}

function getOrderButtonsHTML(tipo) {
	var htmlCode = "";
	var asc_selected = false;
	var desc_selected = false;

	if (tipo == sortHomer) {
		if (sortTypeHomer == "asc") {
			asc_selected = true;
		} else if (sortTypeHomer == "desc") {
			desc_selected = true;
		}
	}
	htmlCode += "<ul class=\"d_d\">";
	htmlCode += "	<li><a href=\"javascript:changeOrderHomer('" + tipo + "','asc')\"  title=\"Orden ascendente\">";
	if (asc_selected) {
		htmlCode += "			<img src=\"/public/i/buscaDatos/flechaBlancaUp.png\" alt=\"Orden ascendente\">";
	} else {
		htmlCode += "			<img src=\"/public/i/buscaDatos/flechaAzulUp.png\" alt=\"Orden ascendente\">";
	}
	htmlCode += "	</a></li>";
	htmlCode += "	<li><a href=\"javascript:changeOrderHomer('" + tipo + "','desc')\"  title=\"Orden descendente\">";
	if (desc_selected) {
		htmlCode += "			<img src=\"/public/i/buscaDatos/flechaBlancaDown.png\" alt=\"Orden descendente\">";
	} else {
		htmlCode += "			<img src=\"/public/i/buscaDatos/flechaAzulDown.png\" alt=\"Orden descendente\">";
	}
	htmlCode += "	 </a></li>";
	htmlCode += "</ul>";
	return htmlCode;
}

function doQueryHomer() {
	parseInitialHomerParams();

	if (txtHomer != "*") {
		$("#txtHOMER").val(txtHomer);
	}
	tryToSelectItem($("#langHOMERFilter")[0], langHomer);
	$("#langHOMERFilter").trigger("chosen:updated")

	changeHomerLabels(langHomer);

	var txtABuscar = '*';
	if (txtHomer != "*") {
    txtABuscar = txtHomer + '&lang=' + langHomer;
  }

  var queryHomer = '/proxyHomer?q=' + txtABuscar + '&sort=' + sortHomer + '%20' + sortTypeHomer;
	queryHomer += '&start=' + startHomer + '&rows=' + rowsHomer + '&wt=xml';

	//tryToSelectItem($("#langHOMERFilter")[0], urlListParam[2]);

	$.ajax({
		url: queryHomer,
		dataType: "xml",
		success: function (data) {
			var textHTML = "";

			var homerCount = $(data).find("result").attr("numFound");

			if (homerCount < 1) {
				textHTML = "No se encontraron resultados en HOMER";
			} else { 
				if (homerCount > 1) {
					tituloHTML = "Encontrados " + homerCount + " resultados en HOMER";
				} else {
					tituloHTML = "Encontrado " + homerCount + " resultado en HOMER";
				}
				textHTML += "<table class='tablaResultadosDataset'>";
				textHTML += "<tr>";
				textHTML += "<th class='cabeceraTablaResultadosDataset'>";
				textHTML += "<div class='labelCabeceraTablaResultadosHomer'>" + tituloHTML;
				textHTML += getOrderButtonsHTML("title") + "</div></th>";
				textHTML += "<th class='cabeceraTablaResultadosDataset centrado tamPocoEstrecho'>";
				textHTML += "<div class='labelCabeceraTablaResultadosHomer'>Portal";
				textHTML += getOrderButtonsHTML("portal") + "</div></th>";
				textHTML += "<th class='cabeceraTablaResultadosDataset centrado tamMuyEstrecho'>";
				textHTML += "<div class='labelCabeceraTablaResultadosHomer'>Idioma";
				textHTML += getOrderButtonsHTML("language") + "</div></th>";
				textHTML += "</tr>";
				$(data).find('doc').each(function() {

//						var author = "-";
//						var descript = "-";
					var titulo = "-";
					var portal = "-";
					var enlace = "";
					var langu = "-";

/*					$(this).find("arr").each(function() {

            if ($(this).attr("name") == "author") {
							author = $(this).text();
						}
					});*/
					$(this).find("str").each(function() {
/*             if ($(this).attr("name") == "description") {
							descript = $(this).text();
						}*/
            if ($(this).attr("name") == "title") {
							title = $(this).text();
						}
            if ($(this).attr("name") == "package_id") {
							enlace = "/catalogo/detallesHOMER/" + $(this).text();
						}
            if ($(this).attr("name") == "portal") {
							portal = $(this).text();
						}
            if ($(this).attr("name") == "language") {
							langu = $(this).text();
						}
					});

					textHTML += "<tr>";
					if (enlace != "") {
						textHTML += "<td class='izquierda'><a href='" + enlace + "' title='" + title + "'>" + title + "</a></td>";
					} else {
						textHTML += "<td class='izquierda'>" + title + "</td>";
					}
					textHTML += "<td>" + portal + "</td>";
					textHTML += "<td>" + langu + "</td>";
					textHTML += "</tr>";
				});
				textHTML += "</table>";
			}

			textHTML += getPaginationHomer(homerCount);
			$("#homerResults").html(textHTML);

		},
		error: function (data,textStatus,  errorThrown) {
			$("#homerResults").html("No se ha podido obtener los resultados de HOMER");
		}
	});
}
