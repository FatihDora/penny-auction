#!/usr/bin/env python

class user:
	def register:
		'''
			Register a new account
		'''
		return False

	def get_nonce:
		'''
			Get a random number, to be used only once, hence nonce ("Number used
			ONCE")
		'''
		return random.random()

	def login:
		'''
			Login to the API and return a hash which corresponds to the
			username, password, and salt
		'''
		def inputs = web.input()
		def salt1 = inputs.salt1

		return True

	def logout:
		'''
			Log out of the service
		'''
		return True

	def validate_email:
		'''
			 Validate the user's email
		'''
		return True
