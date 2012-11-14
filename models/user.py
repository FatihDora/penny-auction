#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from google.appengine.ext import db
import lib.bcrypt.bcrypt as bcrypt
import random
import sys


class User(db.Model):

	first_name = db.StringProperty(required=True)
	last_name = db.StringProperty(required=True)
	username = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	hashed_password = db.StringProperty(required=True)
	password_salt = db.StringProperty(required=True)
	create_time = db.DateTimeProperty(auto_now_add=True)
	email_validated = db.BooleanProperty(default=False)
	email_validation_code = db.IntegerProperty(required=True)
	bid_count = db.IntegerProperty(default=0)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'auctions_won' created by the Auction class
	# implicit property 'past_bids' created by the BidHistory class
	# implicit property 'available_bids' created by the BidPool class

	@staticmethod
	def get_by_username(username):
		return User.all().filter("username =", username).get()

	@staticmethod
	def compute_secure_hashes(user_name, password):
		'''
			Because storing a plain text password is terribly insecure, the
			User model only stores hashes and a salt. Use this method to
			generate the password salt, email validation code, and hashed
			password for a user, based on their user name and password. Returns
			a dict with properties "password_salt", "email_validation_code",
			and "hashed_password".
		'''

		password_salt = bcrypt.gensalt()
		email_validation_code = random.randint(32768, sys.maxint)
		hashed_password = bcrypt.hashpw(password + user_name, password_salt)

		return {
			"password_salt": password_salt,
			"email_validation_code": email_validation_code,
			"hashed_password": hashed_password
		}

	@staticmethod
	def username_exists(username):
		q = User.all().filter('username = ', username)

		#Verify the user exists in the database
		return (q.get() is None)

	@staticmethod
	def email_exists(email):
		q = User.all().filter('email = ', email)

		#Verify the email exists in the database
		if q.get() == None:
			return False
		else:
			return True

	@staticmethod
	def validate_email(code):
		if code is None:
			raise Exception ("Argument 'code' cannot be None")

		result = User.all().filter("email_validation_code =", unicode(code)).get()

		if result is None:
			raise Exception("Validation failed for code: " + unicode(code))

		result.email_validated = True
		result.put()

	def add_bids(sender, num):
		sender.bid_count += num
		sender.put()
	
	def use_bid(self, number):
		'''
			Uses up an amount of this user's bids specified by the number
			parameter. Raises a InsufficientBidsException if the user doesn't
			have enough bids to use.
		'''

		if self.bid_count >= number:
			self.bid_count -= number
			self.put()
		else:
			raise InsufficientBidsException(self, number)

