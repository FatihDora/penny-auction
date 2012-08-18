#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidHistory(db.Model):
    id = db.IntegerProperty(required=True)
    # implicit property 'auctions' created by the Auction class
    # implicit property 'users' created by the Auction class

