###############################################################################
# These functions handle the client side of user login with Mozilla Persona.
# They requires the set_cookie() function in core.js
###############################################################################

# takes the browser's assertion code and sets it in a cookie
persona_login_callback = (assertion) ->
	window.set_cookie 'browser_id_assertion', assertion
	window.location.reload()

# initiates the login process by requesting the browser's assertion code and
# passing the code to persona_login_callback
persona_login = ->
	navigator.id.getVerifiedEmail persona_login_callback

# destroys the Persona cookie
persona_logout = ->
	window.set_cookie 'browser_id_assertion', '', -10
	window.location.reload

$(document).ready ->
	$(".persona-login-button").click persona_login

