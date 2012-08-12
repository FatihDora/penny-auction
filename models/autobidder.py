#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class Autobidder(db.Model):
		id = db.IntegerProperty()
		user_id = db.IntegerProperty()
		auction_id = db.IntegerProperty()
		bid_type_id = db.IntegerProperty()
		remaining_bids = db.IntegerProperty()
		create_time = db.DateTimeProperty()

