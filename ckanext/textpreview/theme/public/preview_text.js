// json preview module
ckan.module('textpreview', function (jQuery, _) {
  return {
    options: {
      i18n: {
        error: _('An error occurred: %(text)s %(error)s')
      },
      parameters: {
        json: {
          contentType: 'application/json',
          dataType: 'json',
          dataConverter: function (data) { return JSON.stringify(data, null, 2); },
          language: 'json'
        },
        jsonp: {
          contentType: 'application/javascript',
          dataType: 'jsonp',
          dataConverter: function (data) { return JSON.stringify(data, null, 2); },
          language: 'json'
        },
        xml: {
          contentType: 'text/xml',
          dataType: 'text',
          language: 'xml'
        },
        text: {
          contentType: 'text/plain',
          dataType: 'text',
          language: ''
        }
      }
    },
    initialize: function () {
      var self = this;
      var format = preload_resource['format'].toLowerCase();

      var TEXT_FORMATS = preview_metadata['text_formats'];
      var XML_FORMATS = preview_metadata['xml_formats'];
      var JSON_FORMATS = preview_metadata['json_formats'];
      var JSONP_FORMATS = preview_metadata['jsonp_formats'];

      var p;

      if (JSON_FORMATS.indexOf(format) !== -1) {
        p = this.options.parameters.json;
      } else if (JSONP_FORMATS.indexOf(format) !== -1) {
        p = this.options.parameters.jsonp;
      } else if(XML_FORMATS.indexOf(format) !== -1) {
        p = this.options.parameters.xml;
      } else {
        p = this.options.parameters.text;
      }

      if (format == "px") {
        jQuery.ajax(preload_resource['url'], {
          type: 'GET',
          contentType: p.contentType,
          dataType: p.dataType,
          success: function(data, textStatus, jqXHR) {
            data = p.dataConverter ? p.dataConverter(data) : data;

            var resourceData = self.parsePX(data);

            dataset = new recline.Model.Dataset(resourceData);
            errorMsg = "Error cargando la previsualizaci&oacute;n: Error accediendo a los datos";

            dataset.fetch()
              .done(function(dataset){      
                dataset.bind('query:fail', function (error) {        
                  jQuery('.data-view-container', self.el).hide();
                  jQuery('.header', self.el).hide();
                });

                self.initializeDataExplorer(dataset);

                $("#titlePX").html(titlePX);
                $("#sourcePX").html(sourcePX);
                $("#notePX").html(notePX);
              })
              .fail(function(error){
                if (error.message) errorMsg += ' (' + error.message + ')';
                showError(errorMsg);
              });

          },
          error: function(jqXHR, textStatus, errorThrown) {
            if (textStatus == 'error' && jqXHR.responseText.length) {
              self.el.html(jqXHR.responseText);
            } else {
              self.el.html(self.i18n('error', {text: textStatus, error: errorThrown}));
            }
          }
        });
      } else {
        jQuery.ajax(preload_resource['url'], {
          type: 'GET',
          contentType: p.contentType,
          dataType: p.dataType,
          success: function(data, textStatus, jqXHR) {
            data = p.dataConverter ? p.dataConverter(data) : data;

            var highlighted;

            if (p.language) {
              highlighted = hljs.highlight(p.language, data, true).value;
            } else {
              highlighted = '<pre>' + data + '</pre>';
            }

            self.el.html(highlighted);
          },
          error: function(jqXHR, textStatus, errorThrown) {
            if (textStatus == 'error' && jqXHR.responseText.length) {
              self.el.html(jqXHR.responseText);
            } else {
              self.el.html(self.i18n('error', {text: textStatus, error: errorThrown}));
            }
          }
        });
      }
    },
    parsePX: function (data) {
      var px = new Px(data);

      var resourceData = preload_resource;
      resourceData.format = resourceData.formatNormalized;
      resourceData.backend = "Memory";

      resourceData.fields = ['-'];
      var typeHeading = px.metadata.HEADING.TABLE;
      var typeStub = px.metadata.STUB.TABLE;
      var dimensionsList = "";

      if (typeof(px.metadata.HEADING.TABLE) == "object") {
          // there are several dimensions, show only one, fix other to first value
        typeHeading = px.metadata.HEADING.TABLE[px.metadata.HEADING.TABLE.length-1];

        for (var z = 0; z < px.metadata.HEADING.TABLE.length-1; z++) {
          var currentDimension = px.metadata.HEADING.TABLE[z];
          dimensionsList += "(" + currentDimension + "=" + px.values(currentDimension)[0] + ") ";
        }
      }
    
      if (typeof(px.metadata.STUB.TABLE) == "object") {
          // there are several dimensions, show only one, fix other to first value
        typeStub = px.metadata.STUB.TABLE[px.metadata.STUB.TABLE.length-1];
        for (var z = 0; z < px.metadata.STUB.TABLE.length-1; z++) {
          var currentDimension = px.metadata.STUB.TABLE[z];
          dimensionsList += "(" + currentDimension + "=" + px.values(currentDimension)[0] + ")";
        }
      }

      var numCols = 0;
      for (ii in px.values(typeHeading)) {
        if (parseInt(ii) < 10) { //only show 10 columns max
          resourceData.fields.push(px.values(typeHeading)[ii]);
          numCols++;
        } else {
          break;
        }
      }
      resourceData.records = [];
      var numRow = 0;

      var offset = 1;

      if (typeof(px.metadata.HEADING.TABLE) == "object") {
        for (idx in px.metadata.HEADING.TABLE) {
          offset = offset * px.values(px.metadata.HEADING.TABLE[idx]).length;
        }
      } else {
        offset = px.values(px.metadata.HEADING.TABLE).length;
      }

      for (jj in px.values(typeStub)) {
        if (parseInt(jj) < 30) { //only show 30 rows max
          var aux = {};
          aux['-'] = px.values(typeStub)[jj];
          var kk = 0;

          for (ii in px.values(typeHeading)) {
            if (parseInt(ii) < 10){ //only show 10 columns max
              aux[px.values(typeHeading)[ii]] = px.datum([0,kk+(numRow*offset)]);
              kk++;
            } else {
              break;
            }
          }
          numRow++;
          resourceData.records.push(aux);
        } else {
          break;
        }
      }

      if (dimensionsList != "") {
        titlePX = "<strong>Mostrando los valores para las dimensiones" + dimensionsList + "</strong>";
      }

      sourcePX = "";
      if (px.metadata.SOURCE) {
        if (px.metadata.SOURCE.TABLE) {
          sourcePX = "Fuente: " + px.metadata.SOURCE.TABLE;
        }
      }
      notePX = "";
      if (px.metadata.NOTE) {
        if (px.metadata.NOTE.TABLE) {
          notePX = "Notas: " + px.metadata.NOTE.TABLE;
        }
      }

      return resourceData;
    },
    initializeDataExplorer: function(dataset) {
      var views = [
        {
          id: 'grid',
          label: 'Tabla',
          view: new recline.View.SlickGrid({
            model: dataset,
      state: {fitColumns: true}
          })
        },
        {
          id: 'graph',
          label: 'Gr&aacute;ficas',
          view: new recline.View.Graph({
            model: dataset
          })
        }
      ];

      var sidebarViews = [
        {
          id: 'valueFilter',
          label: 'Filtros',
          view: new recline.View.ValueFilter({
            model: dataset
          })
        }
      ];

      var dataExplorer = new recline.View.MultiView({
        el: this.el,
        model: dataset,
        views: views,
        sidebarViews: sidebarViews,
        config: {
          readOnly: true
        }
      });

    }
  };
});


