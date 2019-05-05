#!/bin/bash

while [ 1 ]
do
    sudo rm /private//var/run/syslog
    results=`sudo lsof -U +c 0 | grep run/syslog`
    if [ "$results" == "" ]
    then 
        sudo ./namedServer /private//var/run/syslog &
    fi

done