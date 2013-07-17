// var createPlist = function(tabs) {
	console.log("made some tabs");

	tabs = [{
			"Title":"XKCD",
			"URL":"https://xckd.com/"
		},
		{
			"Title":"Goooogle",
			"URL":"http://google.com/"
		}
	]

	b = {
		"DeviceName":"chrome",
		"LastModified":JSON.parse(JSON.stringify(new Date())),
		"Tabs":tabs
	}

	var buffer = tab_plist_with_header([b]);
	var base64_tabs = btoa(String.fromCharCode.apply(null, buffer));

	console.log( base64_tabs );

	

// };
