	// mover la cabecera superior al hacer scroll
$(function(){
	$(window).scroll(function() {
		$html = $("html");
		if($html.hasClass('webkit')){
			var scrollTop = $("body")[0].scrollTop;
		}else if($html.hasClass('firefox')){
			var scrollTop = $("html")[0].scrollTop;
		}else{
			var scrollTop = $("html")[0].scrollTop;
		}

		if( scrollTop < 160 ){
			$('body').removeClass('mini');
		}else{
			$('body').addClass('mini');
		}
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
	if (currentUrl) {
		// mirar si tiene ?
		if (currentUrl.indexOf('?') != -1) {
			window.location = currentUrl + "&" + newOrder;
		} else {
			window.location = currentUrl + "?" + newOrder;
		}
	}
}

function tryToSelectOrder(orderType) {
	alert(orderType);
}

function tryToSelectItem(obj, txt) {
	for (k =0 ; k < obj.length; k++) {
		if (obj[k].value == txt) {
			obj[k].selected = true;
		}
	}
}

$(document).ready(function() {
	refinaAutocomplete();
	
  if (($("#cajaDeBusqInput").val() != "")) {
    $("#cajaDeBusqInput").css("background", "#FFFFFF");
  }
	
	var config  = {
		disable_search: true
	};
	
	var valueIsEstadist = "bienal";
	
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
		if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist){
			var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;
			if (idxGrupo != 0) {
				urlToGo += "/" + $("#estadisNivel1_Filter")[0][idxGrupo].value;
			}
		}
		window.location = urlToGo;
		return false;
	}
	var fOnChgChosen_estadistica = function onChgChosen_estadistica() {
		var urlToGo = "/catalogo";
		var idxTema = $("#temaFilter")[0].selectedIndex;
		if (idxTema != 0) {
			urlToGo += "/" + $("#temaFilter")[0][idxTema].value;
		}
		var idxTipo = $("#tipoFilter")[0].selectedIndex;
		if (idxTipo != 0) {
			urlToGo += "/" + $("#tipoFilter")[0][idxTipo].value;
		}
		var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;
		if (idxGrupo != 0) {
			urlToGo += "/" + $("#estadisNivel1_Filter")[0][idxGrupo].value;
			var idxSubgrupo = $("#estadisNivel2_grp" + idxGrupo + "_Filter")[0].selectedIndex;
			if (idxSubgrupo != 0) {
				urlToGo += "/" + $("#estadisNivel2_grp" + idxGrupo + "_Filter")[0][idxSubgrupo].value;
			}
		}
		
		window.location = urlToGo;
		return false;
	}
	
	
	var urlListParam  = new Array();
	if (currentUrl) {
		urlListParam = currentUrl.split("/");
		if (urlListParam.length == 3) {
				// O es tema o es tipo
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
			tryToSelectItem($("#tipoFilter")[0], urlListParam[2]);
			var idxTipo = $("#tipoFilter")[0].selectedIndex;
			if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {				
				$("#estadisNivel1_FilterDiv").removeClass("oculto");
				$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
			}
		} else if (urlListParam.length == 4) {
				// O es tema+tipo o es tipo/grupo
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
			var idxTema = $("#temaFilter")[0].selectedIndex;
			if (idxTema != 0) {
					// es tema+tipo				
				tryToSelectItem($("#tipoFilter")[0], urlListParam[3]);
				var idxTipo = $("#tipoFilter")[0].selectedIndex;				
				if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {
					$("#estadisNivel1_FilterDiv").removeClass("oculto");
					$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
				}
			}
			
			
			tryToSelectItem($("#tipoFilter")[0], urlListParam[2]);
			var idxTipo = $("#tipoFilter")[0].selectedIndex;
			if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {				
				$("#estadisNivel1_FilterDiv").removeClass("oculto");
				tryToSelectItem($("#estadisNivel1_Filter")[0], urlListParam[3]);
				$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
				var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;				
				if (idxGrupo != 0) {					
					$("#estadisNivel2_grp" + idxGrupo + "_FilterDiv").removeClass("oculto");					
					$("#estadisNivel2_grp" + idxGrupo + "_Filter").chosen(config).change(fOnChgChosen_estadistica);
				}
			}
		} else if (urlListParam.length == 5) {
				// puede ser tema+tipo+grupo o tipo+grupo+subgrupo
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);

			var idxTema = $("#temaFilter")[0].selectedIndex;
			if (idxTema != 0) {
					// es tema+tipo+grupo
				
				tryToSelectItem($("#tipoFilter")[0], urlListParam[3]);

				var idxTipo = $("#tipoFilter")[0].selectedIndex;
				if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {					
					$("#estadisNivel1_FilterDiv").removeClass("oculto");
					tryToSelectItem($("#estadisNivel1_Filter")[0], urlListParam[4]);
					$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
				}
			}
			
			tryToSelectItem($("#tipoFilter")[0], urlListParam[2]);
			var idxTipo = $("#tipoFilter")[0].selectedIndex;
			if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {
					// es tipo + grupo + subgrupo			
				$("#estadisNivel1_FilterDiv").removeClass("oculto");
				tryToSelectItem($("#estadisNivel1_Filter")[0], urlListParam[3]);
				$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
				
				var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;
				if (idxGrupo != 0) {					
					$("#estadisNivel2_grp" + idxGrupo + "_FilterDiv").removeClass("oculto");
					tryToSelectItem($("#estadisNivel2_grp" + idxGrupo + "_Filter")[0], urlListParam[4]);
					$("#estadisNivel2_grp" + idxGrupo + "_Filter").chosen(config).change(fOnChgChosen_estadistica);
				}
			}
		} else if (urlListParam.length ==  6) {
				// debe ser tema+tipo+grupo+subgrupo
			tryToSelectItem($("#temaFilter")[0], urlListParam[2]);
			var idxTema = $("#temaFilter")[0].selectedIndex;
			if (idxTema != 0) {
					// es tema+tipo				
				tryToSelectItem($("#tipoFilter")[0], urlListParam[3]);
				var idxTipo = $("#tipoFilter")[0].selectedIndex;				
				if ($("#tipoFilter")[0][idxTipo].value == valueIsEstadist) {
					$("#estadisNivel1_FilterDiv").removeClass("oculto");
					tryToSelectItem($("#estadisNivel1_Filter")[0], urlListParam[4]);					
					$("#estadisNivel1_Filter").chosen(config).change(fOnChgChosen_estadistica);
					
					var idxGrupo = $("#estadisNivel1_Filter")[0].selectedIndex;
					if (idxGrupo != 0) {					
						$("#estadisNivel2_grp" + idxGrupo + "_FilterDiv").removeClass("oculto");
						tryToSelectItem($("#estadisNivel2_grp" + idxGrupo + "_Filter")[0], urlListParam[5]);
						$("#estadisNivel2_grp" + idxGrupo + "_Filter").chosen(config).change(fOnChgChosen_estadistica);
					}
				}
			}
		}
	}

	$("#temaFilter").chosen(config).change(fOnChgChosen);
	$("#tipoFilter").chosen(config).change(fOnChgChosen);

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
		     })
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
		     })
	$.ajax({
			url: "/catalogo/api/getDataCount",
			dataType: "jsonp",
			success: function (data) {
				var htmlCodeDatasets = getContadorHTML(data[0].datasetCount);
				var htmlCodeRecursos = getContadorHTML(data[0].resourceCount);
				$('#numDatasets').html(htmlCodeDatasets);
				$('#numRecursos').html(htmlCodeRecursos);
			},
			error: function (data) {
				var htmlCodeDatasets = getContadorHTML(448);
				var htmlCodeRecursos = getContadorHTML(1049);
				$('#numDatasets').html(htmlCodeDatasets);
				$('#numRecursos').html(htmlCodeRecursos);
			}
		     })
});

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
