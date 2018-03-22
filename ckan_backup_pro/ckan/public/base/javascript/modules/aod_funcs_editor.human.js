var alreadyCreatedResource = new Array();
var errorCreating = "";

function initializeDashboard() {
  var numZonesDashboard = 3;
  for (var i = 0; i < numZonesDashboard; i++) {
    $("#dashboardZone" + i).attr('onclick', 'activateDashboardZone("' + i + '");');
  }

  var numZonesEditor = 8;
  for (var i = 0; i < numZonesEditor; i++) {
    $("#editorZone" + i).attr('onclick', 'activateEditorZone("' + i + '");');
  }
  var config = {disable_search: true};
  if ($("#extras__1100__value")) {
    $("#extras__1100__value").chosen(config);
  }
  if ($("#groups__0__id")) {
    $("#groups__0__id").chosen(config);
  }

  var fOnChgChosen_changeResType = function onChgChosen_changeResType() {
    var _value = this[this.selectedIndex].value;
    var idx = this.id.substr("resType".length);
    if (_value == "vista") {
      toggleZoneResource(this.attributes.id.value, "vista");     
    } else if (_value == "file.upload") {
      toggleZoneResource(this.attributes.id.value, "file.upload");
      $("#jfilestyle-" + idx).trigger("click");
    } else {
      toggleZoneResource(this.attributes.id.value, "file");
    }
    return false;
  }

  if (typeof resourceCount != 'undefined') { 
    for (var idx = 0; idx < resourceCount; idx++) {
      if ($( "#resType" + idx )) {
        $( "#resType" + idx ).chosen(config).change(fOnChgChosen_changeResType);
      }
    }
    for (var idx = resourceCount; idx < (resourceCount+10); idx++) {
      if ($( "#resType" + idx )) {
        $( "#resType" + idx ).chosen(config).change(fOnChgChosen_changeResType);
      }
    }
    for (var idx = resourceCount; idx <= (resourceCount + MAX_URL_LIST); idx++) {
      alreadyCreatedResource[idx] = false;
    }

//          $(":file").jfilestyle();
  }

  if (typeof availableOrganizations != 'undefined') { 
    var fOnChgChosen_organizat = function onChgChosen_organizat() {
      for (var i=0; i < availableOrganizations; i++) {
        $("#organization" + i + "_org").addClass("oculto");
      }
      $("#organization" + (this.selectedIndex+1) + "_org").removeClass("oculto");
      return false;
    }
    $( "#owner_org" ).chosen(config).change(fOnChgChosen_organizat);
  }

  $('#textQueryOrgDataset').keypress(function(event) {
        if (event.keyCode == 13) {
            submitTxtQueryOrg();
        }
  });

    // toggle zone
  var currentUrl = window.location.toString();
  var queriedTxt = "";

  urlListParamPrev = currentUrl.split("?");

  if (urlListParamPrev[0].indexOf("/catalogo/pizarra/info-organizacion") != -1) {
    activateDashboardZone(0);
  }
  if (urlListParamPrev[0].indexOf("/catalogo/pizarra/datos") != -1) {
    activateDashboardZone(1);
  }
  if (urlListParamPrev[0].indexOf("/catalogo/pizarra/actividad") != -1) {
    activateDashboardZone(2);
  }
}


var currentOptionDashboardZone = 2;
function activateDashboardZone(newOption) {
  if (newOption != currentOptionDashboardZone) {
    $("#dashboardZone" + currentOptionDashboardZone).removeClass('blockDashboardSelected');
    $("#dashboardZone" + currentOptionDashboardZone).addClass('blockDashboard');
    $("#dashboardZonePage" + currentOptionDashboardZone).fadeOut();

    currentOptionDashboardZone = newOption;
    $("#dashboardZone" + currentOptionDashboardZone).removeClass('blockDashboard');
    $("#dashboardZone" + currentOptionDashboardZone).addClass('blockDashboardSelected');
    $("#dashboardZonePage" + currentOptionDashboardZone).fadeIn();
  }
}

function toggleZoneResource(id, type) {
  $("#vistaDiv_"+id).addClass('oculto');
  if (type=="vista") {
    $("#datos_"+id).addClass('oculto');
    $("#uploadFile_"+id).addClass('oculto');
    $("#vista_"+id).removeClass('oculto');
    resetSelect(id);
  } else if (type=="file.upload") {
    $("#datos_"+id).addClass('oculto');
    $("#uploadFile_"+id).removeClass('oculto');
    $("#vista_"+id).addClass('oculto');
    resetSelect(id);
  } else {
    $("#datos_"+id).removeClass('oculto');
    $("#uploadFile_"+id).addClass('oculto');
    $("#vista_"+id).addClass('oculto');
    resetSelect(id);
  }
}

var currentOptionEditorZone = 0;
function activateEditorZone(newOption) {
  if (newOption != currentOptionEditorZone) {
    $("#editorZone" + currentOptionEditorZone).removeClass('blockEditorSelected');
    $("#editorZone" + currentOptionEditorZone).addClass('blockEditor');
    $("#editorZonePage" + currentOptionEditorZone).fadeOut();

    currentOptionEditorZone = newOption;
    $("#editorZone" + currentOptionEditorZone).removeClass('blockEditor');
    $("#editorZone" + currentOptionEditorZone).addClass('blockEditorSelected');
    $("#editorZonePage" + currentOptionEditorZone).fadeIn();
  }
}

