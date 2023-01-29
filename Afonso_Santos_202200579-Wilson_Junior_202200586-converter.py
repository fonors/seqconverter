#!/usr/bin/env python3
from sys import argv, stderr, exit
import argparse

inputfile = open(argv[1], "r")
#outputfile = open(argv[2], "w")

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
    filetype = None
    inputfirstline = inputfirstln(inputf)
    if inputfirstline.startswith(">"):
        filetype = "FASTA"
    elif inputfirstline.startswith("#NEXUS"):
        filetype = "NEXUS"
    else:
        try:
            if int(inputfirstline):
                filetype = "Phylip"
        except ValueError as err:
            filetype = filetype
    return filetype

def fileanalyser(inputf):
    """
    Takes an input file and stores essential data for conversion. Serves as a middle ground solution
    """
    seqdict = {}
    filetype = filetype(inputf)
    if filetype == "FASTA":
        for line in inputf:
            line = line.strip()
            if line.startswith(">"):
                line = line[1:]
                seqname = line
            else:
                seqdict[seqname] += line
            inputf.seek(0)
    elif filetype == "NEXUS":
        for line in inputf:
            line = line.strip()
            if line.upper() != "#NEXUS" and line.endswith(";") and line.upper() != "MATRIX":
                seqname = line[:" "]
            else:
                seqdict[seqname] += line.upper() 
                seqdict[seqname[0]] = seq[1]
            inputf.seek(0)


class Sequence():
    '''This class defines a DNA sequence'''
    def seqlen(self):
        """
        Checks the length of the sequence.
        """
        seqlen = len(self)
        return seqlen

def phylip_writer(seqdict, outputf):
    with open(output, "w"):
        output.write(str(len(seqdict[seq])) + " " +
inputfile.close
