#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db
import models.user as user
import models.auction as auction
import models.bid_type as bid_type

class Autobidder(db.Model):
	''' This class models an auto bidder, which places bids on an auction
	automatically on behalf of its creator. '''

	id = db.IntegerProperty(required=True)
	user = db.ReferenceProperty(user.User, collection_name='active_autobidders')
	auction = db.ReferenceProperty(auction.Auction, collection_name='attached_autobidders')
	bid_type = db.ReferenceProperty(bid_type.BidType, collection_name='active_autobidders')
	remaining_bids = db.IntegerProperty(required=True)
	create_time = db.DateTimeProperty(required=True)

	def use_bid(self):
		''' Uses up one of the bids in this autobidder. Throws a
		NoBidsRemainingException if there are no bids left to use. '''

		if self.remaining_bids > 0:
			self.remaining_bids -= 1
			self.put()
		else:
			raise NoBidsRemainingException(self)

