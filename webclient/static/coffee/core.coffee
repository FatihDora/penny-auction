######################
# NOTE: Coffee doesn't allow anything into the global namespace, so
#		anything you want to be global needs to be prefixed with {window.}
######################

# Autobidder
window.AUTOBIDDERS_LIST_ALL = "/autobidders_list_all"
window.AUTOBIDDERS_LIST_BY_AUCTION = "/autobidders_list_by_auction"
window.AUTOBIDDER_STATUS_BY_AUCTION = "/autobidder_status_by_auction"

#Auctions
window.AUCTIONS_LIST_CURRENT = "/auctions_list_current"
window.AUCTIONS_STATUS_BY_ID = "/auctions_status_by_id"
window.AUCTION_BID = "/auction_bid"
window.AUCTION_DETAIL = "/auction_detail"
window.AUCTION_RECENT_BIDS = "/auction_recent_bids"
window.AUCTION_ADD_PENDING_BIDS = "/auction_add_pending_bids"
window.AUCTION_GET_PENDING_BIDS_FOR_USER = "/auction_get_pending_bids_for_user"
window.AUCTION_CANCEL_PENDING_BIDS_FOR_USER = "/auction_cancel_pending_bids_for_user"
window.AUCTION_ADD_PENDING_BIDS_FOR_USER = "/auction_add_pending_bids_for_user"
window.AUCTION_REMOVE_PENDING_BIDS_FOR_USER = "/auction_remove_pending_bids_for_user"

# User
window.USER_REGISTER = "/user_register"
window.USER_AUTHENTICATE = "/user_authenticate"
window.VALIDATE_EMAIL = "/user_validate_email"
window.USER_USERNAME_EXISTS = "/user_username_exists"
window.USER_EMAIL_EXISTS = "/user_email_exists"
window.USER_INFO = "/user_info"
window.USER_LOGOUT = "/user_logout"

############################################
# A function for setting cookies.
############################################
window.set_cookie = (name, value, expiration_days) ->
	expiration_days ?= 7300 # default to twenty years

	now = new Date
	expiration_date = new Date now.getTime + (expiration_days * 86400000)

	cookie_text = "#{escape value}; expires=#{expiration_date.toUTCString}"
	document.cookie = "#{name}=#{cookie_text}"


$(document).ready ->

	# Set up the jQuery AJAX stuff
	$.ajaxSetup
		async: true
		cache: false # default for 'jsonp'
		type: "GET"
		beforeSend: (xhr, settings) ->
			# Before every AJAX request, do this
		complete: (xhr, status) ->
			# After every AJAX request, and after success/error handlers are
			# called
		error: (xhr, status, error) ->
			# Error handler
			if xhr.statusText isnt "abort"
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
		fetchingInfo = jQuery.ajax
			url: USER_INFO
			data: {}
			success: (data) ->
				if data.result
					user.loggedIn = true
					user.username = data.result[0]['username']
					user.bids = data.result[0]['bids']
					user.autobidders = data.result[0]['auto-bidders']
					login.showLoggedIn user.username
					user.update()
				fetchingInfo = null

	update: ->
		$('#topbar-bids').text user.bids
		$('#topbar-autobidders').text user.autobidders



############################################
# Login
############################################

window.login =
	init: ->
		$("#login-form").submit (e) ->
			e.preventDefault()
			username = $("#login-username").val()
			password = $("#login-password").val()
			jQuery.ajax
				url: USER_AUTHENTICATE
				data: {
					username: username
					password: password
				}
				success: (data) ->
					if data.result? then user.refresh()
					if data.exception? then showDialog "error", "Login Error", data.exception

		$('#logout-link').click (e) ->
			e.preventDefault()
			jQuery.ajax
				url: USER_LOGOUT
				data: {}
				success: (data) ->
					login.showLoggedOut()

		$("#login-form").delegate "#login-username, #login-password", "focus", ->
			if $(@).val() is "username" or $(@).val() is "password"
				$(@).val ""
				$(@).addClass "login-focus"

		$("#login-form").delegate "#login-username, #login-password", "blur", ->
			if $(@).val() is ""
				$(@).val $(@).attr("id").split("-")[1]
				$(@).removeClass "login-focus"

	showLoggedIn: (username) ->
		$('div#login-wrapper').fadeOut 'fast', ->
			$('.username-label').html user.username
			$('#logout-wrapper').fadeIn 'slow', ->
				$('#top-account-info').fadeIn 'slow'
	showLoggedOut: ->
		$('#logout-wrapper').fadeOut 'fast', ->
			$('.username-label').html ""
			$('#login-wrapper').fadeIn 'slow', ->
				$('#top-account-info').fadeOut 'slow'

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

