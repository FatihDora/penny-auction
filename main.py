#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
from fixtures import dummy_users
from fixtures import dummy_items
from fixtures import dummy_bidtypes
from fixtures import dummy_auctions

from google.appengine.ext import db
from lib import web
import os
from django.utils import simplejson as json
import logging

from controllers import user_controller, auction_controller
import models.auction as auction
import models.autobidder as autobidder
import models.bid_history as bid_history
import models.bid_type as bid_type
import models.bid_type_value as bid_type_value
import models.item as item
import models.user as user

urls = (
	'/', 'index',
	'/reset_data', 'reset_data',

	'/autobidder_create', 'autobidder_create',
	'/autobidder_status', 'autobidder_status',
	'/autobidder_cancel', 'autobidder_cancel',
	'/autobidders_list', 'autobidders_list',
	'/autobidders_list_by_auction', 'autobidders_list_by_auction',
	
	'/auctions_status_by_id', 'auctions_status_by_id',
	'/auctions_list_active', 'auctions_list_active',
	'/auctions_list_all', 'auctions_list_all',
	'/auction_bid', 'auction_bid',

	'/user_get_nonce', 'user_get_nonce',
	'/user_register', 'user_register',
	'/user_validate_email', 'user_validate_email',
	'/user_authenticate', 'user_authenticate',
	'/user_info', 'user_info',
	'/user_username_exists', 'user_username_exists',
	'/user_email_exists', 'user_email_exists',
	'/user_logout', 'user_logout'
)

class index:
	def GET(self):
		return "index stub"

class autobidder_create:
	def GET(self):
		return "autobidder_create stub"

class autobidder_status:
	def GET(self):
		return "autobidder_status stub"

class autobidder_cancel:
	def GET(self):
		return "autobidder_cancel stub"

class autobidders_list:
	def GET(self):
		return "autobidders_list stub"

class autobidders_list_by_auction:
	def GET(self):
		return "autobidders_list_by_auction stub"


# AUCTIONS

class auctions_status_by_id:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auctions_status_by_id(inputs.ids)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class auctions_list_active:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auctions_list_active(inputs.count)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

# TODO: MOVE THIS TO THE ADMIN / PRIVATE API! -- HERE FOR TESTING
class auctions_list_all:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auctions_list_all()}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class auction_bid:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auction_bid(inputs.id)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"


# USER Stuff

class get_nonce:
	def GET(self):
		return user_controller.user_get_nonce()

class user_info:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':user_controller.user_info()}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class user_logout:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':user_controller.user_logout()}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"


class user_register:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:
			result = {'result':user_controller.user_register(inputs.first_name,inputs.last_name,inputs.username,inputs.email,inputs.password)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class user_validate_email:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:
			result = {'result':user_controller.user_validate_email(inputs.code)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class user_authenticate:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:
			result ={'result':user_controller.user_authenticate(inputs.username, inputs.password)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class user_authenticate_cookie:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')
		try:
			result ={'result':user_controller.user_authenticate_cookie()}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"


class user_username_exists:
	def GET(self):
		inputs = web.input()
		try:
			if not inputs.username:
				result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
				return inputs.callback + "(" + json.dumps(result) + ");"

			web.header('Content-Type', 'application/json')
			result ={'result':user_controller.user_username_exists(inputs.username)}
			return inputs.callback + "(" + json.dumps(result) + ");"
		except Exception, e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class user_email_exists:
	def GET(self):
		inputs = web.input()
		try:
			if not inputs.email:
				result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
				return inputs.callback + "(" + json.dumps(result) + ");"

			web.header('Content-Type', 'application/json')
			result ={'result':user_controller.user_email_exists(inputs.email)}
			return inputs.callback + "(" + json.dumps(result) + ");"
		except Exception, e:
			result = {'exception':'empty'} # Figure out a nicer way to handle exceptions
			return inputs.callback + "(" + json.dumps(result) + ");"

class reset_data:
	def GET(self):
		br = '<br/>'
		result = ""
		try :

			result += 'Loading Data...' + br
			dummy_users.DummyUsers.setup()
			dummy_items.DummyItems.setup()
			dummy_bidtypes.DummyBidTypes.setup()
			dummy_auctions.DummyAuctions.setup()
			result += 'Done...' + br


		except Exception, e:
			return str(e)

		return result


app = web.application(urls, globals())
application = app.gaerun()
if (os.getenv("APPLICATION_ID").startswith("dev~")):
	logging.getLogger().setLevel(logging.ERROR)

