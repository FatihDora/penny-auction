#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from fixtures import dummy_users
from fixtures import dummy_items
from fixtures import dummy_auctions

from google.appengine.ext import db
from google.appengine.ext.webapp import template
from lib import web
import os
from django.utils import simplejson as json
import logging
import datetime
from datetime import timedelta

from controllers import user_controller, auction_controller
import models.auction
import models.bid_history as bid_history
import models.item as item
import models.user as user

urls = (
    '/reset_data', 'reset_data',

    '/', 'index',
    '/account','account',
    '/account/auto_bidders','account_auto_bidders',
    '/account/bidding_history','account_bidding_history',
    '/auction/.*','auction',
    '/bid_packs','bid_packs',
    '/checkout','checkout',
    '/forgot_credentials','forgot_credentials',
    '/register','register',
    '/support','support',
    '/validate_email','validate_email',
    '/winners','winners',
    
    '/autobidders_list_all', 'autobidders_list_all',
    '/autobidders_list_by_auction', 'autobidders_list_by_auction',

    '/auctions_status_by_id', 'auctions_status_by_id',
    '/auctions_list_current', 'auctions_list_current',
    '/auctions_list_all', 'auctions_list_all',
    '/auction_bid', 'auction_bid',
    '/auction_detail', 'auction_detail',
    '/auction_recent_bids', 'auction_recent_bids',
	'/auction_add_pending_bids', 'auction_add_pending_bids',
	'/auction_get_pending_bids_for_user', 'auction_get_pending_bids_for_user',
	'/auction_cancel_pending_bids_for_user', 'auction_cancel_pending_bids_for_user',
	'/auction_add_pending_bids_for_user', 'auction_add_pending_bids_for_user',
	'/auction_remove_pending_bids_for_user', 'auction_remove_pending_bids_for_user',

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
JSON_KEY_ID = "id"
JSON_KEY_PRICE = "price"
JSON_KEY_WINNER = "winner"
JSON_KEY_REMAINING_TIME = "time_left"
JSON_KEY_IS_ACTIVE = "active"
JSON_KEY_ITEM_NAME = "name"
JSON_KEY_BASE_PRICE = "base_price"
JSON_KEY_PRODUCT_URL = "product_url"
JSON_KEY_IMAGE_URL = "image_url"


'''
    begin Webclient
'''
class index:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/index.html')
        return template.render(path, {})

class account:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/account.html')
        return template.render(path, {})

class account_bidding_history:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/bidding_history.html')
        return template.render(path, {})

class account_auto_bidders:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/auto_bidders.html')
        return template.render(path, {})

class auction:
    def GET(self):
        auction_id = web.ctx.path.replace("/auction/","")
        path = os.path.join(os.path.dirname(__file__), 'webclient/auction.html')
        return template.render(path, {'id':auction_id})

class bid_packs:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/bid_packs.html')
        return template.render(path, {})

class checkout:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/checkout.html')
        return template.render(path, {})

class forgot_credentials:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/forgot_credentials.html')
        return template.render(path, {})

class register:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/register.html')
        return template.render(path, {})

class support:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/support.html')
        return template.render(path, {})

class validate_email:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/validate_email.html')
        return template.render(path, {})

class winners:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'webclient/winners.html')
        return template.render(path, {})


        

'''
    end Webclient
'''


class autobidders_list_all:
    def GET(self):
        return "autobidders_list_all stub"

class autobidders_list_by_auction:
    def GET(self):
        return "autobidders_list_by_auction stub"


# AUCTIONS

class auctions_status_by_id:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            auctions = auction_controller.AuctionController.auctions_status_by_ids(inputs.ids)

            # Build the JSON payload
            result = []
            delta = ""
            count = 0

            for elem in auctions:
                count += 1

                if not elem:
                    continue
                delta = elem.auction_end - datetime.datetime.now()
                if delta.total_seconds() <= 0:
                    delta = timedelta(seconds=0)

                username = "No Bidders"
                if elem.current_winner:
                    username = elem.current_winner.username

                price = "{0:.2f}".format(elem.current_price)

                result.append({
                    JSON_KEY_ID: unicode(elem.key().id()),
                    JSON_KEY_PRICE: unicode(price),
                    JSON_KEY_WINNER: unicode(username),
                    JSON_KEY_REMAINING_TIME: unicode(delta.total_seconds()),
                    JSON_KEY_IS_ACTIVE: unicode(elem.active)
                })

            return json.dumps({'result': result})

        except Exception, e:
    		# TODO: Don't print raw exception messages, this is a security leak! See: http://cwe.mitre.org/data/definitions/209.html
    		return json.dumps({'exception':unicode(e)})

class auctions_list_current:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            auctions = auction_controller.AuctionController.auctions_list_current(inputs.count)

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
                        JSON_KEY_ID: unicode(elem.key().id()),
                        JSON_KEY_IS_ACTIVE: unicode(elem.active),   # Is Auction Active? "True" or "False"
                        JSON_KEY_ITEM_NAME: unicode(elem.item.name),
                        JSON_KEY_BASE_PRICE: unicode(elem.item.base_price),
                        JSON_KEY_PRODUCT_URL: unicode(elem.item.product_url),
                        JSON_KEY_IMAGE_URL: unicode(elem.item.image_url),
                        JSON_KEY_PRICE: unicode(price),
                        JSON_KEY_WINNER: unicode(username),
                        JSON_KEY_REMAINING_TIME: unicode(delta.total_seconds())
                    })
                except Exception, e:
                    logging.error(unicode(e))
                    json.dumps({'error': unicode(e)})


            return json.dumps({'result': result})

        except Exception, e:
            # TODO: Don't print raw exception messages, this is a security leak! See: http://cwe.mitre.org/data/definitions/209.html
            return json.dumps({'exception':unicode(e)})

