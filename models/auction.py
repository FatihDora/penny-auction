#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from threading import Timer
from google.appengine.ext import db
from models import item, user, decimal_property
import datetime
from datetime import timedelta

class Auction(db.Model):
	''' This class represents a single auction. '''
	item = db.ReferenceProperty(item.Item, collection_name='auctions')
	current_price = decimal_property.DecimalProperty(default="0.00")
	current_winner = db.ReferenceProperty(user.User, collection_name='auctions_won')
	auction_end = db.DateTimeProperty()
	# implicit property 'attached_autobidders' created by the Autobidder class
	# implicit property 'past_bids' created by the BidHistory class

	@staticmethod
	def get_by_ids(ids):
		'''
			Generates a list of auctions whose id is contained in the {ids} list
		'''
		ids = [map(int, x) for x in ids]

		print ids[0]
		return Auction.all().filter("id IN", ids).get()

	@staticmethod
	def get_current(count=10):
		'''
			Lists the top {count=10} active auctions
		'''
		#return Auction.all().filter("auction_end < " .order("auction_end").fetch(count)

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
