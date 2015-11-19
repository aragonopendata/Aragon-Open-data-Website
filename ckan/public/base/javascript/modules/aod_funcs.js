	// mover la cabecera superior al hacer scroll
//$(function(){

//Esta funcion hace los correspondientes cambios para cuando se haga 
function responsiveScroll() {
	$(window).scroll(function() {
		if ($(window).width()>=1012){
			$html = $("html");
			$('.mini .botones').css('top','35px');
			//Esto se debe de modificar ya que todos los navegadores lo pueden hacer de modo diferente
			/*if($html.hasClass('webkit')){
				var scrollTop = $("body")[0].scrollTop;
			}else if($html.hasClass('firefox')){
				var scrollTop = $("html")[0].scrollTop;
			}else{
				var scrollTop = $(document).scrollTop();
			
				//var scrollTop = $("body")[0].scrollTop;
				//var scrollTop = $("html")[0].scrollTop;
			}*/

		
			//Con window creo que pilla La barra de scroll ya que el lÃ­mite esta en 754 con lo que esta barra tiene 14 pixeles
			//if (($( window ).width()>754) && ($(document).scrollTop() >= 160)){
			if ($(document).scrollTop() >= 150){
				$('body').addClass('mini');
				//$('#anchoBanner').css('top', $(document).scrollTop()+'px');
				$('#anchoBanner').css({
					'position':'fixed',
					'top': '-10px',
					'height':$('.banner').height(),
					'width':'100%',
					'z-index':1110
				});
				$('.banner').css('left', (($(window).width()-$('.banner').width())/2)+'px');
			}
			else{
				$('body').removeClass('mini');
				$('.banner').removeAttr('style');
				$('#anchoBanner').removeAttr('style');
				$('#anchoBanner').css('background-color', '#76a1b8');
				if ($(document).scrollTop() >= 150){
					//alert('borrar el style del banner');
					$('.banner').removeAttr('style');
				}
			}
			/*if( scrollTop < 160 ){
				$('body').removeClass('mini');
			}else{
				$('body').addClass('mini');
			}*/
		}
		else{
			$('.mini .botones').removeAttr('style');
			$('.banner').removeAttr('style');
		}
	});
	$("body").trigger('scroll');
}
//});

function refinaAutocomplete() {
	$.ui.autocomplete.prototype._renderItem = function( ul, item) {
		return $( "<li></li>" )
			.data( "item.autocomplete", item )
			.append( "<a href='/catalogo/" + item.valor + "'>" + item.label + "</a>" )
			.appendTo( ul );
	};	
}

function changeOrder(newOrder, destinationUrl) {
	var txtToFind = '';
	var aux = window.location.search;
	var paramStr = aux.split('?');
	for (var itemStr=0; itemStr < paramStr.length; itemStr++) {
		if (paramStr[itemStr] != "") {
			var paramList = paramStr[itemStr].split("&");
			for (var item=0; item < paramList.length; item++) {
				var currentItem = paramList[item].split("=");
				if ((currentItem[0].toLowerCase() == "q")  && (currentItem.length > 1)) {
					txtToFind = "q=" + currentItem[1];
				}
			}
		}
	}
   
	if (destinationUrl) {
		window.location = destinationUrl + "?" + txtToFind + "&" + newOrder ;		
	} else {
		if (currentUrl) {
			 // mirar si tiene ?
			if (currentUrl.indexOf('?') != -1) {
				window.location = currentUrl + "&" + txtToFind + "&" + newOrder ;
			} else {
				window.location = currentUrl + "?" + txtToFind + "&" + newOrder;
			}
		}
	}
}


function tryToSelectOrder(orderType) {
	//alert(orderType);
}

function tryToSelectItem(obj, txt) {
	if (obj != null) {
		for (k =0 ; k < obj.length; k++) {
			if (obj[k].value == txt) {
				obj[k].selected = true;
			}
		}
	}
}

function changeHomerLabels(valorLang) {
	$("#labelBuscarHomer_es").addClass("oculto");
	$("#labelIdiomaHomer_es").addClass("oculto");
	$("#labelBuscarHomer_en").addClass("oculto");
	$("#labelIdiomaHomer_en").addClass("oculto");
	$("#labelBuscarHomer_fr").addClass("oculto");
	$("#labelIdiomaHomer_fr").addClass("oculto");
	$("#labelBuscarHomer_it").addClass("oculto");
	$("#labelIdiomaHomer_it").addClass("oculto");
	$("#labelBuscarHomer_el").addClass("oculto");
	$("#labelIdiomaHomer_el").addClass("oculto");
	$("#labelBuscarHomer_sl").addClass("oculto");
	$("#labelIdiomaHomer_sl").addClass("oculto");
	$("#labelBuscarHomer_sr").addClass("oculto");
	$("#labelIdiomaHomer_sr").addClass("oculto");

	$("#labelBuscarHomer_" + valorLang).toggleClass("oculto");
	$("#labelIdiomaHomer_" + valorLang).toggleClass("oculto");
}

