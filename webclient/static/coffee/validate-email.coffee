################################################################################
# © 2013
# main author: Darin Hoover
################################################################################

$(document).ready ->
	validate_email.init()

	# End $(document).ready

validate_email = init: ->
		#------------------#
		# Email Validation #
		#------------------#
		
		# Find a better way to determine if we're on /validate_email page.
		if $("div#validate-email")?
			code = getParameterByName 'code'
			jQuery.ajax
				url: VALIDATE_EMAIL
				data: {code: code}
				success: (data) ->
					$("div#validate-email div#please-wait").hide()

					if data.exception
						$("#validation-error h2").text data.exception
						$("#validation-error").fadeIn 1000
						return

					if data.result
						$("#validation-success").fadeIn 1000
						return
