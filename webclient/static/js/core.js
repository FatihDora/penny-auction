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

// Auctions
var BID = '/bid';
var GET_AUCTION_INFO = '/get_auction_info';


$(document).ready(function() {
	/* Set up the jQuery AJAX stuff */
	$.ajaxSetup({
		async: true,
		dataType: "jsonp",
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
			showDialog("error", "Unexpected Error", status);
		}
	});

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

	/* Bid Button Clicked */
	$(".auction-bid-button").click(function() {
		var auction_id = $(this).parent().attr("id");
		jQuery.ajax({
			url: API + BID,
			dataType: "jsonp",
			type: "GET",
			data: {id : auction_id},
			success: function(data) {
				alert(data);
			}
		});
	});

	/* Login Button Clicked */
	$("#user-login").click(function() {
		var u = 'tester2';
		var p = 'tester2';
		jQuery.ajax({
			url: API + USER_REGISTER,
			dataType: "jsonp",
			type: "GET",
			data: {username : u,
				   password : p},
			success: function(data) {
				alert(data);
			}
		});
	});

	/***************** TEST LOGIN STUFF ********************/

	$(".login").click(function(e) {
					e.preventDefault();
					$("fieldset#login-menu").toggle();
					$(".login").toggleClass("menu-open");
				});

				$("fieldset#login-menu").mouseup(function() {
					return false
				});

				$(document).mouseup(function(e) {
					if($(e.target).parent("a.login").length==0) {
						$(".login").removeClass("menu-open");
						$("fieldset#login-menu").hide();
					}
				});

	$("#show-registration").click(function() {
		$("#overlay").css('display','block');
		$("#overlay").css('height',$(document).height()+'px');
		$("#overlay").css('width',$(document).width()+'px');
		$("fieldset#registration-menu").css('display','block');
	});
	
	$("#overlay").click(function() {
		$(this).css('display','none');
		$("fieldset#registration-menu").css('display','none');
	});


	/************** END TEST LOGIN STUFF *******************/


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
