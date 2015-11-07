'use strict';

/* Directives */


angular.module('myApp.directives', []).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }])
  
  //.directive('watch_newSaltModule', ['$scope.newModuleAction', function(scope, controller) {
   // $scope.$watch('$scope.newModuleAction', function(newVal, oldVal) {
    //  console.log("WATCH 22: " + newVal + " " + oldVal);
   // })
  //}])
  
  
  ;
