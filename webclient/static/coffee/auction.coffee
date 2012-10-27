$(document).ready ->
	auction.init()

	# End $(document).ready

auction = init: ->
	# The page should be rendered with the ID in a javascript tag for us.
	# Auction ID is stored in auction_id

	callApi AUCTION_DETAIL,(id: auction_id), (data) ->
			if data.result
				auctions = data.result
				if not auctions?
					$("#onecol .gallery").html '<h2 class="red">Auctions</h2><br/><p style="font-size: 14px; width:100%">Unfortunately, there aren\'t any auctions in the system.  To spin up some auctions, visit http://pisoapi.appspot.com/reset_data.</p><br/><br/><br/><div class="clear"></div>'
					return

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
					auction_list[i] = auctions[ix]
					$("#auctions").append(buildAuction(i, n, b, u, m, p, w, t))

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