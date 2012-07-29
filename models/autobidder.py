#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class Autobidder(db.Model):
		id = db.IntegerProperty(required=True)
		user = db.ReferenceProperty(User, collection_name='active_autobidders')
		auction = db.ReferenceProperty(Auction, collection_name='attached_autobidders')
		bid_type_id = db.IntegerProperty(required=True)
		remaining_bids = db.IntegerProperty(required=True)
		create_time = db.DateTimeProperty(required=True)

