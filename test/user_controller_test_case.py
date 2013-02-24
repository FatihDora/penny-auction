#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

import fixtures.dummy_items as dummy_items

import models.user as user
import controllers.auction_controller as auction_controller
import controllers.user_controller as user_controller

import unittest
from datetime import *

from google.appengine.ext import db
from google.appengine.ext import testbed

class UserControllerTestCase(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_taskqueue_stub(root_path=".")

	def tearDown(self):
		self.testbed.deactivate()

	def make_user(self):
		user_controller.UserController.create(first_name="test",
			last_name="user", username="testUser", email="testUser@me.com")
		user_object = user.User.get_by_username("testUser")
		self.assertNotEquals(None, user_object, "Failed to create User!")

	def testUserInfoWithNoAutoBidders(self):
		# create a user
		self.testCreateSuccess()
		the_user = user.User.get_by_username("testUser")

		# validate user info
		info = user_controller.UserController.user_info(the_user)
		self.assertEquals(info["username"], "testUser")
		self.assertEquals(info["bids"], 100)
		self.assertEquals(info["auto-bidders"], 0)

	def testUserInfoWithMultipleAutoBidders(self):
		# fixtures
		dummy_items.DummyItems.setup()

		# create 2 auctions
		mba_auction = auction_controller.AuctionController.create("MacBook Air",
			timedelta(seconds=10), timedelta(10))
		mbp_auction = auction_controller.AuctionController.create("MacBook Pro",
			timedelta(seconds=10), timedelta(10))

		# create a user
		self.testCreateSuccess()
		the_user = user.User.get_by_username("testUser")

		# make some auto-bidders (25 to Air, 20 to Pro)
		auction_controller.AuctionController.attach_autobidder(mba_auction.key().id(),
			the_user.username, 25)
		auction_controller.AuctionController.attach_autobidder(mbp_auction.key().id(),
			the_user.username, 20)

		# validate user info
		info = user_controller.UserController.user_info(the_user)
		self.assertEquals(info["username"], "testUser")
		self.assertEquals(info["bids"], 100)
		self.assertEquals(info["auto-bidders"], 2)

	def testCreateWithDuplicateUsername(self):
		self.testCreateSuccess()
		try:
			user_controller.UserController.create(first_name="test",
				last_name="user", username="testUser", email="tu@them.com")
			self.fail("Expected failure with duplicate username")
		except Exception, ex:
			pass

	def testCreateWithDuplicateEmail(self):
		self.testCreateSuccess()
		self.make_user()
		try:
			user_controller.UserController.create(first_name="test",
				last_name="user", username="them", email="testUser@me.com")
			self.fail("Expected failure with duplicate email")
		except Exception, ex:
			pass

	def testCreateSuccess(self):
		try:
			self.make_user()
		except Exception, ex:
			self.fail("Expected success creating user")

# cannot test, due to GAE sandbox limitations:
# -- user_controller._session_start
# -- user_controller.persona_login
# -- user_controller.user_logout
# -- user_controller.validate_cookie


if __name__ == '__main__':
	unittest.main()
