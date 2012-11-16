$(document).ready ->
	auction.init()

	if $("#auctions").length isnt 0
			window.setInterval auction.updateAuction, 1000

	# End $(document).ready

auction = init: ->
	oAuction = null
	# The page should be rendered with the ID in a javascript tag for us.
	# Auction ID is stored in auction_id
	# init will do the following:
	# * Get the detail for the auction_id and display it in the page.
	# * Get the top 3 auctions to put in the side bar.
	# * Setup a timer to get the data for the main and 3 side auctions every 1 second.
	# * The main auction should return the same data as the side auctions as well as
	#   the previous 9 bidders (for a total of 10 bidders).
	callApi AUCTION_DETAIL,(id: auction_id), (data) ->
			if not data.result
				document.location.href = '/'
			else
				oAuction = data.result[0]

				i = oAuction.id # ID
				n = oAuction.name # Name
				b = oAuction.base_price # Base Price
				u = oAuction.product_url # Manufacturer's URL
				m = oAuction.image_url # Image Url
				p = oAuction.price # Current Price
				w = oAuction.winner # Winner Username
				oAuction.time_left = secondsToHms(oAuction.time_left)

				# Update the page with the data
				$('#auction-name').html(oAuction.name)
				$('#auction-image').html('<img src="' + oAuction.image_url + '" alt="' + oAuction.name + '" width="292" height="242" />')
				$('#current-price').html('P' + oAuction.price)
				$('#current-winner').html(oAuction.winner)
				$('#auction-baseprice').html(oAuction.base_price)
				$('#auction-time-left').html(oAuction.time_left)

	callApi AUCTIONS_LIST_CURRENT,({count: 4}), (data) ->
		'''
			We get 4 to guarantee that at least 3 of them aren't the current auction.
		'''
			$("#auctions").html ""
			sideAuctions = data.result

			for ix of auctions
				i = auctions[ix].id
				n = auctions[ix].name
				b = auctions[ix].base_price
				u = auctions[ix].product_url
				m = auctions[ix].image_url
				p = auctions[ix].price
				w = auctions[ix].winner
				t = secondsToHms(auctions[ix].time_left)
				auction_ids.push i
				auction_list[i] = auctions[ix]
				$("#auctions").append(buildAuction(i, n, b, u, m, p, w, t))

	updateAuctions: ->
		if auction_ids.length is 0 then return
		console.log("Auction List Length: " + auction_list.length)

		tmplist = []
		i = 0
		for id in auction_ids
			try 
				if auction_list[id].time_left > 0.0
					tmplist.push id
			catch error
				console.log("!!! ERROR !!! :: [" + id + "] :: " + error)
			i++

		auction_ids = tmplist

		if fetchingAuctionUpdates then fetchingAuctionUpdates.abort()
		fetchingAuctionUpdates = jQuery.ajax
			url: API + AUCTIONS_STATUS_BY_ID
			data:
				ids: auction_ids.join()

			success: (data) ->
				$.map data, (auction) ->
					auctions = data.result
					console.log("Updated Auctions Length: " + auctions.length)
					auction_list = []
					for ix of auctions
						i = auctions[ix].id
						p = auctions[ix].price
						w = auctions[ix].winner
						t = secondsToHms(auctions[ix].time_left)
						a = auctions[ix].active
						# IF WE NEED TO BLINK...
						#if $("#" + i + " span.winner").text isnt w
						#	$("#" + i + " span.winner").css "backgroundColor", "#CC0000"
						#	$("#" + i + " span.winner").animate backgroundColor: "#FFFFFF"
						auction_list[i] = auctions[ix]
						buttonText =""
						if auctions[ix].time_left > 11.0
							buttonText = "Starting Soon..."
						else
							if user.loggedIn?
								buttonText = "BID NOW!"
							else
								buttonText = "REGISTER NOW!"

						$("#" + i + " span.winner").html "<a href=\"#\">" + w + "</a>"
						$("#" + i + " span.price").text "P " + p
						$("#" + i + " span.timeleft").html(t)

						if auctions[ix].time_left == 0
							if w is "No Bidder" then  buttonText = "SOLD" else buttonText = "ENDED"
		
						$("#" + i + " div.bid").html '<a href="javascript:void(0);" class="button-default cart"><span class="hover">' + buttonText + '</span><span>' + buttonText + '</span></a>'


	# Setup the registration form.
	$("#createautobidder-form").submit (e) ->
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

