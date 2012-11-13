#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template        

class AccountHandler(webapp.RequestHandler):
	def get(self):					
		self.response.out.write(
			template.render('../account.html', {}))
	def post(self):
		self.redirect('/')
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', AccountHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)
	
	
if __name__ == "__main__":
	main()