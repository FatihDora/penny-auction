#!/usr/bin/env python
# -*- coding: utf-8 -*-

import controllers.user_controller as user_controller
import unittest

from google.appengine.ext import db
from google.appengine.ext import testbed

class UserControllerTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
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

if __name__ == '__main__':
    unittest.main()
