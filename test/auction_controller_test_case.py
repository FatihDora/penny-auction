#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

import controllers.auction_controller as auction_controller
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed

class AuctionControllerTestCase(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def make_item(self):
		# make an item

		pass

	def make_auction(self):
		# using the item, make an auction
		pass
