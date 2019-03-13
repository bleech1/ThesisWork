#!/bin/python
# Script to remove usernames from output

import sys
import re

filename = sys.argv[1]
username = sys.argv[2].split()
if not username:
	exit()	
secretNum = filename.split(".", 1)[0]
restFilename = filename.split(".", 1)[1]
outputFile = open(secretNum + ".a" + restFilename, "a", encoding="latin-1")

with open(filename, encoding="latin-1") as inputFile:
	for row in inputFile:
		newRow = row
		# Anonymize for all usernames on the computer
		for name in username:
			regex = r"((?<=\W)" + re.escape(name) + r"(?=\W)|(^" + re.escape(name) + r"(?=\W))|(\s" + re.escape(name) + r"\s))"
			newRow = re.sub(regex, "USERNAME", newRow)
		outputFile.write(newRow)


