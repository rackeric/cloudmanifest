(function() {
   'use strict';

   /* Services */

   angular.module('myApp.services', ['myApp.service.login', 'myApp.service.firebase'])

      // put your services here!
      // .service('serviceName', ['dependency', function(dependency) {}]);

      .service('serviceUserlist', ["$firebase", function($firebase) {
          var ref = new Firebase("https://deploynebula.firebaseio.com/users");
          return $firebase(ref);
      }])

      .service('serviceFeedbacklist', ["$firebase", function($firebase) {
          var ref = new Firebase("https://deploynebula.firebaseio.com/feedbacklist");
          return $firebase(ref);
      }])

      .service('serviceAnsibleModuleslist', ["$firebase", function($firebase) {
          var ref = new Firebase("https://deploynebula.firebaseio.com/moduleslist/ansible");
          return $firebase(ref);
      }])

      .service('serviceAnsibleRepo', ["$firebase", function($firebase) {
          var ref = new Firebase("https://deploynebula.firebaseio.com/public_repos/ansible");
          return $firebase(ref);
      }])

      .service('serviceAnsibleRepoItem', ["$firebase", function($firebase) {
          return function(roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/public_repos/ansible/" + roleID);
              return $firebase(ref);
          }
      }])

      .service('serviceProjects', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects");
          return $firebase(ref);
      }])

      .service('serviceProject', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID);
              return $firebase(ref);
          }
      }])

      .service('serviceProjectName', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + '/name');
              return $firebase(ref);
          }
      }])

      .service('serviceRolesGit', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/rolesgit");
              return $firebase(ref);
          }
      }])

      .service('serviceRoleGit', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/rolesgit/" + roleID);
              return $firebase(ref);
          }
      }])

      .service('serviceRoles', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles");
              return $firebase(ref);
          }
      }])

      .service('serviceRole', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID);
              return $firebase(ref);
          }
      }])

      .service('serviceRoleManual', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/rolesmanual/" + roleID);
              return $firebase(ref);
          }
      }])

      .service('serviceRolesManual', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/rolesmanual/");
              return $firebase(ref);
          }
      }])

      .service('serviceRoleModules', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID + "/modules/");
              return $firebase(ref);
          }
      }])

      .service('serviceRoleVariable', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID, varID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID + "/variables/" + varID);
              return $firebase(ref);
          }
      }])

      .service('serviceRoleVariables', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID + "/variables/");
              return $firebase(ref);
          }
      }])

      .service('serviceRoleHandlers', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID + "/handlers/");
              return $firebase(ref);
          }
      }])

      .service('serviceRoleIncludes', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, roleID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/roles/" + roleID + "/includes/");
              return $firebase(ref);
          }
      }])

      .service('serviceInventoryHost', ["$rootScope", "$firebase", function($rootScope, $firebase) {
          return function(projectID, hostID) {
              var ref = new Firebase("https://deploynebula.firebaseio.com/users/" + $rootScope.auth.user.uid + "/projects/"  + projectID + "/inventory/" + hostID);
              return $firebase(ref);
          }
      }])

})();