function initializeEditor() {
    // strange way of determining is editing, but it works
  if (document.getElementById("autocomplete_eurovoc")) {

    var f_tab = function () {
        if (window.confirm("Está a punto de salir del editor. Si no ha guardado los cambios realizados, se perderán. Confirme que realmente desea salir.")) {
          return true;
        } else {
          return false;
        }
      }

    $("#tab_organizacion").click(f_tab);
    $("#tab_datos").click(f_tab);
    $("#tab_actividad").click(f_tab);

     /*   $( document ).tooltip({
           track: true,
           content: function(callback) { 
                // original: http://stackoverflow.com/questions/13066909/how-to-break-line-in-jqueryui-tooltip
             callback($(this).prop('title').replace(/\|/g, '<br /><br />')); 
           }
        });*/
    $('.tips').powerTip({
      'followMouse': true
    });

    initializeAutocompletes();

      //maybe does not work on IE <9
    $("#extras__3099__value").on('input',function(e){
      if ($("#extras__3099__value").val() != "") {
        $("#extras__3098__value").prop('checked', true);
      }
    });
  }
}

function activateFileUploadForm() {
    // Activate file form input using jfilestyle
  $('.jfilestyle').each(function () { 
     var $this = $(this),
          options = {
              'buttonText': $this.attr('data-buttonText'),
              'input': $this.attr('data-input') === 'false' ? false : true,
              'icon': $this.attr('data-icon') === 'false' ? false : true,
              'size': $this.attr('data-size'),
              'iconName': $this.attr('data-iconName'),
              'theme': $this.attr('data-theme')
          };

      $this.jfilestyle(options);
  });
}

function initializeAutocompletes() {
  var accentMap = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "ü": "u"
  };
  var normalize = function( term ) {
    var ret = "";
    for ( var i = 0; i < term.length; i++ ) {
      ret += accentMap[ term.charAt(i) ] || term.charAt(i);
    }
    return ret;
  };

  $("#autocomplete_eurovoc" ).keypress(function(event) {
    if (event.keyCode == 13) {
      addTag();
    }      
  });

  $("#autocomplete_eurovoc" ).autocomplete({
      source: function( request, response ) {
        var suggestUrl = "/eurovoc_autocomplete?start=0&rows=1000&wt=json&q=search_text_es:" + $("#autocomplete_eurovoc").val() + "*";
        $.ajax({ dataType: "json",url: suggestUrl}).done(function( data ) {
          var suggests = new Array();
          $.each(data.response.docs, function(index, doc) {
             suggests.push({id: doc.term, label: doc.term, value: doc.term});
          });
          return response(suggests);
        });
      }
  }).data('ui-autocomplete')._renderItem = function( ul, item ) {
        return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
  };

  /*if (typeof resourceCount !== 'undefined') { 
    for (var idx = 0; idx < resourceCount; idx++) {
      $( "#mimeTypeRes" + idx ).autocomplete({
        source: formatList,
      }).data('ui-autocomplete')._renderItem = function( ul, item ) {
          return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
      };
      $( "#mimeTypeInnerRes" + idx ).autocomplete({
        source: formatList,
      }).data('ui-autocomplete')._renderItem = function( ul, item ) {
          return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
      };
    }
  }*/

  $('input:radio[name=typeSpatial]').change(function(event) {
    $( "#spatial_provincia" ).val("");
    $( "#spatial_comarca" ).val("");
    $( "#spatial_municipio" ).val("");
    $( "#spatial_otro" ).val("");
  })

  $( "#spatial_provincia" ).keypress(function(event) {
    $('input:radio[name=typeSpatial]')[1].checked = true;
  });

  $( "#spatial_provincia" ).autocomplete({
      source: function( request, response ) {
        var matcher = new RegExp( $.ui.autocomplete.escapeRegex( request.term ), "i" );
        response( $.grep( prov, function( value ) {
          value = value.label || value.value || value;
          return matcher.test( value ) || matcher.test( normalize( value ) );
        }) );
      },
      change: function( event, ui ) {
        var valid = false;
        if ( !ui.item ) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i" );
          for (value in prov) {
            if (matcher.test( prov[value] )) {
              valid = true;
              $(this).val(prov[value]);
              break;
            }
          }
          if (!valid) {
            // remove invalid value, as it didn't match anything
            $(this).val("");
            //input.data("autocomplete").term = "";
            return false;
          }
        }
      }
  }).data('ui-autocomplete')._renderItem = function( ul, item ) {
       return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
  };

  $( "#spatial_comarca" ).keypress(function(event) {
    $('input:radio[name=typeSpatial]')[2].checked = true;
  });
  $( "#spatial_comarca" ).autocomplete({
      source: function( request, response ) {
        var matcher = new RegExp( $.ui.autocomplete.escapeRegex( request.term ), "i" );
        response( $.grep( comarca, function( value ) {
          value = value.label || value.value || value;
          return matcher.test( value ) || matcher.test( normalize( value ) );
        }).slice(0, 10) );
      },
      change: function( event, ui ) {
        var valid = false;
        if ( !ui.item ) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i" );
          for (value in comarca) {
            if (matcher.test( comarca[value] )) {
              valid = true;
              $(this).val(comarca[value]);
              break;
            }
          }
          if (!valid) {
            // remove invalid value, as it didn't match anything
            $(this).val("");
            //input.data("autocomplete").term = "";
            return false;
          }
        }
      }
  }).data('ui-autocomplete')._renderItem = function( ul, item ) {
        return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
  };

  $( "#spatial_municipio" ).keypress(function(event) {
    $('input:radio[name=typeSpatial]')[3].checked = true;
  });
  $( "#spatial_municipio" ).autocomplete({
      source: function( request, response ) {
        var matcher = new RegExp( $.ui.autocomplete.escapeRegex( request.term ), "i" );
        response( $.grep( munis, function( value ) {
          value = value.label || value.value || value;
          return matcher.test( value ) || matcher.test( normalize( value ) );
        }).slice(0, 10) );
      },
      change: function( event, ui ) {
        var valid = false;
        if ( !ui.item ) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i" );
          for (value in munis) {
            if (matcher.test( munis[value] )) {
              valid = true;
              $(this).val(munis[value]);
              break;
            }
          }
          if (!valid) {
            // remove invalid value, as it didn't match anything
            $(this).val("");
            //input.data("autocomplete").term = "";
            return false;
          }
        }
      }
  }).data('ui-autocomplete')._renderItem = function( ul, item ) {
        return $( "<li>" ).append("<a>" + item.label + "</a>").appendTo( ul );
  };

  $( "#spatial_otro" ).keypress(function(event) {
    $('input:radio[name=typeSpatial]')[4].checked = true;
   /* $("#spatial_provincia").val("");
    $("#spatial_comarca").val("");
    $("#spatial_municipio").val("");*/
  });

  var listUrl = ['extras__4010', 'extras__4020'];
  for (var id in listUrl) {
    for (var idx = 0; idx < MAX_URL_LIST; idx++) {
      $("#" + listUrl[id] + idx + "__value").keypress(function(event) {
        if (event.keyCode == 13) {
          addURL_keypress(this.id);
        }
      });
    }
  }
  var config  = {
    disable_search: false,
    default_single_text: 'Hola'
  };

  for (var idx = 0; idx < (resourceCount+10); idx++) {
    if ($("#mimetypeSelect" + idx )) {
      $("#mimetypeSelect" + idx ).chosen(config).default_single_text= 'Hola';
    }
    if ($("#mimetype_innerSelect" + idx )) {
      $("#mimetype_innerSelect" + idx ).chosen(config).default_single_text= 'Hola';
    }
  }
}

