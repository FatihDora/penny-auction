$(document).ready(function() {
	/* 1s Timer */
	window.setInterval(function() {
		$(".auction-time-remaining").each(function(i) {
			var parts = this.innerHTML.split(":");
			var d = new Date();
			d.setHours(parts[0]);
			d.setMinutes(parts[1]);
			d.setSeconds(parts[2]);
			var oldHours = d.getHours();
			d.setSeconds(d.getSeconds() - 1);
			if (oldHours >= d.getHours()) {
				this.innerHTML = padzero(d.getHours(),2) + ":" + padzero(d.getMinutes(),2) + ":" + padzero(d.getSeconds(),2);
				if (this.innerHTML == "00:00:00") { this.style.backgroundColor="#CC0000"; $(this).animate({backgroundColor: '#FFFFFF'}, 'slow');}
			}
			else
			{
				this.innerHTML = "00:00:00";
			}
		})
	},1000);
	
	/* Bid Button Clicked */
	$(".auction-bid-button").click(function() {
	  	//$.getJSON('/user/', { username: 'darin', password: 'letmein' }, function(data) {
		//$(this).innerHTML = data;
		//});
		var id = $(this).parent().attr("id");
	});
	
	/* Login Button Clicked */
	
	
	/* Count auctions down */
	$(".auction-time-remaining").each(function(i) {
		var parts = this.innerHTML.split(":");
		var d = new Date();
		d.setHours(parts[0]);
		d.setMinutes(parts[1]);
		d.setSeconds(parts[2]);
		var oldHours = d.getHours();
		if (oldHours >= d.getHours()) {
			this.innerHTML = padzero(d.getHours(),2) + ":" + padzero(d.getMinutes(),2) + ":" + padzero(d.getSeconds(),2);
		}
	});
	
	
});