#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class AuctionController:
	''' This class manipulates auction models. '''

	def invoke_auto_bidders(auction):
		''' Pass an Auction object to have the next auto bidder attached to that
		auction place a bid. If no auto bidders with remaining bids are
		attached, nothing happens. '''

		next_auto_bidder = None
		for this_auto_bidder in auction.attached_autobidders:
			if next_auto_bidder is None or this_auto_bidder.last_bid_time < next_auto_bidder.last_bid_time:
				next_auto_bidder = this_auto_bidder

		# shortcut out if there are no autobidders on this auction
		if next_auto_bidder is None:
			return
		
		next_auto_bidder.use_bid()
		auction.place_bid(next_auto_bidder.owner)
	
