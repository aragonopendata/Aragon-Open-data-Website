angular.module('aosd.directives', [])

  /* Sigma JS directive */
  .directive('sigmajs', function(sigmaSingleton) {
    //over-engineered random id, so that multiple instances can be put on a single page
    var divId = 'sigmjs-dir-container-'+Math.floor((Math.random() * 999999999999))+'-'+Math.floor((Math.random() * 999999999999))+'-'+Math.floor((Math.random() * 999999999999));
    return {
      restrict: 'E',
      template: '<div id="'+divId+'" style="width: 100%;height: 100%;"></div>',
      scope: {
        graph: '=',
        width: '@',
        height: '@',
      },
      link: function (scope, element, attrs) {
        var zoomMax = 1;
        var zoomMin = 1/32;

        var s = new sigma({
          renderer: {
            container: document.getElementById(divId),
            type: 'canvas'
          },
          settings: {
            batchEdgesDrawing: true,
            hideEdgesOnMove: true,
            defaultNodeColor: "#ec5148",
            labelThreshold: 6.0,
            labelSize: "proportional",
            zoomMax: zoomMax,
            zoomMin: zoomMin,
            maxNodeSize: 12.0,
            minEdgeSize: 0.2,
            maxEdgeSize: 3,
            sideMargin: 100
          }
        });

        sigmaSingleton.instance = s;

        scope.$watch('graph', function(newVal,oldVal) {
          s.graph.clear();
          s.graph.read(scope.graph);
          s.refresh();
          if (s.graph.nodes.length < 5) {
            s.camera.goTo({x: s.camera.x, y: s.camera.y, ratio: zoomMax});
          }
        });

        scope.$watch('width', function(newVal,oldVal) {
          element.children().css("width",scope.width);
          s.refresh();
          window.dispatchEvent(new Event('resize')); //hack so that it will be shown instantly
        });

        scope.$watch('height', function(newVal,oldVal) {
          element.children().css("height",scope.height);
          s.refresh();
          window.dispatchEvent(new Event('resize'));//hack so that it will be shown instantly
        });

        element.on('$destroy', function() {
          s.graph.clear();
        });
      }
    };
  })

  /* Logo */
  .directive('logo', function() {
    return {
      restrict: 'E',
      templateUrl: '/public/socialdata/html/partials/logo.html',
    }
  })

  /* Side nav menu directive */
  .directive('sidenav', function() {
    return {
      restrict: 'E',
      templateUrl: '/public/socialdata/html/partials/sidenav.html',
      controller: 'sidenavController',
    }
  })

  /* Selection help text */
  .directive('selectionhelp', function() {
    return {
      restrict: 'E',
      templateUrl: '/public/socialdata/html/partials/selectionHelp.html',
      controller: 'selectionHelpController',
    }
  });