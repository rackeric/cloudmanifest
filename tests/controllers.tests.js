describe('HomeCtrl', function(){

    // we'll use this scope in our tests
    var $httpBackend, $rootScope, createController;

    // mock Application to allow us to inject our own dependencies
    beforeEach(angular.mock.module('myApp'));

    beforeEach(inject(function($injector) {
        // Set up the mock http service responses
        $httpBackend = $injector.get('$httpBackend');

        // Get hold of a scope (i.e. the root scope)
        $rootScope = $injector.get('$rootScope');

        // The $controller service is used to create instances of controllers
        var $controller = $injector.get('$controller');

        createController = function() {
            return $controller('HomeCtrl', {'$scope' : $rootScope });
        };
    }));

    afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    // tests start here //

    // test initial setting of tools var
    it('should have tools from api', function(){
        var controller = createController();
        $httpBackend.flush();
        expect($rootScope.myName).toEqual("eric");
    });

});