class auctions_list_all:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        # TODO: check that an administrative user issued this request

        try:
            auctions = auction_controller.AuctionController.auctions_list_all()

            # Build the JSON payload
            result = []
            delta = ""

            for elem in auctions:
                try:
                    if not elem:
                        continue
                    delta = elem.auction_end - datetime.datetime.now()

                    result.append({
                        JSON_KEY_ID: unicode(elem.key().id()),
                        JSON_KEY_IS_ACTIVE: unicode(elem.active),   # Is Auction Active? "True" or "False"
                        JSON_KEY_ITEM_NAME: unicode(elem.item.name),
                        JSON_KEY_BASE_PRICE: unicode(elem.item.base_price),
                        JSON_KEY_PRODUCT_URL: unicode(elem.item.product_url),
                        JSON_KEY_IMAGE_URL: unicode(elem.item.image_url),
                        JSON_KEY_PRICE: unicode(elem.current_price),
                        JSON_KEY_WINNER: unicode(elem.current_winner.username),
                        JSON_KEY_TIME_REMAINING: unicode(delta.total_seconds())
                    })
                except Exception, e:
                    logging.error(unicode(e))

            return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_bid:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            username = user_controller.UserController.validate_cookie()

            if username is None:
                raise Exception("Not logged in!")

            result = auction_controller.AuctionController.auction_bid(inputs.id, username)

            return json.dumps({'result': result})

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_detail:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        # STUB:
        ad = []
        ad.append({'id':inputs.id,
                        'name':'test auction',
                        'base_price':'58.91',
                        'product_url':'http://www.google.com',
                        'image_url':'http://www.randomwebsite.com/images/head.jpg',
                        'price':'2.05',
                        'winner':'darin',
                        'time_of_bid':'14:39:58',
                        'time_left':'8'})
        return json.dumps({'result':ad}) 
        



        try:
            result = {'result':auction_controller.AuctionController.auction_detail(inputs.id)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class auction_recent_bids:
    def GET(self):
        inputs = web.inputs
        web.header('Content-Type', 'application/json')

        ad = []
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:58'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:52'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:47'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:44'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:40'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:33'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:32'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:29'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:24'})
        ad.append({'username':'darin','price':'2.05','time_of_bid':'14:39:21'})
        return json.dumps({'result':ad}) 

class auction_add_pending_bids:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		result = auction_controller.AuctionController.attach_autobidder(
				auction_id=int(inputs.auction_id),
				user_name=inputs.user_name,
				num_bids=inputs.num_bids
		)
		return json.dumps({'result': unicode(result)})

class auction_get_pending_bids_for_user:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		result = auction_controller.AuctionController.get_autobidder_remaining_bids(
				auction_id=int(inputs.auction_id),
				user_name=inputs.user_name
		)
		return json.dumps({'result': unicode(result)})

class auction_cancel_pending_bids_for_user:
    def GET(self):
        return "auction_cancel_pending_bids_for_user stub"

class auction_add_pending_bids_for_user:
    def GET(self):
        return "auction_add_pending_bids_for_user stub"

class auction_remove_pending_bids_for_user:
    def GET(self):
        return "auction_remove_pending_bids_for_user stub"

# USER Stuff

class user_info:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            result = {'result':user_controller.UserController.user_info()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_logout:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
            result = {'result':user_controller.UserController.user_logout()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})


class user_register:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result = {'result':user_controller.UserController.user_register(inputs.first_name,inputs.last_name,inputs.username,inputs.email,inputs.password)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_validate_email:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result = {'result':user_controller.UserController.user_validate_email(inputs.code)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_authenticate:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result ={'result':user_controller.UserController.user_authenticate(inputs.username, inputs.password)}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_authenticate_cookie:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')
        try:
            result ={'result':user_controller.UserController.user_authenticate_cookie()}
            return json.dumps(result)

        except Exception, e:
            return json.dumps({'exception':unicode(e)})


class user_username_exists:
    def GET(self):
        inputs = web.input()
        web.header('Content-Type', 'application/json')

        try:
			if not inputs.username:
				raise Exception('required string parameter "username" was not passed to the server, or was an empty string')

			result = user_controller.UserController.user_username_exists(inputs.username)
			return json.dumps({'result': result})
        except Exception, e:
            return json.dumps({'exception':unicode(e)})

class user_email_exists:
    def GET(self):
		inputs = web.input()
		web.header('Content-Type', 'application/json')

		try:
			if not inputs.email:
				raise Exception('required string parameter "email" was not passed to the server, or was an empty string')

			result = user_controller.UserController.user_email_exists(inputs.email)
			return json.dumps({'result': result})
		except Exception, e:
			return json.dumps({'exception':unicode(e)})

class reset_data:
    def GET(self):
		br = '<br/>'
		result = ""
		result += 'Loading Data...' + br
		dummy_users.DummyUsers.setup()
		dummy_items.DummyItems.setup()
		dummy_auctions.DummyAuctions.setup()
		result += 'Done...' + br

		return result


app = web.application(urls, globals())
application = app.gaerun()
if (os.getenv("APPLICATION_ID").startswith("dev~")):
    logging.getLogger().setLevel(logging.ERROR)

