#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidPool(db.Model):
	id = db.IntegerProperty(required=True)
	number_of_bids = db.IntegerProperty(required=True)
	user = db.ReferenceProperty(User, collection_name='available_bids')
	bid_type = db.ReferenceProperty(BidType, collection_name='outstanding_bids')