function checkMetadataEditor() {
    // return true => send, return false => cancel form action

  var previousProblem = false;
  errorCreating = "Problemas creando el conjunto de datos. ";

    // check mandatory fields
  if (! checkMandatoryFields()) {
    previousProblem = true;
  }

    // check spatial
  if (! checkSpatial()) {
    previousProblem = true;
  }

    // complete values depending on radio button selected

    // check temporal
  if (! checkTemporal('TemporalFrom', 'extras__1101__value', 'inicial')) {
    previousProblem = true;
  }
  if (! checkTemporal('TemporalUntil', 'extras__1102__value', 'final')) {
    previousProblem = true;
  }

  if (! previousProblem) {
      //everything is ok
    disEnableTemporalItems(true);
    return true;
  } else {
    alert(errorCreating);
  }
  return false;
}

function hideBlankElements() {
  var list = ['extras__4000', 'extras__4001', 'extras__4002'];
  for (var id in listUrl) {
    if ($("#" + listUrl[id] + "__value").val() == "") {
      $("#" + listUrl[id] + "__block").addClass("oculto");
    }
  }
  var listUrl = ['extras__4010', 'extras__4020'];
  for (var id in listUrl) {
    for (var idx = 0; idx < MAX_URL_LIST; idx++) {
      if ($("#" + listUrl[id] + idx + "__value").val() == "") {
        $("#" + listUrl[id] + idx + "__block").addClass("oculto");
      }
    }
  }
}

function addTag() {
  if ($("#autocomplete_eurovoc").val() != '') {
    var _previousValue = '';
    if ($("#field-tags").val() != "") {
      _previousValue = $("#field-tags").val() + ',';
    }

    $("#field-tags").val(_previousValue + $("#autocomplete_eurovoc").val());
    $("#field-tags").trigger("change");
    $("#autocomplete_eurovoc").val('');
  }
}

function checkTemporal(id, idHidden, title) {
  var isoDate = '';
  var _year = $('#' + id + '_year').val();
  var _month = $('#' + id + '_month').val();
  var _day = $('#' + id + '_day').val();
  var _hour = $('#' + id + '_hour').val();
  var _min = $('#' + id + '_min').val();
  var _sec = $('#' + id + '_sec').val();

  if (_month.length == 1) { 
    _month = '0' + _month;
  }
  if (_day.length == 1) { 
    _day = '0' + _day;
  }
  if (_hour.length == 1) { 
    _hour = '0' + _hour;
  }
  if (_min.length == 1) { 
    _min = '0' + _min;
  }
  if (_sec.length == 1) { 
    _sec = '0' + _sec;
  }

  if (_year != '') {
    isoDate = _year;
    if (_month != '') {
      isoDate += '-' + _month;
      if (_day != '') {
        isoDate += '-' + _day;
        if (_hour != '') {
          isoDate += 'T' + _hour;
          if (_min != '') {
            isoDate += ':' + _min;
            if (_sec != '') {
              isoDate += ':' + _sec;
            }
          }
        }
      }
    }
  }
  if (isoDate != '') {
      // añadir timezone offset
    if (moment(isoDate).isValid()) {
      if (isoDate.indexOf("T") != -1) {
        var tzOffset = new Date(isoDate).getTimezoneOffset();
          // tested for Spain (+1/+2), improve for other locations
        if (tzOffset == 0) {
          isoDate = isoDate + 'Z';
        } else if (tzOffset < 0) {
          isoDate = isoDate + '+0' + Math.abs(tzOffset/60) + ':00';
        } else {
            // here for Spain => -1/-2 depending on date
          isoDate = isoDate + '-0' + Math.abs(tzOffset/60) + ':00';
        }
      }
      $('#' + idHidden).val(isoDate);
      return true;
    } else {
      errorCreating += "La fecha " + title + " no es válida. ";
      return false;
    }
  } else {
    $('#' + idHidden).val(isoDate);
    return true;
  }
}

