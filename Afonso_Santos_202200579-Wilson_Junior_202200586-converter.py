#!/usr/bin/env python3
from sys import argv, stderr, exit
import argparse

inputfile = open(argv[1], "r")
#outputfile = open(argv[2], "w")

def inputreader(inputf):
    inputcontent = ""
    for line in inputf:
        line = line.strip()
        inputcontent += line
    inputf.seek(0)
    return inputcontent

def inputfirstln(inputf):
    for line in inputf:
        line = line.strip()
        inputfirstln = line
        break
    inputf.seek(0)
    return inputfirstln

def fastacheck(inputf):
    if inputf.startswith(">"):
        fasta = True
    else:
        fasta = False
    return fasta

def nexuscheck(inputf):
    if inputf.startswith("#NEXUS"):
        nexus = True
    else:
        nexus = False
    return nexus

def phylipcheck(inputf):
    try:
        if int(inputfirstline):
            phylip = True
    except ValueError as err:
        phylip = False
    return phylip

class Sequence():
    '''This class defines a DNA sequence'''
    def seqlen(self):
        """
        Checks the length of the sequence.
        """
        seqlen = len(self)
        return seqlen

def inputchecker(inputf):
    fasta = fastacheck(inputf)
    nexus = nexuscheck(inputf)
    phylip = phylipcheck(inputf)
#    if fasta:
#    elif nexus:
#    elif phylip:
#    else:
#        print("File provided isn't a valid FASTA, NEXUS or Phylip file.", file=stderr)

inputfile.close()