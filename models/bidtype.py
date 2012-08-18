#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class BidType(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty()
    # implicit property 'active_autobidders' created by the Autobidder class

