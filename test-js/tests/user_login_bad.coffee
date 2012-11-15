PisoAuction = casper.PisoAuction

PisoAuction.test ->
	# bad username/password
	casper.then ->
		casper.test.comment "Testing bad user login"
		#login
		PisoAuction.login "bad username", "bad password", ->
			PisoAuction.expectMessage "Invalid username or password"
			casper.test.assertNotVisible "ul#top-account-info", "Account info shouldn't be visible"
