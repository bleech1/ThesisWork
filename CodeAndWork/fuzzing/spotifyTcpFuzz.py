#!/bin/python

import socket
import subprocess
import os
import time


TCP_IP = "127.0.0.1"
PROCESS_NAME = "Spotify"
OUTPUT_FILE = "spotifyTcp.txt"
PATH_TO_APP = "/Applications/Spotify.app/Contents/MacOS/Spotify"
NUM_RUNS = 500000
RECV_SIZE = 1024

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
START = "\x53\x70\x6f\x74\x55\x64\x70\x30"
FIRST_RANDOM = "\x78\xbc\x37\xc2\xbd\x93\x5d\x67"
MIDDLE = "\x00\x01\x00\x04\x48\x95\xc2\x03"
SECOND_RANDOM = "\x4a\xc3\xec\xd2\x37\xf3\x7d\x8c\xff\x0e\x85\x9c\xb2\x64\xfd\x3a\x98\xcb\x53\xa9"

numTests = 0
numCrashes = 0
crashingInput = []

def Main():
    global numCrashes
    global numTests

    StartApp()
    port = int(FindPort())

    # create the socket and connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, port))

    for i in range(NUM_RUNS):
        print(port)
        #time.sleep(100)
        try:
            # get the random pieces using radamsa
            proc1 = subprocess.Popen(["echo", FIRST_RANDOM], stdout = subprocess.PIPE)
            proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
            random1, error = proc2.communicate()
            proc3 = subprocess.Popen(["echo", SECOND_RANDOM], stdout = subprocess.PIPE)
            proc4 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc3.stdout, stdout = subprocess.PIPE)
            random2, error = proc4.communicate()

            # make sure lengths are not too long
            if len(random1) > len(FIRST_RANDOM):
                random1 = random1[ : len(FIRST_RANDOM)]
            if len(random2) > len(SECOND_RANDOM):
                random2 = random2[ : len(SECOND_RANDOM)]

            # put together the data
            randomPacket = bytes(START, "utf-8") + random1 + bytes(MIDDLE, "utf-8") + random2

            # send the packet
            sock.send(randomPacket)
            
            if not CheckIfAlive(PROCESS_NAME):
                crashingInput.append(" ".join(x.encode("hex") for x in randomPacket))
                numCrashes += 1
                StartApp()
                port = int(FindPort())
                # create the socket and connect
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((TCP_IP, port))
            numTests += 1
            print(i)
        except KeyboardInterrupt:
            Clean()
        """
        except Exception as e:
            print("Exception: " + str(e))
            port = int(FindPort())
            # create the socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TCP_IP, port))
        """
    Clean()

def StartApp():
    subprocess.Popen([PATH_TO_APP, "&"])

def FindPort():
    proc1 = subprocess.Popen(["lsof", "-i", "tcp", "+c", "0"], stdout = subprocess.PIPE)
    proc2 = subprocess.Popen(["grep", PROCESS_NAME], stdin = proc1.stdout, stdout = subprocess.PIPE)
    processes, error = proc2.communicate()
    processes = processes.decode("utf-8")
    processes = processes.split("\n")
    for line in processes:
        # ignore established connections (Internet, not local)
        if "ESTABLISHED" in line:
            continue
        # ignore line of port 57621, that's the wrong port
        if "57621" in line:
            continue
        colon = line.find(":")
        port = line[colon + 1 : ]
        paren = port.find("(")
        port = port[ : paren - 1]
        if port.isnumeric():
            return port
    return None

def CheckIfAlive(procName):
    proc1 = subprocess.Popen(["lsof", "-i", "tcp", "+c", "0"], stdout = subprocess.PIPE)
    proc2 = subprocess.Popen(["grep", procName], stdin = proc1.stdout, stdout = subprocess.PIPE)
    processes, error = proc2.communicate()
    if processes == "":
        return False
    return True

def Clean(*args):
    print("\nCrashed on " + str(numCrashes) + " inputs out of " + str(numTests))
    with open(OUTPUT_FILE, "w") as out:
        for i in range(len(crashingInput)):
            out.write("Crashed on:" + crashingInput[i] + "\n\n")
    exit(1)

if __name__ == "__main__":
    Main()
