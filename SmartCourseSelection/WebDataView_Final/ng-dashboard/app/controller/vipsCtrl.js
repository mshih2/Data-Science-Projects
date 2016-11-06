'use strict';

var app = angular.module('app')
app.controller('tagClassChooseCtrl', function ($scope, $rootScope, $window) {
	
	chrome.tabs.executeScript(null, {file: "lib/TreeModel.js"});
	chrome.tabs.executeScript(null, {file: "app/contentScript/vips.js"});
//    var content = $window.localStorage.ClassData;
//    $window.localStorage.ClassData = "hello world"
//
//    console.log("tagClassChoose: \t"+window.localStorage.ClassData);
//	
//	var blob = new Blob([ content ], { type : 'text/plain' });
//	$scope.url = (window.URL || window.webkitURL).createObjectURL( blob );
//    /* The action of tagClassChoose will be fired here */
    $scope.vipsHighlightAll = function(){
        chrome.tabs.executeScript(null, {file: "app/contentScript/vipsHighlightAll.js"});
    };
    $scope.vipsClearAllHighlights = function(){
        chrome.tabs.executeScript(null, {file: "app/contentScript/vipsClearAllHighlights.js"});
    };
    $scope.vipsSuggest = function(){
        chrome.tabs.executeScript(null, {file: "lib/FileSaver.min.js"}, function() {
                chrome.tabs.executeScript(null, {file: "app/contentScript/vipsSuggest.js"});
        });
    };
    $scope.vipsExport = function(){
    	chrome.tabs.executeScript(null, {file: "lib/FileSaver.min.js"}, function() {
    		chrome.tabs.executeScript(null, {file: "app/contentScript/vipsExportAll.js"});
    	});
    };
    $scope.vipsHighlightSiblingBlocks = function(){
    	chrome.tabs.executeScript(null, {file: "lib/FileSaver.min.js"}, function() {
    		chrome.tabs.executeScript(null, {file: "app/contentScript/vipsHighlightSiblingBlocks.js"});
    	});
    };
    $scope.vipsExportCourseInfo = function(){
        chrome.tabs.executeScript(null, {file: "lib/FileSaver.min.js"}, function() {
                chrome.tabs.executeScript(null, {file: "app/contentScript/vipsExportCourseInfo.js"});
        });
    };
    $scope.vipsCourseExtraction = function(){
        chrome.tabs.executeScript(null, {file: "lib/clusterfck.js"}, function() {
            chrome.tabs.executeScript(null, {file: "app/contentScript/vipsClustering.js"});
        });
    };
    $scope.vipsSmartCourseKmean = function(){
        chrome.tabs.executeScript(null, {file: "lib/clusterfck.js"}, function() {
            chrome.tabs.executeScript(null, {file: "app/contentScript/vipsClustering-kmean.js"});
        });
    };
    $scope.vipsSmartCourseHierarchical = function(){
    	chrome.tabs.executeScript(null, {file: "/lib/node_modules/hierarchical-clustering/lib/index.js"}, function() {
    		chrome.tabs.executeScript(null, {file: "app/contentScript/vipsClustering-hierarchical.js"});
    	});
    };
    $scope.vipsExportText = function(){
        chrome.tabs.executeScript(null, {file: "lib/FileSaver.min.js"}, function() {
            chrome.tabs.executeScript(null, {file: "app/contentScript/vipsExportText.js"});
        });
    };
});

app.config(['$compileProvider',
    function ($compileProvider) {
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|file|blob):/);
}]);
