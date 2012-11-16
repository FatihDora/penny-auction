PisoAuction = casper.PisoAuction

PisoAuction.test ->
	# bad username/password
	casper.then ->
		casper.test.comment "Testing bad user login"
		#login
		PisoAuction.login "bad username", "bad password", ->
			PisoAuction.expectMessage "Invalid username or password"
