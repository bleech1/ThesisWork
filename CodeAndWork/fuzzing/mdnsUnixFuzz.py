#!/bin/python

import socket
import subprocess
import os


SOCK_PATH = "/var/run/mDNSResponder"
PROCESS_NAME = "_mdnsresponder"
OUTPUT_FILE = "mdnsUnixFuzzing.txt"
PATH_TO_APP = "/usr/sbin/mDNSResponderHelper"
NUM_RUNS = 500000
RECV_SIZE = 1024

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
P1 = bytes("\x00\x00\x00", "utf-8")
R1 = "\x01"
P2 = bytes("\x00\x00\x00", "utf-8")
R2 = "\x04"
P3 = bytes("\x00\x00\x00\x00\x00\x00\x00", "utf-8")
R3 = "\x13"
P4 = bytes("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", "utf-8")
R4 = "\x01\x52"

numTests = 0
numCrashes = 0
crashingInput = []

def Main():
    global numCrashes
    global numTests

    #StartApp()

    for i in range(NUM_RUNS):
        try:
            # create the socket and connect
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(SOCK_PATH)
            # get the random pieces using radamsa
            proc1 = subprocess.Popen(["echo", R1], stdout = subprocess.PIPE)
            proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
            rand1, error = proc2.communicate()
            proc3 = subprocess.Popen(["echo", R2], stdout = subprocess.PIPE)
            proc4 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc3.stdout, stdout = subprocess.PIPE)
            rand2, error = proc4.communicate()
            proc5 = subprocess.Popen(["echo", R3], stdout = subprocess.PIPE)
            proc6 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc5.stdout, stdout = subprocess.PIPE)
            rand3, error = proc6.communicate()
            proc7 = subprocess.Popen(["echo", R4], stdout = subprocess.PIPE)
            proc8 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc7.stdout, stdout = subprocess.PIPE)
            rand4, error = proc8.communicate()

            # put together the data
            randomPacket = P1 + rand1 + P2 + rand2 + P3 + rand3 + P4 + rand4

            # send the packet
            sock.send(randomPacket)
            
            if not CheckIfAlive(PROCESS_NAME):
                crashingInput.append(" ".join(x.encode("hex") for x in randomPacket))
                numCrashes += 1
                StartApp()
            numTests += 1
            print(i)
        except KeyboardInterrupt:
            Clean(sock)
        except BrokenPipeError:
            print("broken pipe")
        #except Exception as e:
        #    print("Exception: " + str(e))
        #    Clean(sock)
    Clean(sock)

def StartApp():
    subprocess.Popen([PATH_TO_APP, "&"])

def CheckIfAlive(procName):
    proc1 = subprocess.Popen(["lsof", "-U", "+c", "0"], stdout = subprocess.PIPE)
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


