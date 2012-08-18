#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidType(db.Model):
	id = db.IntegerProperty(required=True)
	name = db.StringProperty(required=True)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'past_bids' created by the BidHistory class
	# implicit property 'outstanding_bids' created by the BidPool class
