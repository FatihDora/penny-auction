#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

import models.decimal_property as decimal_property

class Item(db.Model):
	id = db.IntegerProperty(required=True)
	name = db.StringProperty(required=True)
	quantity_in_stock = db.IntegerProperty(required=True)
	base_price = decimal_property.DecimalProperty(required=True)
	product_url = db.StringProperty()
	image_url = db.StringProperty()
	# implicit property 'auctions' created by the Auction class