$(document).ready(function() {
	pintaMenuBuscador();
	
	var pathname = window.location.pathname;
	if (pathname.indexOf("/portal/")<0){
		refinaAutocomplete();
	}

      //al inicio, quitarlo si tiene valor porque lo autorrellene el navegador de otras visitas	
  if (($("#cajaDeBusqInput").val() != "")) {
    $("#cajaDeBusqInput").css("background", "#FFFFFF");
  }
  
  $("#cajaDeBusqInput").on('blur', function() {
    if (($("#cajaDeBusqInput").val() != "")) {
      $("#cajaDeBusqInput").css("background", "#FFFFFF");
    }
  });
//  var ancho = $(window).width();
//  var alto = $(window).height();
//	alert('Ancho '+ancho+' y de alto '+alto);
	modificaComboBusqueda();
	
	resposiveResultadosDatasets();
	responsiveVisorDataset();
	responsiveScroll();
	responsiveOrganizacionPagina();
	marginTag();
	$(window).resize(function() {
		pintaMenuBuscador();
		modificaComboBusqueda();
		resposiveResultadosDatasets();
		responsiveVisorDataset();
		responsiveScroll();
		responsiveOrganizacionPagina();
		marginTag();
	});
	
	
	
	var config  = {
		disable_search: true
	};

	var fOnChgChosen_changeLangHomer = function onChgChosen_changeLangHomer() {
		var idx = $("#langHOMERFilter")[0].selectedIndex;
		var valorLang = $("#langHOMERFilter")[0][idx].value;

		changeHomerLabels(valorLang);
		return false;
	}
	
	var fOnChgChosen = function onChgChosen() {
		var urlToGo = "/catalogo";
		var idxBBDD = $("#bbddFilter")[0].selectedIndex;
		if (idxBBDD != 0) {
			urlToGo += "/base-datos/" + $("#bbddFilter")[0][idxBBDD].value;
		}
		var idxOrganizacion = $("#organizacionFilter")[0].selectedIndex;
		var idxOrganizacionTipo = $("#organizacionTipoFilter")[0].selectedIndex;
		if (idxOrganizacion != 0) {
			if (idxOrganizacionTipo != 0) {
				urlToGo += "/busqueda-organizacion/" + $("#organizacionFilter")[0][idxOrganizacion].value+"/"+$("#organizacionTipoFilter")[0][idxOrganizacionTipo].value;
			}
			else{
				urlToGo += "/busqueda-organizacion/" + $("#organizacionFilter")[0][idxOrganizacion].value;
			}
			
		}
		
		
		
		
		var idxTema = $("#temaFilter")[0].selectedIndex;
		if (idxTema != 0) {
			urlToGo += "/" + $("#temaFilter")[0][idxTema].value;
		}
		var idxTipo = $("#tipoFilter")[0].selectedIndex;
		if (idxTipo != 0) {
			urlToGo += "/" + $("#tipoFilter")[0][idxTipo].value;
		}
		window.location = urlToGo;
		return false;
	}

	var fOnChgChosen_toggle = function onChgChosen_toggle() {
		var idxTipo = $("#tipoBusquedaFilter")[0].selectedIndex;
		//alert('El tipo de busqueda es '+$("#tipoBusquedaFilter")[0][idxTipo].value);
		if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaSPARQL") {
			window.location = "/portal/cliente-sparql";
		} else if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaAPI") {
			window.location = "/portal/desarrolladores/api-ckan";
		}
		else if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaEtiquetas") {
			tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaEtiquetas");
			window.location = "/catalogo/etiqueta";
		}
		else if($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaBBDD"){
			//modicamos para que las options se queden seleccionadas
			/*$('#tipoBusquedaFilter').find('option:selected').removeAttr('selected');
			$('#tipoBusquedaFilter option[value=zonaBBDD]').attr('selected',true);
			$('#tipoBusquedaFilter_chosen .chosen-single span').text('Base de datos');*/
			tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaBBDD");
			//Vamos a la url correspondiente
			window.location = "/catalogo/base-datos";
		}
		else if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaOrganizacionYTipo"){
			tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaOrganizacionYTipo");
			//Vamos a la url correspondiente
			window.location = "/catalogo/busqueda-organizacion";
			
		}
		else {
			var newZone = $("#tipoBusquedaFilter")[0][idxTipo].value;
			if (newZone == "zonaInfoEstadistica") {
				window.location = "/catalogo/informacion-estadistica";
			}
			else if (newZone == "zonaTemaYTipo") {
				window.location = "/catalogo/catalogo.html";
			}
			else if (newZone == "zonaLibre") {
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaLibre");
				window.location = "/catalogo/busqueda-libre";
			}
			else {
				toggleZona($("#tipoBusquedaFilter")[0][idxTipo].value);
			}
		}
		return false;
	}

	var currentComboEstad = null;

	var fOnChgChosen_estadistica_nivel1 = function onChgChosen_estadistica_nivel1() {
		var urlToGo = "/catalogo";

		var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;
		if (idxGrupo != 0) {
			urlToGo += "/tema-estadistico/" + $("#estadisNivel1_Filter")[0][idxGrupo].value;
		}
		window.location = urlToGo;
		return false;
	}

	var fOnChgChosen_estadistica_nivel2 = function onChgChosen_estadistica_nivel2() {
		var urlToGo = "/catalogo";

		if (currentComboEstad) {
			var idxGrupo = $(currentComboEstad)[0].selectedIndex;
			if (idxGrupo != 0) {
				urlToGo += "/tema-estadistico/" + $(currentComboEstad)[0][idxGrupo].value;
			} else {
				var idxGrupoNivel1 = $("#estadisNivel1_Filter")[0].selectedIndex;
				urlToGo += "/tema-estadistico/" + $("#estadisNivel1_Filter")[0][idxGrupoNivel1].value;
			}
		}
		window.location = urlToGo;
		return false;
	}

	var urlListParam  = new Array();
	if (currentUrl) {
		urlListParam = currentUrl.split("/");
		//alert('El urlparam es '+urlListParam.length+ ' y la url actual es '+currentUrl);
		if (urlListParam.length == 3) {
			if (urlListParam[2] == "informacion-estadistica") {
					// o es info estadistica
				toggleZona("zonaInfoEstadistica");
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaInfoEstadistica");
			}
			else if (urlListParam[2] == "base-datos") {
					// o es bbdd
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaBBDD");
			}
			else if (urlListParam[2] == "etiqueta") {
					// o es busqueda de etiquetas
				$('#zonaTemaYTipo').addClass('oculto');
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaEtiquetas");
				//toggleAllZones();
			}
			else if (urlListParam[2] == "busqueda-libre") {
					// o es búsqueda libre
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaLibre");
			}   
			else {
				//alert('entramos por este sitio');
				//alert('urlListParam es '+urlListParam+' y tiene de longitud '+urlListParam.length);
				var parametrosURL  = new Array();
				var urlActual = window.location.toString();
				//alert('La url actual es '+urlActual);
				if (urlActual.indexOf('tags=')>=0) {
					$('div#tipoBusquedaFilter_chosen.chosen-container.chosen-container-single.chosen-container-single-nosearch.chosenImage-container').css('margin-bottom','15px');
					tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaEtiquetas");
					$('#zonaTemaYTipo').addClass('oculto');
					$('.search-form').prepend('<div id="tituloEtiqueta">Datos con la etiqueta '+gup('tags')+'</div>')
					//toggleAllZones();
					
				}
				else{
					// O es tema o es tipo
					tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
					tryToSelectItem($("#tipoFilter")[0], urlListParam[2]);
				}

			}
		} else if (urlListParam.length == 4) {
			// O es tema+tipo o es tipo-estadistico/num o es base-datos/tipobbdd
			//Miro aqui
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
			var idxTema = $("#temaFilter")[0].selectedIndex;
			if (idxTema != 0) {
					// es tema+tipo
				tryToSelectItem($("#tipoFilter")[0], urlListParam[3]);
			}
			//alert('cargado '+urlListParam[2]+'/'+urlListParam[3]);
			if (urlListParam[2] == "busqueda-libre"){
				var txtBusqueda = utf8_decode(unescape(urlListParam[3]));
				$("#cajaDeBusqInputLibre").val(txtBusqueda);
			}
			
			if (urlListParam[2] == "busqueda-organizacion") {
				// o es búsqueda organizacion
				$('#organizacionTipo').removeClass("oculto");
				tryToSelectItem($("#organizacionFilter")[0],urlListParam[3]);
				
			}

			if (urlListParam[2] == "tema-estadistico") {
				var auxTipoEstad = urlListParam[3].substr(0,2);
				var auxSubTipoEstad = urlListParam[3].substr(0,4);
				tryToSelectItem($("#estadisNivel1_Filter")[0], auxTipoEstad);
				if (auxTipoEstad.length == 2) {

					currentComboEstad = "#estadisNivel2_grp" + auxTipoEstad + "_Filter";
					var subnivelItem = $(currentComboEstad);
					if (subnivelItem) {
						tryToSelectItem(subnivelItem[0], auxSubTipoEstad);
						$(currentComboEstad + "Div").removeClass("oculto");
						subnivelItem.chosen(config).change(fOnChgChosen_estadistica_nivel2);
					}
				}
			}
			else if (urlListParam[2] == "base-datos") {
				tryToSelectItem($("#bbddFilter")[0], urlListParam[3]);
			}
			
		}else if ((urlListParam.length == 5) && (urlListParam[2] == "busqueda-organizacion")) {
			//Entramos en la busqueda por organizacion t por tipo de recursos
			$('#organizacionTipo').removeClass("oculto");
			tryToSelectItem($("#organizacionFilter")[0],urlListParam[3]);
			//alert ('aki es donde tiene que estar lo del tipo '+ urlListParam[4]);
			tryToSelectItem($("#organizacionTipoFilter")[0],urlListParam[4]);
		}
		

		if (urlListParam.length >= 3) {
			if (urlListParam[2] != "informacion-estadistica") {
				activateZoneTipoBusqueda(urlListParam[2]);
			}
			else if (urlListParam[2] != "base-datos") {
				activateZoneTipoBusqueda(urlListParam[2]);
			}
			else if (urlListParam[2] != "busqueda-libre") {
				activateZoneTipoBusqueda(urlListParam[2]);
			}
			if (urlListParam[2] == "etiqueta") {
					// o es busqueda de etiquetas
				//$('#zonaTemaYTipo').addClass('oculto');
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaEtiquetas");
				toggleAllZones();
			}
			
			if ((urlListParam.length == 5) && (urlListParam[2] == "busqueda-organizacion")) {
				//Entramos en la busqueda por organizacion t por tipo de recursos
				
				$('#organizacionTipo').removeClass("oculto");
				tryToSelectItem($("#organizacionFilter")[0],urlListParam[3]);
				//alert ('aki es donde tiene que estar lo del tipo '+ urlListParam[4]);
				tryToSelectItem($("#organizacionTipoFilter")[0],urlListParam[4]);
			}
			
			
			
			var parametrosURL  = new Array();
			var urlActual = window.location.toString();
			if (urlActual.indexOf('tags=')>=0) {
				
				$('div#tipoBusquedaFilter_chosen.chosen-container.chosen-container-single.chosen-container-single-nosearch.chosenImage-container').css('margin-bottom','15px');
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaEtiquetas");
				$('#zonaTemaYTipo').addClass('oculto');
				//toggleAllZones();
			}
			
			
		}
		else {
			tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaTemaYTipo");
			toggleZona("zonaTemaYTipo");
		}
	} else {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaTemaYTipo");
		toggleZona("zonaTemaYTipo");
	}

	disEnableAllItemsForm(false);

	if ($("#temaFilter").length > 0){
		$("#temaFilter").chosen(config).change(fOnChgChosen);
	}
	if ($("#tipoFilter").length > 0){
		$("#tipoFilter").chosen(config).change(fOnChgChosen);
	}
	if ($("#bbddFilter").length > 0){
		$("#bbddFilter").chosen(config).change(fOnChgChosen);
	}
	

