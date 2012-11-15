#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from controllers import auction_controller
from models import auction, decimal_property
import random
from google.appengine.ext import db
from datetime import timedelta
import datetime

class DummyAuctions(object):
	@staticmethod
	def setup():
		db.delete(auction.Auction.all())
		
		items = ['MacBook Air', 'MacBook Pro', 'Airport Express']
		delay = timedelta(0)
		for x in range(0, 100):
			delay += timedelta(days=0.1)
			item_name = items[random.randint(0,2)]
			auction_controller.AuctionController.create(item_name=item_name, start_delay=delay)
