PisoAuction = casper.PisoAuction

# define a registration shortcut
PisoAuction.register = (props, callback) ->
	casper.reload ->
		casper.fill "form#registration-form", props, false
		casper.click ".submit-review a.sub-hover"
		casper.waitUntilVisible "#registration-complete", callback
		, ->
			casper.test.error "Timeout occurred when registration was expected to succeed"
			casper.test.assertNotVisible "#registration-complete strong",
				"User registration email shouldn't be visible"
			casper.test.assertVisible "#messageDialog", "Message dialog shown"
			actualMessage = casper.fetchText "#messageDialog p"
			casper.test.error actualMessage

PisoAuction.test ->
	# register a valid account
	casper.then ->
		casper.test.comment "Testing successful user registration"
		casper.click "#register-link"
		casper.waitUntilVisible "form#registration-form", ->
			casper.test.assertTitle "Piso Auction - Register",
				"Check page title"

			email = "sumd00d@hotmail.com"
			PisoAuction.register
				"FirstName": "Some"
				"LastName": "Dude"
				"Username": "somed00d"
				"Email": email
				"Password": "asdf123"
				"termsandconditions": true
			, ->
				casper.test.info "Check registration successful"

				# check that the email address is displayed
				actualEmail = casper.fetchText "#registration-complete strong"
				casper.test.assertEquals actualEmail, email,
					"User should be displayed their own email address"
