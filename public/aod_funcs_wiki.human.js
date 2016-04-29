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
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><button class="btn-search" type="submit">Buscar</button><a href="/catalogo/user/login" title="Iniciar Sesión"><div class="btn-login"></div></form>');
	}
	else{
		//Pintamos el menu cuando estamos logueados
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><a href="/catalogo/pizarra" title="Pizarra de administración"><div class="btn-dashboard"></div></a><a href="/catalogo/user/_logout" title="Salir"><div class="btn-logout"></div></a></form>');
	}
	if ($(window).width()>1024){
		//Este div se usa para que quede centrado
		$('<div id="anchoBanner" style="background-color: #76a1b8;"></div>').insertBefore('.banner');
		$('.banner').appendTo('#anchoBanner');
		//Borramos los #anchoBanner internos que nos guarrean el codigo si andamos agrandando o empequeñeciendo la ventana
		$('#anchoBanner #anchoBanner').remove();
	}
}


//Funcion que esconde o ensenia el menu de la aragopedia que se encuentra a la izquierda, limite es el ancho que usamos para esconder o enseniar el menu
function showHideAragopediaMenu(limite){
	if ($(window).width()<=limite){
		$('#mw-panel').hide();
	}
	else{
		$('#mw-panel').show();
	}
}

//Esta funcion hace responsive las tablas de la Aragopedia, con un tamaño tam
function responsiveAragopediaTables(tam){
	resetAragopediaTables();
	$('table.wikitable.sortable').each(function(){
		if ($(this).width()>tam){
			$(this).css({
				'overflow':'auto',
				'display':'block',
				'max-width':tam+'px'
			});
		}
	});
}

//Esta funcion quita los atributos para las tablas
function resetAragopediaTables(){
	$('table.wikitable.sortable').removeAttr('style');
}

//Esta funcion quita los atributos para los gráficos de los artículos de la Aragoedia
function resetAragopediaCharts(){
	$('#mw-content-text p b img').removeAttr('style');
}

//Esta función sirve para hacer responsive las imágemnes que son los gráficos con un tamaño tan 
function responsiveAragopediaCharts(tam){
	resetAragopediaCharts();
	$('#mw-content-text p b img').each(function(){
		if ($(this).width()>tam){
			$(this).css({
				'max-width':tam+'px'
			});
		}
	});
}



//Esta función hará que los artículos sea puedan ver de manera correcta en los dispositivos móviles
function responsiveAragopediaArticle(limiteExterno, limiteInterno){
	//$('#aragopedia').css('width','100%');
	if ($(window).width()<=limiteExterno){
		//$('#mw-panel').hide();
		//alert('el ancho es '+$(window).width());
		//$('#aragopedia').css('width', '100%');
		$('#aragopedia').css('width', $(window).width()+'px');
		//$('div#content').css('margin-left', '5px');
		//$('div#mw-head').css('width','100% !important');
		//if ($(window).width()<limiteExterno){
			//alert('Entro en el limite medio');
			$('div#mw-head').css('width',$(window).width());
			$('div#content').css('margin-left', '5px');
			$('#infobox_mapa').css('margin-right', '11px');
		//}
		
		
		$('#bodyContent').css('width',$(window).width());
		$('.firstHeading, #firstHeading').css('width',$(window).width());
		resetAragopediaTables();
		resetAragopediaCharts();
		
		if ($(window).width()<=limiteInterno){ 
			
			$('table#toc.toc').after($('#infobox_mapa'));
			$('#infobox_mapa').css({
				'float': 'none',
				'margin-top': '40px'
			});
			responsiveAragopediaTables($(window).width()-10);
			responsiveAragopediaCharts($(window).width()-10);
		}
		else{
			//$('#infobox_mapa').show();
			$('#infobox_mapa').after($('table#toc.toc'));
			$('#infobox_mapa').css({
				'float': 'right',
				'margin-right': '1x',
				'margin-top': '0px'
			});
			responsiveAragopediaTables($(window).width()-10);
			responsiveAragopediaCharts($(window).width()-10);
		}
		
	}
	else{
		$('div#mw-head').css('width','989px');
		$('div#infobox_mapa.infobox').css('margin-right', '0px');
		$('#aragopedia').css('width', '980px');
		$('#bodyContent').css('width','787px');
		$('.firstHeading, #firstHeading').css('width','787px');
		//$('#mw-panel').show();
		$('div#content').css('margin-left', '194px');
		//resetAragopediaTables();
		//resetAragopediaCharts();
		responsiveAragopediaTables($(window).width()-194);
		responsiveAragopediaCharts($(window).width()-194);
	}
}




