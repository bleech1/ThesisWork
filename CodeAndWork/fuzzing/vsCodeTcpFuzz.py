#!/bin/python

import socket
import subprocess
import os


TCP_IP = "127.0.0.1"
PROCESS_NAME = "Code"
OUTPUT_FILE = "codeTcpFuzzing.txt"
PATH_TO_APP = "/Users/Bleecher/Applications/Visual Studio Code.app/Contents/MacOS/Electron"
NUM_RUNS = 1000000
RECV_SIZE = 1024

# need to build the packet together because some parts don't change
# only the RANDOM pieces do, rest don't get sent to radamsa
# this packet is the data of real communication on this port
P1 = "GET "
P2 = " HTTP/1.1\r\nHost: "
P3 = "\r\nContent-type: application/x-www-form-urlencoded\r\nContent-length: "
P4 = "\r\n\r\n"
PAGE = "/bleech1/ThesisWork"
HOST = "www.github.com"
LENGTH = "1000"

numTests = 0
numCrashes = 0
crashingInput = []

def Main():
    global numCrashes
    global numTests

    #StartApp()
    port = int(FindPort())
    if port == None:
        print("couldn't find port")
        exit(1)


    for i in range(NUM_RUNS):
        try:
            # create the socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TCP_IP, port))

            # get the random pieces using radamsa
            proc1 = subprocess.Popen(["echo", PAGE], stdout = subprocess.PIPE)
            proc2 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc1.stdout, stdout = subprocess.PIPE)
            random1, error = proc2.communicate()
            proc3 = subprocess.Popen(["echo", HOST], stdout = subprocess.PIPE)
            proc4 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc3.stdout, stdout = subprocess.PIPE)
            random2, error = proc4.communicate()
            proc5 = subprocess.Popen(["echo", LENGTH], stdout = subprocess.PIPE)
            proc6 = subprocess.Popen(["../../radamsa/bin/radamsa"], stdin = proc5.stdout, stdout = subprocess.PIPE)
            random3, error = proc6.communicate()

            # put together the data
            randomPacket = bytes(P1, "utf-8") + random1 + bytes(P2, "utf-8") + random2 + bytes(P3, "utf-8") + random3 + bytes(P4, "utf-8")

            # send the packet
            sock.send(randomPacket)
            data = sock.recv(RECV_SIZE).decode("utf-8")
            if ("400 Bad Request" not in data) and (data != ""):
                print("!" + data + "!")
                crashingInput.append(" ".join(x.encode("hex") for x in randomPacket))
            
            if not CheckIfAlive(PROCESS_NAME):
                crashingInput.append(" ".join(x.encode("hex") for x in randomPacket))
                numCrashes += 1
                StartApp()
                port = int(FindPort())
            numTests += 1
            print(i)
        except KeyboardInterrupt:
            Clean()
        except Exception as e:
            print("Exception: " + str(e))
            Clean()
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