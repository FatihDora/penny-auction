#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import bid_type
from models import bid_type_value
from google.appengine.ext import db

class DummyBidTypes(object):
	@staticmethod
	def setup():
		db.delete(bid_type_value.BidTypeValue.all())
		db.delete(bid_type.BidType.all())

		# 3 bid types
		bid_type.BidType(key_name="Red", name="Red").put()
		bid_type.BidType(key_name="Blue", name="Blue").put()
		bid_type.BidType(key_name="Green", name="Green").put()

		# bid type values
		red = db.get(db.Key.from_path("BidType", "Red"))
		bid_type_value.BidTypeValue(key_name="Red", bid_type=red,
				value="1").put()
		blue = db.get(db.Key.from_path("BidType", "Blue"))
		bid_type_value.BidTypeValue(key_name="Blue", bid_type=blue,
				value="5").put()
		green = db.get(db.Key.from_path("BidType", "Green"))
		bid_type_value.BidTypeValue(key_name="Green", bid_type=green,
				value="10").put()