/** Funcion para formatear fechas**/

var dateFormat = function () {
        var    token = /d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,
            timezone = /\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
            timezoneClip = /[^-+\dA-Z]/g,
            pad = function (val, len) {
                val = String(val);
                len = len || 2;
                while (val.length < len) val = "0" + val;
                return val;
            };
    
        // Regexes and supporting functions are cached through closure
        return function (date, mask, utc) {
            var dF = dateFormat;
    
            // You can't provide utc if you skip other args (use the "UTC:" mask prefix)
            if (arguments.length == 1 && Object.prototype.toString.call(date) == "[object String]" && !/\d/.test(date)) {
                mask = date;
                date = undefined;
            }
    
            // Passing date through Date applies Date.parse, if necessary
            date = date ? new Date(date) : new Date;
            if (isNaN(date)) throw SyntaxError("invalid date");
    
            mask = String(dF.masks[mask] || mask || dF.masks["default"]);
    
            // Allow setting the utc argument via the mask
            if (mask.slice(0, 4) == "UTC:") {
                mask = mask.slice(4);
                utc = true;
            }
    
            var    _ = utc ? "getUTC" : "get",
                d = date[_ + "Date"](),
                D = date[_ + "Day"](),
                m = date[_ + "Month"](),
                y = date[_ + "FullYear"](),
                H = date[_ + "Hours"](),
                M = date[_ + "Minutes"](),
                s = date[_ + "Seconds"](),
                L = date[_ + "Milliseconds"](),
                o = utc ? 0 : date.getTimezoneOffset(),
                flags = {
                    d:    d,
                    dd:   pad(d),
                    ddd:  dF.i18n.dayNames[D],
                    dddd: dF.i18n.dayNames[D + 7],
                    m:    m + 1,
                    mm:   pad(m + 1),
                    mmm:  dF.i18n.monthNames[m],
                    mmmm: dF.i18n.monthNames[m + 12],
                    yy:   String(y).slice(2),
                    yyyy: y,
                    h:    H % 12 || 12,
                    hh:   pad(H % 12 || 12),
                    H:    H,
                    HH:   pad(H),
                    M:    M,
                    MM:   pad(M),
                    s:    s,
                    ss:   pad(s),
                    l:    pad(L, 3),
                    L:    pad(L > 99 ? Math.round(L / 10) : L),
                    t:    H < 12 ? "a"  : "p",
                    tt:   H < 12 ? "am" : "pm",
                    T:    H < 12 ? "A"  : "P",
                    TT:   H < 12 ? "AM" : "PM",
                    Z:    utc ? "UTC" : (String(date).match(timezone) || [""]).pop().replace(timezoneClip, ""),
                    o:    (o > 0 ? "-" : "+") + pad(Math.floor(Math.abs(o) / 60) * 100 + Math.abs(o) % 60, 4),
                    S:    ["th", "st", "nd", "rd"][d % 10 > 3 ? 0 : (d % 100 - d % 10 != 10) * d % 10]
                };
    
            return mask.replace(token, function ($0) {
                return $0 in flags ? flags[$0] : $0.slice(1, $0.length - 1);
            });
        };
    }();
    
    // Some common format strings
    dateFormat.masks = {
        "default":      "ddd mmm dd yyyy HH:MM:ss",
        shortDate:      "m/d/yy",
        mediumDate:     "mmm d, yyyy",
        longDate:       "mmmm d, yyyy",
        fullDate:       "dddd, mmmm d, yyyy",
        shortTime:      "h:MM TT",
        mediumTime:     "h:MM:ss TT",
        longTime:       "h:MM:ss TT Z",
        isoDate:        "yyyy-mm-dd",
        isoTime:        "HH:MM:ss",
        isoDateTime:    "yyyy-mm-dd'T'HH:MM:ss",
        isoUtcDateTime: "UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"
    };
    
    // Internationalization strings
    dateFormat.i18n = {
        dayNames: [
            "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat",
            "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
        ],
        monthNames: [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ]
    };
    
    // For convenience...
    Date.prototype.format = function (mask, utc) {
        return dateFormat(this, mask, utc);
    };




