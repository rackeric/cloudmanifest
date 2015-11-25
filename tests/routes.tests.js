describe('Routes test', function() {
    // Mock our module in our tests
    beforeEach(module('pivotApp'));

    // We want to store a copy of the three services we'll use in our tests
    // so we can later reference these services in our tests.
    var $httpBackend, $location, $route, $rootScope;

    // We added _ in our dependencies to avoid conflicting with our variables.
    // Angularjs will strip out the _ and inject the dependencies.
    beforeEach(inject(function(_$httpBackend_,_$location_, _$route_, _$rootScope_){
        $httpBackend = _$httpBackend_
        $location = _$location_;
        $route = _$route_;
        $rootScope = _$rootScope_;
    }));

    // Our test code is set up. We can now start writing the tests.

    // When a user navigates to the index page, they are shown the index page with the proper
    // controller
    it('should load the index page on successful load of /', function(){
        $httpBackend.expectGET('static/partials/home.html').respond(200, 'home HTML');
        expect($location.path()).toBe('');

        $location.path('/');

        // The router works with the digest lifecycle, wherein after the location is set,
        // it takes a single digest loop cycle to process the route,
        // transform the page content, and finish the routing.
        // In order to trigger the location request, we’ll run a digest cycle (on the $rootScope)
        // and check that the controller is as expected.
        $rootScope.$digest();

        expect($location.path()).toBe( '/' );
        expect($route.current.controller).toBe('HomeCtrl');
    });

    it('should redirect to the index path on non-existent route', function(){
        $httpBackend.expectGET('static/partials/index.html').respond(200, 'index HTML');
        expect($location.path()).toBe('');

        $location.path('/a/non-existent/route');

        $rootScope.$digest();

        expect($location.path()).toBe( '/' );
        expect($route.current.controller).toBe('HomeCtrl');
    });

});
