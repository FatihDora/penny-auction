#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

import models.user as user
import controllers.user_controller as user_controller
import unittest

import lib.bcrypt.bcrypt as bcrypt
from lib import web

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
		user_controller.UserController.create(first_name="test", last_name="user",
			username="testUser", email="testUser@me.com")
		user_object = user.User.get_by_username("testUser")
		self.assertNotEquals(None, user_object, "Failed to create User!")

	def testPersonaAuthentication(self):
		self.make_user()

		# test failed login
		user_controller.UserController._PERSONA_AUTH_URL = "mock:failure"
		assertion = "fake assertion"
		expected_result = None
		actual_result = user_controller.UserController.persona_login(assertion)

		# check return value
		if actual_result != expected_result:
			self.fail(
				"""persona_login() did not return the expected value for an invalid login.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=expected_result,
					actual=actual_result
				)
			)

		# check that no session cookie was set
		if web.cookies().get(UserController._COOKIE_NAME):
			self.fail("User logged in with invalid credentials and got a session cookie set.")
		



		# test successful login with existing user
		user_controller.UserController._PERSONA_AUTH_URL = "mock:success:testUser@me.com"
		assertion = "fake assertion"
		expected_result = User.get_by_email("testUser@me.com")
		actual_result = user_controller.UserController.persona_login(assertion)

		# check return value
		if actual_result != expected_result:
			self.fail(
				"""persona_login() did not return the expected value for an expected successful login of pre-existing user.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=expected_result,
					actual=actual_result
				)
			)

		expected_cookie_contents = bcrypt.hashpw(assertion + "testUser@me.com", bcrypt.gensalt())
		actual_cookie_contents = web.cookies().get(UserController._COOKIE_NAME)
		if actual_cookie_conents is None:
			self.fail("User logged in with valid credentials but no session cookie was set.")
		elif cookie_contents != expected_cookie_contents:
			self.fail(
				"""User logged in successfully but session cookie contents don't match expected contents.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=expected_cookie_contents,
					actual=cookie_contents
				)
			)


if __name__ == '__main__':
	unittest.main()
