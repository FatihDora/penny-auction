#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from threading import Timer
from google.appengine.ext import db
from models import item, user, decimal_property
import datetime, decimal
from datetime import timedelta

class Auction(db.Model):
	''' This class represents a single auction. '''
	item = db.ReferenceProperty(item.Item, collection_name='auctions')
	current_price = decimal_property.DecimalProperty(default="0.00")
	current_winner = db.ReferenceProperty(user.User, collection_name='auctions_won')
	auction_end = db.DateTimeProperty()
	# Do we want to explicitly define an auction as active, or derive it from the end time?
	active = db.BooleanProperty(default = True)
	# implicit property 'attached_autobidders' created by the Autobidder class
	# implicit property 'past_bids' created by the BidHistory class

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
		return Auction.all().filter("active", True).filter("auction_end > ",
				datetime.datetime.now()).order("auction_end").fetch(int(count))

	@staticmethod
	def get_all():
		'''
			Lists all the auctions
		'''

		return Auction.all()

	@staticmethod
	def create(item, auction_end):
		'''
			Creates an auction
		'''
		Auction(item=item, auction_end=auction_end).put()

	def increment_price(sender, amount=0.01):
		'''
			Increments the price of the auction by the amount
		'''
		sender.current_price = sender.current_price + decimal.Decimal(amount)

	#def __init__(self):

		# initialize the auction timer, but do not start it
		#self.countdown_timer = Timer(
		#	AppSettings().AUCTION_INITIAL_DURATION,
		#	AuctionController.invoke_auto_bidding,
		#	(self)
		#)

	#def begin(self):
		#''' Begins this auction. '''
		#self.countdown_timer.start()
