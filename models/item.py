#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

import models.decimal_property as decimal_property

class Item(db.Model):
	name = db.StringProperty(required=True)
	quantity_in_stock = db.IntegerProperty(required=True)
	base_price = decimal_property.DecimalProperty(required=True)
	product_url = db.StringProperty()
	image_url = db.StringProperty()
	# implicit property 'auctions' created by the Auction class

	@staticmethod
	def get_by_ids(ids):
		'''
			Generates a list of items whose id is contained in the {ids} list
		'''
		ids = [map(int, x) for x in ids]
		return Item.all().filter("id IN", ids).get()

	@staticmethod
	def create(name, quantity, price, url, image_url):
		'''
			Creates an item
		'''
		Item(name=name, quantity_in_stock=quantity, base_price=price,
				product_url=url, image_url=image_url).put()
