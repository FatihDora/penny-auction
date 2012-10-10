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
		callApi AUCTIONS_LIST_ACTIVE,(count: 30), (data) ->
			$("#auctions").html ""
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

		# Bid Button Clicks
		$("ul#auctions").delegate "div.cart-button", "click", ->
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
			tmplAuction += '\t\t\t\t<div class="imgb thumbnail-zoom">\n'
			tmplAuction += '\t\t\t\t\t<a href="{url}" class="fadeable">\n'
			tmplAuction += '\t\t\t\t\t\t<span class="light-background">\n'
			tmplAuction += '\t\t\t\t\t\t<span class="thumb-arrow">&#8594;</span>\n'
			tmplAuction += '\t\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t\t\t<span>\n'
			tmplAuction += '\t\t\t\t\t\t\t<img src="{image-url}" width="194" height="144" alt="{item-name}" />\n'
			tmplAuction += '\t\t\t\t\t\t\t<!--<span class="sale-img">NEW<span>ITEM</span></span>-->\n'
			tmplAuction += '\t\t\t\t\t\t</span>\n'
			tmplAuction += '\t\t\t\t\t</a>\n'
			tmplAuction += '\t\t\t\t</div>\n'
			tmplAuction += '\t\t\t\t<span class="winner"><a href="#">{winner}</a></span>\n'
			tmplAuction += '\t\t\t\t<span class="price">P {current-price}</span>\n'
			tmplAuction += '\t\t\t\t<span class="timeleft">{time-remaining}</span>\n'
			tmplAuction += '\t\t\t</div>\n'
			tmplAuction += '\t\t<!-- top block -->\n'
			tmplAuction += '\t\t<div class="cart-button"><a href="javascript:void(0);"><span>BID NOW</span></a></div>\n'
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
		tmplist = []
		i = 0
		while i < auction_ids.length
			if auction_list[auction_ids[i]].t > 0.0
				tmplist.push auction_ids[i]
			i++

		auction_ids = tmplist
		if fetchingAuctionUpdates then fetchingAuctionUpdates.abort()
		fetchingAuctionUpdates = jQuery.ajax
			url: API + AUCTIONS_STATUS_BY_ID
			data:
				ids: auction_ids.join()

			jsonp: "callback"
			success: (data) ->
				$.map data, (auction) ->
					auctions = data.result
					auction_list = []
					for ix of auctions
						i = auctions[ix].i
						p = auctions[ix].p
						w = auctions[ix].w
						t = secondsToHms(auctions[ix].t)
						a = auctions[ix].a
						# IF WE NEED TO BLINK...
						#if $("#" + i + " span.winner").text isnt w
						#	$("#" + i + " span.winner").css "backgroundColor", "#CC0000"
						#	$("#" + i + " span.winner").animate backgroundColor: "#FFFFFF"
						auction_list[i] = auctions[ix]
						buttonText =""
						if auctions[ix].t > 11.0
							buttonText = "Starting Soon..."
						else
							if user.loggedIn?
								buttonText = "BID NOW!"
							else
								buttonText = "REGISTER NOW!"

						$("#" + i + " span.winner").html "<a href=\"#\">" + w + "</a>"
						$("#" + i + " span.price").text "P " + p
						$("#" + i + " span.timeleft").html(t)

						if a is "False"
							if w is "No Bidder" then  buttonText = "SOLD" else buttonText = "ENDED"
							$("#" + i + " div.cart-button").html '<a href="javascript:void(0);"><span>' + buttonText + '</span></a>'
						else
							$("#" + i + " div.cart-button").html '<a href="javascript:void(0);"><span>' + buttonText + '</span></a>'
