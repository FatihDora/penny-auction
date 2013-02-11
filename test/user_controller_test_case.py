#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.user as user
import controllers.user_controller as user_controller
import unittest

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
		user_controller.UserController.create(firstName="test", lastName="user",
			username="testUser", email="testUser@me.com")
		user_object = user.User.get_by_username("testUser")
		self.assertNotEquals(None, user_object, "Failed to create User!")

	def testUserAuthenticate(self):
		self.make_user()

		# bad username
		try:
			user_controller.UserController.user_authenticate("fakeUser",
				"doesn't matter")
			self.fail("User permitted to login with bad username!")
		except:
			# expected behavior
			pass

		# bad password
		try:
			user_controller.UserController.user_authenticate("testUser",
				"bad password")
			self.fail("User permitted to login with bad password!")
		except:
			# expected behavior
			pass

# cannot run this part because the cookie cannot be set due to path resolution
# problems in web.py's setcookie function
#
#		# good login
#		user_hash = user_controller.UserController.user_authenticate("testUser",
#			"testPassword")
#		user_key = db.Key.from_path("User", "testUser")
#		user_object = db.get(user_key)
#		hashed_password = user_controller.UserController.user_hash_password(
#			"testUser", "testPassword", user_object.password_salt)
#		self.assertEquals(hashed_password, user_hash)
#		user_key = db.Key.from_path("User", "testUser")
#		user_object = db.get(user_key)
#		hashed_password = user_controller.UserController.user_hash_password(
#			"testUser", "testPassword", user_object.password_salt)

if __name__ == '__main__':
	unittest.main()
