#!/usr/bin/env python3
from sys import argv, stderr, exit
import argparse

inputfile = open(argv[1], "r")
#outputfile = open(argv[2], "w")

def inputreader(inputf):
    inputcontent = ""
    for line in inputfile:
        line = line.strip()
        inputcontent += line
    inputfile.seek(0)
    return inputcontent

def inputfirstln(inputf):
    for line in inputfile:
        line = line.strip()
        inputfirstln = line
        break
    inputfile.seek(0)
    return inputfirstln

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
    try:
        if int(inputfirstline):
            phylip = True
    except ValueError as err:
        phylip = False
    return phylip

def inputchecker(file):
    fasta = fastacheck(file)
    nexus = nexuscheck(file)
    phylip = phylipcheck(file)
    if fasta:
    elif nexus:
    elif phylip:
    else:
        print("File provided isn't a valid FASTA, NEXUS or Phylip file.", file=stderr)

inputfile.close()
