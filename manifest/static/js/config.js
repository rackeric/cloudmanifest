'use strict';

// Declare app level module which depends on filters, and services
angular.module('myApp.config', [])

   // version of this seed app is compatible with angularFire 0.6
   // see tags for other versions: https://github.com/firebase/angularFire-seed/tags
   .constant('version', '0.1')

   // where to redirect users if they need to authenticate (see module.routeSecurity)
   .constant('loginRedirectPath', '/login')

   // your Firebase URL goes here
   .constant('FBURL', 'https://deploynebula.firebaseio.com')
   
   // Destiny servers
   
   //.constant('DestinyURL', 'https://destiny.cloudmanifest.com')
   .constant('DestinyURL', '/api/v1')
   //.constant('DestinyURL', 'https://dev-destiny.cloudmanifest.com')
