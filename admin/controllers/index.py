#!/usr/bin/env python
# -*- coding: utf-8 -*-

# make Python do floating-point division by default
from __future__ import division

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template 
import simplejson as json
import logging

class IndexHandler(webapp.RequestHandler):
	def get(self):					
		self.response.out.write(
			template.render('../index.html', {}))
	def post(self):
		self.redirect('/')

def main():
	app = webapp.WSGIApplication([(r'.*', IndexHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()
