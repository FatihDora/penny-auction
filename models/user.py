#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class User(db.Model):
	username = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	hashed_password = db.StringProperty(required=True)
	password_salt = db.StringProperty(required=True)
	create_time = db.DateTimeProperty(required=True)
	personal_information = db.StringProperty()
	email_validated = db.BooleanProperty(default=False)
	email_validation_code = db.StringProperty(required=True)
	# implicit property 'active_autobidders' created by the Autobidder class
	# implicit property 'auctions_won' created by the Auction class
	# implicit property 'past_bids' created by the BidHistory class
	# implicit property 'available_bids' created by the BidPool class
