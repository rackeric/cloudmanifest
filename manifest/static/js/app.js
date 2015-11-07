'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp',
      ['myApp.config', 'myApp.routes', 'myApp.filters', 'myApp.services', 'myApp.directives', 'myApp.controllers',
         'waitForAuth', 'routeSecurity', 'xeditable', 'ui.bootstrap', 'ui', 'ui.sortable']
   )

   .run(function(editableOptions) {
      editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
   })

   .run(['loginService', '$rootScope', 'DestinyURL', 'FBURL', function(loginService, $rootScope, DestinyURL, FBURL) {
      if( FBURL === 'https://INSTANCE.firebaseio.com' ) {
         // double-check that the app has been configured
         angular.element(document.body).html('<h1>Please configure app/js/config.js before running!</h1>');
         setTimeout(function() {
            angular.element(document.body).removeClass('hide');
         }, 250);
      }
      else {
         // establish authentication
         $rootScope.auth = loginService.init('/login');
         $rootScope.FBURL = FBURL;
         $rootScope.DestinyURL = DestinyURL;
      }
   }]);
