#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
import cgi
import cgitb     #this...
cgitb.enable()   #..and this are not really necessary but helps debuging


class Api_Handler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Not Implemented')
	def post(self):
		data= cgi.FieldStorage()
		if (username == 'darin' and password == 'letmein'):
			self.response.out.write('Success!')
		else
			self.response.out.write('Failure!')
	
	
def main():
	app = webapp.WSGIApplication([
	  (r'.*', Api_Handler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)


if __name__ == '__main__':
	main()