#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from google.appengine.ext import db

import models.auction as auction
import models.user as user

class BidHistory(db.Model):
	id = db.IntegerProperty(required=True)
	transaction_time = db.DateTimeProperty(auto_now_add=True)
	auction = db.ReferenceProperty(auction.Auction, collection_name='past_bids')
	user = db.ReferenceProperty(user.User, collection_name='past_bids')
