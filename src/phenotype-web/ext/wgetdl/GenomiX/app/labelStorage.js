/* 
Grace Hu
12/9/15
labelStorage.js 
Description: This file handles all user actions in the extension--adding,
deleting, and selecting labels to create a Google Calendar event with.
Chrome.storage is essential in saving these custom tags beyond one session.
*/

var allTags = [];
var ext_id = "maemgfannganhmelfonecdbggfkfmahl" //gcal-to-gsheets extension

angular.module('app').service('labelStorage', function ($q) {
    var _this = this;
    this.data = [];
	
	//finds all labels user has enetered
    this.findAll = function(callback) {
        chrome.storage.sync.get('label', function(keys) {
            if (keys.label != null) {
                _this.data = keys.label;
                allTags = []; //refresh allTags
                for (var i=0; i<_this.data.length; i++) {
                    _this.data[i]['id'] = i + 1;
					allTags[i] = _this.data[i].content.toUpperCase();  //all labels get sent to receiving extension
                }
                console.log("allTags in findAll is: " + allTags);
                callback(_this.data);
            }
        });
    }
	
	//whenever function sync is called, also send updated labels to gcal-to-sheets extension
	//implemented with cross-extension messaging
    this.sync = function() {
        chrome.storage.sync.set({label: this.data}, function() {
            console.log('Data is stored in Chrome storage');
            allTags = []; //refresh allTags
            for (var i=0; i<_this.data.length; i++) {    //refill it up with updated storage data
                allTags[i] = _this.data[i].content.toUpperCase();  //all labels get sent to receiving extension
            }
            console.log("allTags is: " + allTags);
            
            chrome.runtime.sendMessage(ext_id, {myCustomMessage: allTags}, function(response) { 
       			 //appendLog("response: "+JSON.stringify(response));
     		 })
        });
    }
	
	//add a new label to the list
    this.add = function (newContent) {
        var id = this.data.length + 1;
        var label = {
            id: id,
            content: newContent,
            completed: false,
            createdAt: new Date()
        };
        this.data.push(label);
        this.sync();
    }
	
	//remove the label from the list
    this.remove = function(label) {
        this.data.splice(this.data.indexOf(label), 1);
        this.sync();        
    }
	
	//send message to listener to launch GCal's Create Event page
	//passes all selected labels to the listener
	this.submit = function(callback){
		this.sync();
		chrome.storage.sync.get('label', function(keys) {
            var combinedTags = ""; 
            
            if (keys.label != null) {
                _this.data = keys.label;
                
                
                //concatenate all checked labels into the combinedTags string
                for (var i=0; i<_this.data.length; i++) {
                    _this.data[i]['id'] = i + 1;
                    
                    if(_this.data[i].completed == true){
                    	console.log("completed" + _this.data[i].content);
                    	combinedTags = combinedTags.concat(" " + _this.data[i].content.toUpperCase());
                    }
                }                
                console.log(combinedTags);
				
				//open up the GCal page
				if(combinedTags != ""){
					chrome.runtime.sendMessage({type:combinedTags});
					console.log("after chrome sent message");
				}
            }
        });		
	}
});


//sends all tags to gcal-extension when user presses the "Create" button
//implemented with cross-extension messaging
(function(context){
  var send = document.getElementById("btn-submit");
  send.addEventListener('click', function() {
    chrome.runtime.sendMessage(ext_id, {myCustomMessage: allTags}, function(response) { 
        //appendLog("response: "+JSON.stringify(response));
      })
  });
  
  /* for displaying message sent - testing only
  var appendLog = function(message) {
    logField.innerText+="\n"+message;
  }
  context.appendLog = appendLog;
 */
})(window)

