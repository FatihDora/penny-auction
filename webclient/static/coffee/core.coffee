# API
API = "http://localhost:8081"

# Autobidder
CREATE_AUTO_BIDDER = "/create_auto_bidder"
GET_AUTO_BIDDER_STATUS = "/get_auto_bidder_status"
CANCEL_AUTO_BIDDER = "/cancel_auto_bidder"
LIST_AUTO_BIDDERS_FOR_USER = "/list_auto_bidders_for_user"
LIST_AUTO_BIDDERS_FOR_AUCTION = "/list_auto_bidders_for_auction"

# User Auth
USER_REGISTER = "/user_register"
USER_AUTHENTICATE = "/user_authenticate"
VALIDATE_EMAIL = "/user_validate_email"
USER_USERNAME_EXISTS = "/user_username_exists"
USER_EMAIL_EXISTS = "/user_email_exists"

# Auctions
BID = "/bid"
AUCTION_LIST_ACTIVE = "/auction_list_active"

# Misc
AJAX_KEYPRESS_DELAY = 500 # In milliseconds, how long to wait after a keypress before initiating ajax request.

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

	#auctions.init()
	login.init()
	registration.init()
	validate_email.init()

	# END $(document).ready

auctions = init: ->
	#Get Auctions

	# If the array arrAuctionIDs contains IDs, get auction data by id.
	# Otherwise get active auctions
	#if arrAuctionIDs?
	
	$.ajax
		url: API + AUCTION_LIST_ACTIVE
		success: (data) ->
			$.map data, (auction) ->
				$('#auction#{auction.id} span.winner').html '<a href="#">#{auction.winner}</a>'
				$('#auction#{auction.id} span.price').text auction.current-price
				$('#auction#{auction.id} span.timeleft').html auction.time-left
		error: (data) ->
			alert 'Well, no auctions yet.'
	


login = init: ->
	$("#login-username").val "username"
	$("#login-password").val "password"
	$("#login-form").submit (e) ->
		username = $("#login-username").val()
		password = $("#login-password").val()
		callApi USER_AUTHENTICATE,
			username: username
			password: password
		, (data) ->
	
				if data.result?
					# Hide the login form.
					# TODO: We need to check if the user is logged in and hide it before the page loads.
					# TODO: Determine how we will know when a user is logged in.  Cookie?
					$('div#login-wrapper').animate marginRight: -400, 1000

				if data.exception
						showDialog "error", "Login Error", data.exception

		false

	$("#login-form").delegate "#login-username, #login-password", "focus", ->
		if $(@).val() is "username" or $(@).val() is "password"
			$(@).val ""
			$(@).addClass "login-focus"

	$("#login-form").delegate "#login-username, #login-password", "blur", ->
		if $(@).val() is ""
			$(@).val $(@).attr("id").split("-")[1]
			$(@).removeClass "login-focus"


# Registration Stuff

registration = init: ->
	$("div#registration-complete").hide()
	$("#registration-form").submit (e) ->
		error = "<ul style='clear: both'>"
		first_name = $("#FirstName").val()
		last_name = $("#LastName").val()
		username = $("#Username").val()
		email = $("#Email").val()
		password = $("#Password").val()
		termsaccepted = $("#termsandconditions:checked").val()

		if first_name.length == 0 then error += "<li>A First Name is required.<li/>"
		if last_name.length == 0 then error += "<li>A Last Name is required.<li/>"
		if username.length == 0 then error += "<li>A username is required.<li/>"
		if email.length == 0 then error += "<li>An email address is required.<li/>"
		if password.length == 0 then error += "<li>A password is required.<li/>"
		if not termsaccepted then error += "<li>You must accept our terms and conditions to register an account.<li/>"

		error += "</ul>"

		if error != "<ul style='clear: both'></ul>"
			showDialog "error", "Registration Error", error
			return false


		callApi USER_REGISTER,
			first_name: first_name
			last_name: last_name
			username: username
			email: email
			password: password
		, (data) ->
			if data.exception
				showDialog "error", "Registration Error", data.exception
				return

			if data.result
				$("div#registration-form").hide();
				$("div#registration-complete").fadeIn 1000
				return

		false


validate_email = init: ->
	$("#validation-error").hide()
	$("#validation-success").hide()

	# Find a better way to determine if we're on /validate_email page.
	if $("div#validate-email")?
		code = getParameterByName 'code'
		callApi VALIDATE_EMAIL,
			code: code
		, (data) ->
			$("div#validate-email div#please-wait").hide()

			if data.exception
				$("#validation-error h2").text data.exception
				$("#validation-error").fadeIn 1000
				return

			if data.result
				$("#validation-success").fadeIn 1000
				return


# UNUSED STUFF
###
# Bid Button Clicked 
$(".auction-bid-button").click ->
	auction_id = $(@).parent().attr("id")
	$.ajax
		url: API + BID
		data:
			id: auction_id
		success: (data) ->
			alert data

# validate cookie 
cookie = getCookie("pisoauction")
if cookie? and cookie isnt ""
	return

# 1s Timer 
window.setInterval (->
	$(".auction-time-remaining").each (i) ->
		parts = @innerHTML.split(":")
		d = new Date()
		d.setHours parts[0]
		d.setMinutes parts[1]
		d.setSeconds parts[2]
		oldHours = d.getHours()
		d.setSeconds d.getSeconds() - 1
		if oldHours >= d.getHours()
			@innerHTML = padzero(d.getHours(), 2) + ":" + padzero(d.getMinutes(), 2) + ":" + padzero(d.getSeconds(), 2)
			if @innerHTML is "00:00:00"
				@style.backgroundColor = "#CC0000"
				$(@).animate
					backgroundColor: "#FFFFFF"
				, "slow"
		else
			@innerHTML = "00:00:00"

), 1000



# Count auctions down 
$(".auction-time-remaining").each (i) ->
	parts = @innerHTML.split(":")
	d = new Date()
	d.setHours parts[0]
	d.setMinutes parts[1]
	d.setSeconds parts[2]
	oldHours = d.getHours()
	@innerHTML = padzero(d.getHours(), 2) + ":" + padzero(d.getMinutes(), 2) + ":" + padzero(d.getSeconds(), 2)  if oldHours >= d.getHours()

###

# ************************ #
# FUNCTIONS                #
# ************************ #

typewatch = (->
	timer = 0
	(callback, ms) ->
		clearTimeout timer
		timer = setTimeout(callback, ms)
)()

showDialog = (dialogType, title, message) ->
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

# For getting parameters from the Query String
getParameterByName = (name) ->
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]")
	regexS = "[\\?&]" + name + "=([^&#]*)"
	regex = new RegExp(regexS)
	results = regex.exec(window.location.search)
	unless results?
		""
	else
		decodeURIComponent results[1].replace(/\+/g, " ")

