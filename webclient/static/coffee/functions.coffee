padzero = (number, length) ->
	str = "" + number
	str = "0" + str	while str.length < length
	str
	
getCookie = (c_name) ->
	i = undefined
	x = undefined
	y = undefined
	ARRcookies = document.cookie.split(";")
	i = 0
	while i < ARRcookies.length
		x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="))
		y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1)
		x = x.replace(/^\s+|\s+$/g, "")
		return unescape(y)	if x is c_name
		i++
		
callApi = (method, data, callback) ->
	jQuery.ajax
		url: API + method
		data: data
		jsonp: "callback"
		success: callback
