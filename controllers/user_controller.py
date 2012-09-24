#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.user as user
import lib.bcrypt.bcrypt as bcrypt

from google.appengine.ext import db
from datetime import datetime
import hashlib
import random
import sys

def user_get_nonce():
	'''
		Get a random number, to be used only once, hence nonce ("Number used
		ONCE")
	'''
	return random.randint(32768, sys.maxint)

def user_authenticate(username, password):
	'''
		Login to the API and return a hash which corresponds to the
		username, password, and salt
	'''
	user_key = db.Key.from_path("User", username)
	u = db.get(user_key)

	# Verify the user exists in the database
	if not user_username_exists(username):
		raise Exception("Invalid username or password!")

	# Verify the username/password combination (including the user's password
	# salt) matches the hashed password currently stored to the user object
	hashed_password = user_hash_password(username, password, u.password_salt)
	if hashed_password != u.hashed_password:
		raise Exception("Invalid username or password")

<<<<<<< HEAD
	# TODO: Create a hash that uniquely identifies a user.	This will be stored
	#		in a cookie.  The auth hash will be used to authenticate the user in
	#		future requests.  For now, I'm using the user's username.
	# http://webpy.org/cookbook/cookies
	web.setcookie('pisoauction', u.username, 3600)
	return u.hashed_password

def user_authenticate_hash(authhash):
	'''
		This will be used to authenticate a user auth-hash.  This hash is generated
		by the user_authentication() method and is stored in a cookie for user
		requests.
	'''

	# TODO: We are currently using the user's username as the hash until a new
	#		hashing method is built.
	username = hash_to_username(authhash)
	user_key = db.Key.from_path("User",username)

	if not user_key:
		raise Exception("Invalid hash.")

	return username
=======
	# TODO: Create a hash that uniquely identifies a user.	This will be stored
	#		in a cookie.  The auth hash will be used to authenticate the user in
	#		future requests.  For now, I'm using the user's username.
	# http://webpy.org/cookbook/cookies
	web.setcookie('pisoauction', u.username, 3600)
	return u.hashed_password

def user_authenticate_hash(authhash):
	'''
		This will be used to authenticate a user auth-hash.  This hash is generated
		by the user_authentication() method and is stored in a cookie for user
		requests.
	'''

	# TODO: We are currently using the user's username as the hash until a new
	#		hashing method is built.
	username = hash_to_username(authhash)
	user_key = db.Key.from_path("User",username)

	if not user_key:
		raise Exception("Invalid hash.")

	return username
>>>>>>> models

def user_register(username, email, password):
	'''
		Register a new account
	'''
	if user_username_exists(username):
		raise Exception("Another account already exists with this username!")

	if user_email_exists(email):
		raise Exception("Another account already exists with this email!")

	# create a new user and hash their password
	user_object = user.User(key_name=username,
			username=username, email=email, create_time=datetime.now())
	user_update_password(user_object, password)
	user_object.put()

	# return the new username
	return username

def user_update_password(user_object, new_password):
	'''
		Update the specified user to now have the specified salt. Also,
		recompute a random password salt
	'''
	# compute a new salt for the user
	new_salt = bcrypt.gensalt()

	# compute the new password hash using the new salt
	user_object.hashed_password = user_hash_password(user_object.username,
			new_password, new_salt)
	user_object.password_salt = new_salt
	user_object.put()

def user_hash_password(username, password, salt):
	'''
		Generate a password hash based on the provided username, password, and
		salt
	'''
	# compute the new password hash using the new salt
	return bcrypt.hashpw(password + username, salt)

def user_username_exists(username):
	'''
		Check to see if the given username exists in the database.
	'''
	user_key = db.Key.from_path("User", username)
	u = db.get(user_key)

	#Verify the user exists in the database
	if u == None:
		return False
	else:
		return True

def user_email_exists(email):
	'''
		Check to see if the given email address exists in the database.
	'''
	q = user.User.all().filter('email =', email)

	# Verify the email exists in the database
	if q.get() == None:
		return False
	else:
		return True

def hash_to_username(userhash):
	'''
		Converts the user hash to a username (the user key)
	'''

	# TODO: ReWrite this to actually do something.	Since the hash is currently the
	#		username, there's nothing to do.

	return userhash
