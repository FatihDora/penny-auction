#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from threading import Timer
from google.appengine.ext import db
import models.item as item
import models.user as user

class Auction(db.Model):
	''' This class represents a single auction. '''

	id = db.IntegerProperty(required=True)
	name = db.StringProperty(required=True)
	item = db.ReferenceProperty(item.Item, collection_name='auctions')
	currentPrice = decimal.DecimalProperty(default='0.0')
	currentWinner = db.ReferenceProperty(user.User, collection_name='auctions_won')
	auctionEnd = db.DateTimeProperty()
	# implicit property 'attached_autobidders' created by the Autobidder class
	# implicit property 'past_bids' created by the BidHistory class

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
