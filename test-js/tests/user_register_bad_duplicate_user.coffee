PennyAuction = casper.PennyAuction

# define a registration shortcut
PennyAuction.register = (props, messageRegex) ->
	casper.reload ->
		casper.fill "form#registration-form", props, false
		casper.click ".submit-review a.sub-hover"
		casper.waitUntilVisible "#registration-complete", ->
			if messageRegex?
				casper.test.error "Registration was completed successfully, when it shouldn't have"
		, ->
			if messageRegex?
				PennyAuction.expectMessageRegex messageRegex
				casper.test.assertNotVisible "#registration-complete strong",
					"User registration email shouldn't be visible"
			else
				casper.test.error "Timeout occurred when registration was expected to succeed"

PennyAuction.registrationProperties = ->
	"FirstName": "Some"
	"LastName": "Dude"
	"Username": "somed00d"
	"Email": "sumd00d@hotmail.com"
	"Password": "asdf123"
	"termsandconditions": true

PennyAuction.test ->
	casper.then ->
		casper.test.comment "Testing bad user registration (duplicate user)"
		casper.click "#register-link"
		casper.waitUntilVisible "form#registration-form", ->
			casper.test.assertTitle "Piso Auction - Register",
				"Check page title"

	# first registration
	casper.then ->
		casper.test.comment "First registration"
		props = PennyAuction.registrationProperties()
		PennyAuction.register props, null

	# second registration
	casper.then ->
		casper.test.comment "Second registration (duplicate username)"
		props = PennyAuction.registrationProperties()
		PennyAuction.register props, /username already exists/

	# third registration
	casper.then ->
		casper.test.comment "Third registration (duplicate email)"
		props = PennyAuction.registrationProperties()
		props["Username"] = "a different, unique username"
		PennyAuction.register props, /email address has already been registered/
