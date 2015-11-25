describe('HomeCtrl', function(){

    // we'll use this scope in our tests
    var $rootScope, createController;

    // mock Application to allow us to inject our own dependencies
    beforeEach(angular.mock.module('myApp'));

    beforeEach(inject(function($injector) {
        // Get hold of a scope (i.e. the root scope)
        $rootScope = $injector.get('$rootScope');

        // The $controller service is used to create instances of controllers
        var $controller = $injector.get('$controller');

        createController = function() {
            return $controller('HomeCtrl', {'$scope' : $rootScope });
        };
    }));

    afterEach(function() {

    });

    // tests start here //

    // test initial setting of tools var
    it('should have myName be manifest', function(){
        var controller = createController();
        expect($rootScope.myName).toEqual("manifest");
    });

});
