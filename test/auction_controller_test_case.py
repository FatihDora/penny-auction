#!/usr/bin/env python
# -*- coding: utf-8 -*-

import controllers.auction_controller as auction_controller
import models.auction as auction
import fixtures.dummy_items as dummy_items
import fixtures.dummy_auctions as dummy_auctions
import unittest
import re
from datetime import timedelta

from google.appengine.ext import db
from google.appengine.ext import testbed

class AuctionControllerTestCase(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_taskqueue_stub(root_path=".")

		# fixtures
		dummy_items.DummyItems.setup()

	def tearDown(self):
		self.testbed.deactivate()

	# shortcut for creating a valid auction
	def make_valid_auction(self):
		return auction_controller.AuctionController.create("MacBook Pro",
			timedelta(seconds=10), timedelta(10))

	def testAuctionCreationWhenItemDoesntExist(self):
		try:
			auction_controller.AuctionController.create("Fake item",
				timedelta(seconds=60000), timedelta(seconds=10))
			self.fail("Auction creation with fake item permitted!")
		except Exception, e:
			# expected behavior
			assert re.search("no item exists", str(e), re.IGNORECASE)

	def testAuctionCreationWhenStartDelayInvalid(self):
		try:
			auction_controller.AuctionController.create("MacBook Pro",
				timedelta(-4300), timedelta(seconds=10))
			self.fail("Auction creation with invalid start_delay permitted!")
		except Exception, e:
			# expected behavior
			assert re.search("start_delay", str(e), re.IGNORECASE)
			assert re.search("must be a positive", str(e), re.IGNORECASE)

	def testAuctionCreationWhenBidPushbackInvalid(self):
		try:
			auction_controller.AuctionController.create("MacBook Pro",
				timedelta(60000), timedelta(-1289))
			self.fail(
				"Auction creation with invalid bid_pushback_time permitted!")
		except Exception, e:
			# expected behavior
			assert re.search("bid_pushback_time", str(e), re.IGNORECASE)
			assert re.search("must be a positive", str(e), re.IGNORECASE)

	def testAuctionCreationWhenValid(self):
		the_auction = self.make_valid_auction()
		auction_copy = auction.Auction.get(the_auction.key())
		self.assertEquals(the_auction, auction_copy)

# test auction_controller.AuctionController.auctions_status_by_ids(auction_ids)
# -- when no ids are specified
# -- when the id list doesn't parse
# -- when more than 40 ids are specified
# -- when some of the ids specified don't exist
# -- successful auctions statuses

# test auction_controller.AuctionController.auctions_list_current(count)
# -- when no auctions exist
# -- when no auctions are "current"
# -- successful current auctions list

# test auction_controller.AuctionController.auctions_list_all()
# -- when no auctions exist
# -- successful auctions list

# test auction_controller.AuctionController.auction_bid(auction_id, username)
# -- when user doesn't exist
# -- (maybe) when user isn't authorized to bid
# -- when user doesn't have enough bids
# -- when auction id isn't an integer
# -- when auction doesn't exist
# -- when auction is not active
# -- when auction has ended
# -- successful bid

# test auction_controller.AuctionController.auction_detail(auction_id)
# -- not implemented

# test auction_controller.AuctionController.attach_autobidder(auction_id,
#	user_name, num_bids)
# -- when user doesn't exist
# -- (maybe) when user isn't authorized to bid
# -- when user doesn't have enough bids
# -- when auction id isn't an integer
# -- when auction doesn't exist
# -- when auction is not active
# -- when auction has ended
# -- successful autobidder attach
