var app = angular.module('aosd', [
  'aosd.controllers',
  'aosd.services',
  'aosd.directives',
  'aosd.filters',
  'ngRoute',
  'ngCookies',
  'ngScrollTo',
  'angular-loading-bar',
  'googlechart',
  'uiGmapgoogle-maps',
  'gridshore.c3js.chart',
  'highcharts-ng',
])
  .constant('settings', {
    'API_URL': 'http://lxbifi86.bifi.unizar.es:8003',
    'MAX_SUBSCRIPTIONS': 10,
    'MAX_TERMS': 10,
  })
  .config(function($interpolateProvider, $httpProvider, $routeProvider, uiGmapGoogleMapApiProvider,
    cfpLoadingBarProvider) {
/*    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');*/

    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    //disable IE ajax request caching
    $httpProvider.defaults.headers.common['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.common['Pragma'] = 'no-cache';

    $routeProvider
      .when("/main", {templateUrl: "/static/html/partials/main.html", controller: "mainController"})
      .when("/report", {templateUrl: "/static/html/partials/report.html", controller: "reportController"})
      .when("/evolution", {templateUrl: "/static/html/partials/evolution.html", controller: "evolutionController"})
      .when("/heatmap", {templateUrl: "/static/html/partials/heatmap.html", controller: "heatmapController"})
      .when("/stats", {templateUrl: "/static/html/partials/stats.html", controller: "statsController"})
      .when("/polarity", {templateUrl: "/static/html/partials/polarity.html", controller: "polarityController"})
      .when("/communities", {templateUrl: "/static/html/partials/communities.html", controller: "communitiesController"})
      .when("/subscribe", {templateUrl: "/static/html/partials/subscribe.html", controller: "subscribeController"})
      .when("/login", {templateUrl: "/static/html/partials/login.html", controller: "loginController"})
      .when("/register", {templateUrl: "/static/html/partials/register.html", controller: "registerController"})
      .when("/password_change", {templateUrl: "/static/html/partials/password_change.html", controller: "passwordChangeController"})
      .when("/password_reset", {templateUrl: "/static/html/partials/password_reset.html", controller: "passwordResetController"})
      .when("/password_reset_confirm", {templateUrl: "/static/html/partials/password_reset_confirm.html", controller: "passwordResetConfirmController"})
      .otherwise({redirectTo: '/main'});

    cfpLoadingBarProvider.includeSpinner = false;

    uiGmapGoogleMapApiProvider.configure({
      v: '3.17',
      libraries: 'visualization'
    });
  })
  .run(function($rootScope, $location, subscriptionsAPI) {
    var routesThatRequireAuth = ['/subscribe', '/password_change']

    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      // if route requires auth and user is not logged in
      var urlPath = $location.url().split('?')[0];
      if (routesThatRequireAuth.indexOf(urlPath) >= 0 && !subscriptionsAPI.is_logged()) {
        // redirect back to login
        $location.path('/login');
      }
    });
  });
