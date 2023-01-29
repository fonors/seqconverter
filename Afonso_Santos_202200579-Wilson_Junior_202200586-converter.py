#!/usr/bin/env python3
from sys import argv, stderr, exit
from textwrap import wrap
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
            if int(inputfirstline.replace(" ", "")):
                filetype = "Phylip"
        except ValueError as err:
            filetype = None
            print("File provided isn't a valid FASTA, NEXUS or Phyilip format.", file=stderr)
            exit()
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
                seqname = line[1:]
            else:
                seqdict[seqname] += line
    elif fformat == "NEXUS":
        for line in inputf:
            line = line.strip()
            if "     " in line:
                seqstart = line.index("     ") + 5
                seqname_end = line.index("     ")
                seqname = line[:seqname_end]
                seqdict[seqname] = line[seqstart:]
    elif fformat == "Phylip":
        for line in inputf:
            line = line.strip()
            if "   " in line:
                seqstart = line.index("   ") + 3
                seqname_end = line.index("   ")
                seqname = line[:seqname_end]
                seqdict[seqname] = line[seqstart:]
    else:
        print("File provided isn't a valid FASTA, NEXUS or Phyilip format.", file=stderr)
        exit()
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

def Nexus_writer(seqdict, outputf):
    with open(outputf, "w") as file:
        file.write("#NEXUS\n")
        file.write("BEGIN DATA;\n")
        file.write("DIMENSIONS NTAX=" + str(len(seqdict))) + "NACHAR=" + str(seqlen) + ";\n")
        file.write("FORMAT DATATYPE=DNA MISSING=N GAP=-;\n")
        file.write("MATRIX\n")
        for seq in seqdict:
            file.write(seq + "     " + seqdict[seq] + "\n")
        file.write(";\n")
        fie.write("END;")  

#def phylip_writer(seqdict, outputf):
#    with open(output, "w"):
#        output.write(str(len(seqdict[seq])) + " " +

#def outputformat(outputf):
#    if outputf.endswith(".fasta"):
#        converttofasta()
#    elif outputf.endswith(".nexus")
#    elif outputf.endswith(".phy")
#    else:
#        print("Output file does not have a valid extension! Try '.fasta', '.nexus' or '.phy'.", file=stderr)
#        exit()

def converttofasta(inputf, outputf):
    seqdict = fileanalyser(inputf)
    with open(outputf, "w") as newfastaf:
        for seq in seqdict:
            seqdict[seq] = seqdict[seq].upper().replace("-", "")
            newfastaf.write(f">{seq}\n")
            newfastaf.write("\n".join(wrap(seqdict[seq], 80)))
            newfastaf.write("\n\n")

inputfile.close
