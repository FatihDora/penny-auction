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

import models.user as user
import controllers.user_controller as user_controller

import lib.bcrypt.bcrypt as bcrypt

import unittest
import urllib
import urllib2
import cookielib
import json

from google.appengine.ext import db
from google.appengine.ext import testbed

class UserControllerTestCase(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()

	def tearDown(self):
		self.testbed.deactivate()

	def make_user(self):
		user_controller.UserController.create(first_name="test",
			last_name="user", username="testUser", email="testUser@me.com")
		user_object = user.User.get_by_username("testUser")
		self.assertNotEquals(None, user_object, "Failed to create User!")

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
