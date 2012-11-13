#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from models import auction, item, user
from controllers import user_controller
from datetime import timedelta
import datetime
import logging

from google.appengine.ext import db

class AuctionController(object):
	''' This class manipulates auction models. '''

	@staticmethod
	def create(item_name, start_delay, bid_pushback_time):
		'''
			Creates an auction using the following parameters:
				item_name: the name of the item being auctioned
				start_delay: the number of seconds to wait before opening the auction to bidding
				bid_pushback_time: the number of seconds added to an active auction when a bid is placed
		'''
		Auction(item=Item.get(item_name), start_delay=start_delay, bid_pushback_time=bid_pushback_time)

	@staticmethod
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

	@staticmethod
	def auctions_status_by_id(auction_ids):
		'''
			List the auctions specified
		'''
		if not auction_ids:
			return

		# Try to parse the IDs and create a list of ints.
		try:
			sids = auction_ids.split(',')
		except Exception, e:
			raise Exception("The list of IDs provided could not be parsed.")
		ids = []
		for sid in sids:
			try:
				ids.append(int(sid))
			except Exception, e:
				raise Exception("The list of IDs provided could not be parsed.")

		if len(ids) > 40:
			raise Exception("Too many ids")

		# Try to get some auctions from the list of IDs
		auctions = auction.Auction.get_by_id(ids)
		if not auctions:
			raise Exception("There were no auctions for the IDs you provided.")

		return auctions


	@staticmethod
	def auctions_list_active(count=10):
		'''
			List the currently-running auctions
		'''
		auctions = auction.Auction.get_active(count)

		if not auctions:
			raise Exception("No active auctions.")

		return auctions

	@staticmethod
	def auctions_list_all():
		'''
			List all auctions (administrative only)
		'''
		auctions = auction.Auction.all()

		if not auctions:
			raise Exception("No auctions in the system.")

		return auctions

	@staticmethod
	def auction_bid(auction_id, username):
		'''
			Performs a single bid on the given auction on behalf of the specified user.
		'''

		userInfo = user.User.get_by_username(username)

		if userInfo is None:
			raise Exception("Couldn't get info for " + username)

		if userInfo.bid_count <= 0:
			raise Exception("Out of bids!")

		auctionInfo = auction.Auction.get_by_id(int(auction_id))

		if auctionInfo is None or auctionInfo.active is False:
			raise Exception("Auction does not exists.")

		if (auctionInfo.auction_end - datetime.datetime.now()).total_seconds() > 10:
			raise Exception("This auction has not yet started.")

		# Perform Bid:

		userInfo.bid_count -= 1
		userInfo.put()

		auctionInfo.current_winner = userInfo

		# If you ever need to change the time added to an auction when it's bid on
		# THIS is the place to do it.
		auctionInfo.auction_end = datetime.datetime.now() + timedelta(seconds=11)
		auctionInfo.increment_price()
		auctionInfo.put()

	@staticmethod
	def auction_detail(auction_id):
		'''
			Returns detailed auction information for the auction page.
		'''
		pass

