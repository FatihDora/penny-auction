#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
import models.user as user
import models.bid_type as bid_type

class BidPool(db.Model):
	id = db.IntegerProperty(required=True)
	number_of_bids = db.IntegerProperty(required=True)
	user = db.ReferenceProperty(user.User, collection_name='available_bids')
	bid_type = db.ReferenceProperty(bid_type.BidType, collection_name='outstanding_bids')

