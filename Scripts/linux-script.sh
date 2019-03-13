#!/bin/bash

# Script to gather information about Mac local IPC
cd /
username=`whoami`
pathPrefix="/tmp/ipcFiles/$username"
if [ -e "/tmp/ipcFiles/" ];
then
    sudo rm -r /tmp/ipcFiles
fi
mkdir /tmp/ipcFiles

# Remove files if they exist, then touch to make exist
touch "$pathPrefix.OpenUnixSockets.txt"
touch "$pathPrefix.AllPipes.txt"
touch "$pathPrefix.OpenPipes.txt"
touch "$pathPrefix.OpenFifos.txt"
touch "$pathPrefix.OpenUnixSocketsCount.txt"
touch "$pathPrefix.OpenPipesCount.txt"
touch "$pathPrefix.OpenFifosCount.txt"
touch "$pathPrefix.OpenTcpConns.txt"
touch "$pathPrefix.OpenUdpConns.txt"
touch "$pathPrefix.TcpConnsCount.txt"
touch "$pathPrefix.UdpConnsCount.txt"

counter=0

# Get 10 data points for each computer
while [ $counter -lt 10 ];
do
    echo $i
    date >> "$pathPrefix.OpenUnixSockets.txt"
    # Find all the open Unix Domain Sockets
    sudo lsof -U +c 0 >> "$pathPrefix.OpenUnixSockets.txt"


    # Find all of the named pipes, not as helpful because 
    # we care more about open (being used), so look below
    sudo find * -type p >> "$pathPrefix.AllPipes.txt"

    # Find all open pipes
    sudo lsof +c 0 | grep 'PIPE' >> "$pathPrefix.OpenPipes.txt"
    sudo lsof +c 0 | grep 'FIFO' >> "$pathPrefix.OpenFifos.txt"


    # Can search by a process name
    #sudo lsof -c Spotify | grep PIPE >> "$username.SpotifyPipes.txt"
    #sudo lsof -c Spotify | grep FIFO >> "$username.SpotifyFIFOs.txt"
    #sudo lsof -c Spotify | grep unix  >> "$username.SpotifyUnix.txt"

    # Get the counts of open unix domain sockets/pipes for each process
    sudo lsof -U +c 0 | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.OpenUnixSocketsCount.txt"
    sudo lsof +c 0 | grep 'PIPE' | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.OpenPipesCount.txt"
    sudo lsof +c 0 | grep 'FIFO' | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.OpenFifosCount.txt"


    # Find all open TCP/UDP connections
    sudo lsof -i tcp -nP +c 0 >> "$pathPrefix.OpenTcpConns.txt"
    sudo lsof -i udp -nP +c 0 >> "$pathPrefix.OpenUdpConns.txt"

    # Get the counts of open TCP/UDP connections for each command (application)
    sudo lsof -i tcp -nP +c 0 | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.TcpConnsCount.txt"
    sudo lsof -i udp -nP +c 0 | awk '//{print $1}' | grep -v COMMAND | uniq -c | sort -k 2 >> "$pathPrefix.UdpConnsCount.txt"


    # Between iterations, enter 2 new lines to each file to separate output
    for j in `seq 1 2`;
    do
        echo >> "$pathPrefix.OpenUnixSockets.txt"
        echo >> "$pathPrefix.AllPipes.txt"
        echo >> "$pathPrefix.OpenPipes.txt"
        echo >> "$pathPrefix.OpenFifos.txt"
        echo >> "$pathPrefix.OpenUnixSocketsCount.txt"
        echo >> "$pathPrefix.OpenPipesCount.txt"
        echo >> "$pathPrefix.OpenFifosCount.txt"
        echo >> "$pathPrefix.OpenTcpConns.txt"
        echo >> "$pathPrefix.OpenUdpConns.txt"
        echo >> "$pathPrefix.TcpConnsCount.txt"
        echo >> "$pathPrefix.UdpConnsCount.txt"
    done

    # Sleep for an hour after each iteration
    # This script will pause whenever a computer is sleeping, but
    # will resume after.  Since we mostly want apps used by users
    # (and not system apps as much) this will be ok because we
    # will capture only while the computer is awake and being used.
    sleep 3600
    let counter=counter+1
done


# Send the files over to Brendan's computer

# Option 1: email them
cat "$pathPrefix.OpenUnixSockets.txt" | mail -s "Open Unix Sockets" bleech@middlebury.edu

# Option 2: ssh and scp them
sudo scp -r /tmp/ipcFiles bleech@basin.cs.middlebury.edu:/home/bleech/