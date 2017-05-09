function getCookie(d){var b=d+"=";var a=document.cookie.split(";");for(var e=0;e<a.length;e++){var f=a[e];while(f.charAt(0)==" "){f=f.substring(1)}if(f.indexOf(b)==0){return f.substring(b.length,f.length)}}return""}function isEmpty(a){return(a==null||a==="")}function pintaMenuBuscador(){var a=getCookie("auth_tkt");$(".bannerBuscador").empty();if(isEmpty(a)){$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><button class="btn-search" type="submit">Buscar</button><a href="/catalogo/user/login" title="Iniciar Sesión"><div class="btn-login"></div></form>')}else{$(".bannerBuscador").append('<form id="cajaBusqBanner" action="/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><a href="/catalogo/pizarra" title="Pizarra de administración"><div class="btn-dashboard"></div></a><a href="/catalogo/user/_logout" title="Salir"><div class="btn-logout"></div></a></form>')}if($(window).width()>1024){$('<div id="anchoBanner" style="background-color: #76a1b8;"></div>').insertBefore(".banner");$(".banner").appendTo("#anchoBanner");$("#anchoBanner #anchoBanner").remove()}}function showHideAragopediaMenu(a){if($(window).width()<=a){$("#mw-panel").hide()}else{$("#mw-panel").show()}}function responsiveAragopediaTables(a){resetAragopediaTables();$("table.wikitable.sortable").each(function(){if($(this).width()>a){$(this).css({overflow:"auto",display:"block","max-width":a+"px"})}})}function resetAragopediaTables(){$("table.wikitable.sortable").removeAttr("style")}function resetAragopediaCharts(){$("#mw-content-text p b img").removeAttr("style")}function responsiveAragopediaCharts(a){resetAragopediaCharts();$("#mw-content-text p b img").each(function(){if($(this).width()>a){$(this).css({"max-width":a+"px"})}})}function responsiveAragopediaArticle(b,a){if($(window).width()<=b){$("#aragopedia").css("width",$(window).width()+"px");$("div#mw-head").css("width",$(window).width());$("div#content").css("margin-left","5px");$("#infobox_mapa").css("margin-right","11px");$("#bodyContent").css("width",$(window).width());$(".firstHeading, #firstHeading").css("width",$(window).width());resetAragopediaTables();resetAragopediaCharts();if($(window).width()<=a){$("table#toc.toc").after($("#infobox_mapa"));$("#infobox_mapa").css({"float":"none","margin-top":"40px"});responsiveAragopediaTables($(window).width()-10);responsiveAragopediaCharts($(window).width()-10)}else{$("#infobox_mapa").after($("table#toc.toc"));$("#infobox_mapa").css({"float":"right","margin-right":"1x","margin-top":"0px"});responsiveAragopediaTables($(window).width()-10);responsiveAragopediaCharts($(window).width()-10)}}else{$("div#mw-head").css("width","989px");$("div#infobox_mapa.infobox").css("margin-right","0px");$("#aragopedia").css("width","980px");$("#bodyContent").css("width","787px");$(".firstHeading, #firstHeading").css("width","787px");$("div#content").css("margin-left","194px");responsiveAragopediaTables($(window).width()-194);responsiveAragopediaCharts($(window).width()-194)}}var dateFormat=function(){var a=/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,b=/\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,d=/[^-+\dA-Z]/g,c=function(f,e){f=String(f);e=e||2;while(f.length<e){f="0"+f}return f};return function(i,v,q){var g=dateFormat;if(arguments.length==1&&Object.prototype.toString.call(i)=="[object String]"&&!/\d/.test(i)){v=i;i=undefined}i=i?new Date(i):new Date;if(isNaN(i)){throw SyntaxError("invalid date")}v=String(g.masks[v]||v||g.masks["default"]);if(v.slice(0,4)=="UTC:"){v=v.slice(4);q=true}var t=q?"getUTC":"get",l=i[t+"Date"](),e=i[t+"Day"](),j=i[t+"Month"](),p=i[t+"FullYear"](),r=i[t+"Hours"](),k=i[t+"Minutes"](),u=i[t+"Seconds"](),n=i[t+"Milliseconds"](),f=q?0:i.getTimezoneOffset(),h={d:l,dd:c(l),ddd:g.i18n.dayNames[e],dddd:g.i18n.dayNames[e+7],m:j+1,mm:c(j+1),mmm:g.i18n.monthNames[j],mmmm:g.i18n.monthNames[j+12],yy:String(p).slice(2),yyyy:p,h:r%12||12,hh:c(r%12||12),H:r,HH:c(r),M:k,MM:c(k),s:u,ss:c(u),l:c(n,3),L:c(n>99?Math.round(n/10):n),t:r<12?"a":"p",tt:r<12?"am":"pm",T:r<12?"A":"P",TT:r<12?"AM":"PM",Z:q?"UTC":(String(i).match(b)||[""]).pop().replace(d,""),o:(f>0?"-":"+")+c(Math.floor(Math.abs(f)/60)*100+Math.abs(f)%60,4),S:["th","st","nd","rd"][l%10>3?0:(l%100-l%10!=10)*l%10]};return v.replace(a,function(m){return m in h?h[m]:m.slice(1,m.length-1)})}}();dateFormat.masks={"default":"ddd mmm dd yyyy HH:MM:ss",shortDate:"m/d/yy",mediumDate:"mmm d, yyyy",longDate:"mmmm d, yyyy",fullDate:"dddd, mmmm d, yyyy",shortTime:"h:MM TT",mediumTime:"h:MM:ss TT",longTime:"h:MM:ss TT Z",isoDate:"yyyy-mm-dd",isoTime:"HH:MM:ss",isoDateTime:"yyyy-mm-dd'T'HH:MM:ss",isoUtcDateTime:"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"};dateFormat.i18n={dayNames:["Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],monthNames:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","January","February","March","April","May","June","July","August","September","October","November","December"]};Date.prototype.format=function(a,b){return dateFormat(this,a,b)};function responsiveAragopediaCabeceraHome(){var a=new Date();var b=a.format("yyyy.mm.dd | HH:MM:ss");if($(window).width()<975){$("#etiquetasHome").hide();$("#infowiki").insertBefore("#txt_bienvenida");$("#infowiki").empty();$("#infowiki").css({"text-align":"left",position:"inherit",width:"210px",left:"0"});$("#seleccion input").css("padding-left","0px");$("#infowiki").empty();$("#infowiki").append("<p>768 ARTÍCULOS  "+b+"</p>");$("#p-search").insertAfter("#txt_bienvenida");$("#txt_bienvenida").css("width",$("#cabecera_aragopedia").width()*0.9+"px");$("#infowiki p").css("width",$("#cabecera_aragopedia").width()*0.9+"px");$("#p-search").css({"float":"inherit",position:"static",top:"0px","margin-top":"10px","margin-left":"0em"});var c=window.location.pathname;if(c.indexOf("/aragopedia/index.php/")>=0){$("#p-search").css("margin-top","0px")}else{$("#p-search").css("width",$("#cabecera_aragopedia").width()*0.9+"px")}$("#bienvenida").css("width",$("#cabecera_aragopedia").width()*0.9+"px");$("#simpleSearch").css("width",$("#cabecera_aragopedia").width()*0.9+"px");$("#searchButton").css("height","24px");if($(window).width()>900){$("#cabecera_aragopedia").css("height","215px")}else{if(($(window).width()<=900)&&($(window).width()>825)){$("#cabecera_aragopedia").css("height","200px")}else{if(($(window).width()<=825)&&($(window).width()>775)){$("#cabecera_aragopedia").css("height","195px")}else{if(($(window).width()<=775)&&($(window).width()>650)){$("#cabecera_aragopedia").css("height","185px")}else{if(($(window).width()<=650)&&($(window).width()>575)){$("#cabecera_aragopedia").css("height","195px")}else{if(($(window).width()<=575)&&($(window).width()>375)){$("#cabecera_aragopedia").css("height","210px")}else{if($(window).width()<=375){$("#cabecera_aragopedia").css("height","220px")}}}}}}}}else{$("#p-search").insertAfter("#portada");$("#searchButton").removeAttr("style");$("#txt_bienvenida").removeAttr("style");$("#simpleSearch").css("width","190px");$("#bienvenida").removeAttr("style");$("#p-search").removeAttr("style");$("#cabecera_aragopedia").css("heigth","100px");$("#infowiki").removeAttr("style");$("#infowiki").empty();$("#infowiki").append("<p>768 ARTÍCULOS </p><p> "+b+"</p>");$("#txt_bienvenida").insertBefore("#infowiki");$("#etiquetasHome").show();$("#seleccion input").css("padding-left","10px")}}function responsiveAragopediaHomeBusqueda(){if($(window).width()<800){$("#busqueda_comarcas").css("width",$("#cabecera_aragopedia").width()*0.9+"px");$("#busqueda_municipios").css({"margin-left":"0px","margin-top":"10px",width:$("#cabecera_aragopedia").width()*0.9+"px"});$("#busqueda").css("height","110px")}else{$("#busqueda").css("height","90px");$("#busqueda_comarcas").removeAttr("style");$("#busqueda_municipios").removeAttr("style")}}function responsiveAragopediaHomeMapa(){if($(window).width()<450){$("#mapa").hide()}else{$("#mapa").show()}}function responsiveAragopediaHome(a){if($(this).width()<a){centrarHome(a)}else{restableceAragopediaHome()}}function restableceAragopediaHome(){$(".contenido").css("margin-left","194px");$(".contenido").removeAttr("style");$("#portada").removeAttr("style");$("#portada").css("margin-left","194px");$("#portada").css({position:"auto",left:"0px"});$(".contenido").css("margin-left","194px");$(".contenido").css({position:"auto",left:"0px"});$("div#simpleSearch").css("border-bottom","0px solid #76A1B8")}function centrarHome(a){if($(window).width()<a){$("#footer").css("width",$(window).width()-(($(window).width()-$(".contenido").width())));$("div#footer").css("left",0);$("#portada").css("margin-left","0px");$("div#simpleSearch").css("border-bottom","1px solid #76A1B8");if($(".contenido").width()>$(window).width()){$("#portada").css({position:"auto",left:"0px"})}else{$("#portada").css({position:"relative",left:($(window).width()-$(".contenido").width())/2})}$(".contenido").css("margin-left","0px");$(".contenido").css("width",$(window).width());$(".contenido").css({position:"auto",left:"0px"})}}function responsiveScroll(){$(window).scroll(function(){if($(window).width()>=1012){$html=$("html");var a=window.location.pathname;if(a.indexOf("/aragopedia/index.php/")>=0){$(".mini .botones").css("top","41px")}else{$(".mini .botones").css("top","41px")}if($(document).scrollTop()>=210){$("body").addClass("mini");$("#anchoBanner").css({position:"fixed",top:"-10px",height:$(".banner").height()+"px",width:"100%","z-index":1110});$(".banner").css({left:(($(window).width()-$(".banner").width())/2)+"px",width:"980px"})}else{$("body").removeClass("mini");$(".banner").removeAttr("style");$("#anchoBanner").removeAttr("style");$("#anchoBanner").css("background-color","#76a1b8")}}else{$(".mini .botones").removeAttr("style");$(".banner").removeAttr("style")}});$("body").trigger("scroll")}function borradoInicial(){if(($("#cajaDeBusqInput").val()!="")){$("#cajaDeBusqInput").css("background","#FFFFFF")}$("#cajaDeBusqInput").on("blur",function(){if(($("#cajaDeBusqInput").val()!="")){$("#cajaDeBusqInput").css("background","#FFFFFF")}})}$(document).ready(function(){borradoInicial();pintaMenuBuscador();showHideAragopediaMenu(980);responsiveAragopediaArticle(980,767);responsiveAragopediaHome(980);/**$(".banner").css("background","red")*/;if(($("#cajaDeBusqInput").val()!="")){$("#cajaDeBusqInput").css("background","#FFFFFF")}$("#cajaDeBusqInput").on("blur",function(){if(($("#cajaDeBusqInput").val()!="")){$("#cajaDeBusqInput").css("background","#FFFFFF")}});responsiveAragopediaCabeceraHome();responsiveAragopediaHomeBusqueda();responsiveAragopediaHomeMapa();responsiveScroll();$(window).resize(function(){pintaMenuBuscador();showHideAragopediaMenu(980);responsiveAragopediaArticle(980,767);responsiveAragopediaHome(980);responsiveAragopediaCabeceraHome();responsiveAragopediaHomeBusqueda();responsiveAragopediaHomeMapa();responsiveScroll()})});
