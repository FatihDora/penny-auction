#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        user_controller.user_register("testUser", "testUser@me.com",
                "testPassword")

    def testUserCannotRegisterTwice(self):
        self.make_user()
        try:
            self.make_user()
            self.fail("Repeat registration was permitted!")
        except:
            # expected behavior
            pass

    def testUserEmailExists(self):
        self.assertFalse(user_controller.user_email_exists("testUser@me.com"))

        self.make_user()
        self.assertTrue(user_controller.user_email_exists("testUser@me.com"))

    def testUserUsernameExists(self):
        self.assertFalse(user_controller.user_username_exists("testUser"))

        self.make_user()
        self.assertTrue(user_controller.user_username_exists("testUser"))

    def testUserUpdatePassword(self):
        self.make_user()

        # validate the password hash
        user_key = db.Key.from_path("User", "testUser")
        user_object = db.get(user_key)
        hashed_password = user_controller.user_hash_password("testUser",
            "testPassword", user_object.password_salt)
        self.assertEquals(hashed_password, user_object.hashed_password)

        # change the password
        user_controller.user_update_password(user_object, "testNewPassword")

        # validate the new password hash
        new_hashed_password = user_controller.user_hash_password("testUser",
            "testNewPassword", user_object.password_salt)
        self.assertEquals(new_hashed_password, user_object.hashed_password)

        # pull a new refrence to the user from the DB and re-validate the new
        # password hash
        dup_user_key = db.Key.from_path("User", "testUser")
        dup_user_object = db.get(dup_user_key)
        self.assertEquals(new_hashed_password, dup_user_object.hashed_password)

if __name__ == '__main__':
    unittest.main()