//	$("#tipoBusquedaFilter").chosenImage(config).change(fOnChgChosen_toggle);
	if ($("#tipoBusquedaFilter").length > 0){
		$("#tipoBusquedaFilter").chosen(config).chosenImage().change(fOnChgChosen_toggle);
	}

	if ($("#langHOMERFilter").length > 0){
		$("#langHOMERFilter").chosen(config).change(fOnChgChosen_changeLangHomer);
	}

	if ($("#estadisNivel1_Filter").length > 0){
		$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica_nivel1);
	}

	if ($("#organizacionTipoFilter").length > 0){
		$("#organizacionTipoFilter").chosen(config).change(fOnChgChosen);
	}
	
	if ($("#organizacionFilter").length > 0){
		
		
		
		$("#organizacionFilter").chosen(config).change(fOnChgChosen);
		//Si se cambia "reseteamos" el filtro para que no salga
		if ($('#organizacionFilter option:selected').val() != ""){
			tryToSelectItem($("#organizacionTipoFilter")[0],"");
		}
	}
	
	

   $('#txtHOMER').keypress(function(event) {
        if (event.keyCode == 13) {
            submitHomer();
        }
    });

   $('#cajaDeBusqInputLibre').keypress(function(event) {
        if (event.keyCode == 13) {
            submitTxtQuery();
        }
    });

