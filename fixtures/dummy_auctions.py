#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import auction, decimal_property
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
		
		# testing auctions
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=20))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=33))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=46))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=59))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=72))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=85))

		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=98))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=101))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=114))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=127))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=140))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=153))

		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=166))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=179))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=192))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=205))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=218))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=231))

		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=244))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=257))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=270))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=283))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=296))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=309))

		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=322))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=335))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=348))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=361))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=374))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=387))