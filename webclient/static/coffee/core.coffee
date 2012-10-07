# API
API = "http://localhost:8081"

# Autobidder
CREATE_AUTO_BIDDER = "/create_auto_bidder"
GET_AUTO_BIDDER_STATUS = "/get_auto_bidder_status"
CANCEL_AUTO_BIDDER = "/cancel_auto_bidder"
LIST_AUTO_BIDDERS_FOR_USER = "/list_auto_bidders_for_user"
LIST_AUTO_BIDDERS_FOR_AUCTION = "/list_auto_bidders_for_auction"

#Auctions
AUCTIONS_LIST_ACTIVE = "/auctions_list_active"
AUCTIONS_STATUS_BY_ID = "/auctions_status_by_id"
AUCTION_BID = "/auction_bid"

# User
USER_REGISTER = "/user_register"
USER_AUTHENTICATE = "/user_authenticate"
VALIDATE_EMAIL = "/user_validate_email"
USER_USERNAME_EXISTS = "/user_username_exists"
USER_EMAIL_EXISTS = "/user_email_exists"
USER_INFO = "/user_info"
USER_LOGOUT = "/user_logout"

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

	auctions.init()
	login.init()
	registration.init()
	validate_email.init()
	user.init()

	if $("#auctions").length isnt 0
		window.setInterval auctions.updateAuctions, 1000

	# END $(document).ready

user = 
	username: null
	bids: null
	autobidders: null
	init: ->
		user.update()

	update: ->
		callApi USER_INFO,{},(data) ->

			if data.result
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


				$('#topbar-bids').text user.bids
				$('#topbar-autobidders').text user.autobidders



auction_ids = []
auctions =
	init: ->
		callApi AUCTIONS_LIST_ACTIVE,(count: 30), (data) ->
			$("#auctions").html ""
			auctions = data.result
			for ix of auctions
				i = auctions[ix].i
				n = auctions[ix].n
				b = auctions[ix].b
				u = auctions[ix].u
				m = auctions[ix].m
				p = auctions[ix].p
				w = auctions[ix].w
				t = secondsToHms(auctions[ix].t)
				auction_ids.push i
				$("#auctions").append(buildAuction(i, n, b, u, m, p, w, t))

		# Bid Button Clicks
		$("ul#auctions").delegate "div.cart-button a", "click", ->
			auction_id = $(@).parent().parent().attr("id")
			callApi AUCTION_BID,(id: auction_id), (data) ->
				user.update()


		buildAuction = (id, productName, basePrice, productUrl, imageUrl, currentPrice, currentWinner, timeTilEnd) ->
			tmplAuction = undefined
			tmplAuction = ''
			tmplAuction += ' <li id="{auction-id}">\n'
			tmplAuction += '\t\t<!-- top block -->\n'
			tmplAuction += '\t\t<div class="top-block">\n'
			tmplAuction += '\t\t\t<h3 class="nocufon"><a href="{url}" title="{item-name}">{item-name}</a></h3>\n'
			tmplAuction += '\t\t\t\t<div class="imgb thumbnail-zoom">\n'
			tmplAuction += '\t\t\t\t\t<a href="{url}" class="fadeable">\n'
			tmplAuction += '\t\t\t\t\t\t<span class="light-background">\n'
			tmplAuction += '\t\t\t\t\t\t<span class="thumb-arrow">&#8594;</span>\n'
			tmplAuction += '\t\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t\t\t<span>\n'
			tmplAuction += '\t\t\t\t\t\t\t<img src="{image-url}" width="194" height="144" alt="{item-name}" />\n'
			tmplAuction += '\t\t\t\t\t\t\t<!--<span class="sale-img">NEW<span>ITEM</span></span>-->\n'
			tmplAuction += '\t\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t\t</a>\n'
			tmplAuction += '\t\t\t\t</div>\n'
			tmplAuction += '\t\t\t\t<span class="winner"><a href="#">{winner}</a></span>\n'
			tmplAuction += '\t\t\t\t<span class="price">P {current-price}</span>\n'
			tmplAuction += '\t\t\t\t<span class="timeleft">{time-remaining}</span>\n'
			tmplAuction += '\t\t\t</div>\n'
			tmplAuction += '\t\t<!-- top block -->\n'
			tmplAuction += '\t\t<div class="cart-button js-button"><a class="hov" href="javascript:void(0);"><span>BID NOW</span></a><a href="javascript:void(0);"><span>BID NOW</span></a></div>\n'
			tmplAuction += '\t</li>\n'
			tmplAuction = tmplAuction.replaceAll("{auction-id}", id)
			tmplAuction = tmplAuction.replaceAll("{url}", productUrl)
			tmplAuction = tmplAuction.replaceAll("{item-name}", productName)
			tmplAuction = tmplAuction.replaceAll("{image-url}", imageUrl)
			tmplAuction = tmplAuction.replaceAll("{current-price}", currentPrice)
			tmplAuction = tmplAuction.replaceAll("{winner}", currentWinner)
			tmplAuction = tmplAuction.replaceAll("{time-remaining}", timeTilEnd)
			return tmplAuction
	
	updateAuctions: ->
		jQuery.ajax
			url: API + AUCTIONS_STATUS_BY_ID
			data:
				ids: auction_ids.join()

			jsonp: "callback"
			success: (data) ->
				$.map data, (auction) ->
					auctions = data.result
					for ix of auctions
						i = auctions[ix].i
						p = auctions[ix].p
						w = auctions[ix].w
						t = secondsToHms(auctions[ix].t)
						a = auctions[ix].a
						# IF WE NEED TO BLINK...
						#if $("#" + i + " span.winner").text isnt w
						#	$("#" + i + " span.winner").css "backgroundColor", "#CC0000"
						#	$("#" + i + " span.winner").animate backgroundColor: "#FFFFFF"
						buttonText =""
						if t > 10
							buttonText = "Starting Soon..."
						else
							if user.username?
								buttonText = "BID NOW!"
							else
								buttonText = "REGISTER NOW!"

						$("#" + i + " span.winner").html "<a href=\"#\">" + w + "</a>"
						$("#" + i + " span.price").text "P " + p
						$("#" + i + " span.timeleft").html(t)

						if a is "False"
							if w is "No Bidder" then  buttonText = "SOLD" else buttonText = "ENDED"
							$("#" + i + " div.cart-button").html '<a href="javascript:void(0);"><span>' + buttonText + '</span></a>'


login = init: ->
	$("#top-account-info").hide()
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
					user.update()

				if data.exception?
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
				$("div#registration-form").slideUp 'slow', ->
					$("div#registration-complete strong").text(email)
					$("div#registration-complete").fadeIn 1000
				return

		false


validate_email =
	init: ->
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


# ************************ #
# FUNCTIONS								#
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

secondsToHms = (d) ->
	d = Number(d)
	h = Math.floor(d / 3600)
	m = Math.floor(d % 3600 / 60)
	s = Math.floor(d % 3600 % 60)
	padzero(h,2) + ":" + padzero(m,2) + ":" + padzero(s,2)

String::replaceAll = (str1, str2, ignore) ->
	@replace new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, "\\$&"), ((if ignore then "gi" else "g"))), (if (typeof (str2) is "string") then str2.replace(/\$/g, "$$$$") else str2)
