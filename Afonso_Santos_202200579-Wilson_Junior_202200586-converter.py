#!/usr/bin/env python3
import argparse
from sys import stderr, exit
from textwrap import wrap

class Sequence():
    '''This class defines a DNA sequence'''
    def seqlen(self):
        """
        Checks the length of the sequence.
        """
        seqlen = len(self)
        return seqlen

def inputfirstln(inputfile):
    """
    Returns the first line found in the file.
    """
    for line in inputfile:
        line = line.strip()
        inputfirstln = line
        break
    inputfile.seek(0)
    return inputfirstln

def filetype(inputfile):
    """
    Returns a string containing the input file's format.
    """
    filetype = None
    inputfirstline = inputfirstln(inputfile)
    if inputfirstline.startswith(">"):
        filetype = "FASTA"
    elif inputfirstline.startswith("#NEXUS"):
        filetype = "NEXUS"
    else:
        try:
            if int(inputfirstline.replace(" ", "")):
                filetype = "Phylip"
        except ValueError as err:
            filetype = None
            print("File provided isn't a valid FASTA, NEXUS or Phyilip format.", file=stderr)
            exit()
    return filetype

def fileanalyser(inputfile):
    """
    Takes an input file and stores essential data for conversion. Serves as a middle ground solution.
    """
    seqdict = {}
    fileformat = filetype(inputfile)
    if fileformat == "FASTA":
        for line in inputfile:
            line = line.strip()
            if line.startswith(">"):
                seqname = line[1:]
            else:
                seqdict[seqname] += line
                seqdict[seqname] = Sequence()
    elif fileformat == "NEXUS":
        for line in inputfile:
            line = line.strip()
            if "     " in line:
                seqstart = line.index("     ") + 5
                seqname_end = line.index("     ")
                seqname = line[:seqname_end]
                seqdict[seqname] = line[seqstart:]
                seqdict[seqname] = Sequence()
    elif fileformat == "Phylip":
        for line in inputfile:
            line = line.strip()
            if "   " in line:
                seqstart = line.index("   ") + 3
                seqname_end = line.index("   ")
                seqname = line[:seqname_end]
                seqdict[seqname] = line[seqstart:]
                seqdict[seqname] = Sequence()
    else:
        print("File provided isn't a valid FASTA, NEXUS or Phyilip format.", file=stderr)
        exit()
    inputfile.seek(0)
    return seqdict

def fasta_writer(inputfile, outputfile):
    """
    Takes the intermediate data from a file using the fileanalyser() function and creates a FASTA file.
    """
    seqdict = fileanalyser(inputfile)
    with open(outputfile, "w") as newfastafile:
        for seq in seqdict:
            seqdict[seq] = seqdict[seq].upper().replace("-", "")
            newfastafile.write(f">{seq}\n")
            newfastafile.write("\n".join(wrap(seqdict[seq], 80)))
            newfastafile.write("\n\n")

def nexus_writer(inputfile, outputfile):
    """
    Takes the intermediate data from a file using the fileanalyser() function and creates a NEXUS file.
    """
    seqdict = fileanalyser(inputfile)
    with open(outputfile, "w") as newnexusfile:
        newnexusfile.write("#NEXUS\n\n")
        newnexusfile.write("BEGIN DATA;\n")
        newnexusfile.write(f"DIMENSIONS NTAX={str(len(seqdict))} NACHAR={str(seqdict[seq].seqlen())};\n")
        newnexusfile.write("FORMAT DATATYPE=DNA MISSING=N GAP=-;\n")
        newnexusfile.write("MATRIX\n\n")
        for seq in seqdict:
            newnexusfile.write(f"{seq}     {seqdict[seq]}\n")
        newnexusfile.write(";\n")
        newnexusfile.write("END;")

def phylip_writer(inputfile, outputfile):
    """
    Takes the intermediate data from a file using the fileanalyser() function and creates a Phylip file.
    """
    seqdict = fileanalyser(inputfile)
    with open(outputfile, "w") as newphylipfile:
        newphylipfile.write(f"{str(len(seqdict))} {str(seqlen)}\n")
        for seq in seqdict:
            newphylipfile.write(f"{seq}   {seqdict[seq]}\n")

def output_writer(outputfile):
    """
    Determines the output format and executes the adequate function to convert to it.
    """
    if outputfile.endswith(".fasta"):
        converttofasta(outputfile)
    elif outputfile.endswith(".nexus"):
        nexus_writer(outputfile)
    elif outputfile.endswith(".phy"):
        phylip_writer(outputfile)
    else:
        print("Output file does not have a valid extension! Try '.fasta', '.nexus' or '.phy'.", file=stderr)
        exit()