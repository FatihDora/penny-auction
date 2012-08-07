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

	/***************** BEGIN REGISTER & LOGIN STUFF ********************/

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
	
	/* Registration Form */
	$("#register-username").keyup(function(e) {
		clearTimeout($.data(this, 'timer'));
		if ($("#register-username").val() == 0) {
			$("#register-username-icon").css('visibility','hidden');
			return;
		}
		var username = $(this).val();
	    $(this).data('timer', setTimeout(function() {
			callApi(USER_USERNAME_EXISTS,{username:username},function(data) {
				if (data.exception) {return;}
				$("#register-username-icon").css('visibility','visible');
				if(data.result) {
					// True = Username Exists
					// Display Red X Icon
					$("#register-username-icon").attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
					$("#register-username-icon").attr('title','Username exists');
				} else {
					// False = Username Does Not Exist
					// Display Green Checkmark Icon
					$("#register-username-icon").attr('class','ui-icon ui-corner-all ui-icon-check data-valid');
					$("#register-username-icon").attr('title','Username not in use');	
				}
		});
		}, AJAX_KEYPRESS_DELAY));    
	});
	
	$("#register-email").keyup(function() {
		clearTimeout($.data(this, 'timer'));
		if ($("#register-email").val().length == 0) {
			$("#register-email-icon").css('visibility','hidden');
			return;
		} else {
			$("#register-email-icon").css('visibility','visible');
		}
		
		var email = $(this).val();
		var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		if(re.test(email)){
			// No need for a timer, since we won't send until they provide a valid email.
				callApi(USER_EMAIL_EXISTS,{email:email},function(data) {
					if (data.exception) {return;}
					if(data.result) {
						// True = Username Exists
						// Display Red X Icon
						$("#register-email-icon").attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
						$("#register-email-icon").attr('title','Email has already been registered.');
					} else {
						// False = Username Does Not Exist
						// Display Green Checkmark Icon
						$("#register-email-icon").attr('class','ui-icon ui-corner-all ui-icon-check data-valid');
						$("#register-email-icon").attr('title','Email has not been registered.');						
					}
				});
		} else {
			// True = Username Exists
			// Display Red X Icon
			$("#register-email-icon").attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
			$("#register-email-icon").attr('title','Invalid Email.');
		}    
	});

	var typewatch = (function(){
	  var timer = 0;
	  return function(callback, ms){
	    clearTimeout (timer);
	    timer = setTimeout(callback, ms);
	  }  
	})();
	/************** END REGISTER & LOGIN STUFF *******************/

	function callApi(method, data, callback) {
		jQuery.ajax({
			url: API + method,
			data: data,
			jsonp: "callback",
			success: callback
			});
	}
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
