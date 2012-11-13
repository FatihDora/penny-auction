#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from google.appengine.ext import db
import datetime
import models.user as user
import models.auction as auction


class Autobidder(db.Model):
	'''
		This class models an auto bidder, which places bids on an auction
		automatically on behalf of its creator.
	'''

	id = db.IntegerProperty(required=True)
	user = db.ReferenceProperty(user.User, collection_name='active_autobidders')
	auction = db.ReferenceProperty(auction.Auction, collection_name='attached_autobidders')
	remaining_bids = db.IntegerProperty(required=True)
	create_time = db.DateTimeProperty(required=True)
	last_bid_time = db.DateTimeProperty(default=None)

	def __init__(self, user, auction, bids):
		self.user = user
		self.auction = auction
		self.remaining_bids = bids
		self.create_time = datetime.now()

	def use_bid(self):
		'''
			Uses up one of the bids in this autobidder and returns the number of
			bids remaining after using this bid. Throws a NoBidsRemainingException if
			there are no bids left to use.
		'''

		if self.remaining_bids > 0:
			self.auction.bid(self.user)
			self.remaining_bids -= 1
			self.put()
		else:
			raise NoBidsRemainingException(self.user, self)

		return self.remaining_bids

