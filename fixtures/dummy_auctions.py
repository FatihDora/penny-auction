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
		auction.Auction(id=1,item=item1,current_winner=darin,auction_end=datetime.datetime.now()+timedelta(seconds=20)).put()
		auction.Auction(id=2,item=item2,current_winner=kevin,auction_end=datetime.datetime.now()+timedelta(seconds=33)).put()
		auction.Auction(id=3,item=item3,current_winner=brent,auction_end=datetime.datetime.now()+timedelta(seconds=46)).put()
		auction.Auction(id=4,item=item1,current_winner=kevin,auction_end=datetime.datetime.now()+timedelta(seconds=59)).put()
		auction.Auction(id=5,item=item2,current_winner=brent,auction_end=datetime.datetime.now()+timedelta(seconds=62)).put()
		auction.Auction(id=6,item=item3,current_winner=darin,auction_end=datetime.datetime.now()+timedelta(seconds=75)).put()