function disEnableTemporalItems(value) {
  $("input:radio[name=typeSpatial]").attr("disabled", value);
  disEnableTemporal('TemporalFrom', 'extras__1101__value', value);
  disEnableTemporal('TemporalUntil', 'extras__1102__value', value);
}

function disEnableTemporal(id, idHidden, value) {
  $('#' + id + '_day').attr("disabled", value);
  $('#' + id + '_month').attr("disabled", value);
  $('#' + id + '_year').attr("disabled", value);
  $('#' + id + '_hour').attr("disabled", value);
  $('#' + id + '_min').attr("disabled", value);
  $('#' + id + '_sec').attr("disabled", value);
  $('#' + idHidden).attr("disabled", ! value);
}

  // return true => ok, return false => Problems
function checkSpatial() {
  var value = $("input:radio[name=typeSpatial]:checked").val();

  if (value == "Aragón") {
    $( "#extras__2000__value" ).val(value);
    $( "#extras__2001__value" ).val("Aragón");
    $( "#extras__2002__value" ).val( "http://opendata.aragon.es/recurso/territorio/ComunidadAutonoma/Aragón" );
    $( "#extras__2003__value" ).val( "Aragón" );
  } else if (value == "Provincia") {
    var item = $("#spatial_provincia").val();
    if (item != '') {
      $( "#extras__2000__value" ).val(value);
      $( "#extras__2001__value" ).val( item );
      $( "#extras__2002__value" ).val( "http://opendata.aragon.es/recurso/territorio/Provincia/" + item );
      $( "#extras__2003__value" ).val( item );
    } else {
      errorCreating += 'Incluya un valor válido de provincia en "Cobertura geográfica". ';
      return false;
    }
  } else if (value == "Comarca") {
    var item = $("#spatial_comarca").val();
    if (item != '') {
      if (aragopCom[item]) {
        $( "#extras__2000__value" ).val(value);
        $( "#extras__2001__value" ).val( item );
        $( "#extras__2002__value" ).val( "http://opendata.aragon.es/recurso/territorio/Comarca/" + aragopCom[item] );
        $( "#extras__2003__value" ).val( aragopCom[item] );
      } else {
        errorCreating += 'Incluya un valor válido de comarca en "Cobertura geográfica". ';
        return false;
      }
    } else {
      errorCreating += 'Incluya un valor válido de comarca en "Cobertura geográfica". ';
      return false;
    }
  } else if (value == "Municipio") {
    var item = $("#spatial_municipio").val();
    if (item != '') {
      if (aragopMun[item]) {
        $( "#extras__2000__value" ).val(value);
        $( "#extras__2001__value" ).val( item );
        $( "#extras__2002__value" ).val( "http://opendata.aragon.es/recurso/territorio/Municipio/" + aragopMun[item] );
        $( "#extras__2003__value" ).val( aragopMun[item] );
      } else {
        errorCreating += 'Incluya un valor válido de municipio en "Cobertura geográfica". ';
        return false;
      }
    } else {
      errorCreating += 'Incluya un valor válido de municipio en "Cobertura geográfica". ';
      return false;
    }
  } else if (value == "Otro") {
    var item = $("#spatial_otro").val();
    if (item != '') {
      $( "#extras__2000__value" ).val(value);
      $( "#extras__2001__value" ).val( item );
      $( "#extras__2002__value" ).val( "" );
      $( "#extras__2003__value" ).val( item );
    } else {
      errorCreating += 'Incluya un valor para otro en "Cobertura geográfica". ';
      return false;
    }
  }
  return true;
}

var MAX_URL_LIST = 99;

function removeURL(id, idx) {
  var idxToHidden = parseInt(idx);
    // si borran uno intermedio => desplazar todos un lugar antes

  var mustContinue = false;

  if (idxToHidden < MAX_URL_LIST) {
    if ($("#" + id + (idxToHidden+1) + "__value").val() != "") {
      mustContinue = true;
    }
  }

  while ( mustContinue ) {
    $("#" + id + idxToHidden + "__value").val($("#" + id + (idxToHidden+1) + "__value").val());
    idxToHidden++;
    mustContinue = false;

    if (idxToHidden < MAX_URL_LIST) {
      if ($("#" + id + (idxToHidden+1) + "__value").val() != "") {
        mustContinue = true;
      }
    }
  }

  $("#" + id + idxToHidden + "__value").val('');
  if (idxToHidden != 0) {
    $("#" + id + idxToHidden + "__block").addClass("oculto");
  }
}

function addURL_keypress(currentId) {
    // currentId == 'extras__40X0X__value
    // extract id
  var id = parseInt(currentId.substr(8).substr(0,5));

  if ((id % (MAX_URL_LIST+1)) < MAX_URL_LIST) {
    if ($("#" + currentId.substr(0,8) + (id + 1) + "__value").val() == "") {
      $("#" + currentId.substr(0,8) + (id + 1) + "__block").removeClass("oculto");
      $("#" + currentId.substr(0,8) + (id + 1) + "__value").focus();
    }
  }
}

