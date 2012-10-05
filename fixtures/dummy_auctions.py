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

		darin = db.get(db.Key.from_path('User', 'darin'))
		kevin = db.get(db.Key.from_path('User', 'kevin'))
		brent = db.get(db.Key.from_path('User', 'brent'))
		
		# testing auctions
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=20))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=33))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=46))
		auction.Auction.create(item1,datetime.datetime.now()+timedelta(seconds=59))
		auction.Auction.create(item2,datetime.datetime.now()+timedelta(seconds=62))
		auction.Auction.create(item3,datetime.datetime.now()+timedelta(seconds=75))