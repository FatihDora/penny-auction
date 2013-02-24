#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# © 2013
# main author: Kevin Mershon
################################################################################

# make Python do floating-point division by default
from __future__ import division
# make string literals be Unicode strings
from __future__ import unicode_literals

from google.appengine.ext import db
import datetime

class TimedeltaProperty(db.Property):
	data_type = datetime.timedelta

	def get_value_for_datastore(self, model_instance):
		value = self.__get__(model_instance, model_instance.__class__)
		if value is not None:
			return value.total_seconds()

	def make_value_from_datastore(self, value):
		if value is not None:
			return datetime.timedelta(seconds=value)

