#!/bin/python
# Script to get what each named pipe 
# and UNIX domain socket are connected to

import sys

filename = sys.argv[1]
secretNum = filename.split(".")[0]
name = filename.split(".")[1]

deviceDict = dict()
with open(filename, encoding="latin-1") as inputFile:
    for row in inputFile:
        splitRow = row.split()
        if len(splitRow) < 0:
            continue
        command = splitRow[0]
        if command == "COMMAND":
            continue
        if len(splitRow) < 6:
            continue
        user = splitRow[2]
        device = splitRow[5]
        # Get the user and command for each device in use
        if device in deviceDict.keys():
            deviceDict[device].append((command, user))
        else:
            deviceDict[device] = [(command, user)]
with open(filename, encoding="latin-1") as inputFile:
    with open(secretNum + ".Conn" + name + ".txt", "w", encoding="latin-1") as outputFile:
        # For each row, print the command and user that
        # this row is connected to
        for row in inputFile:
            splitRow = row.split()
            if len(splitRow) < 8:
                outputFile.write(row)
                continue
            device = splitRow[7]
            if not device.startswith("->0x"):
                outputFile.write(row)
                continue
            else:
                device = device[2:]
            newRow = row[:-1]
            if device in deviceDict.keys():
                newRow += "\t("
                for entry in deviceDict[device]:
                    newRow += entry[0] + ", " + entry[1] + " || "
                newRow += ")"
            outputFile.write(newRow + "\n")