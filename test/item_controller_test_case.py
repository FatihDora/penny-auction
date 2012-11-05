#!/usr/bin/env python
# -*- coding: utf-8 -*-

import controllers.item_controller as item_controller
import fixtures.dummy_items as dummy_items
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed

class ItemControllerTestCase(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

		# make some fixture items
		dummy_items.DummyItems.setup()

	def tearDown(self):
		self.testbed.deactivate()

	def make_item(self, quantity=9001, price="14.99"):
		# make an item
		item_controller.ItemController.item_add("Gorilla Munch", quantity,
			price, "http://thereisnoneed.com", "http://i.imgur.com/1jqAT.png")

	def testCreateItem(self):
		# verify the item doesn't exist
		all_items = item_controller.ItemController.items_list()
		for item in all_items:
			if item.name == "Gorilla Munch":
				self.fail("Impossible! Gorilla Munch already exists!")
				return

		# make the item
		self.make_item()

		# verify the item exists
		found = False
		all_items = item_controller.ItemController.items_list()
		for item in all_items:
			if item.name == "Gorilla Munch":
				success = True
		if not (success):
			self.fail("Failed to create item 'Gorilla Munch'")

	def testCannotCreateDuplicateItems(self):
		self.make_item()
		try:
			self.make_item()
			self.fail("Duplicate item creation was permitted!")
		except:
			# expected behavior
			pass

	def testCannotCreateItemWithInsaneQuantity(self):
		try:
			self.make_item(-37, "14.99")
			self.fail("Item creation with insane quantity was permitted!")
		except:
			# expected behavior
			pass

	def testItemUpdateQuantityIsSane(self):
		# test for negative quantities, etc.
		self.fail("implement me")

	def testCannotCreateItemWithInsanePrice(self):
		try:
			self.make_item(9001, "-40000")
			self.fail("Item creation with insane price was permitted!")
		except:
			# expected behavior
			pass

	def testItemUpdatePriceIsSane(self):
		# test for negative prices, etc.
		self.fail("implement me")

	def testItemAccessorsWhenItemDoesNotExist(self):
		# test:
		# - items_list
		# - item_get_info
		# - item_list_auctions ??
		self.fail("implement me")

	def testItemAccessorsWhenItemExists(self):
		# test:
		# - items_list
		# - item_get_info
		# - item_list_auctions ??
		self.fail("implement me")