//Función que hace responsive la cabecera que es a partir de 825 px que se tiene que empezar a mover cosas, si es mayor deja las properties como estaban
function responsiveAragopediaCabeceraHome(){
	
	var hoy =  new Date();
	var dateString = hoy.format("yyyy.mm.dd | HH:MM:ss");
	
	if ($(window).width()<975){
		$('#etiquetasHome').hide();
		$('#infowiki').insertBefore('#txt_bienvenida');
		$('#infowiki').empty();
		$('#infowiki').css({
			'text-align': 'left',
			position: 'inherit',
			width:'210px',
			left:'0'
		});
		
		$('#seleccion input').css('padding-left', '0px');
		
		$('#infowiki').empty();
		$('#infowiki').append('<p>768 ARTÍCULOS  '+dateString+'</p>');
		
		$('#p-search').insertAfter('#txt_bienvenida');//Meter las proprties
		$('#txt_bienvenida').css('width',$('#cabecera_aragopedia').width()*0.9+'px');
		$('#infowiki p').css('width',$('#cabecera_aragopedia').width()*0.9+'px');
		$('#p-search').css({
			'float':'inherit',
			'position': 'static',
			'top': '0px',
			'margin-top':'10px',
			'margin-left': '0em'
		});
		
		var pathname = window.location.pathname;
		//if (pathname.includes("/aragopedia/index.php/")){
		if (pathname.indexOf("/aragopedia/index.php/")>=0){
			$('#p-search').css('margin-top','0px');
		}
		else{
			$('#p-search').css('width',$('#cabecera_aragopedia').width()*0.9+'px');
		}
		
		$('#bienvenida').css('width', $('#cabecera_aragopedia').width()*0.9+'px');
		$('#simpleSearch').css('width', $('#cabecera_aragopedia').width()*0.9+'px');
		$('#searchButton').css('height','24px');
		//$('#cabecera_aragopedia').css('height', '175px');
		
		if ($(window).width()>900) {
			$('#cabecera_aragopedia').css('height', '215px');
		}
		else if ( ($(window).width()<=900) && ($(window).width()>825)) {
			$('#cabecera_aragopedia').css('height', '200px');
		}
		else if ( ($(window).width()<=825) && ($(window).width()>775)){
			$('#cabecera_aragopedia').css('height', '195px');
		}
		else if ( ($(window).width()<=775) && ($(window).width()>650)) {
			$('#cabecera_aragopedia').css('height', '185px');
		}
		else if ( ($(window).width()<=650) && ($(window).width()>575)) {
			$('#cabecera_aragopedia').css('height', '195px');
		}
		else if (($(window).width()<=575) && ($(window).width()>375)) {
			$('#cabecera_aragopedia').css('height', '210px');
		}
		else if ($(window).width()<=375){
			$('#cabecera_aragopedia').css('height', '220px');
		}
		
	}
	else{//restablecemos esta parte
		
		$('#p-search').insertAfter('#portada');
		$('#searchButton').removeAttr('style');
		$('#txt_bienvenida').removeAttr('style');
		$('#simpleSearch').css('width', '190px');
		$('#bienvenida').removeAttr('style');
		$('#p-search').removeAttr('style');
		$('#cabecera_aragopedia').css('heigth', '100px');
		$('#infowiki').removeAttr('style');
		$('#infowiki').empty();
		$('#infowiki').append('<p>768 ARTÍCULOS </p><p> '+dateString+'</p>');
		$('#txt_bienvenida').insertBefore('#infowiki');
		$('#etiquetasHome').show();
		$('#seleccion input').css('padding-left', '10px');
	}
}


//Funcion que realiza responsive el apartado de búsqueda y el mapa
function responsiveAragopediaHomeBusqueda(){
	if ($(window).width()<800){
		$('#busqueda_comarcas').css('width',$('#cabecera_aragopedia').width()*0.9+'px');
		$('#busqueda_municipios').css({
			'margin-left': '0px',
			'margin-top':'10px',
			'width': $('#cabecera_aragopedia').width()*0.9+'px'
		});
		$('#busqueda').css('height','110px');
	}
	else{
		$('#busqueda').css('height','90px');
		$('#busqueda_comarcas').removeAttr('style');
		$('#busqueda_municipios').removeAttr('style');
	}
}

//Función que oculta o enseeña el mapa del home
function responsiveAragopediaHomeMapa(){
	if ($(window).width()<450){
		$('#mapa').hide();
	}
	else{
		$('#mapa').show();
		
	}
}


//Esta funcion sirve para hacer responsive la home de la aragopedia
function responsiveAragopediaHome(limite){
	if ($(this).width()<limite){
		centrarHome(limite)
	}
	else{
		restableceAragopediaHome();
	}
}

