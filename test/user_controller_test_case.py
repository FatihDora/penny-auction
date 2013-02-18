#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

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
		user_controller.UserController.user_register("test", "user",
			"testUser", "testUser@me.com", "testPassword")
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

	def testUserCannotRegisterTwice(self):
		self.make_user()
		try:
			self.make_user()
			self.fail("Repeat registration was permitted!")
		except:
			# expected behavior
			pass

	def testUserUpdatePassword(self):
		self.make_user()

		# validate the password hash
		user_object = user.User.get_by_username("testUser")
		hashed_password = user_controller.UserController.user_hash_password(
			"testUser", "testPassword", user_object.password_salt)
		self.assertEquals(hashed_password, user_object.hashed_password)

		# change the password
		user_controller.UserController.user_update_password(user_object,
			"testNewPassword")

		# validate the new password hash
		new_hashed_password = user_controller.UserController.user_hash_password(
			"testUser", "testNewPassword", user_object.password_salt)
		self.assertEquals(new_hashed_password, user_object.hashed_password)

		# pull a new refrence to the user from the DB and re-validate the new
		# password hash
		dup_user_object = user.User.get_by_username("testUser")
		self.assertEquals(new_hashed_password, dup_user_object.hashed_password)

if __name__ == '__main__':
	unittest.main()
