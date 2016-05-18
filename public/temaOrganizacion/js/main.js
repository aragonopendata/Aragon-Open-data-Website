/*** Funciones para el funcionamiento de la app **/

//Función que sirve para cuando se haga over sobre una organizacion y cambie el div con más info
function organizacionOver(){
	$(".resultadosOrganizaciones .thumbnail").hover(
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').addClass("oculto");
			$('#'+id+' .back').removeClass("oculto");
			//console.log('Se entra en '+id);
		}, 
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').removeClass("oculto");
			$('#'+id+' .back').addClass("oculto");
			//console.log('Se sale de '+id);
		}
	);
}

//Función que sirve para cuando se haga over sobre un tema y cambie el div con más info
function temaOver(){
	$(".resultadosTemas .thumbnail").hover(
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').addClass("oculto");
			$('#'+id+' .back').removeClass("oculto");
			//console.log('Se entra en '+id);
		}, 
		function(){
			var id = $(this).attr('id');
			//$('#'+id+' .front').removeClass("oculto");
			$('#'+id+' .back').addClass("oculto");
			//console.log('Se sale de '+id);
		}
	);
}




$(document).ready(function() {
	var config	= {
		disable_search: true
	};
	$('.organizacionLista').hide();
	$('.organizacionFicha').show();
	var fOnChgChosen = function onChgChosen() {

		var tipoVisualizacion = $("#tipoVisualizacion option:selected").val();
		
		if (tipoVisualizacion=='lista'){
			$('.organizacionFicha').hide();
			$('.organizacionLista').show();
		}
		else if (tipoVisualizacion=='ficha'){
			$('.organizacionLista').hide();
			$('.organizacionFicha').show();
		}
	}
	
	$("#tipoVisualizacion").chosen(config).chosenImage().change(fOnChgChosen);
	
	var pathname = window.location.pathname;
	if (pathname.indexOf('/tema')>-1){
		temaOver();
	}
	else if (pathname.indexOf('/organizacion')>-1){
		organizacionOver();
	}
} );

var pathname = window.location.pathname;
if ((pathname.indexOf('/tema/')>-1) || (pathname.indexOf('/organizacion/')>-1)){
	$('.tablaResultadosDataset').DataTable({
		"pagingType": "simple_numbers",
		"pageLength": 20,
		"language": {
			"paginate": {
				"previous": "<<",
				"next": ">>"
			}
		}
	});
	$('.dataTables_length').remove();
	$('.dataTables_filter').remove();
	$('.dataTables_info').remove();
	
	
	var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
	// Firefox 1.0+
	var isFirefox = typeof InstallTrigger !== 'undefined';
	// At least Safari 3+: "[object HTMLElementConstructor]"
	var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
	// Internet Explorer 6-11
	var isIE = /*@cc_on!@*/false || !!document.documentMode;
	// Edge 20+
	var isEdge = !isIE && !!window.StyleMedia;
	// Chrome 1+
	var isChrome = !!window.chrome && !!window.chrome.webstore;
	// Blink engine detection
	var isBlink = (isChrome || isOpera) && !!window.CSS;

	if(isChrome || isSafari){
		if ($('.dataTables_wrapper .dataTables_paginate .ellipsis').length>0){
			$('.dataTables_wrapper .dataTables_paginate .ellipsis').css('padding', '9px 1em');
		}
		else if (isOpera){
			if ($('.dataTables_wrapper .dataTables_paginate .ellipsis').length>0){
				$('.dataTables_wrapper .dataTables_paginate .ellipsis').css('padding', '9px 1em');
			}
		}
		else{
			//alert('Nowebkit');
		}
	}

	$('.textPopular').insertBefore('.dataTables_paginate.paging_simple_numbers'); 
}

