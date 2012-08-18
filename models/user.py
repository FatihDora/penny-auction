#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class User(db.Model):
    id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    hashed_password = db.StringProperty(required=True)
    password_salt = db.StringProperty(required=True)
    create_time = db.DateTimeProperty(required=True)
    personal_information = db.StringProperty()
    # implicit property 'active_autobidders' created by the Autobidder class
    # implicit property 'auctions' created by the Auction class