function addURL(id) {
  var limit = true;

  for (var idx = 0; idx <= MAX_URL_LIST; idx++) {
    if ($("#" + id + idx + "__value").val() == "") {
      $("#" + id + idx + "__block").removeClass("oculto");
      $("#" + id + idx + "__value").focus();
      limit = false;
      break;
    }
  }
  if (limit) {
    alert("No es posible incluir más valores para este campo");
  }
}

function disEnableCheckboxes(value) {
  $(':checkbox:not(:checked)').each(function() {
    var auxId = this.id.replace(/__value/g, "__key");
    if ("#" + auxId) {
      $('#' + auxId).attr("disabled", value);
    }
  });
}

function removeExistingResource(url, idx) {
  var answer = window.confirm("¿Está seguro que desea borrar el recurso?");
  if (answer) {
    showPleaseWait();
    $.ajax({
      async: false,
      type: 'POST',
      url: url,
      success: function (data) {
                 alert("Recurso borrado correctamente");
                 $("#existing_resource" + idx).addClass("oculto");
                 changedResource[idx] = false;
                 alreadyCreatedResource[idx] = false;
                 hideModalDialog();
               },
      error: function (data) {
               alert("Problemas borrado el recurso. Envíe un email a opendata@aragon.es");
               hideModalDialog();
             }
    });
  }
}


function isBlankResource(idx) {
  if ($("#nameRes" + idx).val() == "") {
//    if ($("#mimeTypeRes" + idx).val() == "") {
  //    if ($("#mimeTypeInnerRes" + idx).val() == "") {
        if ($("#resType"+idx)[0].selectedIndex == 0) {
          if ($("#urlText_resType" + idx).val() == "") {
            return true;
          }
        } else {
          return true;
        }
    //  }
   // }
  }
  return false;
}

function removeNewResource(idx) {
  var idxToHidden = parseInt(idx);
    // si borran uno intermedio => desplazar todos un lugar antes

  var mustContinue = false;

  if (idxToHidden < MAX_URL_LIST) {
    if (! isBlankResource(idxToHidden+1)) {
      mustContinue = true;
    }
  }

  while ( mustContinue ) {
    shiftResource(idxToHidden);
    idxToHidden++;
    mustContinue = false;

    if (idxToHidden < MAX_URL_LIST) {
      if (! isBlankResource(idxToHidden+1)) {
        mustContinue = true;
      }
    }
  }

  clearResource(idxToHidden);
}

function shiftResource(idx) {
  $("#nameRes" + idx).val($("#nameRes" + (idx+1)).val());
//  $("#mimeTypeRes" + idx).val($("#mimeTypeRes" + (idx+1)).val());
  //$("#mimeTypeInnerRes" + idx).val($("#mimeTypeInnerRes" + (idx+1)).val());
  $("#resType"+idx)[0].selectedIndex = $("#resType"+(idx+1))[0].selectedIndex;
  $("#urlText_resType" + idx).val($("#urlText_resType" + (idx+1)).val());
  // TODO: ver lo que hay que borrar de la parte de vistas o file upload
  // TODO: Actualizar combos chosen
}

function clearResource(idx) {
  $("#new_resource" + idx).addClass("oculto");

  $("#nameRes" + idx).val("");
 // $("#mimeTypeRes" + idx).val("");
  //$("#mimeTypeInnerRes" + idx).val("");
  $("#resType"+idx)[0].selectedIndex = 0;
  $("#urlText_resType" + idx).val("");
  // TODO: ver lo que hay que borrar de la parte de vistas o file upload
  // TODO: Actualizar combos chosen
}

function addResource() {
  activateFileUploadForm();

  var limit = true;
  for (var idx = resourceCount; idx <= (resourceCount + MAX_URL_LIST); idx++) {
    if (isBlankResource(idx)) {
      $("#new_resource" + idx).removeClass("oculto");
      limit = false;
      break;
    }
  }
  if (limit) {
    alert("No es posible incluir más valores para este campo");
  }
}
function changesOnResource(idx) {
  changedResource[idx] = true;
}

function correctUrl(idx) {
  var item = document.getElementById("resType" + idx)
  var _value = item[item.selectedIndex].value;
  if (_value == "vista") {
    var vista = document.getElementById("vistas_value_resType"+idx).value;
    $("#vista_id_resType" + idx).val(vista);
      // don't care next URL because will be modified at controller
      // and it isn't ok
    $("#url_resType" + idx).val("http://" + document.location.host + "/catalogo/dataset/showVista?id=" + vista);
  } else if (_value == "file.upload") {
    $("#url_resType" + idx).val($("#uploadUrl_resType" + idx).val());
    $("#vista_id_resType" + idx).attr("disabled",true);
    $("#uploadUrl_resType" + idx).attr("disabled",true);
  } else {
    if ($("#urlText_resType" + idx).val() != "") {
      $("#url_resType" + idx).val($("#urlText_resType" + idx).val());
      $("#vista_id_resType" + idx).attr("disabled",true);
      $("#urlText_resType" + idx).attr("disabled",true);
    } else {
      return false;
    }
  }
  return true;
}

function updateFormat(idx) {
  var item = document.getElementById("mimetypeSelect" + idx)
  var _value = item[item.selectedIndex].value;
  var item_inner = document.getElementById("mimetype_innerSelect" + idx)
  var _value_inner = item_inner[item_inner.selectedIndex].value;
  if (_value_inner != '') {
    $("#format" + idx).val(item_inner[item_inner.selectedIndex].label);
  } else {
    $("#format" + idx).val(item[item.selectedIndex].label);
  }
}

