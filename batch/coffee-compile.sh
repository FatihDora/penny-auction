#!/bin/bash
curdir=`dirname $0`
coffee -b -o "$curdir/../webclient/static/js" \
  -c "$curdir/../webclient/static/coffee"
