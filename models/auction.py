#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class Auction(db.Model):
	''' This class represents a single auction. '''

	id = db.IntegerProperty()
	name = db.StringProperty()
	user = db.ReferenceProperty(User, collection_name='auctions')
	productUrl = db.StringProperty()
	imageUrl = db.StringProperty()
	currentPrice = db.FloatProperty()
	currentWinner = db.StringProperty()
	auctionEnd = db.DateTimeProperty()
	# there is an implicit property 'attached_autobidders' created by the Autobidder class

	def __init__(self):

		# initialize the auction timer, but do not start it
		self.countdown_timer = Timer(
				AppSettings().AUCTION_INITIAL_DURATION,
				AuctionController.invoke_auto_bidding,
				(self)
		)

	def begin(self):
		''' Begins this auction. '''
		self.countdown_timer.start()