function updateResources() {
  for (var idx = 0; idx < resourceCount; idx++) {
    if (changedResource[idx]) {

      if (correctUrl(idx)) {
        updateFormat(idx);

//      $("#resourceForm" + idx).submit();
        $.ajax({
          async: false,
          url: $("#resourceForm" + idx)[0].action,
          type: 'POST',
          data: $("#resourceForm" + idx).serialize(),
          success: function (data) {
                     $("#uploadUrl_resType" + idx).attr("disabled", false);
                     $("#urlText_resType" + idx).attr("disabled", false);
                   },
          error: function (data) {
                   $("#uploadUrl_resType" + idx).attr("disabled", false);
                   $("#urlText_resType" + idx).attr("disabled", false);
                   alert("Problemas actualizando recurso");
                 }
        });
      } else {
        alert("La URL del recurso no puede dejarse vacía");
      }
      changedResource[idx] = false;
    }
  }
}

function createNewResources() {
  for (var idx = resourceCount; idx <= (resourceCount + MAX_URL_LIST); idx++) {
    if (changedResource[idx]) {
      if (! isBlankResource(idx)) {
        if (! alreadyCreatedResource[idx]) {
          if (correctUrl(idx)) {
            updateFormat(idx);

            var action = '/catalogo/new_resource/' + $("#field-name").val();
            $.ajax({
              async: false,
              url: action,
              type: 'POST',
              data: $("#resourceForm" + idx).serialize(),
              success: function (data) {
                $("#uploadUrl_resType" + idx).attr("disabled", false);
                $("#urlText_resType" + idx).attr("disabled", false);

                $("#resourceForm" + idx)[0].action = '/catalogo/' + $("#field-name").val() + '/resource_edit/' + data;
                $("#removeResourceButton" + idx).attr("href", "javascript:removeExistingResource('/catalogo/" + $("#field-name").val() + "/resource_delete/" + data + "', '" + idx + "');");

                alreadyCreatedResource[idx] = true;
              },
              error: function (data) {
                $("#uploadUrl_resType" + idx).attr("disabled", false);
                $("#urlText_resType" + idx).attr("disabled", false);
                alert("Problemas creando el nuevo recurso"); 
              }
            });
          } else {
            alert("La URL del recurso no puede dejarse vacía");
          }
        } else {
          if ($("#urlText_resType" + idx).val() != "") {
            $.ajax({
              async: false,
              url: $("#resourceForm" + idx)[0].action,
              type: 'POST',
              data: $("#resourceForm" + idx).serialize(),
              success: function (data) {
                         $("#uploadUrl_resType" + idx).attr("disabled", false);
                         $("#urlText_resType" + idx).attr("disabled", false);
                       },
              error: function (data) {
debugger;
                       $("#uploadUrl_resType" + idx).attr("disabled", false);
                       $("#urlText_resType" + idx).attr("disabled", false);
                       alert("Problemas creando el nuevo recurso");
                     }
            });
          } else {
            alert("La URL del recurso no puede dejarse vacía");
          }
        }
      }
      changedResource[idx] = false;
    }
  }
}

function checkMandatoryFields() {
  var result = true;
  if ($("#field-title").val() == "") {
    errorCreating += "Es obligatorio incluir título. ";
    result = false;
  }
  if ($("#field-notes").val() == "") {
    errorCreating += "Es obligatorio incluir descripción. ";
    result = false;
  }

  return result;
}

function confirmRemove(url) {
  showModalDialog('<p class="letraGrande">¿Está seguro que desea borrar el conjunto de datos?</p><ul style="padding:10px;"><li><button onclick="javascript:removeConfirmed(\'' + url + '\');">Aceptar</button><button onclick="javascript:removeCancelled();">Cancelar</button> </li></ul><p>ATENCIÓN, si presiona &quot;Aceptar&quot; el conjunto de datos se borrará y dejará de ser accesible para los usuarios.</p><p>Recuerde que el acceso a los datos públicos es un derecho que tenemos todos los ciudadanos</p>');
}

function removeConfirmed(url) {
  hideModalDialog();
  showPleaseWait();
  $("#metadataEditorForm").attr("action", url);
  $("#metadataEditorForm").submit();
}

function removeCancelled() {
  hideModalDialog();
}

