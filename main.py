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
	'/auction_detail', 'auction_detail',

	'/user_get_nonce', 'user_get_nonce',
	'/user_register', 'user_register',
	'/user_validate_email', 'user_validate_email',
	'/user_authenticate', 'user_authenticate',
	'/user_info', 'user_info',
	'/user_username_exists', 'user_username_exists',
	'/user_email_exists', 'user_email_exists',
	'/user_logout', 'user_logout'
)

# JSON objects passed back to the client use these keys
JSON_KEY_ID = "i"
JSON_KEY_PRICE = "p"
JSON_KEY_WINNER = "w"
JSON_KEY_REMAINING_TIME = "t"
JSON_KEY_IS_ACTIVE = "a"
JSON_KEY_ITEM_NAME = "n"
JSON_KEY_BASE_PRICE = "b"
JSON_KEY_PRODUCT_URL = "u"
JSON_KEY_IMAGE_URL = "m"


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
			auctions = auction_controller.auctions_status_by_id(auction_ids)

			# Build the JSON payload
			result = []
			delta = ""

			for elem in auctions:
				try:
					if not elem:
						continue

					delta = elem.auction_end - datetime.datetime.now()
					if delta.total_seconds() <= 0:
						delta = timedelta(seconds=0)
						elem.active = False
						elem.put()
						# TODO: Do winner stuff here... apparently our daemon hasn't gotten to this one.
						# note from Brent: I don't think this is the right place to handle winning auctions

					username = "No Bidders"
					if elem.current_winner:
						username = elem.current_winner.username

					price = "0.00"
					if elem.current_price:
						price = "{0:.2f}".format(elem.current_price)

					result.append({
						JSON_KEY_ID: str(elem.key().id()),
						JSON_KEY_PRICE: str(price),
						JSON_KEY_WINNER: str(username),
						JSON_KEY_REMAINING_TIME: str(delta.total_seconds()),
						JSON_KEY_IS_ACTIVE: str(elem.active)
					})
				except Exception, e:
					# TODO: Don't print raw exception messages, this is a security leak! See: http://cwe.mitre.org/data/definitions/209.html
					print e

			result_json = json.dumps({'result':auction_controller.auctions_status_by_id(inputs.ids)})
			return inputs.callback + "(" + result_json + ");"

		except Exception, e:
			# TODO: Don't print raw exception messages, this is a security leak! See: http://cwe.mitre.org/data/definitions/209.html
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class auctions_list_active:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			# Build the JSON payload
			result = []
			delta = ""

			for elem in auctions:
				try:
					if not elem:
						continue
					delta = elem.auction_end - datetime.datetime.now()

					username = "No Bidders"
					if elem.current_winner:
						username = elem.current_winner.username

					price = "0.00"
					if elem.current_price:
						price = "{0:.2f}".format(elem.current_price)

					result.append({
						JSON_KEY_ID: str(elem.key().id()),
						JSON_KEY_IS_ACTIVE: str(elem.active),	# Is Auction Active? "True" or "False"
						JSON_KEY_ITEM_NAME: str(elem.item.name),
						JSON_KEY_BASE_PRICE: str(elem.item.base_price),
						JSON_KEY_PRODUCT_URL: str(elem.item.product_url),
						JSON_KEY_IMAGE_URL: str(elem.item.image_url),
						JSON_KEY_PRICE: str(price),
						JSON_KEY_WINNER: str(username),
						JSON_KEY_TIME_REMAINING: str(delta.total_seconds())
						})
				except Exception, e:
					logging.error(str(e))

			result_json = json.dumps({'result':auction_controller.auctions_list_active(inputs.count)})
			return inputs.callback + "(" + result_json + ");"

		except Exception, e:
			# TODO: Don't print raw exception messages, this is a security leak! See: http://cwe.mitre.org/data/definitions/209.html
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

class auction_detail:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auction_detail(inputs.id)}
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

