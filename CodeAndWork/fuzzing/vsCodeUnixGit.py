#!/bin/python

import socket
import subprocess
import os


SOCK_PATH = "/var/folders/th/3_4wg0x53w7_01g6m_2fd5rr0000gn/T/vscode-git-askpass-f34746039da54e3b11eb40831aeb4cc1296"
PROCESS_NAME = "Code"
OUTPUT_FILE = "codeUnixGitFuzzing.txt"
PATH_TO_APP = "/Users/Bleecher/Applications/Visual Studio Code.app/Contents/MacOS/Electron"
NUM_RUNS = 500000
RECV_SIZE = 1024

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
R1 = "\x01"
P1 = bytes("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", "utf-8")
R2 = "\x05\x01"
P2 = bytes("\x00\x00\x00\x00", "utf-8")
R3 = "\x01"
P3 = bytes("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", "utf-8")
R4 = "\x0e\x04"
P4 = bytes("\x00\x00\x00", "utf-8")
R5 = "\x01\x05"
P5 = bytes("\x00\x00\x00", "utf-8")
R6 = "\x03\x32\x30\x30"
P6 = bytes("\x00", "utf-8")

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
            proc3 = subprocess.Popen(["echo", R2], stdout = subprocess.PIPE)
            proc4 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc3.stdout, stdout = subprocess.PIPE)
            rand2, error = proc4.communicate()
            proc5 = subprocess.Popen(["echo", R3], stdout = subprocess.PIPE)
            proc6 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc5.stdout, stdout = subprocess.PIPE)
            rand3, error = proc6.communicate()
            proc7 = subprocess.Popen(["echo", R4], stdout = subprocess.PIPE)
            proc8 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc7.stdout, stdout = subprocess.PIPE)
            rand4, error = proc8.communicate()
            proc9 = subprocess.Popen(["echo", R5], stdout = subprocess.PIPE)
            proc10 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc9.stdout, stdout = subprocess.PIPE)
            rand5, error = proc10.communicate()
            proc11 = subprocess.Popen(["echo", R6], stdout = subprocess.PIPE)
            proc12 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc11.stdout, stdout = subprocess.PIPE)
            rand6, error = proc12.communicate()

            # put together the data
            randomPacket = rand1 + P1 + rand2 + P2 + rand3 + P3 + rand4 + P4 + rand5 + P5 + rand6 + P6

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
