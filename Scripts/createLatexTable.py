#!/bin/python

NUM_COLS = 7
INPUT_FILE = "../ThesisData/grouped_results.txt"
OUTPUT_FILE = "../ThesisPaper/latexTable.txt"

with open(INPUT_FILE, "r") as inFile:
    with open(OUTPUT_FILE, "w") as outFile:
        for line in inFile:
            splitLine = line.split("  ")
            splitLine = list(filter(None, splitLine))
            splitLine = splitLine[ : NUM_COLS]
            newLine = ""
            for element in splitLine:
                if "\\x20" in element:
                    element = element.replace("\\x20", " ")
                if "_" in element:
                    element = element.replace("_", "\\_")
                newLine += (element + " & ")
            # remove the last ampersand
            newLine = newLine[ : -2]
            newLine += "\\\\ \\hline\n"
            outFile.write(newLine)