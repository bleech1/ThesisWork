#!/bin/python

import glob
import subprocess
import os

# Filenames that we are going to look at
FIFO = "FifosCount.txt"
PIPE = "PipesCount.txt"
TCP = "TcpConnsCount.txt"
UDP = "UdpConnsCount.txt"
UNIX = "UnixSocketsCount.txt"
DIRECTORY = "ipcFiles/"
RESULTS = "./results"

# Read the file and add contents to dicts
def ReadFile(filename, avgDict, appNames):
    try:
        with open(filename, "r") as infile:
            for line in infile:
                # Ignore empty lines
                if not line.strip():
                    continue
                # Index 0 is num of that type of IPC for that app, 1 is app name
                splitLine = line.split()
                numTimes = splitLine[0]
                appName = splitLine[1]
                appNames.add(appName)
                if appName in avgDict.keys():
                    avgDict[appName] += [int(numTimes)]
                else:
                    avgDict[appName] = [int(numTimes)]
    except FileNotFoundError:
        return

# Add each app that appeared to the app dictionary
def CountAppearances(nameSet, countDict):
    for appName in nameSet:
        if appName in countDict.keys():
            countDict[appName] += 1
        else:
            countDict[appName] = 1

# Average the amount for each type of local IPC
def AverageAppearances(countDict):
    if len(countDict.keys()) == 0:
        return
    for key in countDict.keys():
        countDict[key] = sum(countDict[key]) / len(countDict[key])

# Calculate the percentage of times an app was used
def CalculatePercentages(countDict, total):
    if len(countDict.keys()) == 0:
        return
    for key in countDict.keys():
        countDict[key] = countDict[key] / total * 100

# Print the top count of each dictionary
def PrintOutput(type, dictionary, orderedKeys, count):
    count = int(count)
    if count > len(orderedKeys):
        count = len(orderedKeys)
    print("Type: " + str(type))
    if count == 0:
        print("None\n")
        return
    for i in range(count):
        key = orderedKeys[i]
        print(f"{key:40}{str(dictionary[key]):7}")
    print("")

def WriteOutput(type, dictionary, orderedKeys):
    with open(RESULTS, "a") as outfile:
        outfile.write(type + "\n")
        if len(orderedKeys) == 0:
            outfile.write("None\n")
        for i in range(len(orderedKeys)):
            key = orderedKeys[i]
            outfile.write(f"{key:40}{str(dictionary[key]):7}\n")
        outfile.write("\n\n")



# MAIN METHOD

# Get all of the zip files
zips = glob.glob("*ipcFiles.zip")

userCount = 0
appsUsed = dict()
fifos = dict()
pipes = dict()
tcp = dict()
udp = dict()
unix = dict()

for filename in zips:
    userCount += 1
    number = filename.split(".", 1)[0]
    # Unzip the directory
    subprocess.run(["unzip", filename])

    # Read through the files and collect statistics
    appNames = set()
    ReadFile(DIRECTORY + number + "." + FIFO, fifos, appNames)
    ReadFile(DIRECTORY + number + "." + PIPE, pipes, appNames)
    ReadFile(DIRECTORY + number + "." + TCP, tcp, appNames)
    ReadFile(DIRECTORY + number + "." + UDP, udp, appNames)
    ReadFile(DIRECTORY + number + "." + UNIX, unix, appNames)
    CountAppearances(appNames, appsUsed)

    # Remove the unzipped directory
    subprocess.run(["rm", "-r", "ipcFiles"])

# Get averages for each dictionary
AverageAppearances(fifos)
AverageAppearances(pipes)
AverageAppearances(tcp)
AverageAppearances(udp)
AverageAppearances(unix)
CalculatePercentages(appsUsed, userCount)

# Sort the keys by decreasing values (so highest value-keys at beginning)
topFifos = list(sorted(fifos, key=fifos.__getitem__, reverse=True))
topPipes = list(sorted(pipes, key=pipes.__getitem__, reverse=True))
topTcp = list(sorted(tcp, key=tcp.__getitem__, reverse=True))
topUdp = list(sorted(udp, key=udp.__getitem__, reverse=True))
topUnix = list(sorted(unix, key=unix.__getitem__, reverse=True))
topApps = list(sorted(appsUsed, key=appsUsed.__getitem__, reverse=True))

# If there is already a results directory, remove it
if os.path.exists(RESULTS):
    subprocess.run(["rm", RESULTS])

subprocess.run(["touch", RESULTS])

# Print out the results
count = input("How many apps to print out? ")
PrintOutput("Apps", appsUsed, topApps, count)
WriteOutput("Apps", appsUsed, topApps)
count = input("How many fifos to print out? ")
PrintOutput("Fifos", fifos, topFifos, count)
WriteOutput("Fifos", fifos, topFifos)
count = input("How many pipes to print out? ")
PrintOutput("Pipes", pipes, topPipes, count)
WriteOutput("Pipes", pipes, topPipes)
count = input("How many TCP connections to print out? ")
PrintOutput("TCP", tcp, topTcp, count)
WriteOutput("TCP", tcp, topTcp)
count = input("How many UDP connections to print out? ")
PrintOutput("UDP", udp, topUdp, count)
WriteOutput("UDP", udp, topUdp)
count = input("How many UNIX domain sockets to print out? ")
PrintOutput("UNIX Domain Sockets", unix, topUnix, count)
WriteOutput("UNIX Domain Sockets", unix, topUnix)
