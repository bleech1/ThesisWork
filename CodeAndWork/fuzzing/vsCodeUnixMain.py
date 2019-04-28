#!/bin/python

import socket
import subprocess
import os


SOCK_PATH = "/Users/Bleecher/Library/Application Support/Code/1.33.1-main.sock"
PROCESS_NAME = "Code"
OUTPUT_FILE = "codeUnixMainFuzzing.txt"
PATH_TO_APP = "/Users/Bleecher/Applications/Visual Studio Code.app/Contents/MacOS/Electron"
NUM_RUNS = 1000000
RECV_SIZE = 1024

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
R1 = "\x58\xc1\x87\xd0\xff\x7f"

numTests = 0
numCrashes = 0
crashingInput = []

def Main():
    global numCrashes
    global numTests

    #StartApp()
    # create the socket and connect
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCK_PATH)

    for i in range(NUM_RUNS):
        try:
            # get the random pieces using radamsa
            proc1 = subprocess.Popen(["echo", R1], stdout = subprocess.PIPE)
            proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
            rand1, error = proc2.communicate()

            # put together the data
            randomPacket = rand1

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
