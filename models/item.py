#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

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
		if quantity is None or quantity < 0:
			raise Exception(
				"Argument 'quantity' cannot be None or less than 0")

		if price is None or price < 0:
			raise Exception(
				"Argument 'price' cannot be None or less than 0")

		Item(name=name, quantity_in_stock=quantity, base_price=price,
				product_url=url, image_url=image_url).put()

		theItem = Item.all().filter("name =", name).get()
		if theItem is None:
			raise Exception("Failed to create new Item")
		return theItem

	@staticmethod
	def get(name):
		'''
			Get the specified item
		'''
		return Item.all().filter("name =", name).get()

	def update_price(self, new_price):
		'''
			Update the price of the item
		'''
		if new_price is None or new_price < 0:
			raise Exception(
				"Argument 'new_price' cannot be None or less than 0")

		self.base_price = new_price
		self.put()

	def update_quantity(self, new_quantity):
		'''
			Update the quantity of this item in stock
		'''
		if new_quantity is None or new_quantity < 0:
			raise Exception(
				"Argument 'new_quantity' cannot be None or less than 0")

		self.quantity = new_quantity
		self.put()
