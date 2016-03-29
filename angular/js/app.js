angular = require('angular');
require('angular-material');
require('angular-route');
require('../dist/templateCachePartials');

angular.module('events', ['ngRoute', 'ngMaterial'])
  .config(function ($routeProvider) {
    'use strict';

    var routeConfig = {
      controller: 'EventsCtrl',
      templateUrl: '/partials/events.html',
    };

    $routeProvider
      .when('/', routeConfig)
      .otherwise({
        redirectTo: '/'
      });
  });

require('eventsMain');
