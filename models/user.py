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
	personal_information = db.StringProperty()
	email_validated = db.BooleanProperty(default=False)
	email_validation_code = db.StringProperty(required=True)
	bid_count = db.IntegerProperty(default=0)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'auctions_won' created by the Auction class
	# implicit property 'past_bids' created by the BidHistory class
	# implicit property 'available_bids' created by the BidPool class

	@staticmethod
	def get_by_username(username):
		return User.all().filter("username =", username).get()

	@staticmethod
	def create(first_name,last_name,username,email,password):
		if first_name is None:
			raise Exception("Arugment 'first_name' cannot be None")

		if last_name is None:
			raise Exception("Arugment 'last_name' cannot be None")

		if username is None:
			raise Exception("Arugment 'username' cannot be None")

		if email is None:
			raise Exception("Arugment 'email' cannot be None")

		if password is None:
			raise Exception("Arugment 'password' cannot be None")

		if User.username_exists(username):
			raise Exception("An account with this username already exists")

		if User.email_exists(email):
			raise Exception("An account with this email address already exists")

		salt = bcrypt.gensalt()
		email_validation_code = random.randint(32768, sys.maxint)
		pass_hash = bcrypt.hashpw(password + username, salt)
		user_object = User(key_name=username,
							first_name=first_name,
							last_name=last_name,
							username=username,
							hashed_password=pass_hash,
							password_salt=salt,
							email=email,
							email_validation_code=unicode(email_validation_code))
		user_object.put()
		return user_object

	@staticmethod
	def username_exists(username):
		q = User.all().filter('username = ', username)

		#Verify the user exists in the database
		if q.get() is None:
			return False
		else:
			return True

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

		if result.email_validated is True:
			raise Exception("Email already validated.")
		else:
			result.email_validated = True
			result.put()
			return True

	def add_bids(sender, num):
		sender.bid_count += num
		sender.put()
