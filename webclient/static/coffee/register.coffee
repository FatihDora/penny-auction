###
BEGIN REGISTER & LOGIN STUFF *******************
###
$(".login").click (e) ->
	e.preventDefault()
	$("fieldset#login-menu").toggle()
	$(".login").toggleClass "menu-open"

$("fieldset#login-menu").mouseup ->
	false

$(document).mouseup (e) ->
	if $(e.target).parent("a.login").length is 0
		$(".login").removeClass "menu-open"
		$("fieldset#login-menu").hide()

$("#show-registration").click ->
	$("#overlay").css "display", "block"
	$("#overlay").css "height", $(document).height() + "px"
	$("#overlay").css "width", $(document).width() + "px"
	$("fieldset#registration-menu").css "display", "block"

$("#overlay").click ->
	$(this).css "display", "none"
	$("fieldset#registration-menu").css "display", "none"

$("#close-registration-menu").click ->
	$("#overlay").css "display", "none"
	$("fieldset#registration-menu").css "display", "none"

$("#login-form").submit (e) ->
	username = $("#login-username").val()
	password = $("#login-password").val()
	callApi USER_AUTHENTICATE,
		username: username
		password: password
	, (data) ->
		if data.exception
			showDialog "error", "Login Error", data.exception
			return
		if data.result
			$("#account-navigation").css "visibility", "visible"
			$("#account-navigation").css "display", "block"
			$("#user-account").html "<a href='user'>&#35; " + username + "</a>"
			$("#bid-info").css "visibility", "visible"
			$("#bid-info").css "display", "block"
			$("#login-container").css "visibility", "hidden"
			$("#login-container").css "display", "none"

	false


# Registration Form 
$("#register-username").keyup (e) ->
	clearTimeout $.data(this, "timer")
	if $("#register-username").val() is 0
		$("#register-username-icon").css "visibility", "hidden"
		return
	username = $(this).val()
	$(this).data "timer", setTimeout(->
		callApi USER_USERNAME_EXISTS,
			username: username
		, (data) ->
			if data.exception
				showDialog "error", "Registration Error", data.exception
				return
			$("#register-username-icon").css "visibility", "visible"
			if data.result
				
				# True = Username Exists
				# Display Red X Icon
				$("#register-username-icon").attr "class", "ui-icon ui-corner-all ui-icon-closethick data-invalid"
				$("#register-username-icon").attr "title", "Username exists"
			else
				
				# False = Username Does Not Exist
				# Display Green Checkmark Icon
				$("#register-username-icon").attr "class", "ui-icon ui-corner-all ui-icon-check data-valid"
				$("#register-username-icon").attr "title", "Username not in use"

	, AJAX_KEYPRESS_DELAY)

$("#register-email").keyup ->
	clearTimeout $.data(this, "timer")
	if $("#register-email").val().length is 0
		$("#register-email-icon").css "visibility", "hidden"
		return
	else
		$("#register-email-icon").css "visibility", "visible"
	email = $(this).val()
	re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	if re.test(email)
		
		# No need for a timer, since we won't send until they provide a valid email.
		callApi USER_EMAIL_EXISTS,
			email: email
		, (data) ->
			return	if data.exception
			if data.result
				
				# True = Username Exists
				# Display Red X Icon
				$("#register-email-icon").attr "class", "ui-icon ui-corner-all ui-icon-closethick data-invalid"
				$("#register-email-icon").attr "title", "Email has already been registered."
			else
				
				# False = Username Does Not Exist
				# Display Green Checkmark Icon
				$("#register-email-icon").attr "class", "ui-icon ui-corner-all ui-icon-check data-valid"
				$("#register-email-icon").attr "title", "Email has not been registered."

	else
		
		# True = Username Exists
		# Display Red X Icon
		$("#register-email-icon").attr "class", "ui-icon ui-corner-all ui-icon-closethick data-invalid"
		$("#register-email-icon").attr "title", "Invalid Email."

$("#registration-form").submit (e) ->
	username = $("#register-username").val()
	email = $("#register-email").val()
	password = $("#register-password").val()
	callApi USER_REGISTER,
		username: username
		email: email
		password: password
	, (data) ->
		if data.exception
			showDialog "error", "Registration Error", data.exception
			return
		if data.result
			$("#account-navigation").css "visibility", "visible"
			$("#account-navigation").css "display", "block"
			$("#user-account").html "<a href='user'>&#35; " + username + "</a>"
			$("#bid-info").css "visibility", "visible"
			$("#bid-info").css "display", "block"
			$("#login-container").css "visibility", "hidden"
			$("#login-container").css "display", "none"
			$("#overlay").css "display", "none"
			$("fieldset#registration-menu").css "display", "none"

	false

typewatch = (->
	timer = 0
	(callback, ms) ->
		clearTimeout timer
		timer = setTimeout(callback, ms)
)()

###
END REGISTER & LOGIN STUFF ******************
###