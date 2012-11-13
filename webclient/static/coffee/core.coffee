######################
# NOTE: Coffee doesn't allow anything into the global namespace, so
#       anything you want to be global needs to be prefixed with {window.} 
######################

# API
window.API = "http://localhost:8080"

# Autobidder
window.AUTOBIDDER_CREATE = "/autobidder_create"
window.AUTOBIDDER_STATUS = "/autobidder_status"
window.AUTOBIDDER_CANCEL = "/autobidder_cancel"
window.AUTOBIDDERS_LIST = "/autobidders_list"

#Auctions
window.AUCTIONS_LIST_ACTIVE = "/auctions_list_active"
window.AUCTIONS_STATUS_BY_ID = "/auctions_status_by_id"
window.AUCTION_BID = "/auction_bid"
window.AUCTION_DETAIL = "/auction_detail"

# User
window.USER_REGISTER = "/user_register"
window.USER_AUTHENTICATE = "/user_authenticate"
window.VALIDATE_EMAIL = "/user_validate_email"
window.USER_USERNAME_EXISTS = "/user_username_exists"
window.USER_EMAIL_EXISTS = "/user_email_exists"
window.USER_INFO = "/user_info"
window.USER_LOGOUT = "/user_logout"

$(document).ready ->
	
	# Set up the jQuery AJAX stuff 
	$.ajaxSetup
		async: true
		dataType: "jsonp"
		jsonp: false
		cache: false # default for 'jsonp'
		type: "GET"
		beforeSend: (xhr, settings) ->
			# Before every AJAX request, do this
		complete: (xhr, status) ->
			# After every AJAX request, and after success/error handlers are
			# called
		error: (xhr, status, error) ->
			# Error handler
			if result.statusText isnt "abort"
				showDialog "error", "Unexpected Error", error

	$("#messageDialog").dialog
		autoOpen: false
		modal: true
		width: 300
		height: 200
		buttons:
			Ok: ->
				$(@).dialog "close"

	login.init()
	user.init()

	# END $(document).ready

window.user = 
	fetchingInfo: null
	username: null
	bids: null
	autobidders: null
	loggedIn: false
	init: ->
		user.refresh()

	refresh: ->
		if fetchingInfo then fetchingInfo.abort()
		fetchingInfo = callApi USER_INFO,{},(data) ->
			if data.result
				user.loggedIn = true
				user.username = data.result[0]['username']
				user.bids = data.result[0]['bids']
				user.autobidders = data.result[0]['auto-bidders']
				$('div#login-wrapper').fadeOut 'fast', ->
					newHtml = '<span class="heading">'
					newHtml += '<img src="/images/ico_man.png" width="15" height="15" alt="man" />'
					newHtml += 'Logged in as <a href="#"><strong>' + user.username + '</strong></a></span>'
					newHtml += '<span class="logout"><a href="javascript:void(0);">Logout</a></span>'
					$('span.logout a').live('click', (e) ->
						e.preventDefault()
						callApi USER_LOGOUT,{}, (data) ->
							document.location.href='/'
						)
					$(@).html newHtml
					$(@).fadeIn 'slow'
					$('#top-account-info').fadeIn 1000
					user.update()
					fetchingInfo = null

	update: ->
		$('#topbar-bids').text user.bids
		$('#topbar-autobidders').text user.autobidders



############################################
# Login
############################################

window.login = init: ->
	
	#------------#
	# Login Form #
	#------------#

	$("#login-form").submit (e) ->
		e.preventDefault()
		username = $("#login-username").val()
		password = $("#login-password").val()
		callApi USER_AUTHENTICATE,
			username: username
			password: password
		, (data) ->
				if data.result? then document.location.reload true
				if data.exception? then showDialog "error", "Login Error", data.exception

	$("#login-form").delegate "#login-username, #login-password", "focus", ->
		if $(@).val() is "username" or $(@).val() is "password"
			$(@).val ""
			$(@).addClass "login-focus"

	$("#login-form").delegate "#login-username, #login-password", "blur", ->
		if $(@).val() is ""
			$(@).val $(@).attr("id").split("-")[1]
			$(@).removeClass "login-focus"

# Functions

window.showDialog = (dialogType, title, message) ->
	# figure out which icon to use
	icon = "info"
	switch dialogType
		when "info"
			icon = "info"
		when "error"
			icon = "alert"
		else
			icon = "info"
	
	# update the message dialog
	$("#messageDialog p").html "<span class='ui-icon ui-icon-" + icon + "' style='float:left; margin:0 7px 20px 0;'></span>" + message
	$("#messageDialog").dialog title: title
	
	# show the message dialog
	$("#messageDialog").dialog "open"

window.padzero = (number, length) ->
	str = "" + number
	str = "0" + str	while str.length < length
	str
	
window.getCookie = (c_name) ->
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
		
window.callApi = (method, data, callback) ->
	jQuery.ajax
		url: API + method
		data: data
		jsonp: "callback"
		success: callback

# For getting parameters from the Query String
window.getParameterByName = (name) ->
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]")
	regexS = "[\\?&]" + name + "=([^&#]*)"
	regex = new RegExp(regexS)
	results = regex.exec(window.location.search)
	unless results?
		""
	else
		decodeURIComponent results[1].replace(/\+/g, " ")

window.secondsToHms = (d) ->
	d = Number(d)
	h = Math.floor(d / 3600)
	m = Math.floor(d % 3600 / 60)
	s = Math.floor(d % 3600 % 60)
	padzero(h,2) + ":" + padzero(m,2) + ":" + padzero(s,2)

String::replaceAll = (str1, str2, ignore) ->
	@replace new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, "\\$&"), ((if ignore then "gi" else "g"))), (if (typeof (str2) is "string") then str2.replace(/\$/g, "$$$$") else str2)

