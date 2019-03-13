#!/bin/bash

# Script to gather information about Mac local IPC
cd ~
randomNum=`echo $RANDOM`
path=`pwd`
folderPath="$path/ipcFiles"
pathPrefix="$folderPath/$randomNum"
if [ -e "$folderPath" ];
then
    sudo rm -r "$folderPath" 
fi
mkdir "$folderPath"

version=0
# Get python version
if command -v python3 &> /dev/null;
then
    version=3
else
    version=2
fi

counter=0
# Make python scripts executable
if [ "$version" -eq "3" ];
then
    chmod +x anonymize3.py
    chmod +x getConnections3.py
else
    chmod +x anonymize2.py
    chmod +x getConnections2.py
fi

# Find the user account on the computer to anonymize data
username=`dscl . list /Users | grep -v _ | grep -v daemon | grep -v Guest | grep -v nobody | grep -v root`

# Get 10 data points for each computer
while [ $counter -lt 5 ];
do
    echo $counter
    date >> "$pathPrefix.aConnUnixSockets.txt"

    # Run the lsof commands and save output
    openSockets=`sudo lsof -U +c 0`
    allOpenFiles=`sudo lsof +c 0`
    openTcp=`sudo lsof -i tcp -nP +c 0`
    openUdp=`sudo lsof -i udp -nP +c 0`

    # Find all the open Unix Domain Sockets
    echo "$openSockets" > "$pathPrefix.UnixSockets.txt"

    # Find all open pipes
    echo "$allOpenFiles" | grep 'PIPE' > "$pathPrefix.Pipes.txt"
    echo "$allOpenFiles" | grep 'FIFO' > "$pathPrefix.Fifos.txt"

    # Get the counts of open unix domain sockets/pipes for each process
    echo "$openSockets" | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.UnixSocketsCount.txt" 
    echo "$allOpenFiles" | grep 'PIPE' | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.PipesCount.txt" 
    echo "$allOpenFiles" | grep 'FIFO' | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.FifosCount.txt" 

    # Find all open TCP/UDP connections
    echo "$openTcp" > "$pathPrefix.TcpConns.txt"
    echo "$openUdp" > "$pathPrefix.UdpConns.txt"

    # Get the counts of open TCP/UDP connections for each command (application)
    echo "$openTcp" | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.TcpConnsCount.txt" 
    echo "$openUdp" | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.UdpConnsCount.txt" 

    # Get the running process list and anonymize it
    sudo ps auxww > "$pathPrefix.Ps.txt"


    # Anonymize all of the files
    if [ "$version" -eq "3" ];
    then
        python3 getConnections3.py "$pathPrefix.UnixSockets.txt"
        python3 anonymize3.py "$pathPrefix.ConnUnixSockets.txt" "$username"
        python3 getConnections3.py "$pathPrefix.Pipes.txt"
        python3 getConnections3.py "$pathPrefix.Fifos.txt"
        python3 anonymize3.py "$pathPrefix.ConnPipes.txt" "$username"
        python3 anonymize3.py "$pathPrefix.ConnFifos.txt" "$username"
        python3 anonymize3.py "$pathPrefix.TcpConns.txt" "$username"
        python3 anonymize3.py "$pathPrefix.UdpConns.txt" "$username"
        python3 anonymize3.py "$pathPrefix.Ps.txt" "$username"
    else
        python getConnections2.py "$pathPrefix.UnixSockets.txt"
        python anonymize2.py "$pathPrefix.ConnUnixSockets.txt" "$username"
        python getConnections2.py "$pathPrefix.Pipes.txt"
        python getConnections2.py "$pathPrefix.Fifos.txt"
        python anonymize2.py "$pathPrefix.ConnPipes.txt" "$username"
        python anonymize2.py "$pathPrefix.ConnFifos.txt" "$username"
        python anonymize2.py "$pathPrefix.TcpConns.txt" "$username"
        python anonymize2.py "$pathPrefix.UdpConns.txt" "$username"
        python anonymize2.py "$pathPrefix.Ps.txt" "$username"
    fi

    # Between iterations, enter 2 new lines to each file to separate output
    for j in `seq 1 2`;
    do
        echo >> "$pathPrefix.aConnUnixSockets.txt"
        echo >> "$pathPrefix.aConnPipes.txt"
        echo >> "$pathPrefix.aConnFifos.txt"
        echo >> "$pathPrefix.UnixSocketsCount.txt"
        echo >> "$pathPrefix.PipesCount.txt"
        echo >> "$pathPrefix.FifosCount.txt"
        echo >> "$pathPrefix.aTcpConns.txt"
        echo >> "$pathPrefix.aUdpConns.txt"
        echo >> "$pathPrefix.TcpConnsCount.txt"
        echo >> "$pathPrefix.UdpConnsCount.txt"
        echo >> "$pathPrefix.aPs.txt"
    done

    # Sleep for an hour after each iteration
    # This script will pause whenever a computer is sleeping, but
    # will resume after.  Since we mostly want apps used by users
    # (and not system apps as much) this will be ok because we
    # will capture only while the computer is awake and being used.
    sleep 3600
    let counter=counter+1
done

# Remove un-anonymized output before zipping
rm "$pathPrefix.Ps.txt"
rm "$pathPrefix.UnixSockets.txt" "$pathPrefix.ConnUnixSockets.txt"
rm "$pathPrefix.Pipes.txt" "$pathPrefix.ConnPipes.txt"
rm "$pathPrefix.Fifos.txt" "$pathPrefix.ConnFifos.txt"
rm "$pathPrefix.TcpConns.txt" "$pathPrefix.UdpConns.txt"

# Send the files over to Brendan's computer
zip -r "$randomNum.ipcFiles.zip" "ipcFiles/"

# Use curl to send the file to basin
curl -F "data=@$randomNum.ipcFiles.zip" http://www.cs.middlebury.edu/~bleech/gimme2.php

# Clean up
rm -r ipcFiles "$randomNum.ipcFiles.zip"
rm getConnections2.py getConnections3.py anonymize2.py anonymize3.py