function sendContent(mustContinue) {
  var msg = "¿Está seguro que desea actualizar el conjunto de datos y finalizar la edición?";
  if (mustContinue) {
    msg = "¿Está seguro que desea actualizar el conjunto de datos y seguir editando?";
  }
  var answer = window.confirm(msg);
  if (answer) {
      // TODO: improve these part
      // it is possible to create resources and delete later
    if ((resourceCount == 0) && (isBlankResource(0))) {
      if (! window.confirm("Parece que no ha definido ficheros de datos y debería haber al menos uno. ¿Desea continuar?")) {
        return; 
      }
    }

    if (checkMetadataEditor()) {
      disEnableCheckboxes(true);
      hideBlankElements();
      disEnableAllItemsForm(true);
/*
          updateResources();
          createNewResources();

          showPleaseWait();
          if (mustContinue) {
            $("#metadataEditorForm").attr('target', 'hiddenIframe')
            $.ajax({
              type: 'POST',
              data: $("#metadataEditorForm").serialize(),
              success: function (data) { alert("Conjunto de datos actualizado correctamente. Puede continuar la edición. "); hideModalDialog();},
              error: function (data) { alert("Problemas actualizando el conjunto de datos. Envíe un email a opendata@aragon.es"); hideModalDialog();}
            });
          } else {
            $("#metadataEditorForm").attr('target', '_self');
            $('#metadataEditorForm').submit();
          }
*/

      if (isEditing) {
          // previous dataset => always maintain previous name for same url access
          // unless you are sysadmin
        if (isSysAdmin) {
          var question = "Al modificar el título, cambiará la url de acceso. ¿Desea que se modifique? Si pulsa aceptar, se modificará. Si pulsa cancelar, se mantendrá la anterior";
          if (! window.confirm(question)) {
            alert("Ok, mantenemos la anterior");
            $("#field-name").val($("#field-previous-name").val());
          }
        } else {
          $("#field-name").val($("#field-previous-name").val());
        }
      }

      showPleaseWait();

      $("#metadataEditorForm").attr('target', 'hiddenIframe')
      $.ajax({
        async: false,
        type: 'POST',
        data: $("#metadataEditorForm").serialize(),
        success: function (data) {
                   if (mustContinue) {
                     disEnableAllItemsForm(false);
                     disEnableCheckboxes(false);
                     disEnableTemporalItems(false);
                   }
                 },
        error: function (data) {
                 alert("Problemas actualizando el conjunto de datos. Envíe un email a opendata@aragon.es");
               }
      });
          
      updateResources();
      createNewResources();
      //alert("Conjunto de datos actualizado correctamente. Puede continuar la edición. "); 
      if (! mustContinue) {
        $("#metadataEditorForm").attr('action', '/catalogo/' + $("#field-name").val());
        $("#metadataEditorForm").attr('target', '_top');
        $("#metadataEditorForm").submit();
      } else {
          // we need to update _maxPositon's extras from package after creating/updating resources
        $.ajax({
          url: '/catalogo/api/action/package_show?id=' + $("#field-name").val(),
          async: false,
          type: 'POST',
          dataType: 'json',
          success: function(data) {
                     document.getElementById("extrasMaxPositionZone").innerHTML = "";
                     var count = 1;
                     var strHTML = "";
                     $.each(data['result']['extras'], function(index, element) {
                       var currentKey = element['key'];
                       if (currentKey.indexOf("_maxPosition") != -1) {
                         strHTML += '<input id="extras__4040' + count + '__key" type="hidden" value="' + currentKey + '" name="extras__4040' + count + '__key" autocomplete="off">';
                         strHTML += '<input id="extras__4040' + count + '__value" type="text" placeholder="" value="' + element['value'] + '" name="extras__4040' + count + '__value" autocomplete="off">';
                         count++;
                       }
                     });
                     document.getElementById("extrasMaxPositionZone").innerHTML = strHTML;
                   },
          error: function (data) {
                   alert("Problemas actualizando el conjunto de datos. Envíe un email a opendata@aragon.es");
                 }
        });
      }
      hideModalDialog();
    }
  }
}

function showPleaseWait() {
  showModalDialog('<p class="letraGrande">Cargando...</p> <p class="letraGrande">Espere por favor</p><img src="/public/i/loadingAODiconWhite.gif" width="100">');
}

function showModalDialog(content) {
  var htmlCode ='<div style="z-index: 22222; background-color: #888888; width: 100%; height: 100%; position: fixed; top: 0px; left: 0px; opacity: 0.4;" id="modalDialogDiv"></div>'
    + '<div style="float:right;width:100%;top: 40%;position:fixed;z-index:22222;" id="modalDialogText">'
    + '  <div style="float:left;left:50%;position:relative;width:200px">'
    + '<div style="z-index: 22222; right: 50%; float: right; width: 400px; padding: 20px; opacity: 1 ! important; background-color: #73A5BD; color: rgb(255, 255, 255);">'
    + content
    + '</div>'
    + '  </div></div>';
    
  $(htmlCode).appendTo("body");
}

function hideModalDialog() {
  $("#modalDialogDiv").remove();
  $("#modalDialogText").remove();
}

function loadComboboxesVistas() {
    // strange way of determining is editing, but it works
  if (document.getElementById("autocomplete_eurovoc")) {
    $.ajax({
      url: '/catalogo/cargarVistasUsuario/',
      async: false,
      data:"user=" + currentUser,
      dataType: 'json',
      success: 
        function(data) {
          $.each(data, function(index, element) {
            for (var idx = 0; idx < (resourceCount+10); idx++) {
              if ($("#vistas_value_resType" + idx )) {
                if (element[0] == currentViewResource[idx]) {
                  $("#vistas_value_resType" + idx ).append('<option value="' + element[0] + '" selected>' + element[1] + '</option>');
                } else {
                  $("#vistas_value_resType" + idx ).append('<option value="' + element[0] + '">' + element[1] + '</option>');
                }
              }
            }
          });
          var config  = {
            disable_search: true
          };
          var fOnChgChosen_resource = function onChgChosen_resource() {
            /*limpiarPantalla(this.id.substr("vistas_value_".length));
            cargarVista(false, this.id.substr("vistas_value_".length));*/
          }

          for (var idx = 0; idx < resourceCount; idx++) {
            if ($("#vistas_value_resType" + idx )) {
              $("#vistas_value_resType" + idx ).chosen(config).change(fOnChgChosen_resource);
            }
          }

          for (var idx = resourceCount; idx < (resourceCount+10); idx++) {
            if ($("#vistas_value_resType" + idx )) {
              $("#vistas_value_resType" + idx ).chosen(config).change(fOnChgChosen_resource);
            }
          }
       },
       error: function(jqXHR, textStatus, errorThrown) {
         alert("No se ha podido obtener la lista de vistas a bases de datos");
       }
    });
  }
}