//		if (window.location.href.indexOf("catalogo")>=0){
			$( "#cajaDeBusqInput" ).autocomplete({
				source:function(request, response) {
					$.ajax({
							url: "/catalogo/api/2/util/dataset/autocomplete?incomplete=%" + $("#cajaDeBusqInput").val() + "%",
						dataType: "jsonp",
						success: function (data) {
						response($.map(data.ResultSet.Result, 
							function(item)	{
								return {
									label: item.title,
									valor: item.name,
									value: item.title
								};
							}
						));
						}			
						    })
					 },
				minLength: 1,
				open: function(event, ui) {
							$(this).autocomplete("widget").css({
								"width": 425
							});
						},
				select: function( event, item) {
					$("#cajaBusqBanner").attr("action",  "/catalogo/" + item.item.valor);
					$("#cajaDeBusqInput").val("");
					$("#cajaBusqBanner").submit();
				}
			});
			initializeDashboard();
			initializeEditor();
			loadComboboxesVistas();
			
//		}
    




    if (document.getElementById("zonaVentanaDatosDescargados1")) {
	$.ajax({
			url: "/catalogo/api/mostDownloadedDataset",
			dataType: "jsonp",
			success: function (data) {
				var htmlCode = '';
				for (var ii = 0; ii < 3; ii++) {
					htmlCode += '<div><a href="/catalogo/' + (data[ii].name) + '" title="' + (data[ii].title) + '">' + (data[ii].title) + '</a></div>';
					if (ii != 2) {
						htmlCode += '<div class="separadorVentana"></div>';
					}
				}
				$('#zonaVentanaDatosDescargados1').html(htmlCode);
			}
		     });
    }

    if (document.getElementById("zonaVentanaDatosRecientes1")) {
	$.ajax({
			url: "/catalogo/api/mostRecentDataset",
			dataType: "jsonp",
			success: function (data) {
				var htmlCode = '';
				for (var ii = 0; ii < 3; ii++) {
					htmlCode += '<div><a href="/catalogo/' + (data[ii].name) + '" title="' + (data[ii].title) + '">' + (data[ii].title) + '</a></div>';
					if (ii != 2) {
						htmlCode += '<div class="separadorVentana"></div>';
					}
				}
				$('#zonaVentanaDatosRecientes1').html(htmlCode);
			}
		     });
    }

    if (document.getElementById("numDatasets")) {
//	$.ajax({
//			url: "/catalogo/api/getDataCount",
//			dataType: "jsonp",
//			success: function (data) {
//				var htmlCodeDatasets = getContadorHTML(data[0].datasetCount);
//				var htmlCodeRecursos = getContadorHTML(data[0].resourceCount);
//				$('#numDatasets').html(htmlCodeDatasets);
//				$('#numRecursos').html(htmlCodeRecursos);
//			},
//			error: function (data) {
//				var htmlCodeDatasets = getContadorHTML(1709);
//				var htmlCodeRecursos = getContadorHTML(2724);
//				$('#numDatasets').html(htmlCodeDatasets);
//				$('#numRecursos').html(htmlCodeRecursos);
//			}
//	   });
			var htmlCodeDatasets =getContadorHTML(datasetCount);
			var htmlCodeRecursos = getContadorHTML(resourceCount);
			$('#numDatasets').html(htmlCodeDatasets);
			$('#numRecursos').html(htmlCodeRecursos);
    }

	if ($("#homerResults").html() != null) {
		doQueryHomer();
	}
	
	marginTag();
	
});

