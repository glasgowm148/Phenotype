/* 
Grace Hu
12/9/15
labelCtrl.js 
Description: Implements body tags that were declared in the html file.
Contains listener that responds to request to launch Google Calendar
Create Event page.
*/

'use strict';

angular.module('app').controller('labelCtrl', function ($scope, labelStorage) {

    $scope.labelStorage = labelStorage;

    $scope.$watch('labelStorage.data', function() {
        $scope.labelList = $scope.labelStorage.data;
    });

    $scope.labelStorage.findAll(function(data){
        $scope.labelList = data;
        $scope.$apply();
    });

    $scope.add = function() {
        labelStorage.add($scope.newContent);
        $scope.newContent = '';
    }

    $scope.remove = function(label) {
        labelStorage.remove(label);
    }

    $scope.submit = function(data) {
        labelStorage.submit(data);
    }

    $scope.toggleCompleted = function() {
        labelStorage.sync();
    }

});



// Responds to user clicking "Create"
// Opens up the URL of a Create Event page in GCal 
// The Event Title field should already be partially filled with selected label names
chrome.runtime.onMessage.addListener(function(request) {
    console.log("inside chrome.runtime listener");
	//concatenates the selected labels onto end of URL
	chrome.tabs.create({
		url: 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + request.type + ': ',
		active: true
	}, function(tab) {
		// After the tab has been created, open a window to inject the tab
		chrome.tabs.create({
			tabId: tab.id,
			type: 'popup',
			focused: true   //brings this new tab to current tab
		});
	});
    
});
