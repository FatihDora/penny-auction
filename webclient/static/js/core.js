// API
var API = 'http://localhost:8081';

// Autobidder
var CREATE_AUTO_BIDDER = '/create_auto_bidder';
var GET_AUTO_BIDDER_STATUS = '/get_auto_bidder_status';
var CANCEL_AUTO_BIDDER = '/cancel_auto_bidder';
var LIST_AUTO_BIDDERS_FOR_USER = '/list_auto_bidders_for_user';
var LIST_AUTO_BIDDERS_FOR_AUCTION = '/list_auto_bidders_for_auction';

// User Auth
var USER_REGISTER = '/user_register';
var USER_AUTHENTICATE = '/user_authenticate';
var GET_NONCE = '/get_nonce';
var USER_USERNAME_EXISTS = '/user_username_exists';
var USER_EMAIL_EXISTS = '/user_email_exists';

// Auctions
var BID = '/bid';
var GET_AUCTION_INFO = '/get_auction_info';

// Misc
var AJAX_KEYPRESS_DELAY = 500; // In milliseconds, how long to wait after a keypress before initiating ajax request.


$(document).ready(function() {
	
	/* 
	 * Order of Operations
	 *
	 * 1) Initialize objects. Set Defaults. Hook-up events.
	 * 2) Check for and validate cookie hash.
	 *    2.a - Get user info (username,bids,level,etc.)
	 *    2.b - Display user info bars and hide login/register (top & bottom)
	 * 3) Load auctions
	 *
	 */
	
	/***********************************
	 *  (1) Initialize                 *
	 ***********************************/
	
	/* Set up the jQuery AJAX stuff */
	$.ajaxSetup({
		async: true,
		dataType: "jsonp",
		jsonp: false,
		cache: false, /* default for 'jsonp' */
		type: "GET",
		beforeSend: function(xhr, settings) {
			// Before every AJAX request, do this
		},
		complete: function(xhr, status) {
			// After every AJAX request, and after success/error handlers are
			// called
		},
		error: function(xhr, status, error) {
			// Error handler
			showDialog("error", "Unexpected Error", error);
		}
	});

	/* Bid Button Clicked */
	$(".auction-bid-button").click(function() {
		var auction_id = $(this).parent().attr("id");
		jQuery.ajax({
			url: API + BID,
			data: {id : auction_id},
			success: function(data) {
				alert(data);
			}
		});
	});

	/***********************************
	 *  (2) User Auth                  *
	 ***********************************/
	
	/* validate cookie */
	var cookie = getCookie("pisoauction");
	if (cookie!=null && cookie!="")
  	{
		$('#account-navigation').css('visibility','visible');
		$('#account-navigation').css('display','block');
		$('#bid-info').css('visibility','visible');
		$('#bid-info').css('display','block');
		$('#login-container').css('visibility','hidden');
		$('#login-container').css('display','none');
		
	}
	else
	{	
		$.getScript("/js/register.js", function() {
			// enable login / register buttons here
		});	
		
		$('#account-navigation').css('visibility','hidden');
		$('#account-navigation').css('display','none');
		$('#bid-info').css('visibility','hidden');
		$('#bid-info').css('display','none');
		$('#login-container').css('visibility','visible');
		$('#login-container').css('display','block');
	}

	/*** 2.a - Get user info ***********/
	
	/*** 2.b - Display user info *******/
	

    /***********************************
	 *  (3) Load auctions              *
	 ***********************************/

	/* 1s Timer */
	window.setInterval(function() {
		$(".auction-time-remaining").each(function(i) {
			var parts = this.innerHTML.split(":");
			var d = new Date();
			d.setHours(parts[0]);
			d.setMinutes(parts[1]);
			d.setSeconds(parts[2]);
			var oldHours = d.getHours();
			d.setSeconds(d.getSeconds() - 1);
			if (oldHours >= d.getHours()) {
				this.innerHTML = padzero(d.getHours(),2) + ":" + padzero(d.getMinutes(),2) + ":" + padzero(d.getSeconds(),2);
				if (this.innerHTML == "00:00:00") { this.style.backgroundColor="#CC0000"; $(this).animate({backgroundColor: '#FFFFFF'}, 'slow');}
			}
			else
			{
				this.innerHTML = "00:00:00";
			}
		})
	},1000);
	
	/* Count auctions down */
	$(".auction-time-remaining").each(function(i) {
		var parts = this.innerHTML.split(":");
		var d = new Date();
		d.setHours(parts[0]);
		d.setMinutes(parts[1]);
		d.setSeconds(parts[2]);
		var oldHours = d.getHours();
		if (oldHours >= d.getHours()) {
			this.innerHTML = padzero(d.getHours(),2) + ":" + padzero(d.getMinutes(),2) + ":" + padzero(d.getSeconds(),2);
		}
	});


});
