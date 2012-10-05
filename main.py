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
import json

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
	'/create_auto_bidder', 'create_auto_bidder',
	'/get_auto_bidder_status', 'get_auto_bidder_status',
	'/cancel_auto_bidder', 'cancel_auto_bidder',
	'/list_auto_bidders_for_user', 'list_auto_bidders_for_user',
	'/list_auto_bidders_for_auction', 'list_auto_bidders_for_auction',
	
	'/auctions_status_by_id', 'auctions_status_by_id',
	'/auctions_list_active', 'auctions_list_active',

	'/get_nonce', 'get_nonce',
	'/user_register', 'register',
	'/user_authenticate', 'authenticate',
	'/user_username_exists', 'username_exists',
	'/user_email_exists', 'email_exists',

	'/reset_data', 'reset_data'
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

# AUCTIONS

class auctions_status_by_id:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auctions_status_by_id(inputs.ids)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception as e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"

class auctions_list_active:
	def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			result = {'result':auction_controller.auctions_list_active(inputs.count)}
			return inputs.callback + "(" + json.dumps(result) + ");"

		except Exception as e:
			return inputs.callback + "(" + json.dumps({'exception':str(e)}) + ");"




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

class reset_data:
	def GET(self):
		br = '<br/>'
		try :

			result = 'Preparing Database...' + br
			# Clear Database
			result += '&gt; Deleting Auctions: ' + str(db.delete(auction.Auction.all())) + br
			result += '&gt; Deleting Auto Bidders: ' + str(db.delete(autobidder.Autobidder.all())) + br
			result += '&gt; Deleting Bid History: ' + str(db.delete(bid_history.BidHistory.all())) + br
			result += '&gt; Deleting Bid Types: ' + str(db.delete(bid_type.BidType.all())) + br
			result += '&gt; Deleting Bid Value: ' + str(db.delete(bid_type_value.BidTypeValue.all())) + br
			result += '&gt; Deleting Items: ' + str(db.delete(item.Item.all())) + br
			result += '&gt; Deleting Users: ' + str(db.delete(user.User.all())) + br
			result += '... Done.' + br + br

			result += 'Loading Data...' + br


		except Exception as e:
			result = result + str(e)

		return result

app = web.application(urls, globals())
main = app.cgirun()
if (os.getenv("APPLICATION_ID").startswith("dev~")):
	dummy_users.DummyUsers.setup()
	dummy_items.DummyItems.setup()
	dummy_bidtypes.DummyBidTypes.setup()
	dummy_auctions.DummyAuctions.setup()
