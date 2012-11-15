#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from google.appengine.ext import db, deferred
from models import item, user, decimal_property
import datetime, decimal, logging

class Auction(db.Model):
	''' This class represents a single auction. '''

	item = db.ReferenceProperty(item.Item, collection_name='auctions')
	current_price = decimal_property.DecimalProperty(default="0.00")
	current_winner = db.ReferenceProperty(user.User, collection_name='auctions_won', default=None)

	# the time at which this auction began accepting bids, NOT the time the auction was created
	start_time = db.DateTimeProperty(default=None)

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
		auctions = []
		count = 0
		for auction_id in ids:
			count += 1
			auctions.append(Auction.get_by_id(auction_id))

		return auctions

		#ids = [map(int, x) for x in ids]
		#raise Exception(Auction.all().filter("id =", ids).fetch())
		#return Auction.all().get()
		#return Auction.all().filter("id IN", ids).run()

	@staticmethod
	def get_current(count):
		'''
			Lists the top {count} auctions that are either open or waiting to open.
		'''
		return db.Query(model_class=Auction, keys_only=False).order("auction_end").run(limit=count)
	
	def start_countdown(self, delay=3600):
		'''
			Begins the countdown to making this auction active after the number
			of seconds given by delay, or makes this auction active immediately
			if delay is zero. Newly instantiated auction objects are dormant
			until this method is called.
		'''

		if delay > 0:
			# initialize the timer counting down to auction start
			self.start_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
			self.auction_end = self.start_time + datetime.timedelta(seconds=self.bid_pushback_time)
			self.put()
			deferred.defer(self._heartbeat, _countdown=delay, _queue="auction-heartbeat")
		else:
			self.start_time = datetime.datetime.now()
			self.auction_end = self.start_time + datetime.timedelta(seconds=self.bid_pushback_time)
			self.put()
			self.heartbeat()

	def _heartbeat(self):
		'''
			Called when an auction first becomes active, and when the end time for an auction is reached,
			and then takes actions to maintain the state of the auction properly.
		'''

		# if this is the first heartbeat, take care of activating the auction
		if not self.active:
			self.active = True

		else:
			if not self._invoke_autobidders():
				# if there are no autobidders, close the auction
				self.active = False
				self.auction_end = datetime.datetime.now()
				if self.current_winner:
					logging.info("Auction of {item} begun at {start_time} closed at {end_time} with a final price of {price} and winning user {winner}.".format(
						item = self.item.name,
						start_time = self.start_time,
						end_time = self.auction_end,
						price = self.current_price,
						winner = self.current_winner
					))
				else:
					logging.info("Auction of {item} begun at {start_time} closed at {end_time} with no bidders.".format(
						item = self.item.name,
						start_time = self.start_time,
						end_time = self.auction_end
					))

		self.put()

		# set up the next heartbeat if this auction is still live
		if self.active:
			deferred.defer(self._heartbeat, _countdown=self.bid_pushback_time, _queue="auction-heartbeat")

	def bid(self, user):
		'''
			Places a bid on this auction on behalf of the specified user, where
			user is the object corresponding to the user placing the bid. Note
			that this method does not modify the user object.
			Raises an Exception if the user parameter is None.
		'''

		if user is None:
			raise Exception("The user passed to Auction.bid() cannot be None.")

		self.current_price += PRICE_INCREASE_FROM_BID
		self.auction_end += datetime.timedelta(seconds=bid_pushback_time)
		self.current_winner = user
		self.put()

	def _invoke_autobidders(self):
		'''
			Make the next auto bidder attached to this auction place a bid.
			Returns a boolean indicating whether any bids were placed (no bids
			would be placed if either no auto bidders with remaining bids are
			attached or there simply are no attached autobidders to this
			auction).
		'''

		autobidders = self.attached_autobidders.fetch(None)

		# shortcut out if there are no autobidders on this auction
		if not autobidders:
			return False

		# sort autobidders by last bid time, oldest to youngest, with autobidders that haven't bid yet
		# sorted at the very front of the list
		autobidders.sort(key=lambda this_autobidder: this_autobidder.last_bid_time
				if(this_autobidder.last_bid_time)
				else datetime.datetime(datetime.MINYEAR))

		bid_placed = False
		for next_autobidder in autobidders:
			try:
				bids_remaining = next_auto_bidder.use_bid()
				bid_placed = True
				if bids_remaining < 1:
					del next_autobidder
				break
			except InsufficientBidsException as exception:
				del autobidders[this_autobidder_index]

		self.attached_autobidders = autobidders
		self.attached_autobidders.put()
		self.put()

		return bid_placed
	
	def attach_autobidder(self, user, bids):
		'''
			Attaches an autobidder to this auction, where user is the user
			model object for the user this autobidder belongs to and bids is
			the number of bids to place in the newly created autobidder. Raises
			an Exception if user is None, if the number of bids is less than 1,
			or if another autobidder on this auction belongs to the same user
			owning the new autobidder.
		'''

		if user is None:
			raise Exception("The user passed to Auction.attach_autobidder() cannot be None.")

		if bids < 1:
			raise Exception("The number of bids passed to Auction.attach_autobidder() must be at least 1.")

		user_list = ()
		for autobidder in self.attached_autobidders:
			user_list.append(autobidder.user)
		if user in user_list:
			raise Exception("The user passed to Auction.attached_autobidder() already owns an autobidder on this auction.")
		
		self.attached_autobidders.append(Autobidder(user, self, bids))
		self.attached_autobidders.put()
		self.put()

