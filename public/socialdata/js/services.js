angular.module('aosd.services', [])

  .factory('escuchaAPI', function($http, settings) {
    var escuchaAPI = {};

    escuchaAPI.getMetadata = function() {
      return $http({
        method: 'GET',
        url: settings.API_URL + '/get_metadata/'
      })
    }

    escuchaAPI.getEvolution = function(terms, region, start, end) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_evol/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end}
      });
    }

    escuchaAPI.getMultitermEvolution = function(terms, region, start, end) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/multiterm_evolution/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end}
      });
    }

    escuchaAPI.getTotals = function(terms, region, start, end) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_totals/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end}
      });
    }

    escuchaAPI.getTops = function(terms, region, start, end) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_tops/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end}
      });
    }

    escuchaAPI.getLastItems = function(terms, region, start, end, page, is_geo) {
      if (page === undefined) page = 0;
      if (is_geo === undefined) is_geo = false;
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_last_items/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end, 'page': page, 'is_geo': is_geo}
      });
    }

    escuchaAPI.getPolarity = function(terms, region, start, end) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_polarity/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end}
      });
    }

    escuchaAPI.getGeogrid = function(terms, region, start, end, weight) {
      if (weight === undefined) weight = false;
      return $http({
        method: 'POST',
        url: settings.API_URL + '/geogrid/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end, 'weight': weight}
      });
    }

    escuchaAPI.getGraph = function(terms, region, start, end, num_nodes) {
      return $http({
        method: 'POST',
        url: settings.API_URL + '/get_graph/',
        data: {'terms': terms, 'region': region, 'start': start, 'end': end, 'num_nodes': num_nodes}
      });
    }

    return escuchaAPI;
  })

  .factory('subscriptionsAPI', function($http, $cookies, settings) {
    var subscriptionsAPI = {};

    var errorTranslations = {
      'Invalid request': 'Petición no válida',
      'Invalid credentials': 'Credenciales no válidos',
      'The given email must be set': 'El campo email no debe estar vacío',
      'The given password must be set': 'El campo contraseña no debe estar vacío',
      'The email is yet registered': 'El email introducido ya está registrado',
      'Missed auth token': 'Token de autenticación no encontrado',
      'Invalid token': 'Token de autenticación no válido',
      'Empty subscription': 'Subscripción sin términos',
      'Invalid reset link': 'Link de restablecimiento de contraseña no válido',
    }

    subscriptionsAPI.login = function(email, password) {
      var response = $http({
        method: 'POST',
        url: settings.API_URL + '/auth/',
        data: {'email': email, 'password': password}
      });
      response.success(function (resp_data) {
        $cookies.put('jwt_token', resp_data.jwt_token);
      }).error(function (resp_data) {
        resp_data.error = errorTranslations[resp_data.error];
      });
      return response;
    }

    subscriptionsAPI.logout = function() {
      $cookies.remove('jwt_token');
    }

    subscriptionsAPI.is_logged = function() {
      return $cookies.get('jwt_token') !== undefined;
    }

    subscriptionsAPI.register = function (email, password) {
      var response = $http({
        method: 'POST',
        url: settings.API_URL + '/register/',
        data: {'email': email, 'password': password}
      });
      response.error(function (resp_data) {
        resp_data.error = errorTranslations[resp_data.error];
      });
      return response;
    }

    subscriptionsAPI.passwordChange = function(old_password, new_password) {
      var response = $http({
        method: 'POST',
        url: settings.API_URL + '/password_change/',
        data: {'old_password': old_password, 'new_password': new_password},
        headers: {'JWT-TOKEN': $cookies.get('jwt_token')},
      });
      response.success(function (resp_data) {
        $cookies.put('jwt_token', resp_data.jwt_token);
      }).error(function (resp_data) {
        resp_data.error = errorTranslations[resp_data.error];
      });
      return response;
    }

    subscriptionsAPI.passwordReset = function(email) {
      var response = $http({
        method: 'POST',
        url: settings.API_URL + '/password_reset/',
        data: {'email': email},
      });
      response.error(function (resp_data) {
        resp_data.error = errorTranslations[resp_data.error];
      });
      return response;
    }

    subscriptionsAPI.passwordResetConfirm = function(t, new_password) {
      var response = $http({
        method: 'POST',
        url: settings.API_URL + '/password_reset_confirm/',
        data: {'t': t, 'new_password': new_password},
      });
      response.error(function (resp_data) {
        resp_data.error = errorTranslations[resp_data.error];
      });
      return response;
    }

    subscriptionsAPI.subscribe = function(subscriptions) {
      if (subscriptionsAPI.is_logged()) {
        var response = $http({
          method: 'POST',
          url: settings.API_URL + '/subscribe/',
          data: {'subscriptions': subscriptions},
          headers: {'JWT-TOKEN': $cookies.get('jwt_token')},
        });
        response.error(function (resp_data) {
          resp_data.error = errorTranslations[resp_data.error];
        });
        return response;
      }
    }

    subscriptionsAPI.get_subscriptions = function() {
      if (subscriptionsAPI.is_logged()) {
        var response = $http({
          method: 'GET',
          url: settings.API_URL + '/get_subscriptions/',
          headers: {'JWT-TOKEN': $cookies.get('jwt_token')},
        });
        response.error(function (resp_data) {
          resp_data.error = errorTranslations[resp_data.error];
        });
        return response;
      }
    }

    subscriptionsAPI.cancel_subscription = function() {
      if (subscriptionsAPI.is_logged()) {
        var response = $http({
          method: 'DELETE',
          url: settings.API_URL + '/cancel_subscription/',
          headers: {'JWT-TOKEN': $cookies.get('jwt_token')},
        });
        response.success(function (resp_data) {
        }).error(function (resp_data){
          resp_data.error = errorTranslations[resp_data.error];
        });
        return response;
      }
    }

    return subscriptionsAPI;
  })

  .factory('selection', function() {
    // Singleton object to store the user selection
    var selection = {
      region: '*',
      start: '',
      end: '',
      terms: [''],
      totals: null,
    }

    selection.updateFromQueryString = function(queryString) {
      this.region = (queryString.region !== undefined) ? queryString.region : '*';
      this.start = (queryString.start !== undefined) ? queryString.start : '';
      this.end = (queryString.end !== undefined) ? queryString.end : '';
      if (queryString.term !== undefined) {
        this.terms = (Array.isArray(queryString.term)) ? queryString.term : [queryString.term];
      } else {
        this.terms = ['*'];
      }
    }

    return selection;
  })

  .factory('sigmaSingleton', function() {
    return sigmaSingleton = {
      instance: null
    }
  })

  .factory('drawers', function(helpers) {
    var drawers = {};

    drawers.drawEvolutionTotal = function(scope, response) {
      scope.evolution_total = {
        "type": "LineChart",
        "data": {
          "cols": [{"type": "date", "label": "Fecha"}, {"type": "number", "label": "Todos los temas"}],
          "rows": [],
        },
        "options": {
          "legend" : {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "tooltip": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "vAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "hAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
        },
        "formatters": {},
        "displayed": true
      }

      for (i=0; i<response.evolution.length; i++) {
        var row = response.evolution[i];;
        scope.evolution_total.data.rows.push({
          "c": [
            {"v": new Date(row.key - 120*1000*60)},
            {"v": row.doc_count},
          ]
        });
      }
    }

    drawers.drawMultitermEvolution = function(scope, response) {
      scope.evolution = {
        "type": "LineChart",
        "data": {
          "cols": [{"type": "date", "label": "Fecha"}],
          "rows": [],
        },
        "options": {
          "legend" : {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "tooltip": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "vAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "hAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
        },
        "formatters": {},
        "displayed": true
      }

      scope.evolution.data.cols.push({"type": "number", "label": 'Mensajes con "' + response.evolution[0].term + '"'})

      for (x=0; x<response.evolution[0].data.length; x++) {
        var row = response.evolution[0].data[x];
        scope.evolution.data.rows.push({
          "c": [
            {"v": new Date(row.key - 120*1000*60)},
            {"v": row.doc_count},
          ]
        })
      }

      for (i=1; i<response.evolution.length; i++) {
        var term = response.evolution[i];
        scope.evolution.data.cols.push({"type": "number", "label": 'Mensajes con "' + term.term + '"'})
        for (x=0; x<term.data.length; x++) {
          var row = term.data[x];
          scope.evolution.data.rows[x]["c"].push({"v": row.doc_count});
        }
      }
    }

    drawers.drawTotals = function(scope, response) {
      // Total by source
      scope.total_by_source = {
        "type": "PieChart",
        "data": {
          "cols": [{type: 'string', label: 'Fuente'}, {type: 'number', label: 'Mensajes'}],
          "rows": [],
        },
        "options": {
          "legend" : {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "tooltip": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "vAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "hAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "chartArea": {"left": 0, "width": "100%"},
        },
        "formatters": {},
        "displayed": true
      }

      for (i=0; i<response.total_by_source.length; i++) {
        var row = response.total_by_source[i];;
        scope.total_by_source.data.rows.push({
          "c": [
            {"v": row.key},
            {"v": row.doc_count},
          ]
        });
      }

      // Total by type
      scope.total_by_type = {
        "type": "PieChart",
        "data": {
          "cols": [{type: 'string', label: 'Tipo de dato'}, {type: 'number', label: 'Mensajes'}],
          "rows": [],
        },
        "options": {
          "legend" : {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "tooltip": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "vAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "hAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "chartArea": {"left": 0, "width": "100%"},
        },
        "formatters": {},
        "displayed": true
      }

      for (i=0; i<response.total_by_type.length; i++) {
        var row = response.total_by_type[i];;
        scope.total_by_type.data.rows.push({
          "c": [
            {"v": row.key},
            {"v": row.doc_count},
          ]
        });
      }

      // Counts
      scope.count = response.count;
      scope.count_geo = response.count_geo;
      scope.count_authors = response.count_authors;
      scope.count_hashtags = response.count_hashtags;
      scope.count_mentions = response.count_mentions;
    }

    drawers.drawHemicycles = function(scope, response) {
      // Hashtags
      scope.hemicycle_hashtags = {
        options: {
          chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false,
            spacingBottom: 0,
            spacingTop: 0,
            spacingLeft: 0,
            spacingRight: 0,
            width: null,
            height: null
          },
          plotOptions: {
            pie: {
              dataLabels: {
                enabled: true,
                style: {
                  fontWeight: 'bold',
                  color: '#666',
                }
              },
              startAngle: -90,
              endAngle: 90,
              center: ['50%', '75%']
            }
          },
          title: {
            text: 'Hashtags',
            align: 'center',
            verticalAlign: 'middle',
            style: {'fontSize': '1vw'},
            y: 80
          },
          tooltip: {
            pointFormat: 'Hashtags: <b>{point.y}</b>'
          },
          credits: {
            enabled: false
          },
        },
        series: [{
          type: 'pie',
          name: 'Usuarios',
          innerSize: '50%',
          data: []
        }],
        loading: false
      }
      for (i=0; i<Math.min(response.top_hashtags.length, 20); i++) {
        var row = response.top_hashtags[i];
        scope.hemicycle_hashtags.series[0].data.push({'name': row.key, 'y': row.doc_count});
      }

      // Mentions
      scope.hemicycle_mentions = {
        options: {
          chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false,
            spacingBottom: 0,
            spacingTop: 0,
            spacingLeft: 0,
            spacingRight: 0,
            width: null,
            height: null
          },
          plotOptions: {
            pie: {
              dataLabels: {
                enabled: true,
                style: {
                  fontWeight: 'bold',
                  color: '#666',
                }
              },
              startAngle: -90,
              endAngle: 90,
              center: ['50%', '75%']
            }
          },
          title: {
            text: 'Menciones',
            align: 'center',
            verticalAlign: 'middle',
            style: {'fontSize': '1vw'},
            y: 80
          },
          tooltip: {
            pointFormat: 'Menciones: <b>{point.y}</b>'
          },
          credits: {
            enabled: false
          },
        },
        series: [{
          type: 'pie',
          name: 'Usuarios',
          innerSize: '50%',
          data: []
        }],
        loading: false
      }
      for (i=0; i<Math.min(response.top_mentions.length, 20); i++) {
        var row = response.top_mentions[i];
        scope.hemicycle_mentions.series[0].data.push({'name': row.key, 'y': row.doc_count});
      }
    }

    drawers.drawPolarity = function(scope, response) {
      // Polarity
      total_positive = 0;
      total_negative = 0;
      total_neutral = 0;
      positive_level = 0;
      negative_level = 0;
      for (i=0; i<response.polarities.length; i++) {
        total_positive += response.polarities[i].polarity.positive.doc_count;
        total_negative += response.polarities[i].polarity.neutral.doc_count;
        total_neutral += response.polarities[i].polarity.negative.doc_count;
        positive_level += response.polarities[i].polarity_pos;
        negative_level += response.polarities[i].polarity_neg;
      }
      if (response.polarities.length > 0) {
        positive_level = positive_level / response.polarities.length;
        negative_level = negative_level / response.polarities.length;
      }

      scope.polarity = {
        "type": "PieChart",
        "data": {
          "cols": [{type: 'string', label: 'Sentimiento'}, {type: 'number', label: 'Valor'}],
          "rows": [
            {"c": [{"v": "Positivo"}, {"v": total_positive}]},
            {"c": [{"v": "Neutro"}, {"v": total_negative}]},
            {"c": [{"v": "Negativo"}, {"v": total_neutral}]},
          ],
        },
        "options": {
          "legend" : {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "tooltip": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "vAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "hAxis": {"textStyle": {"fontName": 'Lato', "fontSize": 13, "bold": false}},
          "slices": {
            0: { "color": '#19AC20' },
            1: { "color": '#1936AC' },
            2: { "color": '#AC2019' },
          }
        },
        "formatters": {},
        "displayed": true
      }

      // Polarity positive
      scope.polarity_pos = [{'Nivel': positive_level}];
      scope.polarity_pos_cols = [{'id': 'Nivel', 'type': 'gauge'}];

      // Polarity negative
      scope.polarity_neg = [{'Nivel': negative_level}];
      scope.polarity_neg_cols = [{'id': 'Nivel', 'type': 'gauge'}];

      // Polarity by term
      scope.terms_polarity = []
      for (i=0; i<response.polarities.length; i++) {
        scope.terms_polarity.push({
          'term': response.polarities[i].term,
          'polarity': [{'polaridad': response.polarities[i].polarity_total}],
          'polarity_cols': [{'id': 'polaridad', 'type': 'bar'}]
        });
      }
    }

    drawers.drawMap = function(scope, response) {
      var gridData = [];
      scope.weight_max = (response.geogrid.length > 0) ? 2 : 0;
      scope.weight_min = null;
      scope.num_items = 0;
      for (i=0; i<response.geogrid.length; i++) {
        var row = response.geogrid[i];
        var weight = (scope.map_weight) ? row.weight.value : row.doc_count;
        gridData.push({
          location: new google.maps.LatLng(row.lat, row.lon),
          weight:weight
        });
        if (weight > scope.weight_max) {
          scope.weight_max = weight;
        }
        if (scope.weight_min === null || weight < scope.weight_min) {
          scope.weight_min = weight;
        }
        scope.num_items += row.doc_count;
      }
      if (scope.weight_min === null) {
        scope.weight_min = 0;
      }

      var pointArray = new google.maps.MVCArray(gridData);
      scope.map.heatLayer.setData(pointArray);
      scope.map.heatLayer.setOptions({maxIntensity: scope.weight_max*0.1});
    }

    drawers.drawGraph = function(scope, response) {
      scope.sigmaGraph = {
          nodes: [],
          edges: []
        }
        for (i = 0; i < response.nodes.length; i++) {
          scope.sigmaGraph.nodes.push({
            id: response.nodes[i].id,
            db_id: response.nodes[i].db_id,
            label: response.nodes[i].l,
            x: response.nodes[i].x,
            y: response.nodes[i].y,
            size: response.nodes[i].s,
            color: helpers.hexToRgb4(response.nodes[i].c).toString()
          });
        }
         for (i = 0; i < response.edges.length; i++) {
          scope.sigmaGraph.edges.push({
            id: response.edges[i].id,
            source: response.edges[i].s,
            target: response.edges[i].t,
            size: response.edges[i].w,
            color: helpers.hexToRgb4(response.edges[i].c).toString(),
            weight: response.edges[i].w,
            type: "curve"
          });
        }
    }

    return drawers;
  })

  .factory('helpers', function() {
    var helpers = {};

    helpers.hexToRgb4 = function(hex) {
      var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})|([a-f\d]{1})([a-f\d]{1})([a-f\d]{1})([a-f\d]{1})$/i.exec(hex);
      return result ? {
        r: parseInt(hex.length <= 4 ? result[4]+result[4] : result[1], 16),
        g: parseInt(hex.length <= 4 ? result[5]+result[5] : result[2], 16),
        b: parseInt(hex.length <= 4 ? result[6]+result[6] : result[3], 16),
        a: parseFloat(parseInt(hex.length <= 4 ? result[7]+result[7] : result[4], 16) / 255.0),
        toString: function() {
          var arr = [];
          arr.push(this.r);
          arr.push(this.g);
          arr.push(this.b);
          arr.push(this.a);
          return "rgba(" + arr.join(",") + ")";
        }
      } : null;
    }

    helpers.titleCase = function(input) {
      var output = [];
      var words = input.split(' ');
      for (i=0; i<words.length; i++) {
        output.push(words[i].charAt(0).toUpperCase() + words[i].slice(1));
      }
      return output.join(' ');
    }

    helpers.strToDate = function(str) {
      // Convert a string to a Date object. String format dd/mm/yyyy
      parts = str.split('/')
      // please put attention to the month (parts[0]), Javascript counts months from 0:
      // January - 0, February - 1, etc
      return new Date(parts[2], parts[1]-1, parts[0])
    }

    helpers.dateToStr = function(date) {
      day = date.getDate();
      month = date.getMonth() + 1;
      year = date.getFullYear();
      return day + '/' + month + '/' + year;
    }

    var defaultDiacriticsRemovalap = [
      {'base':'A', 'letters':'\u0041\u24B6\uFF21\u00C0\u00C1\u00C2\u1EA6\u1EA4\u1EAA\u1EA8\u00C3\u0100\u0102\u1EB0\u1EAE\u1EB4\u1EB2\u0226\u01E0\u00C4\u01DE\u1EA2\u00C5\u01FA\u01CD\u0200\u0202\u1EA0\u1EAC\u1EB6\u1E00\u0104\u023A\u2C6F'},
      {'base':'AA','letters':'\uA732'},
      {'base':'AE','letters':'\u00C6\u01FC\u01E2'},
      {'base':'AO','letters':'\uA734'},
      {'base':'AU','letters':'\uA736'},
      {'base':'AV','letters':'\uA738\uA73A'},
      {'base':'AY','letters':'\uA73C'},
      {'base':'B', 'letters':'\u0042\u24B7\uFF22\u1E02\u1E04\u1E06\u0243\u0182\u0181'},
      {'base':'C', 'letters':'\u0043\u24B8\uFF23\u0106\u0108\u010A\u010C\u00C7\u1E08\u0187\u023B\uA73E'},
      {'base':'D', 'letters':'\u0044\u24B9\uFF24\u1E0A\u010E\u1E0C\u1E10\u1E12\u1E0E\u0110\u018B\u018A\u0189\uA779'},
      {'base':'DZ','letters':'\u01F1\u01C4'},
      {'base':'Dz','letters':'\u01F2\u01C5'},
      {'base':'E', 'letters':'\u0045\u24BA\uFF25\u00C8\u00C9\u00CA\u1EC0\u1EBE\u1EC4\u1EC2\u1EBC\u0112\u1E14\u1E16\u0114\u0116\u00CB\u1EBA\u011A\u0204\u0206\u1EB8\u1EC6\u0228\u1E1C\u0118\u1E18\u1E1A\u0190\u018E'},
      {'base':'F', 'letters':'\u0046\u24BB\uFF26\u1E1E\u0191\uA77B'},
      {'base':'G', 'letters':'\u0047\u24BC\uFF27\u01F4\u011C\u1E20\u011E\u0120\u01E6\u0122\u01E4\u0193\uA7A0\uA77D\uA77E'},
      {'base':'H', 'letters':'\u0048\u24BD\uFF28\u0124\u1E22\u1E26\u021E\u1E24\u1E28\u1E2A\u0126\u2C67\u2C75\uA78D'},
      {'base':'I', 'letters':'\u0049\u24BE\uFF29\u00CC\u00CD\u00CE\u0128\u012A\u012C\u0130\u00CF\u1E2E\u1EC8\u01CF\u0208\u020A\u1ECA\u012E\u1E2C\u0197'},
      {'base':'J', 'letters':'\u004A\u24BF\uFF2A\u0134\u0248'},
      {'base':'K', 'letters':'\u004B\u24C0\uFF2B\u1E30\u01E8\u1E32\u0136\u1E34\u0198\u2C69\uA740\uA742\uA744\uA7A2'},
      {'base':'L', 'letters':'\u004C\u24C1\uFF2C\u013F\u0139\u013D\u1E36\u1E38\u013B\u1E3C\u1E3A\u0141\u023D\u2C62\u2C60\uA748\uA746\uA780'},
      {'base':'LJ','letters':'\u01C7'},
      {'base':'Lj','letters':'\u01C8'},
      {'base':'M', 'letters':'\u004D\u24C2\uFF2D\u1E3E\u1E40\u1E42\u2C6E\u019C'},
      {'base':'N', 'letters':'\u004E\u24C3\uFF2E\u01F8\u0143\u00D1\u1E44\u0147\u1E46\u0145\u1E4A\u1E48\u0220\u019D\uA790\uA7A4'},
      {'base':'NJ','letters':'\u01CA'},
      {'base':'Nj','letters':'\u01CB'},
      {'base':'O', 'letters':'\u004F\u24C4\uFF2F\u00D2\u00D3\u00D4\u1ED2\u1ED0\u1ED6\u1ED4\u00D5\u1E4C\u022C\u1E4E\u014C\u1E50\u1E52\u014E\u022E\u0230\u00D6\u022A\u1ECE\u0150\u01D1\u020C\u020E\u01A0\u1EDC\u1EDA\u1EE0\u1EDE\u1EE2\u1ECC\u1ED8\u01EA\u01EC\u00D8\u01FE\u0186\u019F\uA74A\uA74C'},
      {'base':'OI','letters':'\u01A2'},
      {'base':'OO','letters':'\uA74E'},
      {'base':'OU','letters':'\u0222'},
      {'base':'OE','letters':'\u008C\u0152'},
      {'base':'oe','letters':'\u009C\u0153'},
      {'base':'P', 'letters':'\u0050\u24C5\uFF30\u1E54\u1E56\u01A4\u2C63\uA750\uA752\uA754'},
      {'base':'Q', 'letters':'\u0051\u24C6\uFF31\uA756\uA758\u024A'},
      {'base':'R', 'letters':'\u0052\u24C7\uFF32\u0154\u1E58\u0158\u0210\u0212\u1E5A\u1E5C\u0156\u1E5E\u024C\u2C64\uA75A\uA7A6\uA782'},
      {'base':'S', 'letters':'\u0053\u24C8\uFF33\u1E9E\u015A\u1E64\u015C\u1E60\u0160\u1E66\u1E62\u1E68\u0218\u015E\u2C7E\uA7A8\uA784'},
      {'base':'T', 'letters':'\u0054\u24C9\uFF34\u1E6A\u0164\u1E6C\u021A\u0162\u1E70\u1E6E\u0166\u01AC\u01AE\u023E\uA786'},
      {'base':'TZ','letters':'\uA728'},
      {'base':'U', 'letters':'\u0055\u24CA\uFF35\u00D9\u00DA\u00DB\u0168\u1E78\u016A\u1E7A\u016C\u00DC\u01DB\u01D7\u01D5\u01D9\u1EE6\u016E\u0170\u01D3\u0214\u0216\u01AF\u1EEA\u1EE8\u1EEE\u1EEC\u1EF0\u1EE4\u1E72\u0172\u1E76\u1E74\u0244'},
      {'base':'V', 'letters':'\u0056\u24CB\uFF36\u1E7C\u1E7E\u01B2\uA75E\u0245'},
      {'base':'VY','letters':'\uA760'},
      {'base':'W', 'letters':'\u0057\u24CC\uFF37\u1E80\u1E82\u0174\u1E86\u1E84\u1E88\u2C72'},
      {'base':'X', 'letters':'\u0058\u24CD\uFF38\u1E8A\u1E8C'},
      {'base':'Y', 'letters':'\u0059\u24CE\uFF39\u1EF2\u00DD\u0176\u1EF8\u0232\u1E8E\u0178\u1EF6\u1EF4\u01B3\u024E\u1EFE'},
      {'base':'Z', 'letters':'\u005A\u24CF\uFF3A\u0179\u1E90\u017B\u017D\u1E92\u1E94\u01B5\u0224\u2C7F\u2C6B\uA762'},
      {'base':'a', 'letters':'\u0061\u24D0\uFF41\u1E9A\u00E0\u00E1\u00E2\u1EA7\u1EA5\u1EAB\u1EA9\u00E3\u0101\u0103\u1EB1\u1EAF\u1EB5\u1EB3\u0227\u01E1\u00E4\u01DF\u1EA3\u00E5\u01FB\u01CE\u0201\u0203\u1EA1\u1EAD\u1EB7\u1E01\u0105\u2C65\u0250'},
      {'base':'aa','letters':'\uA733'},
      {'base':'ae','letters':'\u00E6\u01FD\u01E3'},
      {'base':'ao','letters':'\uA735'},
      {'base':'au','letters':'\uA737'},
      {'base':'av','letters':'\uA739\uA73B'},
      {'base':'ay','letters':'\uA73D'},
      {'base':'b', 'letters':'\u0062\u24D1\uFF42\u1E03\u1E05\u1E07\u0180\u0183\u0253'},
      {'base':'c', 'letters':'\u0063\u24D2\uFF43\u0107\u0109\u010B\u010D\u00E7\u1E09\u0188\u023C\uA73F\u2184'},
      {'base':'d', 'letters':'\u0064\u24D3\uFF44\u1E0B\u010F\u1E0D\u1E11\u1E13\u1E0F\u0111\u018C\u0256\u0257\uA77A'},
      {'base':'dz','letters':'\u01F3\u01C6'},
      {'base':'e', 'letters':'\u0065\u24D4\uFF45\u00E8\u00E9\u00EA\u1EC1\u1EBF\u1EC5\u1EC3\u1EBD\u0113\u1E15\u1E17\u0115\u0117\u00EB\u1EBB\u011B\u0205\u0207\u1EB9\u1EC7\u0229\u1E1D\u0119\u1E19\u1E1B\u0247\u025B\u01DD'},
      {'base':'f', 'letters':'\u0066\u24D5\uFF46\u1E1F\u0192\uA77C'},
      {'base':'g', 'letters':'\u0067\u24D6\uFF47\u01F5\u011D\u1E21\u011F\u0121\u01E7\u0123\u01E5\u0260\uA7A1\u1D79\uA77F'},
      {'base':'h', 'letters':'\u0068\u24D7\uFF48\u0125\u1E23\u1E27\u021F\u1E25\u1E29\u1E2B\u1E96\u0127\u2C68\u2C76\u0265'},
      {'base':'hv','letters':'\u0195'},
      {'base':'i', 'letters':'\u0069\u24D8\uFF49\u00EC\u00ED\u00EE\u0129\u012B\u012D\u00EF\u1E2F\u1EC9\u01D0\u0209\u020B\u1ECB\u012F\u1E2D\u0268\u0131'},
      {'base':'j', 'letters':'\u006A\u24D9\uFF4A\u0135\u01F0\u0249'},
      {'base':'k', 'letters':'\u006B\u24DA\uFF4B\u1E31\u01E9\u1E33\u0137\u1E35\u0199\u2C6A\uA741\uA743\uA745\uA7A3'},
      {'base':'l', 'letters':'\u006C\u24DB\uFF4C\u0140\u013A\u013E\u1E37\u1E39\u013C\u1E3D\u1E3B\u017F\u0142\u019A\u026B\u2C61\uA749\uA781\uA747'},
      {'base':'lj','letters':'\u01C9'},
      {'base':'m', 'letters':'\u006D\u24DC\uFF4D\u1E3F\u1E41\u1E43\u0271\u026F'},
      {'base':'n', 'letters':'\u006E\u24DD\uFF4E\u01F9\u0144\u00F1\u1E45\u0148\u1E47\u0146\u1E4B\u1E49\u019E\u0272\u0149\uA791\uA7A5'},
      {'base':'nj','letters':'\u01CC'},
      {'base':'o', 'letters':'\u006F\u24DE\uFF4F\u00F2\u00F3\u00F4\u1ED3\u1ED1\u1ED7\u1ED5\u00F5\u1E4D\u022D\u1E4F\u014D\u1E51\u1E53\u014F\u022F\u0231\u00F6\u022B\u1ECF\u0151\u01D2\u020D\u020F\u01A1\u1EDD\u1EDB\u1EE1\u1EDF\u1EE3\u1ECD\u1ED9\u01EB\u01ED\u00F8\u01FF\u0254\uA74B\uA74D\u0275'},
      {'base':'oi','letters':'\u01A3'},
      {'base':'ou','letters':'\u0223'},
      {'base':'oo','letters':'\uA74F'},
      {'base':'p','letters':'\u0070\u24DF\uFF50\u1E55\u1E57\u01A5\u1D7D\uA751\uA753\uA755'},
      {'base':'q','letters':'\u0071\u24E0\uFF51\u024B\uA757\uA759'},
      {'base':'r','letters':'\u0072\u24E1\uFF52\u0155\u1E59\u0159\u0211\u0213\u1E5B\u1E5D\u0157\u1E5F\u024D\u027D\uA75B\uA7A7\uA783'},
      {'base':'s','letters':'\u0073\u24E2\uFF53\u00DF\u015B\u1E65\u015D\u1E61\u0161\u1E67\u1E63\u1E69\u0219\u015F\u023F\uA7A9\uA785\u1E9B'},
      {'base':'t','letters':'\u0074\u24E3\uFF54\u1E6B\u1E97\u0165\u1E6D\u021B\u0163\u1E71\u1E6F\u0167\u01AD\u0288\u2C66\uA787'},
      {'base':'tz','letters':'\uA729'},
      {'base':'u','letters': '\u0075\u24E4\uFF55\u00F9\u00FA\u00FB\u0169\u1E79\u016B\u1E7B\u016D\u00FC\u01DC\u01D8\u01D6\u01DA\u1EE7\u016F\u0171\u01D4\u0215\u0217\u01B0\u1EEB\u1EE9\u1EEF\u1EED\u1EF1\u1EE5\u1E73\u0173\u1E77\u1E75\u0289'},
      {'base':'v','letters':'\u0076\u24E5\uFF56\u1E7D\u1E7F\u028B\uA75F\u028C'},
      {'base':'vy','letters':'\uA761'},
      {'base':'w','letters':'\u0077\u24E6\uFF57\u1E81\u1E83\u0175\u1E87\u1E85\u1E98\u1E89\u2C73'},
      {'base':'x','letters':'\u0078\u24E7\uFF58\u1E8B\u1E8D'},
      {'base':'y','letters':'\u0079\u24E8\uFF59\u1EF3\u00FD\u0177\u1EF9\u0233\u1E8F\u00FF\u1EF7\u1E99\u1EF5\u01B4\u024F\u1EFF'},
      {'base':'z','letters':'\u007A\u24E9\uFF5A\u017A\u1E91\u017C\u017E\u1E93\u1E95\u01B6\u0225\u0240\u2C6C\uA763'}
    ];

    var diacriticsMap = {};
    for (var i=0; i < defaultDiacriticsRemovalap.length; i++){
      var letters = defaultDiacriticsRemovalap[i].letters.split("");
      for (var j=0; j < letters.length ; j++){
        diacriticsMap[letters[j]] = defaultDiacriticsRemovalap[i].base;
      }
    }

    var accentsMap = {};
    for (var i=0; i < defaultDiacriticsRemovalap.length; i++){
      accentsMap[defaultDiacriticsRemovalap[i].base] = '[' + defaultDiacriticsRemovalap[i].letters + ']';
    }

    helpers.removeDiacritics = function(str) {
      return str.replace(/[^\u0000-\u007E]/g, function(a){
        return diacriticsMap[a] || a;
      });
    }

    /**
     * Creates a RegExp that matches the words in the search string.
     * Case and accent insensitive.
     */
    helpers.make_pattern = function(search_string) {
      // escape meta characters
      search_string = search_string.replace(/([|()[{.+*?^$\\])/g,"\\$1");

      // Remove all diacritics to add all possibilities later
      search_string = helpers.removeDiacritics(search_string);

      // split into words
      var words = search_string.split(/\s+/);

      // sort by length
      var length_comp = function (a,b) {
        return b.length - a.length;
      };
      //words.sort(length_comp);

      // replace characters by their compositors
      var accent_replacer = function(chr) {
        return accentsMap[chr] || chr;
      }

      for (var i = 0; i < words.length; i++) {
        words[i] = words[i].replace(/\S/g, accent_replacer);
      }

      // join as alternatives
      //var regexp = words.join("|");
      var regexp = words.join("\\s+");

      return new RegExp(regexp,"ig");
    }

    helpers.heatmapOptions = {
      radius: 10,
      dissipating: true,
      gradient : [
        'rgba(0, 0, 225, 0)',
        'rgba(0, 0, 255, 1)',
        'rgba(255,255,0, 0.5)',
        'rgba(255,255,0, 1)',
        'rgba(255, 153, 0, 0.5)',
        'rgba(255, 153, 0, 1)',
        'rgba(255, 0, 0, 0.5)',
        'rgba(255, 0, 0, 1)'
      ]
    }

    helpers.dateinputOptions = {
      format: 'dd/mm/yyyy',
      weekStart: 1,
      todayHighlight: true,
      autoclose: true,
      language: "es"
    };

    return helpers;
  });