var uploadIntervalMinutes = 5;
var localUrl = "http://localhost:8080/icloud_tabs/"

function uploadToServer(url, body) {

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);

    xhr.onreadystatechange = function(event) {
        if (xhr.readyState == 4) {
            if (xhr.status !== 200) {
                console.log("Failed to load chrome tabs. Is the server running at" + localUrl + " ?");
            }
        }
    };
    xhr.send(body);
}

var re = /^https?:\/\/.*/;
function isHttpUrl(url) {
  return re.exec(url);
}

function addTab(tab) {
    if (isHttpUrl(tab.url) && tab.status === "complete") tabs.push({"Title":tab.title, "URL":tab.url});
}

function uploadTabs() {

    tabs = []
    chrome.windows.getAll({populate:true}, function (windows) {
        for(var i = 0; i < windows.length; i++) {
            var tabs_array = windows[i].tabs;
            for(var j = 0; j < tabs_array.length; j++) {
                addTab(tabs_array[j]);
            }
        }

        uploadToServer(localUrl, JSON.stringify(tabs));

        setTimeout(uploadTabs, uploadIntervalMinutes * 60 * 1000);
    });
}

function start() {
    setTimeout(uploadTabs, 2000);
}

start();
