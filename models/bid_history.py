#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

import models.auction as auction
import models.user as user

class BidHistory(db.Model):
	id = db.IntegerProperty(required=True)
	transaction_time = db.DateTimeProperty(required=True)
	auction = db.ReferenceProperty(auction.Auction, collection_name='past_bids')
	user = db.ReferenceProperty(user.User, collection_name='past_bids')
