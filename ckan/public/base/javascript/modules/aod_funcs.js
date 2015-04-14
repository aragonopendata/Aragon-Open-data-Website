	// mover la cabecera superior al hacer scroll
$(function(){
	$(window).scroll(function() {
		$html = $("html");
		
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
		//if (($( window ).width()>754) && ( scrollTop >= 160)){
		if (($( window ).width()>754) && ($(document).scrollTop() >= 160)){
			$('body').addClass('mini');
		}
		else{
			$('body').removeClass('mini');
		}
		/*if( scrollTop < 160 ){
			$('body').removeClass('mini');
		}else{
			$('body').addClass('mini');
		}*/
	});
	$("body").trigger('scroll');
});

function refinaAutocomplete() {
	$.ui.autocomplete.prototype._renderItem = function( ul, item) {
		return $( "<li></li>" )
			.data( "item.autocomplete", item )
			.append( "<a href='/catalogo/" + item.valor + "'>" + item.label + "</a>" )
			.appendTo( ul );
	};	
}

function changeOrder(newOrder) {
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
   
	if (currentUrl) {
		 // mirar si tiene ?
		if (currentUrl.indexOf('?') != -1) {
			window.location = currentUrl + "&" + txtToFind + "&" + newOrder ;
		} else {
			window.location = currentUrl + "?" + txtToFind + "&" + newOrder;
		}
	}
}


function tryToSelectOrder(orderType) {
	alert(orderType);
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
	refinaAutocomplete();

      //al inicio, quitarlo si tiene valor porque lo autorrellene el navegador de otras visitas	
  if (($("#cajaDeBusqInput").val() != "")) {
    $("#cajaDeBusqInput").css("background", "#FFFFFF");
  }
  
  $("#cajaDeBusqInput").on('blur', function() {
    if (($("#cajaDeBusqInput").val() != "")) {
      $("#cajaDeBusqInput").css("background", "#FFFFFF");
    }
  });

	var config  = {
		disable_search: true
	};
	
	//var valueIsEstadist = "bienal";

	var fOnChgChosen_changeLangHomer = function onChgChosen_changeLangHomer() {
		var idx = $("#langHOMERFilter")[0].selectedIndex;
		var valorLang = $("#langHOMERFilter")[0][idx].value;

		changeHomerLabels(valorLang);
		return false;
	}
	
	var fOnChgChosen = function onChgChosen() {
		var urlToGo = "/catalogo";
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
		if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaSPARQL") {
			window.location = "/portal/cliente-sparql";
		} else if ($("#tipoBusquedaFilter")[0][idxTipo].value == "zonaAPI") {
			window.location = "/portal/desarrolladores/api-ckan";
		} else {
			var newZone = $("#tipoBusquedaFilter")[0][idxTipo].value;
			if (newZone == "zonaInfoEstadistica") {
				window.location = "/catalogo/informacion-estadistica";
			} else {
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
		if (urlListParam.length == 3) {
			if (urlListParam[2] == "informacion-estadistica") {
					// o es info estadistica
				toggleZona("zonaInfoEstadistica");
				tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaInfoEstadistica");
			} else {
					// O es tema o es tipo
				tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
				tryToSelectItem($("#tipoFilter")[0], urlListParam[2]);
			}
	} else if (urlListParam.length == 4) {
				// O es tema+tipo o es tipo-estadistico/num
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
			var idxTema = $("#temaFilter")[0].selectedIndex;
			if (idxTema != 0) {
					// es tema+tipo
				tryToSelectItem($("#tipoFilter")[0], urlListParam[3]);
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
		}

		if (urlListParam.length >= 3) {
			if (urlListParam[2] != "informacion-estadistica") {
				activateZoneTipoBusqueda(urlListParam[2]);
			}
		} else {
			tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaTemaYTipo");
			toggleZona("zonaTemaYTipo");
		}
	} else {
		tryToSelectItem($("#tipoBusquedaFilter")[0], "zonaTemaYTipo");
		toggleZona("zonaTemaYTipo");
	}

	disEnableAllItemsForm(false);

	$("#temaFilter").chosen(config).change(fOnChgChosen);
	$("#tipoFilter").chosen(config).change(fOnChgChosen);

//	$("#tipoBusquedaFilter").chosenImage(config).change(fOnChgChosen_toggle);
	$("#tipoBusquedaFilter").chosen(config).chosenImage().change(fOnChgChosen_toggle);

	$("#langHOMERFilter").chosen(config).change(fOnChgChosen_changeLangHomer);

	$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica_nivel1);

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

	var htmlCodeDatasets =getContadorHTML(datasetCount);
        var htmlCodeRecursos = getContadorHTML(resourceCount);
        $('#numDatasets').html(htmlCodeDatasets);
        $('#numRecursos').html(htmlCodeRecursos);

	if ($("#homerResults").html() != null) {
		doQueryHomer();
	}
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
	} else if (queriedTxt != '') {
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
}

function submitQuery() {
	disEnableAllItemsForm(true);
	$("#searchFormId").submit();
	return false;
}
