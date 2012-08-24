#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidHistory(db.Model):
	id = db.IntegerProperty(required=True)
	transaction_time = db.DateTimeProperty(required=True)
	bid_type = db.ReferenceProperty(BidType, collection_name='past_bids')
	auction = db.ReferenceProperty(Auction, collection_name='past_bids')
	user = db.ReferenceProperty(User, collection_name='past_bids')
