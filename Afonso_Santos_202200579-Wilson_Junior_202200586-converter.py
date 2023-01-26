#!/usr/bin/env python3
from sys import argv, stderr, exit
import argparse

#inputfile = open(argv[1], "r")
#outputfile = open(argv[2], "w")

def inputreader(inputf):
    for line in inputfile:
        line = line.strip()
        inputcontent += line
    inputfile.seek(0)
    for line in inputfile:
        line = line.strip()
        inputfirstln = line
        break
    inputfile.seek(0)
    return inputcontent, inputfirstln

def fastacheck(file):
    if file.startswith(">"):
        fasta = True
    else:
        fasta = False
    return fasta

def nexuscheck(file):
    if file.startswith("#NEXUS"):
        nexus = True
    else:
        nexus = False
    return nexus

def phylipcheck(file):
    if int(inputfistln):
        phylip = True
    else:
        phylip = False
    return phylip

#inputfile.close()
