#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
import models.bid_type as bid_type
import models.decimal_property as decimal_property

class BidTypeValue(db.Model):
	id = db.IntegerProperty(required=True)
	bid_type = db.ReferenceProperty(bid_type.BidType, collection_name='values')
	value = decimal_property.DecimalProperty(required=True)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'bids' created by the BidHistory class
