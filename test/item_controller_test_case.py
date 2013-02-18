#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

import controllers.item_controller as item_controller
import unittest
from decimal import Decimal

from google.appengine.ext import db
from google.appengine.ext import testbed

class ItemControllerTestCase(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

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
		self.make_item(25, "14.99")
		theItem = item_controller.ItemController.item_get_info("Gorilla Munch")

		try:
			item_controller.ItemController.item_update_quantity("Gorilla Munch",
				-37)
			self.fail("Item update with insane quantity was permitted!")
		except:
			# expected behavior
			item_controller.ItemController.item_update_quantity("Gorilla Munch",
				41)

			# the old item reference quantity will still be the same
			self.assertEquals(25, theItem.quantity_in_stock)

			# new references to the item will have the new quantity
			theItem = item_controller.ItemController.item_get_info(
				"Gorilla Munch")
			self.assertAlmostEqual(41, theItem.quantity_in_stock)

	def testCannotCreateItemWithInsanePrice(self):
		try:
			self.make_item(9001, "-40000")
			self.fail("Item creation with insane price was permitted!")
		except:
			# expected behavior
			pass

	def testItemUpdatePriceIsSane(self):
		self.make_item(9001, "14.99")
		theItem = item_controller.ItemController.item_get_info("Gorilla Munch")

		try:
			item_controller.ItemController.item_update_price("Gorilla Munch",
				"-40000")
			self.fail("Item update with insane price was permitted!")
		except:
			# expected behavior
			item_controller.ItemController.item_update_price("Gorilla Munch",
				"12.99")

			# the old item reference price will still be the same
			self.assertAlmostEqual(Decimal(14.99), theItem.base_price)

			# new references to the item will have the new price
			theItem = item_controller.ItemController.item_get_info(
				"Gorilla Munch")
			self.assertAlmostEqual(Decimal(12.99), theItem.base_price)

	def testItemAccessorsWhenItemDoesNotExist(self):
		# - item_get_info
		nilItem = item_controller.ItemController.item_get_info("asdf")
		if nilItem is not None:
			self.fail("Expected no item with name 'asdf'")

		# - items_list
		emptyItems = item_controller.ItemController.items_list()
		if emptyItems is None:
			self.fail("Expected empty list of items, but was None")
		self.assertEquals(0, len(emptyItems))

		# - item_list_auctions
		try:
			nilAuctions = item_controller.ItemController.item_list_auctions(
				"asdf")
		except:
			# expected behavior
			pass

	def testItemAccessorsWhenItemExists(self):
		self.make_item()

		# - item_get_info
		oneItem = item_controller.ItemController.item_get_info("Gorilla Munch")
		if oneItem is None:
			self.fail("Expected item with name 'Gorilla Munch'")
		self.assertEquals("Gorilla Munch", oneItem.name)

		# - items_list
		oneItemList = item_controller.ItemController.items_list()
		if oneItemList is None:
			self.fail("Expected list of one item, but was None")
		self.assertEquals(1, len(oneItemList))
		self.assertEquals(oneItem, oneItemList[0])

		# - item_list_auctions
		try:
			nilAuctions = item_controller.ItemController.item_list_auctions(
				"Gorilla Munch")
			if nilAuctions is None:
				self.fail("Expected empty list of auctions, but was None")
			self.assertEquals(0, len(nilAuctions))
		except:
			# expected behavior
			pass
