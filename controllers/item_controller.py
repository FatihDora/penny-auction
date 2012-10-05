#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.item as item

from google.appengine.ext import db

def items_list():
	'''
		Get a list of all item names
	'''
	pass

def item_add(name, quantity, price, url, image_url):
	'''
		Create a new item with the specified properties (administrative only)
	'''
	pass

def item_get_info(name):
	'''
		Get the quantity, base price, product url, and image url for the
		specified item
	'''
	pass

def item_update_price(name, price):
	'''
		Update the price of the specified item (administrative only)
	'''
	pass

def item_update_quantity(name, quantity):
	'''
		Update the quantity of the specified item (administrative only)
	'''
	pass

def item_list_auctions(name):
	'''
		List all auctions that have occurred for the specified item
	'''
	pass
