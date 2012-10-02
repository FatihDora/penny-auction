#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.auction as auction

from google.appengine.ext import db

def auctions_by_id(ids):
	'''
		List the auctions specified
	'''
	pass

def auctions_list_active():
	'''
		List the currently-running auctions
	'''
	pass

def auctions_list_all():
	'''
		List all auctions (administrative only)
	'''
	pass

def auction_create(item, scheduled_start_date):
	'''
		Schedule an auction for the specified item on the specified start date
		(administrative only)
	'''
	pass

def auction_start(auction_id):
	'''
		Start the specified auction, effective immediately (administrative only)
	'''
	pass

def auction_pause(auction_id):
	'''
		Pause the specified auction indefinitely (administrative only)
	'''
	pass

def auction_end(auction_id):
	'''
		End the specified auction (administrative only)
	'''
	pass

def auction_assign_winner(auction_id, username):
	'''
		Assign the specified user as the winner of the specified auction
		(administrative only)
	'''
	pass
