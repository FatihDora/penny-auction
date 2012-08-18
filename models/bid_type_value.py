#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidTypeValue(db.Model):
	id = db.IntegerProperty(required=True)
	bid_type = db.ReferenceProperty(BidType, collection_name='values')
	value = db.DecimalProperty(required=True)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'bids' created by the BidHistory class
