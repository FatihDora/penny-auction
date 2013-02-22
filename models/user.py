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

from google.appengine.ext import db
import random
import sys
from models import insufficient_bids_exception
import logging

import lib.bcrypt.bcrypt as bcrypt


class User(db.Model):

	first_name = db.StringProperty(required=False)
	last_name = db.StringProperty(required=False)
	username = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	create_time = db.DateTimeProperty(auto_now_add=True)
	bid_count = db.IntegerProperty(default=0)
	token = db.StringProperty(required=False)
	token_create_time = db.DateTimeProperty(required=False)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'auctions_won' created by the Auction class
	# implicit property 'past_bids' created by the BidHistory class
	# implicit property 'available_bids' created by the BidPool class

	@staticmethod
	def get_by_username(username):
		return User.all().filter("username =", username).get()

	@staticmethod
	def get_by_email(email):
		return User.all().filter("email =", email).get()
	
	@staticmethod
	def get_by_token(token):
		'''
			Retrives the user model for the user with the given token, or None
			if no user has the given token or the given token is expired.
		'''
		# TODO: add expiration checking (24 hours is probably a reasonable expiration time)
		return User.all().filter('token =',token).get()

	@staticmethod
	def username_exists(username):
		q = User.all().filter('username = ', username)

		#Verify the user exists in the database
		return q.get() is not None

	@staticmethod
	def email_exists(email):
		q = User.all().filter('email = ', email)

		#Verify the email exists in the database
		return q.get() is not None

	def add_bids(self, number):
		'''
			Adds bids to this user's account. Prevents accidentally deducting
			bids instead of adding (due to bugs, malicious use, etc) by
			refusing to process negative bid numbers--invoke the use_bids()
			method instead to intentionally deduct bids from a user's account.
		'''

		number = int(number)

		if number < 0:
			raise Exception(
				'''Cannot add negative bids ({number}) to a user's account from
				the add_bids() method. Invoke the use_bids() method instead to
				use up bid in this user's account.'''.format(
					number = number
				)
			)

		self.bid_count += number
		self.put()
	
	def use_bids(self, number):
		'''
			Uses up an amount of this user's bids specified by the number
			parameter. Raises a InsufficientBidsException if the user doesn't
			have enough bids to use. Prevents accidentally adding bids instead
			of removing them (due to bugs, malicious use, etc) by refusing to
			process negative bid numbers--invoke the add_bids() method instead
			to intentionally add bids from a user's account.
		'''

		number = int(number)

		if number < 0:
			raise Exception(
				'''Cannot deduct negative bids ({num}) from a user's account from
				the use_bids() method. Invoke the add_bids() method instead to
				add bids to this user's account.'''.format(
					num = num
				)
			)

		if self.bid_count >= number:
			self.bid_count -= number
			self.put()
		else:
			raise insufficient_bids_exception.InsufficientBidsException(self, number)

	def create_session_token(self, secret):
		'''
			Creates a new session token for this user and returns the token.
		'''
		secret = self.username + secret
		self.token = bcrypt.hashpw(secret, bcrypt.gensalt())
		self.put()
		return self.token

	def destroy_session_token(self):
		'''
			Invalidates this user's session token, logging the user out.
		'''
		self.token = None

