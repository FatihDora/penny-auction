$(document).ready ->
	
	auctions.init()

	if $("#auctions").length isnt 0
				window.setInterval auctions.updateAuctions, 1000
	# End $(document).ready
	


############################################
# Auctions
############################################

auction_ids = []
auction_list = []
auctions =
	fetchingAuctionUpdates: null
	init: ->
		callApi AUCTIONS_LIST_CURRENT,({count: 30}), (data) ->
			$("#auctions").html ""
			auctions = data.result
			if not auctions?
				$("#onecol .gallery").html '<h2 class="red">Auctions</h2><br/><p style="font-size: 14px; width:100%">Unfortunately, there aren\'t any auctions in the system.  To spin up some auctions, visit http://pisoapi.appspot.com/reset_data.</p><br/><br/><br/><div class="clear"></div>'
				return

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

		# Bid Button Clicks
		$("ul#auctions").delegate "div.bid", "click", ->
			if user.loggedIn is false
				document.location.href = "/register"
				return

			id = $(@).closest('li').attr('id')
			if auction_list[id].t > 11.0
				document.location.href = "/auction/" + id

			if user.bids > 0
				auction_id = $(@).closest('li').attr("id")
				callApi AUCTION_BID,(id: auction_id), (data) ->
					user.bids -= 1
					user.update()
					if user.bids % 5 is 0
						user.refresh()  #refresh user info every 5 bids
					


		buildAuction = (id, productName, basePrice, productUrl, imageUrl, currentPrice, currentWinner, timeTilEnd) ->
			tmplAuction = undefined
			tmplAuction = ''
			tmplAuction += ' <li id="{auction-id}">\n'
			tmplAuction += '\t\t<!-- top block -->\n'
			tmplAuction += '\t\t<div class="top-block">\n'
			tmplAuction += '\t\t\t<h3 class="nocufon"><a href="{url}" title="{item-name}">{item-name}</a></h3>\n'
			tmplAuction += '\t\t\t<div class="imgb thumbnail-zoom">\n'
			tmplAuction += '\t\t\t\t<a href="/auction/{auction-id}" class="fadeable">\n'
			tmplAuction += '\t\t\t\t\t<span class="light-background">\n'
			tmplAuction += '\t\t\t\t\t<span class="thumb-arrow">&#8594;</span>\n'
			tmplAuction += '\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t\t\t<span>\n'
			tmplAuction += '\t\t\t\t\t\t<img src="{image-url}" width="194" height="144" alt="{item-name}" />\n'
			tmplAuction += '\t\t\t\t\t\t<!--<span class="sale-img">NEW<span>ITEM</span></span>-->\n'
			tmplAuction += '\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t</a>\n'
			tmplAuction += '\t\t\t</div>\n'
			tmplAuction += '\t\t\t<span class="winner"><a href="#">{winner}</a></span>\n'
			tmplAuction += '\t\t\t<span class="price">P {current-price}</span>\n'
			tmplAuction += '\t\t\t<span class="timeleft">{time-remaining}</span>\n'
			tmplAuction += '\t\t</div>\n'
			tmplAuction += '\t\t<!-- top block -->\n'
			tmplAuction += '\t\t<div class="bid js-button"><a href="javascript:void(0);" class="button-default cart"><span class="hover">BID NOW</span><span>BID NOW</span></a></div>\n'
			tmplAuction += '\t</li>\n'
			tmplAuction = tmplAuction.replaceAll("{auction-id}", id)
			tmplAuction = tmplAuction.replaceAll("{url}", productUrl)
			tmplAuction = tmplAuction.replaceAll("{item-name}", productName)
			tmplAuction = tmplAuction.replaceAll("{image-url}", imageUrl)
			tmplAuction = tmplAuction.replaceAll("{current-price}", currentPrice)
			tmplAuction = tmplAuction.replaceAll("{winner}", currentWinner)
			tmplAuction = tmplAuction.replaceAll("{time-remaining}", timeTilEnd)
			return tmplAuction
	
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