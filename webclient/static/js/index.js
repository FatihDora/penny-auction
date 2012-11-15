// Generated by CoffeeScript 1.3.3
(function() {
  var auction_ids, auction_list, auctions;

  $(document).ready(function() {
    auctions.init();
    if ($("#auctions").length !== 0) {
      return window.setInterval(auctions.updateAuctions, 1000);
    }
  });

  auction_ids = [];

  auction_list = [];

  auctions = {
    fetchingAuctionUpdates: null,
    init: function() {
      var buildAuction;
      callApi(AUCTIONS_LIST_ACTIVE, {
        count: 30
      }, function(data) {
        var b, i, ix, m, n, p, t, u, w, _results;
        $("#auctions").html("");
        auctions = data.result;
        if (!(auctions != null)) {
          $("#onecol .gallery").html('<h2 class="red">Auctions</h2><br/><p style="font-size: 14px; width:100%">Unfortunately, there aren\'t any auctions in the system.  To spin up some auctions, visit http://pisoapi.appspot.com/reset_data.</p><br/><br/><br/><div class="clear"></div>');
          return;
        }
        _results = [];
        for (ix in auctions) {
          i = auctions[ix].id;
          n = auctions[ix].name;
          b = auctions[ix].base_price;
          u = auctions[ix].product_url;
          m = auctions[ix].image_url;
          p = auctions[ix].price;
          w = auctions[ix].winner;
          t = secondsToHms(auctions[ix].time_left);
          auction_ids.push(i);
          auction_list[i] = auctions[ix];
          _results.push($("#auctions").append(buildAuction(i, n, b, u, m, p, w, t)));
        }
        return _results;
      });
      $("ul#auctions").delegate("div.bid", "click", function() {
        var auction_id, id;
        if (user.loggedIn === false) {
          document.location.href = "/register";
          return;
        }
        id = $(this).closest('li').attr('id');
        if (auction_list[id].t > 11.0) {
          document.location.href = "/auction/" + id;
        }
        if (user.bids > 0) {
          auction_id = $(this).closest('li').attr("id");
          return callApi(AUCTION_BID, {
            id: auction_id
          }, function(data) {
            user.bids -= 1;
            user.update();
            if (user.bids % 5 === 0) {
              return user.refresh();
            }
          });
        }
      });
      return buildAuction = function(id, productName, basePrice, productUrl, imageUrl, currentPrice, currentWinner, timeTilEnd) {
        var tmplAuction;
        tmplAuction = void 0;
        tmplAuction = '';
        tmplAuction += ' <li id="{auction-id}">\n';
        tmplAuction += '\t\t<!-- top block -->\n';
        tmplAuction += '\t\t<div class="top-block">\n';
        tmplAuction += '\t\t\t<h3 class="nocufon"><a href="{url}" title="{item-name}">{item-name}</a></h3>\n';
        tmplAuction += '\t\t\t<div class="imgb thumbnail-zoom">\n';
        tmplAuction += '\t\t\t\t<a href="/auction/{auction-id}" class="fadeable">\n';
        tmplAuction += '\t\t\t\t\t<span class="light-background">\n';
        tmplAuction += '\t\t\t\t\t<span class="thumb-arrow">&#8594;</span>\n';
        tmplAuction += '\t\t\t\t\t</span>\n';
        tmplAuction += '\t\t\t\t\t\t<span>\n';
        tmplAuction += '\t\t\t\t\t\t<img src="{image-url}" width="194" height="144" alt="{item-name}" />\n';
        tmplAuction += '\t\t\t\t\t\t<!--<span class="sale-img">NEW<span>ITEM</span></span>-->\n';
        tmplAuction += '\t\t\t\t\t</span>\n';
        tmplAuction += '\t\t\t\t</a>\n';
        tmplAuction += '\t\t\t</div>\n';
        tmplAuction += '\t\t\t<span class="winner"><a href="#">{winner}</a></span>\n';
        tmplAuction += '\t\t\t<span class="price">P {current-price}</span>\n';
        tmplAuction += '\t\t\t<span class="timeleft">{time-remaining}</span>\n';
        tmplAuction += '\t\t</div>\n';
        tmplAuction += '\t\t<!-- top block -->\n';
        tmplAuction += '\t\t<div class="bid js-button"><a href="javascript:void(0);" class="button-default cart"><span class="hover">BID NOW</span><span>BID NOW</span></a></div>\n';
        tmplAuction += '\t</li>\n';
        tmplAuction = tmplAuction.replaceAll("{auction-id}", id);
        tmplAuction = tmplAuction.replaceAll("{url}", productUrl);
        tmplAuction = tmplAuction.replaceAll("{item-name}", productName);
        tmplAuction = tmplAuction.replaceAll("{image-url}", imageUrl);
        tmplAuction = tmplAuction.replaceAll("{current-price}", currentPrice);
        tmplAuction = tmplAuction.replaceAll("{winner}", currentWinner);
        tmplAuction = tmplAuction.replaceAll("{time-remaining}", timeTilEnd);
        return tmplAuction;
      };
    },
    updateAuctions: function() {
      var fetchingAuctionUpdates, i, tmplist;
      if (auction_ids.length === 0) {
        return;
      }
      tmplist = [];
      i = 0;
      while (i < auction_ids.length) {
        if (auction_list[auction_ids[i]].t > 0.0) {
          tmplist.push(auction_ids[i]);
        }
        i++;
      }
      auction_ids = tmplist;
      if (fetchingAuctionUpdates) {
        fetchingAuctionUpdates.abort();
      }
      return fetchingAuctionUpdates = jQuery.ajax({
        url: API + AUCTIONS_STATUS_BY_ID,
        data: {
          ids: auction_ids.join()
        },
        success: function(data) {
          return $.map(data, function(auction) {
            var a, buttonText, ix, p, t, w, _results;
            auctions = data.result;
            auction_list = [];
            _results = [];
            for (ix in auctions) {
              i = auctions[ix].id;
              p = auctions[ix].price;
              w = auctions[ix].winner;
              t = secondsToHms(auctions[ix].time_left);
              a = auctions[ix].active;
              auction_list[i] = auctions[ix];
              buttonText = "";
              if (auctions[ix].t > 11.0) {
                buttonText = "Starting Soon...";
              } else {
                if (user.loggedIn != null) {
                  buttonText = "BID NOW!";
                } else {
                  buttonText = "REGISTER NOW!";
                }
              }
              $("#" + i + " span.winner").html("<a href=\"#\">" + w + "</a>");
              $("#" + i + " span.price").text("P " + p);
              $("#" + i + " span.timeleft").html(t);
              if (a === "False") {
                if (w === "No Bidder") {
                  buttonText = "SOLD";
                } else {
                  buttonText = "ENDED";
                }
              }
              _results.push($("#" + i + " div.bid").html('<a href="javascript:void(0);" class="button-default cart"><span class="hover">' + buttonText + '</span><span>' + buttonText + '</span></a>'));
            }
            return _results;
          });
        }
      });
    }
  };

}).call(this);
