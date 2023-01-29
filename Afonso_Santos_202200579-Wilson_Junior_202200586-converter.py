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
    fformat = filetype(inputf)
    if fformat == "FASTA":
        for line in inputf:
            line = line.strip()
            if line.startswith(">"):
                line = line[1:]
                seqname = line
            else:
                seqdict[seqname] += line
    elif fformat == "NEXUS":
        for line in inputf:
            line = line.strip()
            if "     " in line:
                startseq = line.index("     ") + 5
                seqname_end = line.index("     ")
                seqname = line[:seqname_end]
                seqdict[seqname] = line[startseq:]
    inputf.seek(0)
    return seqdict

class Sequence():
    '''This class defines a DNA sequence'''
    def seqlen(self):
        """
        Checks the length of the sequence.
        """
        seqlen = len(self)
        return seqlen

#def phylip_writer(seqdict, outputf):
#    with open(output, "w"):
#        output.write(str(len(seqdict[seq])) + " " +

inputfile.close