function activateZoneTipoBusqueda(txtParam) {
	var currentUrl = window.location.toString();
	var queriedTxt = "";

	urlListParamPrev = currentUrl.split("?");

	if (urlListParamPrev.length > 1) {
		urlListParam = urlListParamPrev[1].split("&");

		for (var i = 0; i < urlListParam.length; i++) {
			var keyValue = urlListParam[i].split("=");
			switch (keyValue[0]) {
				case 'q': (keyValue[1] ? queriedTxt = decodeURI(decodeURI(keyValue[1])).replace(/\+/g, " ") : j=0); break;
			}
		}
	}

	if (txtParam == "searchHOMER") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaHOMER");
		toggleZona("zonaHOMER");
	} else if (txtParam == "tema-estadistico") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaInfoEstadistica");
		toggleZona("zonaInfoEstadistica");
	}
	else if (txtParam == "informacion-estadistica") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaInfoEstadistica");
		toggleZona("zonaInfoEstadistica");
	}
	else if (txtParam == "busqueda-organizacion") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaOrganizacionYTipo");
		toggleZona("zonaOrganizacionYTipo");
	}
	else if (txtParam == "base-datos") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaBBDD");
		toggleZona("zonaBBDD");
		
		
		urlListParam = currentUrl.split("/");
		if (urlListParam.length==6){
			tryToSelectItem($("#bbddFilter")[0], urlListParam[5]);
		}
	}
	else if (txtParam == "busqueda-libre") {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaLibre");
		toggleZona("zonaLibre");
	}
	else if (queriedTxt != '') {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaLibre");
		toggleZona("zonaLibre");
		$("#cajaDeBusqInputLibre").val(queriedTxt);
	} else {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaTemaYTipo");
		toggleZona("zonaTemaYTipo");
	}
}

function toggleAllZones() {
	$("#zonaTemaYTipo").addClass("oculto");
	$("#zonaInfoEstadistica").addClass("oculto");
	$("#zonaLibre").addClass("oculto");
	$("#zonaHOMER").addClass("oculto");
	$("#zonaBBDD").addClass("oculto");
	$("#zonaOrganizacionYTipo").addClass("oculto");
}

function toggleZona(id) {
	toggleAllZones();
	$("#" + id).toggleClass("oculto");
/*
	if (id == "zonaHOMER") {
		$("#logoHomerCabecera").removeClass("oculto");
	} else {
		$("#logoHomerCabecera").addClass("oculto");
	}*/
}

function getContadorDigit(number) {
	var htmlCode = '';
	if ((number >=0) && (number <=9)) {
		htmlCode = '<img src="/public/i/contador/' + number + '.png" alt="' + number + '">';
	}
	return htmlCode;
}

function getContadorHTML(number) {
	var htmlCode = '';
	var numDigitos = 0;
	var aux = number;
	while (aux > 9) {
		htmlCode = getContadorDigit(aux % 10) + htmlCode;
		aux = Math.floor(aux /10);
		numDigitos++;
	}
	htmlCode = getContadorDigit(aux) + htmlCode;
	numDigitos++;
	
	for (var j = numDigitos; j < 8; j++) {
		htmlCode = '<img src="/public/i/contador/0_off.png" alt="0">' + htmlCode;
	}
	
	return htmlCode;
}

function submitHomer() {
	$('form').attr('action', '/catalogo/searchHOMER');
	submitQuery();
}

function submitTxtQuery() {
	submitQuery();
}

function disEnableAllItemsForm(disEnab) {
  $('div.oculto > input').attr("disabled",disEnab);
  $('div.oculto > select').attr("disabled",disEnab);
  $('div.oculto > div > input').attr("disabled",disEnab);
  $('div.oculto > div > select').attr("disabled",disEnab);
  $('div.oculto > div > ul > li > input').attr("disabled",disEnab);
  $('div.oculto > div > ul > li > select').attr("disabled",disEnab);
  $('#tipoBusquedaFilter').attr("disabled",disEnab);
  $('form > select:hidden').attr("disabled",disEnab);
  
  if ($("#autocomplete_eurovoc")){
    $('#autocomplete_eurovoc').attr("disabled",disEnab);
  }
}

function submitQuery() {
	disEnableAllItemsForm(true);
	if (document.getElementById("tipoBusquedaFilter").value == "zonaHOMER"){
		$("#searchFormId").submit();
	}
	else{
		if (document.getElementsByName("q").length==1){
			window.location = '/catalogo/busqueda-libre/'+document.getElementsByName("q")[0].value;
		}
		else{
			window.location = '/catalogo/busqueda-libre/'+document.getElementsByName("q")[1].value;
		}
	}
	return false;
}


