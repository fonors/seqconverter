#!/usr/bin/env python3
from sys import argv, stderr, exit
import argparse

inputfile = open(argv[1], "r")
#outputfile = open(argv[2], "w")

def fileanalyser(inputf):
    """
    Takes the input gathered using the inputreader() function and stores essential data for conversion. Serves as a middle ground solution
    """
    if filetype == "FASTA":
        for line in inputf:
            line = line.strip()
            if line.startswith(">"):
                line = line[1:]
                seqname = line
            else:
                seqdict[seqname] += line
#    elif filetype == "NEXUS": 

def inputfirstln(inputf):
    """
    Returns the first line found in the file.
    """
    for line in inputf:
        line = line.strip()
        inputfirstln = line
        break
    inputf.seek(0)
    return inputfirstln

def filetype(inputf):
    """
    Returns a string containing the input file's format.
    """
    inputfirstline = inputfirstln(inputf)
    if inputf.startswith(">"):
        filetype = "FASTA"
    if inputf.startswith("#NEXUS"):
        filetype = "NEXUS"
    try:
        if int(inputfirstline):
            filetype = "Phylip"
    except ValueError as err:
        filetype = None
    return filetype

class Sequence():
    '''This class defines a DNA sequence'''
    def seqlen(self):
        """
        Checks the length of the sequence.
        """
        seqlen = len(self)
        return seqlen

inputfile.close()