#!/usr/bin/env python
# -*- coding: utf-8 -*-

import controllers.auction_controller as auction_controller
import models.auction as auction
import random
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
		self.assertEquals(auction_copy, the_auction)

	def testAuctionsStatusesByIdsWhenNoIdsSpecified(self):
		auctions = auction_controller.AuctionController.auctions_status_by_ids(
			None)
		self.assertEquals(auctions, None)

	def testAuctionsStatusesByIdsWhenIdListIsCorrupt(self):
		try:
			auction_controller.AuctionController.auctions_status_by_ids(
				"this is not a numeric list")
		except Exception, e:
			# expected behavior
			assert re.search("could not be parsed", str(e), re.IGNORECASE)

	def testAuctionsStatusesByIdsWhenMoreThan40IdsSpecified(self):
		ids = ",".join(str(x) for x in range(41))
		try:
			auction_controller.AuctionController.auctions_status_by_ids(ids)
			self.fail("Aution statuses retrieved for more than 40 ids!")
		except Exception, e:
			# expected behavior
			assert re.search("too many ids", str(e), re.IGNORECASE)

	def testAuctionsStatusesByIdsWhenSomeIdsDontExist(self):
		# create some valid auctions
		dummy_auctions.DummyAuctions.setup()

		# fetch 10 valid auctions, and shuffle their order
		valid_auctions = auction.Auction.all().fetch(10)
		good_ids = list(int(a.key().id())
			for a in valid_auctions)

		# fudge half the numbers to be invalid
		bad_ids = []
		for x in range(10):
			bad_ids.insert(x, random.randint(101,200))

		# merge the lists and randomize the order
		auction_ids = good_ids + bad_ids
		random.shuffle(auction_ids)

		# verify that only the good ids were returned
		ids_list = ",".join(str(x) for x in auction_ids)
		valid_auctions = auction_controller.AuctionController.auctions_status_by_ids(ids_list)
		valid_auction_ids = sorted(list(int(x.key().id())
			for x in valid_auctions))
		self.assertEquals(valid_auction_ids, good_ids)

	def testAuctionsStatusesByIdsWhenAllIdsExist(self):
		# create some valid auctions
		dummy_auctions.DummyAuctions.setup()

		# fetch 10 valid auctions and randomize the order
		valid_auctions = auction.Auction.all().fetch(10)
		good_ids = list(int(a.key().id())
			for a in valid_auctions)
		random.shuffle(good_ids)

		# verify that all Auctions requested were returned
		ids_list = ",".join(str(x) for x in good_ids)
		valid_auctions = auction_controller.AuctionController.auctions_status_by_ids(ids_list)
		valid_auction_ids = list(int(x.key().id())
			for x in valid_auctions)
		self.assertEquals(sorted(valid_auction_ids), sorted(good_ids))

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
