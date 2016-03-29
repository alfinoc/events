angular = require('angular');
util = require('util');

var ABBREVIATIONS = {
  'The Paramount Theatre': 'Paramount',
  'The Neptune Theatre': 'Neptune',
  'Northwest Film Forum': 'NWFF'
};

var EVENT_TYPES = ['film', 'music'];

var DAYS_PER_WEEK = 7;
var WEEKS_SCROLL_AHEAD = 20;

var allTrueMap = function(keys) {
  var result = {};
  keys.forEach(function(key) {
    result[key] = true;
  });
  return result;
}

var range = function(len) {
  var res = [];
  for (var i = 0; i < len; i++) {
    res.push(i);
  }
  return res;
};

function lastSunday(date) {
  return new Date(date.setDate(date.getDate() - date.getDay()));
}

function fullWeek(sunday) {
  return range(DAYS_PER_WEEK).map(function(offset) {
    var date = new Date(sunday);
    date.setDate(date.getDate() + offset);
    return date;
  });
};

function dayHash(date) {
  return date ? date.toISOString().substring(0, 10) : '';
}

angular.module('events')
  .controller('EventsCtrl', function EventsCtrl($scope, $http) {
    'use strict';

    var weekCache_ = {};
    var firstSunday = lastSunday(new Date());
    var maxLoaded = 0;
    var dates = {};

    $scope.TODAY = new Date();
    $scope.enabledTypes = allTrueMap(EVENT_TYPES);

    $scope.selectedEvent = null;

    $scope.select = function(day) {
      $scope.selectedDate = day;
    };

    $scope.selected = function(day) {
      return $scope.selectedDate == day;
    }

    // TODO(alfino): make this a map from date to list of events on that date.
    $scope.details = new Map();

    $http.get('/test.json').then(function(data) {
      var m = new Map();
      data.data.forEach(function(eventDetail) {
        eventDetail.dates.forEach(function(date) {
          var key = date.substring(0, 10);
          if (!m.get(key)) {
            m.set(key, []);
          }
          m.get(key).push(eventDetail);
        });
        $scope.details = new Map();
        m.forEach(function(v, k) {
          $scope.details.set(k, Array.from(new Set(v)));
        });
      });
    });

    $scope.eventsFor = function(date) {
      if (!date) {
        return undefined;
      }
      return $scope.details.get(dayHash(date));
    }

    $scope.weeks = {
      getItemAtIndex: function(i) {
        if (weekCache_[i]) { return weekCache_[i]; }

        maxLoaded = Math.max(maxLoaded, i);
        var sunday = new Date(firstSunday);
        sunday.setDate(sunday.getDate() + i * DAYS_PER_WEEK);
        var result = fullWeek(sunday);

        // Hack to initially selected 'today'.
        result.forEach(function(day) {
          // TODO(alfino): fix
          console.log($scope.TODAY.toDateString() == day.toDateString());
          if ($scope.TODAY.toDateString() == day.toDateString()) {
            $scope.selectedDate = day;
            console.log($scope.selectedDate);
          }
        });
        weekCache_[i] = result;
        return result;
      },

      getLength: function() {
        return WEEKS_SCROLL_AHEAD + maxLoaded;
      }
    };

    $scope.abbreviate = function(str) {
      return ABBREVIATIONS[str] || str;
    };

    $scope.numberWithType = function(events, type) {
      if (!events) {
        return 0;
      }
      return events.filter(function(evt) {
        return evt.type == type;
      }).length;
    };
  });