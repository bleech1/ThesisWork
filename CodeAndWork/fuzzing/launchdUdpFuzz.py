#!/bin/python

import socket
import subprocess
import os
import random


UDP_IP = "127.0.0.1"
UDP_PORT1 = 137
UDP_PORT2 = 138
PROCESS_NAME = "launchd"
OUTPUT_FILE = "launchdUdpFuzz.txt"
PATH_TO_APP = "/sbin/launchd"
NUM_RUNS = 1000000

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
P1_START = "\x45\x7f\x01\x10\x00\x01\x00\x00\x00\x00\x00\x00"
R1 = "\x20\x41\x42\x41\x43\x46\x50\x46\x50\x45\x4e\x46\x44\x45\x43\x46\x43\x45\x50\x46\x48\x44\x44\x45\x46\x46\x50\x46\x50\x41\x43\x41\x42"
P1_END = "\x00\x00\x20\x00\x01"
P2_START = "\x45\x81\x29\x10\x00\x01\x00\x00\x00\x00\x00"
R2 = "\x01\x20\x45\x43\x46\x43\x45\x46\x45\x4f\x45\x45\x45\x42\x45\x4f\x46\x44\x43\x4e\x45\x4e\x45\x43\x46\x41\x43\x41\x43\x41\x43\x41\x41\x41"
P2_END = "\x00\x00\x20\x00\x01\xc0\x0c\x00\x20\x00\x01\x00\x00\x03\x84\x00\x06\x60\x00\x8c\xe9\xaa\x7e"

numTests = 0
numCrashes = 0
crashingInput = []

def Main():
    global numCrashes
    global numTests

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(NUM_RUNS):
        try:
            # half the time, use one packet
            if random.random() < 0.5:
                # get the random pieces using radamsa
                proc1 = subprocess.Popen(["echo", R1], stdout = subprocess.PIPE)
                proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
                random1, error = proc2.communicate()

                # put together the data
                randomPacket = bytes(P1_START, "utf-8") + random1 + bytes(P1_END, "utf-8")
            # otherwise use other packet
            else:
                # get the random pieces using radamsa
                proc1 = subprocess.Popen(["echo", R2], stdout = subprocess.PIPE)
                proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
                random1, error = proc2.communicate()

                # put together the data
                randomPacket = bytes(P2_START, "utf-8") + random1 + bytes(P2_END, "utf-8")
            
            if len(randomPacket) > 1500:
                randomPacket = randomPacket[ : 1500]

            # send the packet
            if i % 2 == 0:
                sock.sendto(randomPacket, (UDP_IP, UDP_PORT1))
            else:
                sock.sendto(randomPacket, (UDP_IP, UDP_PORT2))
            # check if process crashed
            if not CheckIfAlive(PROCESS_NAME):
                crashingInput.append(" ".join(x.encode("hex") for x in randomPacket))
                numCrashes += 1
                StartApp()
            numTests += 1
            print(i)
        except KeyboardInterrupt:
            Clean(sock)
    Clean(sock)

def StartApp():
    subprocess.Popen([PATH_TO_APP, "&"])

def CheckIfAlive(procName):
    proc1 = subprocess.Popen(["lsof", "-i", "udp", "+c", "0"], stdout = subprocess.PIPE)
    proc2 = subprocess.Popen(["grep", procName], stdin = proc1.stdout, stdout = subprocess.PIPE)
    processes, error = proc2.communicate()
    if processes == "":
        return False
    return True

def Clean(sock):
    print("\nCrashed on " + str(numCrashes) + " inputs out of " + str(numTests))
    with open(OUTPUT_FILE, "w") as out:
        for i in range(len(crashingInput)):
            out.write("Crashed on:" + crashingInput[i] + "\n\n")
    sock.close()
    exit(1)

if __name__ == "__main__":
    Main()