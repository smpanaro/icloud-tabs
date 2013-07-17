var uploadIntervalMinutes = 5;

var re = /^https?:\/\/.*/;
function isHttpUrl(url) {
  return re.exec(url);
}

function addTab(tab) {
    if (isHttpUrl(tab.url) && tab.status === "complete") tabs.push(tab);
}

function uploadTabs() {
    console.log("UPLOADING", new Date());

    tabs = []
    chrome.windows.getAll({populate:true}, function (windows) {
        for(var i = 0; i < windows.length; i++) {
            var tabs_array = windows[i].tabs;
            for(var j = 0; j < tabs_array.length; j++) {
                addTab(tabs_array[j]);
            }
        }
        createPlist(tabs);

        console.log("tabs: ", tabs);
        setTimeout(uploadTabs, uploadIntervalMinutes * 60 * 1000);
    });
}


function start() {
    setTimeout(uploadTabs, 2000);
}

start();

// 
