#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db

class Auction(db.Model):
	id = db.IntegerProperty()
	name = db.StringProperty()
	productUrl = db.StringProperty()
	imageUrl = db.StringProperty()
	currentPrice = db.FloatProperty()
	currentWinner = db.StringProperty()
	auctionEnd = db.DateTimeProperty()
