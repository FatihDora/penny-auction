###############################################################################
# These functions handle the client side of user login with Mozilla Persona.
# They depend on core.js
###############################################################################


window.session =

	loggedIn: false

	init: (assertion) ->
		jQuery.ajax
			url: USER_AUTHENTICATE
			data: {
				assertion: assertion
			}
			success: (data) ->
				if data.result
					window.session.loggedIn = true
					user.refresh
					window.session.showLoggedIn data.username
				else
					if data.error?
						error_message = data.error
					else
						error_message = 'The server could not verify your credentials.'

					showDialog "error", "Login Failed", error_message

	# execute cosmetic page changes on logging in
	showLoggedIn: (username) ->
		$('#login-wrapper').fadeOut 'fast', ->
			$('.username-label').text username
			$('#logout-wrapper').fadeIn 'slow', ->
				$('#top-account-info').fadeIn 'slow'
	
	logOut: ->
		window.session.loggedIn = false
		window.login.showLoggedOut()
		jQuery.ajax
			url: USER_LOGOUT
			data: {}
	
	# execute cosmetic page changes on logging out
	showLoggedOut: ->
		$('#logout-wrapper').fadeOut 'fast', ->
			$('#login-wrapper').fadeIn 'slow', ->
				$('#top-account-info').fadeOut 'slow'


$(document).ready ->
	navigator.id.watch
		onlogin: (assertion) ->
			window.session.init assertion
		onlogout: ->
			window.session.showLoggedOut

	$('.persona-login-button').click ->
		navigator.id.request {siteName: "Piso Auction"} # TODO: add a {siteLogo: "URL"} property to show the user our site's logo when logging in with Persona
	
	$('#logout-link').click (event) ->
		event.preventDefault
		window.session.logOut