//Función para restablecer la home
function restableceAragopediaHome(){
	$('.contenido').css('margin-left', '194px');
	//quitar los estilos
	$('.contenido').removeAttr('style');
	$('#portada').removeAttr('style');
	$('#portada').css('margin-left', '194px');
	$('#portada').css({
		position:'auto',
		left:'0px'
	});
	$('.contenido').css('margin-left', '194px');
	$('.contenido').css({
		position:'auto',
		left:'0px'
	});
	$('div#simpleSearch').css('border-bottom', '0px solid #76A1B8');
}

//Funcion centrar contenido home
function centrarHome(limite){
	
	if ($(window).width()<limite) {
		$('#footer').css('width', $(window).width()-(($(window).width() - $('.contenido').width())));
		$('div#footer').css('left', 0);
		$('#portada').css('margin-left', '0px');
		$('div#simpleSearch').css('border-bottom', '1px solid #76A1B8');
		//Repasar esto de cuando se centra
		if ($('.contenido').width()> $(window).width()) {
			//$('#portada').css('width', $(window).width());
			$('#portada').css({
				position:'auto',
				left:'0px'
			});
			
		}
		else{
			$('#portada').css({
				position:'relative',
				left: ($(window).width() - $('.contenido').width())/2
			});
		}
		
		$('.contenido').css('margin-left', '0px');
		
		
		$('.contenido').css('width', $(window).width());
			$('.contenido').css({
				position:'auto',
				left:'0px'
			});
	}
}

//Esta funcion hace los correspondientes cambios para cuando se haga 
function responsiveScroll() {
	$(window).scroll(function() {
		if ($(window).width()>=1012){
			$html = $("html");
			var pathname = window.location.pathname;
			
			//if (pathname.includes("/aragopedia/index.php/")){
			if (pathname.indexOf("/aragopedia/index.php/")>=0){
				$('.mini .botones').css('top','41px');
			}
			else{
				$('.mini .botones').css('top','41px');
			}
			
		
			//Con window creo que pilla La barra de scroll ya que el límite esta en 754 con lo que esta barra tiene 14 pixeles
			//if (($( window ).width()>754) && ($(document).scrollTop() >= 160)){
			if ($(document).scrollTop() >= 210){
				//$('#anchoBanner').css('top', $(document).scrollTop()+'px');
				$('body').addClass('mini');
				$('#anchoBanner').css({
					'position':'fixed',
					'top': '-10px',
					'height':$('.banner').height()+'px',
					'width':'100%',
					'z-index':1110
				});
				
				$('.banner').css({
					'left': (($(window).width()-$('.banner').width())/2)+'px',
					'width':'980px'
				});
			}
			else{
				$('body').removeClass('mini');
				$('.banner').removeAttr('style');
				$('#anchoBanner').removeAttr('style');
				$('#anchoBanner').css('background-color', '#76a1b8');
				
			}
		}
		else{
			$('.mini .botones').removeAttr('style');
			$('.banner').removeAttr('style');
		}
	});
	$("body").trigger('scroll');
}

//al inicio, quitarlo si tiene valor porque lo autorrellene el navegador de otras visitas
function borradoInicial(){
	if (($("#cajaDeBusqInput").val() != "")) {
    $("#cajaDeBusqInput").css("background", "#FFFFFF");
  }

  $("#cajaDeBusqInput").on('blur', function() {
    if (($("#cajaDeBusqInput").val() != "")) {
      $("#cajaDeBusqInput").css("background", "#FFFFFF");
    }
  });
}




$(document).ready(function() {

	borradoInicial();
	pintaMenuBuscador();
	showHideAragopediaMenu(980);
	responsiveAragopediaArticle(980, 767);
	responsiveAragopediaHome(980);
	$('.banner').css("background", "red");
	//al inicio, quitarlo si tiene valor porque lo autorrellene el navegador de otras visitas	
	if (($("#cajaDeBusqInput").val() != "")) {
		$("#cajaDeBusqInput").css("background", "#FFFFFF");
	}
  
	$("#cajaDeBusqInput").on('blur', function() {
		if (($("#cajaDeBusqInput").val() != "")) {
			$("#cajaDeBusqInput").css("background", "#FFFFFF");
		}
	});
	
	responsiveAragopediaCabeceraHome();
	responsiveAragopediaHomeBusqueda();
	responsiveAragopediaHomeMapa();
	responsiveScroll();
	$(window).resize(function() {
		pintaMenuBuscador();
		showHideAragopediaMenu(980);
		responsiveAragopediaArticle(980, 767);
		responsiveAragopediaHome(980);
		responsiveAragopediaCabeceraHome();
		responsiveAragopediaHomeBusqueda();
		responsiveAragopediaHomeMapa();
		responsiveScroll();
	});
});

