#!/usr/bin/env python
# -*- coding: utf-8 -*-

import controllers.item_controller as item_controller
import fixtures.dummy_items as dummy_items
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed

class ItemControllerTestCase(unittest.TestCase):
	itemName = "Gorilla Munch"

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def make_item(self, quantity=9001, price="14.99"):
		item_controller.ItemController.item_add(self.itemName,
			quantity, price, "http://thereisnoneed.com",
			"http://i.imgur.com/1jqAT.png")

	def testCreateItem(self):
		# verify the item doesn't exist
		all_items = item_controller.ItemController.items_list()
		for item in all_items:
			if item.name == self.itemName:
				self.fail("Impossible! Gorilla Munch already exists!")
				return

		# make the item
		self.make_item()

		# verify the item exists
		found = False
		all_items = item_controller.ItemController.items_list()
		for item in all_items:
			if item.name == self.itemName:
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
		self.make_item()

		try:
			item_controller.ItemController.item_update_quantity(self.itemName,
				-37)
			self.fail("Item update to insane quality was permitted!")
		except Exception, e:
			# expected behavior
			item_controller.ItemController.item_update_quantity(self.itemName,
				21)

	def testCannotCreateItemWithInsanePrice(self):
		try:
			self.make_item(9001, "-40000")
			self.fail("Item creation with insane price was permitted!")
		except:
			# expected behavior
			pass

	def testItemUpdatePriceIsSane(self):
		self.make_item()

		try:
			item_controller.ItemController.item_update_price(self.itemName,
				"-40000")
			self.fail("Item update to insane price was permitted!")
		except Exception, e:
			# expected behavior
			item_controller.ItemController.item_update_price(self.itemName,
				"23.99")

	def testItemAccessorsWhenItemDoesNotExist(self):
		emptyItems = item_controller.ItemController.items_list().get()
		if emptyItems is None:
			self.fail("Expected empty list but was None")
		self.assertEquals(0, len(emptyItems))

		nilItem = item_controller.ItemController.item_get_info("asdf")
		if nilItem is not None:
			self.fail("Expected no item with name 'asdf'")

		nilAuctions = item_controller.ItemController.item_list_auctions("asdf")
		if nilAuctions is None:
			self.fail("Expected empty list but was None")
		self.assertEquals(0, len(nilAuctions))

	def testItemAccessorsWhenItemExists(self):
		# make some fixture items
		dummy_items.DummyItems.setup()

		# test:
		# - items_list
		# - item_get_info
		# - item_list_auctions ??
		self.fail("implement me")
