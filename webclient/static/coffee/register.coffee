$(document).ready ->
	register.init()

	# End $(document).ready

register = init: ->
	#-------------------#
	# Registration Form #
	#-------------------#

	# Setup the registration form.
	$("#registration-form").submit (e) ->
		e.preventDefault()
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