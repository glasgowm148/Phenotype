// This callback function is called when the content script has been 
// injected and returned its results
function onPageDetailsReceived(pageDetails)  { 
    document.getElementById('title').value = pageDetails.title; 
    document.getElementById('url').value = pageDetails.url; 
    document.getElementById('summary').innerText = pageDetails.summary; 
}

// Global reference to the status display SPAN
var statusDisplay = null;

// POST the data to the server using XMLHttpRequest
function addBookmark() {

    // Cancel the form submit
    event.preventDefault();

    // The URL to POST our data to
    var postUrl = 'http://cs.wellesley.edu/~hcilab/pghci_pgp/popup.php';

    // Set up an asynchronous AJAX POST request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', postUrl, true);

    // Prepare the data to be POSTed by URLEncoding each field's contents
    var title = encodeURIComponent(document.getElementById('title').value);
    var url = encodeURIComponent(document.getElementById('url').value);
    var summary = encodeURIComponent(document.getElementById('summary').value);
    var c = document.getElementById('categories');
    var categories = encodeURIComponent(c.options[c.selectedIndex].value);
    var t = document.getElementById('tags');
    var tags = encodeURIComponent(t.options[t.selectedIndex].value);
    var ty = document.getElementById('type');
    var type = encodeURIComponent(ty.options[ty.selectedIndex].value);

    var params = 'title=' + title + 
                 '&url=' + url + 
                 '&summary=' + summary +
                 '&categories=' + categories +
                 '&tags=' + tags +
                 '&type=' + type;

    // Replace any instances of the URLEncoded space char with +
    params = params.replace(/%20/g, '+');

    //edit in function
    Object.prototype.in = function() {
        for(var i=0; i<arguments.length; i++)
           if(arguments[i] == this) return true;
        return false;
    }

    var extension = url.substr(url.length - 4);

    if (extension.in('.jpg','jpeg','.gif','.png')) {
        ty.selectedIndex = "IMG";
    } else if (extension === ".pdf") {
        ty.selectedIndex = "pdf";
    } else {
        ty.selectedIndex = "web";
    }

    // Set correct header for form data 
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    // Handle request state change events
    xhr.onreadystatechange = function() { 
        // If the request completed
        if (xhr.readyState == 4) {
            statusDisplay.innerHTML = '';
            if (xhr.status == 200) {
                // If it was a success, close the popup after a short delay
                statusDisplay.innerHTML = 'Saved!';
                window.setTimeout(window.close, 1000);
            } else {
                // Show what went wrong
                statusDisplay.innerHTML = 'Error saving: ' + xhr.statusText;
            }
        }
    };

    // Send the request and set status
    xhr.send(params);
    statusDisplay.innerHTML = 'Saving...';
}

// When the popup HTML has loaded
window.addEventListener('load', function(evt) {
    // Cache a reference to the status display SPAN
    statusDisplay = document.getElementById('status-display');

    // The URL to GET our data from
    var getUrl = 'http://cs.wellesley.edu/~hcilab/pghci_pgp/boards.php';
    
    // Set up an asynchronous AJAX GET request
    var xhr_get = new XMLHttpRequest();
    xhr_get.open('GET', getUrl, true);
    xhr_get.send();
    xhr_get.onload = function (e) {
        var pages = xhr_get.responseText;
        document.getElementById('pages').innerHTML = pages;
    }
    // Handle the bookmark form submit event with our addBookmark function
    document.getElementById('addbookmark').addEventListener('submit', addBookmark);
    // Get the event page
    chrome.runtime.getBackgroundPage(function(eventPage) {
        // Call the getPageInfo function in the event page, passing in 
        // our onPageDetailsReceived function as the callback. This injects 
        // content.js into the current tab's HTML
        eventPage.getPageDetails(onPageDetailsReceived);
    });
});