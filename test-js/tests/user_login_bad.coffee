PennyAuction = casper.PennyAuction

PennyAuction.test ->
	# bad username/password
	casper.then ->
		casper.test.comment "Testing bad user login"
		#login
		PennyAuction.login "bad username", "bad password", ->
			PennyAuction.expectMessage "Invalid username or password"