function utf8_encode(argString) {
  //  discuss at: http://phpjs.org/functions/utf8_encode/
  // original by: Webtoolkit.info (http://www.webtoolkit.info/)
  // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // improved by: sowberry
  // improved by: Jack
  // improved by: Yves Sucaet
  // improved by: kirilloid
  // bugfixed by: Onno Marsman
  // bugfixed by: Onno Marsman
  // bugfixed by: Ulrich
  // bugfixed by: Rafal Kukawski
  // bugfixed by: kirilloid
  //   example 1: utf8_encode('Kevin van Zonneveld');
  //   returns 1: 'Kevin van Zonneveld'

  if (argString === null || typeof argString === 'undefined') {
    return '';
  }

  var string = (argString + ''); // .replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  var utftext = '',
    start, end, stringl = 0;

  start = end = 0;
  stringl = string.length;
  for (var n = 0; n < stringl; n++) {
    var c1 = string.charCodeAt(n);
    var enc = null;

    if (c1 < 128) {
      end++;
    } else if (c1 > 127 && c1 < 2048) {
      enc = String.fromCharCode(
        (c1 >> 6) | 192, (c1 & 63) | 128
      );
    } else if ((c1 & 0xF800) != 0xD800) {
      enc = String.fromCharCode(
        (c1 >> 12) | 224, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128
      );
    } else { // surrogate pairs
      if ((c1 & 0xFC00) != 0xD800) {
        throw new RangeError('Unmatched trail surrogate at ' + n);
      }
      var c2 = string.charCodeAt(++n);
      if ((c2 & 0xFC00) != 0xDC00) {
        throw new RangeError('Unmatched lead surrogate at ' + (n - 1));
      }
      c1 = ((c1 & 0x3FF) << 10) + (c2 & 0x3FF) + 0x10000;
      enc = String.fromCharCode(
        (c1 >> 18) | 240, ((c1 >> 12) & 63) | 128, ((c1 >> 6) & 63) | 128, (c1 & 63) | 128
      );
    }
    if (enc !== null) {
      if (end > start) {
        utftext += string.slice(start, end);
      }
      utftext += enc;
      start = end = n + 1;
    }
  }

  if (end > start) {
    utftext += string.slice(start, stringl);
  }

  return utftext;
}

function utf8_decode(str_data) {
  //  discuss at: http://phpjs.org/functions/utf8_decode/
  // original by: Webtoolkit.info (http://www.webtoolkit.info/)
  //    input by: Aman Gupta
  //    input by: Brett Zamir (http://brett-zamir.me)
  // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // improved by: Norman "zEh" Fuchs
  // bugfixed by: hitwork
  // bugfixed by: Onno Marsman
  // bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // bugfixed by: kirilloid
  //   example 1: utf8_decode('Kevin van Zonneveld');
  //   returns 1: 'Kevin van Zonneveld'

  var tmp_arr = [],
    i = 0,
    ac = 0,
    c1 = 0,
    c2 = 0,
    c3 = 0,
    c4 = 0;

  str_data += '';

  while (i < str_data.length) {
    c1 = str_data.charCodeAt(i);
    if (c1 <= 191) {
      tmp_arr[ac++] = String.fromCharCode(c1);
      i++;
    } else if (c1 <= 223) {
      c2 = str_data.charCodeAt(i + 1);
      tmp_arr[ac++] = String.fromCharCode(((c1 & 31) << 6) | (c2 & 63));
      i += 2;
    } else if (c1 <= 239) {
      // http://en.wikipedia.org/wiki/UTF-8#Codepage_layout
      c2 = str_data.charCodeAt(i + 1);
      c3 = str_data.charCodeAt(i + 2);
      tmp_arr[ac++] = String.fromCharCode(((c1 & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
      i += 3;
    } else {
      c2 = str_data.charCodeAt(i + 1);
      c3 = str_data.charCodeAt(i + 2);
      c4 = str_data.charCodeAt(i + 3);
      c1 = ((c1 & 7) << 18) | ((c2 & 63) << 12) | ((c3 & 63) << 6) | (c4 & 63);
      c1 -= 0x10000;
      tmp_arr[ac++] = String.fromCharCode(0xD800 | ((c1 >> 10) & 0x3FF));
      tmp_arr[ac++] = String.fromCharCode(0xDC00 | (c1 & 0x3FF));
      i += 4;
    }
  }

  return tmp_arr.join('');
}


//Funcion que añade al combo box tipoBusquedaFilter marginbotton 15px cuando la url sea de la busqueda de tag.
function marginTag(){
	var urlListParam  = new Array();
	var currentUrl = window.location.toString();
	if (currentUrl) {
		urlListParam = currentUrl.split("?");
		if ((urlListParam.length == 2) && (urlListParam[1].indexOf('tags')>=0)){
			$('div#tipoBusquedaFilter_chosen.chosen-container.chosen-container-single.chosen-container-single-nosearch.chosenImage-container').css('margin-bottom','15px');
		}
	}
}

//http://stackoverflow.com/questions/1144783/replacing-all-occurrences-of-a-string-in-javascript
function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}
//http://stackoverflow.com/questions/1144783/replacing-all-occurrences-of-a-string-in-javascript
function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}


//Funcion que devuelve un parametro de la url
//http://www.anieto2k.com/2006/08/17/coge-los-parametros-de-tu-url-con-javascript/
function gup( name ){
	var regexS = "[\\?&]"+name+"=([^&#]*)";
	var regex = new RegExp ( regexS );
	var tmpURL = window.location.href;
	var results = regex.exec( tmpURL );
	if( results == null )
		return "";
	else{
		var devolver = utf8_decode(unescape(results[1]));
		devolver = replaceAll(devolver, '+', ' ');
		return devolver;
	}
}


// cookies function from http://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
  }
  return "";
}


