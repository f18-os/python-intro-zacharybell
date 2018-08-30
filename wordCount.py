#! /usr/bin/env python3

import sys
import os
import string
import re

# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()

textFname = sys.argv[1]
outputFname = sys.argv[2]

#make sure text files exist
if not os.path.exists(textFname):
    print ("text file input %s doesn't exist! Exiting" % textFname)
    exit()

def addStringArrayToDict(d, strArray):
    for s in strArray:
        if s in d:
            d[s] += 1
        else:
            d[s] = 1

# read input text file and store counts in dictionary
with open(textFname, 'r') as textFile:
    textKey = {}
    for line in textFile:
        line = re.sub(r"[{}]".format(string.punctuation), ' ', line)
        addStringArrayToDict(textKey, line.lower().split())

# format and write keys/counts to output file
with open(outputFname, 'w') as outputFile:
    for k, v in sorted(textKey.items()):
        outputFile.write(k + ' ' + str(v) + '\n')
