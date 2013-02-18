################################################################################
# © 2013
# main author: Darin Hoover
################################################################################

$(document).ready ->
	# Load up the auction detail once
	if auction.init()
		window.setInterval auction.update, 1000

	autobidder.init()

	# Update the main auction
	# TODO: auction.update()
	# TODO: autobidder.update()

	#Update the side auctions

	# End $(document).ready

auction =
	init: ->
		# The page should be rendered with the ID in a javascript tag for us.
		# Auction ID is stored in auction_id
		# init will do the following:
		# * Get the detail for the auction_id and display it in the page.
		# * Get the top 3 auctions to put in the side bar.
		# * Setup a timer to get the data for the main and 3 side auctions every 1 second.
		# * The main auction should return the same data as the side auctions as well as
		#   the previous 9 bidders (for a total of 10 bidders).
		jQuery.ajax
			url: AUCTION_DETAIL
			data: {id: auction_id}
			success: (data) ->
				if data.result
					auction = data.result
					if not auction?
						$("#onecol .gallery").html '<h2 class="red">Auctions</h2><br/><p style="font-size: 14px; width:100%">Unfortunately, there aren\'t any auctions in the system.  To spin up some auctions, visit http://pisoapi.appspot.com/reset_data.</p><br/><br/><br/><div class="clear"></div>'
						return false

					i = auction.id # ID
					n = auction.name # Name
					b = auction.base_price # Base Price
					u = auction.product_url # Manufacturer's URL
					m = auction.image_url # Image Url
					p = auction.price # Current Price
					w = auction.winner # Winner Username
					t = secondsToHms(auction.time_left)

					# Update the page with the data
					$('#auction-name').text auction.name
					$('#auction-image img').attr 'src', auction.image_url
					$('#auction-detail div.price span.right').html 'P' + auction.price
					$('#auction-detail div.winner span.right').html auction.winner
					$('#auction-detail div.time-left').html secondsToHms(auction.time_left)
					return true
				else
					return false

	update: ->
		jQuery.ajax
			url: AUCTION_RECENT_BIDS
			data: {id: auction_id}
			success: (data) ->
				if data.result
					recent_bids = data.result




autobidder = init: ->
	# Gets the user's autobidder infor for this auction
	jQuery.ajax
		url: AUTOBIDDER_STATUS_BY_AUCTION
		data: {id: auction_id}
		success: (data) ->
			if data.result

				autobidder = data.result
				# If there is an id present, we assume that an autobidder exists.
				if not autobidder.id
					$('#create-autobidder').show();
					$('#cancel-autobidder').hide();
				else
					$('#cancel-autobidder').show();
					$('#create-autobidder').hide();
	
