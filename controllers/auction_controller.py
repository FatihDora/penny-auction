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
	def create(item_name, start_delay, bid_pushback_time=timedelta(seconds=10)):
		'''
			Creates an auction using the following parameters:
				item_name: the name of the item being auctioned
				start_delay: a timedelta object giving the duration to wait before opening the auction to bidding
					(must represent a positive time duration)
				bid_pushback_time: a timedelta object giving the amount of time to be added to an active auction when a bid is placed
					(must represent a positive time duration)

			Returns the newly created auction object to allow method chaining.
		'''
		item_object = item.Item.get(item_name)
		if not item_object:
			raise Exception('No item exists named "{}"'.format(item_name))
		if start_delay < timedelta(0):
			raise Exception("The start_delay parameter must be a positive time interval, but the passed value was {}.".format(start_delay))
		if bid_pushback_time < timedelta(0):
			raise Exception("The bid_pushback_time parameter must be a positive time interval, but the passed value was {}.".format(bid_pushback_time))
		new_auction = auction.Auction(item=item_object, bid_pushback_time=bid_pushback_time)
		new_auction.put()
		new_auction.start_countdown(start_delay)
		return new_auction

	@staticmethod
	def auctions_status_by_ids(auction_ids):
		'''
			List the auctions specified
		'''
		if not auction_ids:
			return

		# Try to get some auctions from the list of IDs
		auctions = auction.Auction.get_by_id(auction_ids)
		if not auctions:
			auctions = []

		return auctions


	@staticmethod
	def auctions_list_current(count=10):
		'''
			List the currently-running auctions
		'''
		auctions = auction.Auction.get_current(int(count))

		if not auctions:
			raise Exception("No current auctions.")

		return auctions

	@staticmethod
	def auction_bid_history_by_user(auction_id, user_name):
		'''
			Returns a list of bids by the specified user on the specified
			auction. An empty list will be returned if this user has never bid
			on this auction. An Exception will be thrown if either the user or
			auction does not exist.
		'''

		this_auction = auction.Auction.get_by_id(auction_id)
		if not this_auction:
			raise Exception("No auction with ID \"{}\" exists.".format(auction_id))

		this_user = user.User.get_by_username(user_name)
		if not this_user:
			raise Exception("No user exists with user name \"{}\".".format(user_name))

		return this_auction.past_bids.filter("user", this_user).order("transaction_time").run()

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

		try:
			auction_id = int(auction_id)
		except Exception, e:
			raise Exception("Auction ID is invalid.")

		auctionInfo = auction.Auction.get_by_id(auction_id)

		if auctionInfo is None:
			raise Exception("Auction does not exist.")

		if not auctionInfo.active:
			raise Exception("This auction is not currently accepting bids.")

		# Perform Bid:
		userInfo.use_bids(1)
		auctionInfo.bid(userInfo)

	@staticmethod
	def attach_autobidder(auction_id, user_name, num_bids):
		'''
			Creates a new autobidder on the specified auction on behalf of the
			specified user with the specified number of bids.
		'''

		auction_info = auction.Auction.get_by_id(auction_id)

		if auction_info is None:
			raise Exception("Auction does not exist.")

		if not auction_info.active and auction_info.auction_end < datetime.datetime.now():
			raise Exception("Auction has closed.")

		user_info = user.User.get_by_username(user_name)

		if user_info is None:
			raise Exception("Couldn't get info for " + user_name)

		user_info.use_bids(num_bids)
		auction_info.attach_autobidder(user_info, num_bids)


	@staticmethod
	def get_autobidder_remaining_bids(auction_id, user_name):
		'''
			Returns an integer number of bids remaining in the specified user's
			autobidder attached to the specified auction. If the user has no
			autobidder, 0 will be returned.
		'''

		auction_info = auction.Auction.get_by_id(auction_id)

		if auction_info is None:
			raise Exception("Auction does not exist.")

		if not auction_info.active and auction_info.auction_end < datetime.datetime.now():
			raise Exception("Auction has closed.")

		user_info = user.User.get_by_username(user_name)

		if user_info is None:
			raise Exception("Couldn't get info for " + user_name)

		autobidder = auction_info.attached_autobidders.filter("user", user_info).get()
		if autobidder is None:
			return 0
		else:
			return autobidder.remaining_bids

	@staticmethod
	def cancel_autobidder(auction_id, user_name):
		'''
			Cancels any autobidder attached to the specified auction and
			belonging to the specified user. Does nothing if the user has no
			active autobidder on the auction.
		'''

		auction_info = auction.Auction.get_by_id(auction_id)

		if auction_info is None:
			raise Exception("Auction does not exist.")

		if not auction_info.active and auction_info.auction_end < datetime.datetime.now():
			raise Exception("Auction has closed.")

		user_info = user.User.get_by_username(user_name)

		if user_info is None:
			raise Exception("Couldn't get info for " + user_name)

		auction_info.close_autobidder(user_info)