function isEmpty(value){
  return (value == null || value === '');
}
//Esta funcion pinta el menu de buscador según si esta usuario logueado o no
function pintaMenuBuscador(){
	var login=getCookie('auth_tkt');
	//Borramos el menu para pintarlo según el resultado de la cookien que contiene si estamos logueados
	$(".bannerBuscador").empty();
	if (isEmpty(login)){
		//Pintamos el menu para loguearse
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><button class="btn-search" type="submit">Buscar</button><a href="/catalogo/user/login" title="Iniciar Sesión"><img src="/public/i/login.jpg" alt="Iniciar Sesión" class="btn-login"></a></form>');
	}
	else{
		//Pintamos el menu cuando estamos logueados
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><a href="/catalogo/pizarra" title="Pizarra de administración"><img src="/public/i/dashboard.jpg" alt="Pizarra de administración" class="btn-login"></a><a href="/catalogo/user/_logout" title="Salir"><img src="/public/i/logout.jpg" alt="Salir" class="btn-login"></a></form>');
	}
	if ($(window).width()>1024){
		//Este div se usa para que quede centrado
		$('<div id="anchoBanner" style="background-color: #76a1b8;"></div>').insertBefore('.banner');
		$('.banner').appendTo('#anchoBanner');
		//Borramos los #anchoBanner internos que nos guarrean el codigo si andamos agrandando o empequeñeciendo la ventana
		$('#anchoBanner #anchoBanner').remove();
	}
}


//Función que sirve para redimensionar el segundo combobox en la búsqueda de estadística
function redimensionaComboEstadistica(){
	if ($('select#estadisNivel1_Filter').val()!=null){
		$('select#estadisNivel1_Filter').on('change',function(){
			var filtro = $(this).val();;
			var selector = "#estadisNivel2_grp"+filtro+"_Filter_chosen";
			if ($(window).width()<840) {
				var ancho = $('.tablaResultadosDataset').width();
				$(selector).css('width', ancho+'px');
			}
			else{
				$(selector).css('width', '180px');
			}
		});
	}
}


//Esta función mueve el combobox de búsqueda si es inferior a 840 px
function modificaComboBusqueda(){
	if ($('.chosen-single span:contains("Base de datos")').length){
		//alert('Hacemos grandre el filtro de base de datos');
		//$('.filtro').attr("style","width: 525px !important;");
		//$('.filtro').width(525);
	}
	
	if (($(window).width()<=840) && ($(".searchTypesOptions .d_d ").length)){
		//$(".buscaDatos .module").prepend('<div class="busquedaTipo"><img src="/public/i/buscaDatos/filtradoPor.png" alt="FILTRADO POR" title="Filtrado por" style="height:11px;"></div>');
		$(".buscaDatos .module").prepend('<div class="busquedaTipo"></div>');
		$(".busquedaTipo").css('padding-bottom', '15px');
		$(".busquedaTipo").append($(".searchTypesOptions .d_d "));
		$(".busquedaTipo").append($('.busquedaTipo li select'));
		$(".busquedaTipo").append($('.busquedaTipo li #tipoBusquedaFilter_chosen'));
		$(".busquedaTipo li").remove();
	}
	//else if (($(window).width()>840) && ($(".searchTypesOptions .d_d ").length==0)) {
	else if (($(window).width()>840) && ($(".busquedaTipo").length>0)) {
		location.reload();
	}
	
	//Esto lo uso para cuando tenga que recargar la web
	if (($(window).width()<684) && ($('.filtro img').is(":visible"))){
		$(".busquedaTipo").prepend('<div class="recargando"></div>');
	}
	
	//if ($(window).width()<684) {
	if ($(window).width()<840) {
		$('.filtro img').hide();
		$('.busquedaTipo img').hide();
		//El mismo ancho que la tabla
		var ancho = $('.tablaResultadosDataset').width();
		if (ancho == null){
			ancho = $(window).width()-20;
		}
		$('.busquedaTipo').removeAttr('style');
		$('.busquedaTipo').css('width', ancho+'px');
		$('.chosen-container').css('width', ancho+'px');
		$('.chosen-drop').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('.busquedaTipo');
		$('#tipoBusquedaFilter').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#tipoBusquedaFilter');
		$('.filtro').removeAttr('style');
		$('.filtro').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('.filtro');
		$('#temaFilter').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#temaFilter');
		$('#tipoFilter').css('width', ancho+'px'); 
		aniadePropertiesParaAlinearInputYSelect('#tipoFilter');
		$('#bbddFilter').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#bbddFilter');
		$('#estadisNivel1_Filter').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel1_Filter');
		$('#cajaDeBusqInputLibre').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#cajaDeBusqInputLibre');
		$('#cajaDeBusqInputLibre').attr("placeholder", "Término de búsqueda  ");
		$('#txtHOMER').css('width', ancho+'px');
		$('#txtHOMER').css('margin-bottom', '15px');
		$('#txtHOMER').attr("placeholder", "Término de búsqueda en HOMER  ");
		$('#txtHOMER').css('height','20px');
		aniadePropertiesParaAlinearInputYSelect('#txtHOMER');
		$('#langHOMERFilter').css('width', (ancho*85)/100+'px');
		
		
		$('#estadisNivel2_grp01_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp02_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp03_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp04_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp05_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp06_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp07_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp08_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp09_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp10_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp11_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp12_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp13_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp14_Filter').css('width', ancho+'px');
		$('#estadisNivel2_grp15_Filter').css('width', ancho+'px');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp01_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp02_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp03_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp04_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp05_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp06_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp07_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp08_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp09_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp10_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp11_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp12_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp13_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp14_Filter');
		aniadePropertiesParaAlinearInputYSelect('#estadisNivel2_grp15_Filter');
		$('img[alt="BUSCAR EN HOMER"]').removeClass('i_i');
		$('img[alt="BUSCAR EN HOMER"]').css('float', 'right');
		$('img[alt="BUSCAR EN HOMER"]').css('margin-top', '-36px');
	}
	if(($(window).width()>=840) && ($('.recargando').length>0 ))  {
		location.reload();
	}
}

