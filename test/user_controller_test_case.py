#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		user_controller.UserController.create(first_name="test", last_name="user",
			username="testUser", email="testUser@me.com")
		user_object = user.User.get_by_username("testUser")
		self.assertNotEquals(None, user_object, "Failed to create User!")

	def test_failed_login(self):
		''' Test failed login.'''

		self.make_user()

		# instruct the user controller to fail this authentiation attempt
		user_controller.UserController._PERSONA_AUTH_URL = "mock:failure"

		request_parameters = {"assertion": "fake assertion"}
		expected_response = {"result": False, "username": None}
		cookie_jar = cookielib.CookieJar()
		reader = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
		encoded_request_parameters = urllib.urlencode(request_parameters)
		raw_response = reader.open("http://localhost:8080/persona_login?{}".format(encoded_request_parameters))
		actual_response = json.loads(raw_response.read())

		# check return value
		if actual_response != expected_response:
			self.fail(
				"""/persona_login did not return the expected value for an invalid login.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=expected_response,
					actual=actual_response
				)
			)

		# check that no session cookie was set
		for cookie in cookie_jar:
			if cookie.key == user_controller.UserController._COOKIE_NAME:
				self.fail("User logged in with invalid credentials and got a session cookie.")


	def test_successful_login(self):
		''' Test successful login with existing user. '''

		self.make_user()

		# instruct the user controller to pass this authentiation attempt
		user_controller.UserController._PERSONA_AUTH_URL = "mock:success:testUser@me.com"

		request_parameters = {"assertion": "fake assertion"}
		expected_response = {"result": True, "username": "testUser"}
		cookie_jar = cookielib.CookieJar()
		reader = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
		encoded_request_parameters = urllib.urlencode(request_parameters)
		raw_response = reader.open("http://localhost:8080/persona_login?{}".format(encoded_request_parameters))
		actual_response = json.loads(raw_response.read())

		# check return value
		if actual_response != expected_response:
			self.fail(
				"""persona_login() did not return the expected value for an expected successful login of pre-existing user.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=expected_response,
					actual=actual_response
				)
			)

		# check that the correct session cookie was set
		session_cookie = None
		for cookie in cookie_jar:
			if cookie.key == user_controller.UserController._COOKIE_NAME:
				session_cookie = cookie

		if not session_cookie:
			self.fail("User logged in with valid credentials but no session cookie was set.")

		db_cookie = UserCookie.all().filter("username", "testUser").get()
		if not db_cookie:
			self.fail("No session cookie was saved to the database for the intended user after a successful login.")
		session_token = db_cookie.token
		if session_token != session_cookie.value:
			self.fail(
				"""User logged in successfully but session cookie contents don't match session token.
				Expected: {expected!r}
				Actual: {actual!r}""".format(
					expected=session_token,
					actual=session_cookie.value
				)
			)


if __name__ == '__main__':
	unittest.main()
