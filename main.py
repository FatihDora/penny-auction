#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

from google.appengine.ext import db
from lib import web
import json

from controllers import user_controller

urls = (
	'/', 'index',
	'/create_auto_bidder', 'create_auto_bidder',
	'/get_auto_bidder_status', 'get_auto_bidder_status',
	'/cancel_auto_bidder', 'cancel_auto_bidder',
	'/list_auto_bidders_for_user', 'list_auto_bidders_for_user',
	'/list_auto_bidders_for_auction', 'list_auto_bidders_for_auction',

	'/get_nonce', 'get_nonce',
	'/user_register', 'register',
	'/user_authenticate', 'authenticate',
	'/user_username_exists', 'username_exists',
	'/user_email_exists', 'email_exists'
)


class index:
	def GET(self):
		return "index stub"

class create_auto_bidder:
	def GET(self):
		return "create_auto_bidder stub"

class cancel_auto_bidder:
	def GET(self):
		return "cancel_auto_bidder stub"

class list_auto_bidders:
	def GET(self):
		return "list_auto_bidder stub"

class get_auto_bidder_status:
	def GET(self):
		return "get_auto_bidder_status stub"

class list_auto_bidders_for_auction:
	def GET(self):
		return "list_auto_bidders_for_auction stub"



class get_nonce:
	def GET(self):
		return user_controller.user_get_nonce()

class register:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		
		try:
			result = {'result':user_controller.user_register(inputs.username, inputs.email, inputs.password)}
			return inputs.callback + "(" + json.dumps(result) + ");"
	
		except Exception as e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class authenticate:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:
			result ={'result':user_controller.user_authenticate(inputs.username, inputs.password)}
			return inputs.callback + "(" + json.dumps(result) + ");"
			
		except Exception as e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class username_exists:
	def GET(self):
		inputs = web.input()
		try:
			if not inputs.username:
				result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
				return inputs.callback + "(" + json.dumps(result) + ");"
				
			web.header('Content-Type', 'application/json')
			result ={'result':user_controller.user_username_exists(inputs.username)}
			return inputs.callback + "(" + json.dumps(result) + ");"
		except Exception as e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"
	
class email_exists:
	def GET(self):
		inputs = web.input()
		try:
			if not inputs.email:
				result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
				return inputs.callback + "(" + json.dumps(result) + ");"
				
			web.header('Content-Type', 'application/json')
			result ={'result':user_controller.user_email_exists(inputs.email)}
			return inputs.callback + "(" + json.dumps(result) + ");"
		except Exception as e:
			result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
			return inputs.callback + "(" + json.dumps(result) + ");"
		
app = web.application(urls, globals())
main = app.cgirun()

