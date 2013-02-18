#!/bin/bash

################################################################################
# © 2013
# Kevin Mershon
################################################################################

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
"$GAE_PATH/dev_appserver.py" --port=8081 "$CWD" &
PID=$!
echo "Started with process ID $PID"
sleep 2

INCLUDES="$CWD/test-js/includes/setup.coffee"
TARGETS="$CWD/test-js/tests/"
#COMMAND="casperjs test --includes=$INCLUDES --xunit=output.xml $TARGETS"
#echo "command is $COMMAND"
COMMAND="casperjs test --includes=$INCLUDES $TARGETS"
eval "$COMMAND"
kill "$PID"
