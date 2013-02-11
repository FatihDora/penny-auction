#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script passes all currently live auctions to the template.
The template renders the HTML with "loading"                
'''

import os
from google.appengine.ext import webapp2
from google.appengine.ext.webapp import template        

class HomeHandler(webapp2.RequestHandler):
	def get(self):		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

		#self.response.out.write(
		#	template.render('../index.html', {}))
	def post(self):
		self.redirect('/')
	
app = webapp2.WSGIApplication([('/', HomeHandler)])
	