//Esta función añade a las properties necesarias para que los input y los combos se vean alineados, selector sera el el selector por ejemplo .filtro
function aniadePropertiesParaAlinearInputYSelect(selector){
	//$(selector).css('padding', '0');
	//$(selector).css('margin', '0');
	$(selector).css('-moz-box-sizing', 'border-box');
	$(selector).css('-webkit-box-sizing', 'border-box');
	$(selector).css('box-sizing', 'border-box');
	//$(selector).css('float', 'right');
}

//Esta función borra la columna según cual sea su ancho
function resposiveResultadosDatasets(){
	
	$(".tablaResultadosDataset th:nth-child(2)").show();
	$(".tablaResultadosDataset td:nth-child(2)").show();
	$(".tablaResultadosDataset th:nth-child(3)").show();
	$(".tablaResultadosDataset td:nth-child(3)").show();
	
	//Borramos la columna de nº de accesos
	if ($(window).width()<800) {
		$(".tablaResultadosDataset th:nth-child(2)").hide();
		$(".tablaResultadosDataset td:nth-child(2)").hide();
		
		//Borramos la fecha
		if ($(window).width()<741) {
			$(".tablaResultadosDataset th:nth-child(3)").hide();
			$(".tablaResultadosDataset td:nth-child(3)").hide();
		}
	}
}


//Esta funcion sirve para hacer responsive o no 
function responsiveVisorDataset(){
	if ($(".previewZone").length>0 ){
		if ($(window).width()<1024) {
			$(".previewZone").hide();
			$('.metadataZone').css('margin','auto');
			$('.resourceZone').css({
				'width': $('.metadataZone').width()+'px',
				'margin-right':'auto',
				'margin-left':'auto',
				'margin-bottom':'10px',
				'margin-top':'10px'
			});
		}
		else{
			$(".previewZone").show();
			$('.metadataZone').removeAttr('style');
			$('.resourceZone').removeAttr('style');
		}
	}
}

//Esta función sirve para hacer responsive el apartado la hoja de una organización
function responsiveOrganizacionPagina(){
	//Comprobamos si estamos en una organizacion para poder hacer responsive
	if (window.location.href.indexOf('opendata.aragon.es/catalogo/organizacion/')>=0){
		if ($(window).width()>1024){
			//Comprobamos si se ha creado el div con id organizacionResponsive (lo usamos para meter el contenido responsive)
			if ($('#organizacionResponsive').length>0){
				$('#organizacionResponsive').hide();
				$('.contenidoDashboard table').show();
			}
			else{ //Aunque se vera
				$('.contenidoDashboard table').show();
			}
		}
		else{
			//Comprobamos si se ha creado el div con id organizacionResponsive (lo usamos para meter el contenido responsive)
			if ($('#organizacionResponsive').length>0){
				$('#organizacionResponsive').show();
				$('.contenidoDashboard table').hide();
			}
			else{ //Si no esta creado el id con el contenido de los datos de la tabla lo creamos
				var table = $('.contenidoDashboard table')[0];
				var key = new Array();
				var value = new Array();
				for (var i = 0, row; row = table.rows[i]; i++) {
					//iterate through rows
					//rows would be accessed using the "row" variable assigned in the for loop
					key.push(row.cells[0].innerHTML);
					value.push(row.cells[1].innerHTML);
				}
				$('<div id="organizacionResponsive"> </div>').insertAfter('.contenidoDashboard table');
				$('.contenidoDashboard table').hide();
				var contenidoOrganizacion="";
				for (var i=0; i <key.length; i++) {
					contenidoOrganizacion += key[i] + '<div style="margin-bottom: 10px;">&nbsp;</div>';
					contenidoOrganizacion += value[i] + "<br>";
				}
				$('#organizacionResponsive').append(contenidoOrganizacion);
			}
		}
	}
}
