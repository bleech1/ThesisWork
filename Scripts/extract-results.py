#!/bin/python

import glob
import subprocess
import os
import sys

# Filenames that we are going to look at
FILE_PREFIX = "../ThesisData/"
FIFO = "FifosCount.txt"
PIPE = "PipesCount.txt"
TCP = "TcpConnsCount.txt"
UDP = "UdpConnsCount.txt"
UNIX = "UnixSocketsCount.txt"
DIRECTORY = "ipcFiles/"
RESULTS = FILE_PREFIX + "results.txt"
GROUP_FILE = FILE_PREFIX + "groups.txt"
GROUPED_RESULTS = FILE_PREFIX + "grouped_results.txt"

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
def AverageAppearances(countDict, avgDict):
    if len(countDict.keys()) == 0:
        return
    for key in countDict.keys():
        avgDict[key] = round(sum(countDict[key]) / len(countDict[key]), 5)

# Calculate the percentage of times an app was used
def CalculatePercentages(percentDict, countDict, total):
    if len(countDict.keys()) == 0:
        return
    for key in countDict.keys():
        percentDict[key] = round(countDict[key] / total * 100, 5)

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

# Write the output to a file
def WriteOutput(type, dictionary, orderedKeys, appCounts):
    with open(RESULTS, "a") as outfile:
        outfile.write(f"{type:40}{'Avg Num':12}{'Num Machines'}\n")
        if len(orderedKeys) == 0:
            outfile.write("None\n")
        for i in range(len(orderedKeys)):
            key = orderedKeys[i]
            outfile.write(f"{key:40}{str(dictionary[key]):12}{str(appCounts[key])}\n")
        outfile.write("\n\n")

# Get the groups for each file
def GetGroups():
    groups = dict()
    newGroup = True
    lastGroup = ""
    procInGroup = set()
    with open(GROUP_FILE, "r") as groupFile:
        for line in groupFile:
            line = line.strip()
            if line == "":
                newGroup = True
                continue
            if newGroup:
                groups[line] = []
                lastGroup = line
                newGroup = False
                continue
            # else, newGroup is False
            groups[lastGroup].append(line)
            procInGroup.add(line)
    return groups, procInGroup

def FindGroup(groups, group):
    for key in groups.keys():
        if group in groups[key]:
            return key
    return None

def CreateGroupData(dicts, groups, procInGroup):
    appsUsed = dicts[0]
    avgFifos = dicts[1]
    avgPipes = dicts[2]
    avgTcp = dicts[3]
    avgUdp = dicts[4]
    avgUnix = dicts[5]
    # New dict where key is process (or group title)
    # Value is a list: # machines, fifos, pipes, tcp, udp, unix
    # Each item in list is a list of the values, so we can average
    groupData = dict()
    # Initialize with empty keys for each group name
    for item in groups.keys():
        groupData[item] = [[], [], [], [], [], []]
    # For each process, add it to groupData if not part of a group
    # If part of a group, add it there to be averaged later
    for item in appsUsed.keys():
        if item not in appsUsed.keys():
            appsUsed[item] = 0
        if item not in avgFifos.keys():
            avgFifos[item] = 0
        if item not in avgPipes.keys():
            avgPipes[item] = 0
        if item not in avgTcp.keys():
            avgTcp[item] = 0
        if item not in avgUdp.keys():
            avgUdp[item] = 0
        if item not in avgUnix.keys():
            avgUnix[item] = 0
        if item not in procInGroup:
            groupData[item] = [appsUsed[item], avgFifos[item], avgPipes[item], avgTcp[item], avgUdp[item], avgUnix[item]]
        else:
            # Find what group it should be in
            targetGroup = FindGroup(groups, item)
            groupData[targetGroup][0].append(appsUsed[item])
            groupData[targetGroup][1].append(avgFifos[item])
            groupData[targetGroup][2].append(avgPipes[item])
            groupData[targetGroup][3].append(avgTcp[item])
            groupData[targetGroup][4].append(avgUdp[item])
            groupData[targetGroup][5].append(avgUnix[item])
    # For the groups, average their results
    for item in groups.keys():
        group = groupData[item]
        groupData[item][0] = max(group[0])
        groupData[item][1] = sum(group[1])
        groupData[item][2] = sum(group[2])
        groupData[item][3] = sum(group[3])
        groupData[item][4] = sum(group[4])
        groupData[item][5] = sum(group[5])
    return groupData


