#!/usr/bin/env python
# -*- coding: utf-8 -*-

import models.auction as auction
from datetime import timedelta

from google.appengine.ext import db

def auctions_status_by_id(auction_ids):
	'''
		List the auctions specified
	'''
	where = ""
	ids = auction_ids.split(',')

	for id in ids:
		where += "'" +  id + "' or id = "

	where = where[:-9] # get rid of the last " or id = "

	q = db.gqlQuery("SELECT * FROM Auctions WHERE id = $1", where)
	auctions = q.get()

	result = "["
	for auction in auctions
	delta = datetime.now() - auction.auctionEnd
		result += "{'i':'"+ auction.id + "',"
				 + "'p':'" + auction.currentPrice + "',"
				 + "'w':'" + auction.currentWinner + "',"
				 + "'t':'" + delta.total_seconds() + "'},"

	return result[:-1] + "]"

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
