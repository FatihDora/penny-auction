#!/bin/bash

# guard against GAE_PATH not being set
if [ "$GAE_PATH" == "" ]
then
	echo "Please set environment variable GAE_PATH to your Google AppEngine directory!"
	exit 1
fi

# guard against phantomjs and casperjs not being installed
which phantomjs >> /dev/null && which casperjs >> /dev/null
SUCCESS=$?
if [ "$SUCCESS" == "1" ]
then
	echo "PhantomJS and CasperJS must be installed!"
	exit 1
fi

# start up the instance and get the process id for later
CWD=`pwd`/`dirname $0`/..
echo "Working directory is $CWD"
"$GAE_PATH/dev_appserver.py" --port=8081 --datastore_path=.datastore \
	--search_indexes_path=.searchindexes "$CWD" &
PID=$!
echo "Started with process ID $PID"
sleep 2

INCLUDES="$CWD/test-js/includes/setup.coffee"
TARGETS="$CWD/test-js/tests/"
COMMAND="casperjs test --no-colors --includes=$INCLUDES --xunit=output.xml $TARGETS"
#echo "command is $COMMAND"
eval "$COMMAND"
kill "$PID"
