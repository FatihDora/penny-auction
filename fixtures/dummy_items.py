#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import item
from google.appengine.ext import db

class DummyItems(object):
	@staticmethod
	def setup():
		db.delete(item.Item.all())

		# testing items
		item.Item(key_name="MacBook Air", name="MacBook Air",
			quantity_in_stock=400, base_price="999.99",
			product_url="http://www.apple.com/macbookair/",
			image_url="http://i.imgur.com/AssJR.jpg").put()
		item.Item(key_name="MacBook Pro", name="MacBook Pro",
			quantity_in_stock=329, base_price="1499.99",
			product_url="http://www.apple.com/macbook-pro/",
			image_url="http://i.imgur.com/CUUWF.jpg").put()
		item.Item(key_name="Airport Express", name="Airport Express",
			quantity_in_stock=53, base_price="69.99",
			product_url="http://www.apple.com/airportexpress/",
			image_url="http://i.imgur.com/SpDd8.jpg").put()
