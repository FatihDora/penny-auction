#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from models import user, user_cookie
import lib.bcrypt.bcrypt as bcrypt
from lib import web
import logging

from google.appengine.ext import db
from google.appengine.api import mail

from datetime import datetime
import urllib
import json
import hashlib
import random
import sys

class UserController(object):

	COOKIE_NAME = "PISOAUTH"

	@staticmethod
	def _session_start(username, secret):
		'''
			Sets up a session for the current user. Username is the user name
			of the user that logged in and secret is the seed for generating
			the login token (this can be any string that an attacker shouldn't
			be able to guess, such as the password for password-based
			authentication or the Persona assertion if using Persona-based
			login).
		'''
		secret = username + secret
		token = bcrypt.hashpw(secret, bcrypt.gensalt())
		web.setcookie(UserController.COOKIE_NAME, token, 3600)
		user_cookie.UserCookie.create_cookie(username, token)

	@staticmethod
	def persona_login(assertion):
		'''
			Authenticate a user from their Persona assertion (generated
			client-side by the persona-login.coffee script) and start a session
			for them if their login is valid. The User model object for the
			user will be returned if login is successful, otherwise None will
			be returned.
		'''

		if not assertion:
			raise Exception("The assertion passed to UserController.persona_login() must be a non-empty string. Received {!r} instead.".format(assertion))

		# send a message with the assertion to Persona's servers to validate its authenticity
		message = urllib.urlencode(dict(audience=web.ctx.host, assertion=assertion))
		response = json.loads(urllib.urlopen("https://browserid.org/verify", message).read())

		# convert the status entry from a string to a more convenient boolean value
		response["status"] = response["status"] is not "failure"

		this_user = None
		if response["status"]:
			this_user = user.User.get_by_email(response["email"])
			if not this_user:
				# create this user if they don't exist yet
				this_user = UserController.create(email=response["email"])

			UserController._session_start(this_user.username, assertion)
		return this_user

	@staticmethod
	def user_info():
		'''
			This will be used to authenticate a user's cookie information.
		'''

		this_user = UserController.validate_cookie()
		if not this_user:
			raise Exception("Not logged in.")

		numBids = this_user.bid_count
		AutoBidders = this_user.active_autobidders.get()

		if AutoBidders is None:
			numAutoBidders = 0
		else:
			numAutoBidders = AutoBidders.size()

		return {'username':username,'bids':numBids,'auto-bidders':numAutoBidders}

	@staticmethod
	def user_logout():
		'''
			Log the current user out of their session with the server. Does
			nothing if the user has no current session.
		'''
		this_user = UserController.validate_cookie()
		if this_user:
			user_cookie.UserCookie.delete_all_cookies(this_user.username)

	@staticmethod
	def user_register(this_user, first_name=None, last_name=None, username=None):
		'''
			Register account information for a new user. Note that this user
			should already have an account skeleton from logging in with
			Persona (which gives us their email). Parameter this_user is the
			user model object for the user that should be modified, while the
			other parameters are the values that should be updated. All
			parameters except the user model object are optional.
		'''

		if username:
			this_user.username = username

		if first_name:
			this_user.first_name = first_name

		if last_name:
			this_user.last_name = last_name

		this_user.put()
		return this_user

	@staticmethod
	def validate_cookie():
		'''
			Checks the cookie sent by the client and returns the user model
			object for the logged-in user, or None if the user is not logged
			in.
		'''

		# Do they have a cookie?
		token = web.cookies().get(UserController.COOKIE_NAME)
		if token is None:
			return None
		# Validate.
		aCookie = user_cookie.UserCookie.validate_cookie(token)

		if aCookie is None:
			return None

		username = aCookie.username
		this_user = User.get_by_username(username)
		return this_user

	@staticmethod
	def create(email, username=None, first_name=None, last_name=None):
		'''
			Define a new user in the database. Returns the model object for the
			new user to allow method chaining. All arguments are optional
			except email. If a user name is not provided, then the email
			address will be used for the username.
		'''

		if not username:
			username = email

		new_user = user.User(
				first_name=first_name,
				last_name=last_name,
				username=username,
				email=email
		)
		new_user.put()
		return new_user