def WriteGroupFile(dicts):
    # Get the groups
    groups, procInGroup = GetGroups()
    groupData = CreateGroupData(dicts, groups, procInGroup)
    procAlpha = sorted(groupData.keys(), key = lambda s: s.casefold())
    with open(GROUPED_RESULTS, "w") as groupFile:
        groupFile.write(f"{'APP NAME':40}{'NUM MACHINES':12}{'AVG FIFOS':12}{'AVG PIPES':12}{'AVG TCP':12}{'AVG UDP':12}{'AVG UNIX':12}\n")
        for proc in procAlpha:
            item = groupData[proc]
            groupFile.write(f"{proc:40}{item[0]:12}{item[1]:12}{item[2]:12}{item[3]:12}{item[4]:12}{item[5]:12}\n")



# MAIN METHOD

# Only print out arguments if given command line argument True
args = sys.argv
if len(args) < 2:
    debug = False
else:
    debug = args[1]

# Get all of the zip files
zips = glob.glob(FILE_PREFIX + "*ipcFiles.zip")

userCount = 0
appsUsed = dict()
percentApps = dict()
fifos = dict()
avgFifos = dict()
pipes = dict()
avgPipes = dict()
tcp = dict()
avgTcp = dict()
udp = dict()
avgUdp = dict()
unix = dict()
avgUnix = dict()

for filename in zips:
    userCount += 1
    number = filename.split(".")[2].split("/")[2]
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
AverageAppearances(fifos, avgFifos)
AverageAppearances(pipes, avgPipes)
AverageAppearances(tcp, avgTcp)
AverageAppearances(udp, avgUdp)
AverageAppearances(unix, avgUnix)
CalculatePercentages(percentApps, appsUsed, userCount)

# Sort the keys by decreasing values (so highest value-keys at beginning)
topFifos = list(sorted(avgFifos, key=avgFifos.__getitem__, reverse=True))
topPipes = list(sorted(avgPipes, key=avgPipes.__getitem__, reverse=True))
topTcp = list(sorted(avgTcp, key=avgTcp.__getitem__, reverse=True))
topUdp = list(sorted(avgUdp, key=avgUdp.__getitem__, reverse=True))
topUnix = list(sorted(avgUnix, key=avgUnix.__getitem__, reverse=True))
topApps = list(sorted(percentApps, key=percentApps.__getitem__, reverse=True))

# If there is already a results directory, remove it
if os.path.exists(RESULTS):
    subprocess.run(["rm", RESULTS])

subprocess.run(["touch", RESULTS])

# Print out the results if desired
if debug:
    count = input("How many apps to print out? ")
    PrintOutput("Apps", percentApps, topApps, count)
    count = input("How many fifos to print out? ")
    PrintOutput("Fifos", avgFifos, topFifos, count)
    count = input("How many pipes to print out? ")
    PrintOutput("Pipes", avgPipes, topPipes, count)
    count = input("How many TCP connections to print out? ")
    PrintOutput("TCP", avgTcp, topTcp, count)
    count = input("How many UDP connections to print out? ")
    PrintOutput("UDP", avgUdp, topUdp, count)
    count = input("How many UNIX domain sockets to print out? ")
    PrintOutput("UNIX Domain Sockets", avgUnix, topUnix, count)

# Always write the results to results file
WriteOutput("Apps", percentApps, topApps, appsUsed)
WriteOutput("Fifos", avgFifos, topFifos, appsUsed)
WriteOutput("Pipes", avgPipes, topPipes, appsUsed)
WriteOutput("TCP", avgTcp, topTcp, appsUsed)
WriteOutput("UDP", avgUdp, topUdp, appsUsed)
WriteOutput("UNIX Domain Sockets", avgUnix, topUnix, appsUsed)

# Also write out the grouped results to a grouped file
if os.path.exists(GROUPED_RESULTS):
    subprocess.run(["rm", GROUPED_RESULTS])

subprocess.run(["touch", GROUPED_RESULTS])

dicts = [appsUsed, avgFifos, avgPipes, avgTcp, avgUdp, avgUnix]
WriteGroupFile(dicts)