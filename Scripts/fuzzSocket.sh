#!/bin/bash

# Script to fuzz a UNIX domain socket using radamsa

if [ $# -lt 1 ];
then
    echo "Please give UNIX socket path to fuzz"
    exit 1
fi

socketPath=$1

# Send random input to the socket
testInput=`echo "sdgjkhsdhgk" | ../radamsa/bin/radamsa -n 1`
nc -U $socketPath <<< $testInput
