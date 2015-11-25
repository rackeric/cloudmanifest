// Karma configuration
// Generated on Tue Oct 20 2015 10:52:18 GMT-0500 (CDT)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      '../tests/jquery-1.9.1.js',
      '../tests/jquery-ui.js',
      '../tests/angular.js',
      '../tests/angular-route.js',
      '../tests/angular-mocks.js',
      '../tests/angular-ui.min.js',
      '../tests/firebase.js',
      '../tests/firebase-simple-login.js',
      '../tests/angularfire.js',
      '../manifest/static/js/*.js',
      //'../tests/routes.tests.js'
      '../tests/controllers.tests.js'
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
      '*.html': ['ng-html2js'],
      '*.js': ['coverage']
    },

    ngHtml2JsPreprocessor: {
      // strip this from the file path
      stripPrefix: 'src/',
      // create a single module that contains templates from all the files
      moduleName: 'templates'
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['spec', 'progress', 'coverage', 'dots', 'junit'],

    coverageReporter: {
      type : 'html',
      // output coverage reports
      dir : 'coverage/'
    },

    junitReporter: {
      outputFile: 'test-results.xml'
    },


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['PhantomJS'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true
  })
}
