#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from threading import Timer
from google.appengine.ext import db
from models import item, user, decimal_property
import datetime, decimal
from datetime import timedelta

class Auction(db.Model):
	''' This class represents a single auction. '''

	item = db.ReferenceProperty(item.Item, collection_name='auctions')
	current_price = decimal_property.DecimalProperty(default="0.00")
	current_winner = db.ReferenceProperty(user.User, collection_name='auctions_won', default=None)

	# the time, in seconds, added to an auction when a bid is placed
	# also used for how long an auction with no bids should stay open
	bid_pushback_time = db.IntegerProperty(default=10)

	# the time at which the auction is set to end; this will be initially unset and will be updated as
	# bidding progresses
	auction_end = db.DateTimeProperty(default=None)

	# whether the auction is currently running and accepting bids
	# an auction is inactive if either it hasn't been started yet, or has completed already
	active = db.BooleanProperty(default = False)

	# implicit property 'attached_autobidders' created by the Autobidder class
	# implicit property 'past_bids' created by the BidHistory class


	# the amount an auction's price increases when a bid is placed, in centavos
	PRICE_INCREASE_FROM_BID = 0.01 


	@staticmethod
	def get_by_ids(ids):
		'''
			Generates a list of auctions whose id is contained in the {ids} list
		'''
		ids = [map(int, x) for x in ids]
		return Auction.all().filter("id IN", ids).get()

	@staticmethod
	def get_active(count):
		'''
			Lists the top {count} active auctions
		'''
		return db.Query(model_class=Auction, keys_only=True).filter("active", True).filter("auction_end > ",
				datetime.datetime.now()).order("auction_end").run(limit=count)

	def __init__(self, item, start_delay, bid_pushback_time):
		'''
			Create a new auction with the following properties:
				item: an item object representing the item being auctioned
				start_delay: the number of seconds to wait before opening the auction to bidding
				bid_pushback_time: the number of seconds added to an active auction when a bid is placed
		'''	

		if item is None:
			raise Exception("Auction creation failed: the item for this auction cannot be None")

		self.item = item
		if bid_pushback_time is not None:
			self.bid_pushback_time = bid_pushback_time

		# the heartbeat timer will be used when the auction is active, for now it will be set to None
		self.heartbeat_timer = None

		# initialize the timer counting down to auction start
		self.start_timer = Timer(
			start_delay,
			self.heartbeat,
			()
		).start()

		self.put()

	def heartbeat(self):
		'''
			Called when an auction first becomes active, and when the end time for an auction is reached,
			and then takes actions to maintain the state of the auction properly.
		'''
		pass
		'''
		# if this is the first heartbeat, take care of activating the auction
		if not self.active:
			self.active = True
			self.auction_end = datetime.now() + datetime.timedelta(seconds=bid_pushback_time)
			self.start_timer = None

		else:
			# check if there are any available autobidders and if so, place a bid
			if self.attached_autobidders:
				self.bid(...)
			else:
				# if there are no autobidders, close the auction
				self.active = False
				self.auction_end = datetime.now()
				return


		# set up the next heartbeat
		self.heartbeat_timer = Timer(
			bid_pushback_time,
			self.heartbeat,
			()
		).start()
		'''
		
	def bid(self, user):
		''' Place a bid on this auction. '''
		self.current_price += PRICE_INCREASE_FROM_BID
		self.auction_end += datetime.timedelta(seconds=bid_pushback_time)
		self.current_winner = user

