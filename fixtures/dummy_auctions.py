#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import auction, decimal_property
import random
from google.appengine.ext import db
from datetime import timedelta
import datetime

class DummyAuctions(object):
	@staticmethod
	def setup():
		db.delete(auction.Auction.all())

		item1 = db.get(db.Key.from_path('Item', 'MacBook Air'))
		item2 = db.get(db.Key.from_path('Item', 'MacBook Pro'))
		item3 = db.get(db.Key.from_path('Item', 'Airport Express'))
		
		items = []
		items.append(item1)
		items.append(item2)
		items.append(item3)
		auction_end = datetime.datetime.now()
		for x in range(0, 100):
			auction_end += timedelta(seconds=10) # timedelta(seconds=random.randint(120, 180))
			item = items[random.randint(0,2)]
			auction.Auction.create(item,auction_end)


		
		