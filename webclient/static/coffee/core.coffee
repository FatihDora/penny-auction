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
GET_NONCE = "/get_nonce"
USER_USERNAME_EXISTS = "/user_username_exists"
USER_EMAIL_EXISTS = "/user_email_exists"

# Auctions
BID = "/bid"
GET_AUCTION_INFO = "/get_auction_info"

# Misc
AJAX_KEYPRESS_DELAY = 500 # In milliseconds, how long to wait after a keypress before initiating ajax request.

$(document).ready ->
	###
	Order of Operations
	 
	1) Initialize objects. Set Defaults. Hook-up events.
	2) Check for and validate cookie hash.
		2.a - Get user info (username,bids,level,etc.)
		2.b - Display user info bars and hide login/register (top & bottom)
	3) Load auctions
	###


	###
	(1) Initialize
	###

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
			showDialog "error", "Unexpected Error", error

	# Bid Button Clicked 
	$(".auction-bid-button").click ->
		auction_id = $(this).parent().attr("id")
		jQuery.ajax
			url: API + BID
			data:
				id: auction_id
			success: (data) ->
				alert data

	###
	(2) User Auth
	###

	# validate cookie 
	cookie = getCookie("pisoauction")
	if cookie? and cookie isnt ""
		$("#account-navigation").css "visibility", "visible"
		$("#account-navigation").css "display", "block"
		$("#bid-info").css "visibility", "visible"
		$("#bid-info").css "display", "block"
		$("#login-container").css "visibility", "hidden"
		$("#login-container").css "display", "none"
	else
		$.getScript "/js/register.js", ->
			# enable login / register buttons here

		$("#account-navigation").css "visibility", "hidden"
		$("#account-navigation").css "display", "none"
		$("#bid-info").css "visibility", "hidden"
		$("#bid-info").css "display", "none"
		$("#login-container").css "visibility", "visible"
		$("#login-container").css "display", "block"

	###
	2.a - Get user info
	###

	###
	2.b - Display user info
	###

	###
	(3) Load auctions
	###

	#  DO A REQUEST TO GET THE AUCTIONS... PRINT OUT THIS STUFF IN A LOOP:
	###
	<div id='{{auction.id}}' class='auction'>
		<div class='auction-title'><a href='{{auction.productUrl}}'>{{auction.name}}</a></div>
		<div class='auction-image'><img src='{{auction.imageUrl}}' alt='{{auction.name}}' /></div>
		<div class='auction-info'>
			<div class='auction-current-price'>₱{{auction.price}}</div>
			<div class='auction-time-remaining'>{{auction.auctionRemaining}}</div>
			<div class='auction-current-winner'>{{auction.currentWinner}}</div>
		</div>
		<div class='auction-bid-button'>Bid!</div>
		<div class='auction-footer'></div>
	</div>
	###

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
					$(this).animate
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

