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

		# shortcut out if there are no autobidders on this auction
		if len(auction.attached_autobidders) == 0:
			return

		# sort autobidders by last bid time, oldest to youngest
		auction.attached_autobidders.sort(key=lambda this_autobidder: this_autobidder.last_bid_time)

		for next_autobidder in auction.attached_autobidders:
			try:
				next_auto_bidder.use_bid()
			except NoBidsRemainingException as exception:
				del auction.attached_autobidders[this_autobidder_index]
				continue
			break

		auction.place_bid(next_auto_bidder.owner)
	
