PisoAuction = casper.PisoAuction

PisoAuction.test ->
	casper.test.comment "Testing user login"
	casper.then ->
		PisoAuction.login()