function resetSelect(id){
  try{
    var elem = document.getElementById("vistas_value_"+id);
    elem.selectedIndex=-1;
    elem.value=-1;
    limpiarPantalla(id);
  }catch(err){}
}

function limpiarPantalla(id){
  try{
    document.getElementById("filtro_"+id).value = "";
    document.getElementById("botonesDiv_"+id).innerHTML = "";
    document.getElementById("vistaDiv_"+id).innerHTML = "";
  }catch(err){}
}

function cargarVista(completa,id) {
  var vistaDiv = document.getElementById("vistaDiv_"+id);
  var botonesDiv = document.getElementById("botonesDiv_"+id);

  var self = this;
  var vista = document.getElementById("vistas_value_"+id).value;
  if (vista == -1){
    alert("Debe seleccionar una vista de las disponibles");
  }else{
    try{
      var filtro = document.getElementById("filtro_"+id).value;
    }catch(err){
      var filtro = "";
    }

    $.ajax({
          async: false,
          url:'/catalogo/vista/' + vista,
          data:"filtro=" + filtro + ";completa=" + completa,
          dataType: 'json',
          success: function(data) {

      if (data.length != 0){
        var table = '<table style="width:100%;border: 1px solid black;margin-top:20px;margin-bottom:20px;border-collapse:collapse;">';

        $.each(data, function(index, element){
          table= table + '<tr style="border= 1px solid black;">';
          $.each(element, function(i, item){
            if (index== 0){
              table= table + '<td style="border: 1px solid black; font-weight: bold;">' + item + '</td>';
            }else{
              if (index%2!=0){
                table= table + '<td style="border: 1px solid black; background-color:#76a1b8;">' + item + '</td>';
              }else{
                table= table + '<td style="border:1px solid black;">' + item + '</td>';
              }
            }
          });
          table= table + '</tr>';
        });

        table = table +  '</table>';

        if (completa){
          var win = window.open();
          win.document.open();
          win.document.write(table);
          //win.document.close();
        }else{
          $("#vistaDiv_"+id).removeClass('oculto');
          botonesDiv.innerHTML = '<label style="float:left; margin-top: 4px;" class="field_opt" for="filtro">Filtro:&nbsp;&nbsp;</label>' +
             '<input style="float:left;width:300px;height: 25px;" id="filtro_'+id +'" name="filtro_'+id +'" type="text" class="input-small" value="' + filtro + '"/>' +
             '<input style="float:left;" type="button" onClick="cargarVista(false,\'' + id + '\')" class="recuadroRecto" value="Filtrar" />';
          vistaDiv.innerHTML = table + '<input name="execute" onClick="cargarVista(true,\'' + id + '\')" class="recuadroRecto" value="Ver todos los resultados" />';

        }
      }else{
        vistaDiv.innerHTML = '<div style="clear:both"> </div><span>No se han encontrado resultados</span>';
      }

          },
          error: function(jqXHR, textStatus, errorThrown) {
      //alert("No se ha podido llevar a cabo la consulta");
          }

    });
  }
}

function checkUserInfoRequired() {
  if ($("#field-password-confirm").val() == "") {
    return false;
  }
  if ($("#field-password").val() == "") {
    return false;
  }
  if ($("#field-current-password").val() == "") {
    return false;
  }
  if ($("#field-username-email").val() == "") {
    return false;
  }
  return true;
}
function checkOrganizationInfoRequired() {
  return true;
}

function updateOrganizationInfo() {

  if (checkOrganizationInfoRequired()) {
    showPleaseWait();

    if ($("#field-previous-email").val() != $("#field-username-email").val()) {
      $.ajax({
        async: false,
        url: $("#updateEmailForm")[0].action,
        type: 'POST',
        data: $("#updateEmailForm").serialize(),
        success: function (data) {
                   if (data != 'OK') {
                     alert("Problemas actualizando la información del email de contacto: " + data);
                   }
                 },
        error: function (data) {
                 alert("Problemas actualizando el email de contacto de la organización");
               }
      });
    }


    $.ajax({
       async: false,
       url: $("#updateOrganizationForm")[0].action,
       type: 'POST',
       data: $("#updateOrganizationForm").serialize(),
       success: function (data) {
                  if (data == 'OK') {
                    alert("Actualización completada con éxito");
//                  } else {
  //                  alert("Problemas actualizando la información de la organización: " + data);
                  }

                  hideModalDialog();
                },
       error: function (data) {
                alert("Problemas actualizando la información de la organización");
                hideModalDialog();
              }
    });
  }
}

function updateUserInfo() {
  if (checkUserInfoRequired()) {
    showPleaseWait();
    $("#field-email-for-password").val($("#field-username-email").val());
    $.ajax({
       async: false,
       url: $("#updatePasswordForm")[0].action,
       type: 'POST',
       data: $("#updatePasswordForm").serialize(),
       success: function (data) {
                  if (data == 'OK') {
                    alert("Actualización completada con éxito");
                  } else {
                    alert("Problemas actualizando la información de usuario: " + data);
                  }
                  $("#field-password-confirm").val("");
                  $("#field-password").val("");
                  $("#field-current-password").val("");

                  hideModalDialog();
                },
       error: function (data) {
                alert("Problemas actualizando la información de usuario");
                hideModalDialog();
              }
    });
  } else {
    alert("Debe rellenar todos los campos");
  }
}

function submitTxtQueryOrg() {
  $("#textQueryOrgDataset").val(encodeURI($("#textQueryOrgDataset").val()));
  $("#orgDatasetQueryForm").submit();
}


