/***************** BEGIN REGISTER & LOGIN STUFF ********************/

$('.login').click(function(e) {
				e.preventDefault();
				$('fieldset#login-menu').toggle();
				$('.login').toggleClass('menu-open');
			});

			$('fieldset#login-menu').mouseup(function() {
				return false
			});

			$(document).mouseup(function(e) {
				if($(e.target).parent('a.login').length==0) {
					$('.login').removeClass('menu-open');
					$('fieldset#login-menu').hide();
				}
			});

$('#show-registration').click(function() {
	$('#overlay').css('display','block');
	$('#overlay').css('height',$(document).height()+'px');
	$('#overlay').css('width',$(document).width()+'px');
	$('fieldset#registration-menu').css('display','block');
});

$('#overlay').click(function() {
	$(this).css('display','none');
	$('fieldset#registration-menu').css('display','none');
});

$('#close-registration-menu').click(function() {
	$('#overlay').css('display','none');
	$('fieldset#registration-menu').css('display','none');	
});


$('#login-form').submit(function(e) {
	var username = $('#login-username').val();
	var password = $('#login-password').val();
	callApi(USER_AUTHENTICATE,{username:username, password:password},function(data) {
		if (data.exception) {showDialog("error", "Login Error", data.exception);return;}
		if(data.result) {
			$('#account-navigation').css('visibility','visible');
			$('#account-navigation').css('display','block');
			$('#user-account').html('<a href=\'user\'>&#35; ' + username + '</a>');
			$('#bid-info').css('visibility','visible');
			$('#bid-info').css('display','block');
			$('#login-container').css('visibility','hidden');
			$('#login-container').css('display','none');
		}
	});
	return false;
});

/* Registration Form */
$('#register-username').keyup(function(e) {
	clearTimeout($.data(this, 'timer'));
	if ($('#register-username').val() == 0) {
		$('#register-username-icon').css('visibility','hidden');
		return;
	}
	var username = $(this).val();
    $(this).data('timer', setTimeout(function() {
		callApi(USER_USERNAME_EXISTS,{username:username},function(data) {
			if (data.exception) {showDialog("error", "Registration Error", data.exception);return;}
			$('#register-username-icon').css('visibility','visible');
			if(data.result) {
				// True = Username Exists
				// Display Red X Icon
				$('#register-username-icon').attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
				$('#register-username-icon').attr('title','Username exists');
			} else {
				// False = Username Does Not Exist
				// Display Green Checkmark Icon
				$('#register-username-icon').attr('class','ui-icon ui-corner-all ui-icon-check data-valid');
				$('#register-username-icon').attr('title','Username not in use');	
			}
	});
	}, AJAX_KEYPRESS_DELAY));    
});

$('#register-email').keyup(function() {
	clearTimeout($.data(this, 'timer'));
	if ($('#register-email').val().length == 0) {
		$('#register-email-icon').css('visibility','hidden');
		return;
	} else {
		$('#register-email-icon').css('visibility','visible');
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
					$('#register-email-icon').attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
					$('#register-email-icon').attr('title','Email has already been registered.');
				} else {
					// False = Username Does Not Exist
					// Display Green Checkmark Icon
					$('#register-email-icon').attr('class','ui-icon ui-corner-all ui-icon-check data-valid');
					$('#register-email-icon').attr('title','Email has not been registered.');						
				}
			});
	} else {
		// True = Username Exists
		// Display Red X Icon
		$('#register-email-icon').attr('class','ui-icon ui-corner-all ui-icon-closethick data-invalid');
		$('#register-email-icon').attr('title','Invalid Email.');
	}    
});

$('#registration-form').submit(function(e) {
	var username = $('#register-username').val();
	var email = $('#register-email').val();
	var password = $('#register-password').val();
	callApi(USER_REGISTER,{username:username, email:email, password:password},function(data) {
		if (data.exception) {showDialog("error", "Registration Error", data.exception);return;}
		if(data.result) {
			$('#account-navigation').css('visibility','visible');
			$('#account-navigation').css('display','block');
			$('#user-account').html('<a href=\'user\'>&#35; ' + username + '</a>');
			$('#bid-info').css('visibility','visible');
			$('#bid-info').css('display','block');
			$('#login-container').css('visibility','hidden');
			$('#login-container').css('display','none');
			$('#overlay').css('display','none');
			$('fieldset#registration-menu').css('display','none');
			
		}
	});
	return false;
});

var typewatch = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  }  
})();
/************** END REGISTER & LOGIN STUFF *******************/