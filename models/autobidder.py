#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class Autobidder(db.Model):
        id = db.IntegerProperty(required=True)
		user_id = db.IntegerProperty(required=True)
		auction_id = db.IntegerProperty(required=True)
		bid_type_id = db.IntegerProperty(required=True)
		remaining_bids = db.IntegerProperty(required=True)
        create_time = db.DateTimeProperty(required=True)

