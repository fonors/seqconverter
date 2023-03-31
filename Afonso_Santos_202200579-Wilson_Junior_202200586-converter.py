#!/usr/bin/env python3
'''
    FNP Sequence File Converter - A FASTA, NEXUS and Phylip file converter
    Copyright (C) 2023  fonors & Wil-s0n

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import argparse
from sys import stderr, exit
from textwrap import wrap

parser = argparse.ArgumentParser(
                    prog = 'Sequence Storage File Converter',
                    description = 'A file converter in Python that converts FASTA, NEXUS and Phylip files.',
                    epilog = 'Does not work on "interleave" NEXUS or Phylip files.')

parser.add_argument("-i", "--input", help="Takes the source file for conversion")
parser.add_argument("-o", "--output", help="Takes the input file and converts to one with the name and extension provided here")
args = parser.parse_args()

def inputfirstln(inputfile):
    """
    Returns the first line found in the file.
    """
    with open(inputfile, "r") as inputfile:
        for line in inputfile:
            line = line.strip()
            inputfirstln = line
            break
    return inputfirstln

def filetype(inputfile):
    """
    Returns a string containing the input file's format.
    """
    inputfirstline = inputfirstln(inputfile)
    with open(inputfile, "r") as inputfile:
        filetype = None
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
    fileformat = filetype(inputfile)
    with open(inputfile, "r") as inputfile:
        seqdict = {}
        if fileformat == "FASTA":
            for line in inputfile:
                line = line.strip()
                if line.startswith(">"):
                    seqname = line[1:]
                    seqdict[seqname] = ""
                else:
                    seqdict[seqname] += line
                    seqdict[seqname] = seqdict[seqname].lower()
        elif fileformat == "NEXUS":
            for line in inputfile:
                line = line.strip()
                if "     " in line:
                    seqstart = line.index("     ") + 5
                    seqname_end = line.index("     ")
                    seqname = line[:seqname_end]
                    seqdict[seqname] = line[seqstart:]
        elif fileformat == "Phylip":
            for line in inputfile:
                line = line.strip()
                if "   " in line:
                    seqstart = line.index("   ") + 3
                    seqname_end = line.index("   ")
                    seqname = line[:seqname_end]
                    seqdict[seqname] = line[seqstart:]
        else:
            print("File provided isn't a valid FASTA, NEXUS or Phyilip format.", file=stderr)
            exit()
    return seqdict

def maxseqlen(inputfile):
    """
    Uses the fileanalyser() function to dermine the biggest sequence found within a certain source file.
    """
    seqdict = fileanalyser(inputfile)
    seqlist = []
    for seq in seqdict:
        seqlist.append(seqdict[seq])
    #maxseqlen = max(seq.seqlen() for seq in seqlist)
    maxseqlen = max(len(seq) for seq in seqlist)
    return maxseqlen

def dnacheck(inputfile):
    """
    Uses the fileanalyser() function and then checks a given sequence for thiamine or uracile to determine if the sequence is DNA or RNA.
    """
    seq_dict = fileanalyser(inputfile)
    for seq in seq_dict:
        current_sequence = seq_dict[seq].upper()
        if "U" in current_sequence:
            isdna = False
        elif "T" in current_sequence:
            isdna = True
    return isdna

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
    maxseqlength = maxseqlen(inputfile)
    isdna = dnacheck(inputfile)
    with open(outputfile, "w") as newnexusfile:
        newnexusfile.write("#NEXUS\n\n")
        newnexusfile.write("BEGIN DATA;\n")
        newnexusfile.write(f"DIMENSIONS NTAX={str(len(seqdict))} NCHAR={str(maxseqlen(inputfile))};\n")
        if isdna:
            newnexusfile.write("FORMAT DATATYPE=DNA MISSING=N GAP=-;\n")
        else:
            newnexusfile.write("FORMAT DATATYPE=RNA MISSING=N GAP=-;\n")
        newnexusfile.write("MATRIX\n\n")
        for seq in seqdict:
            #if seqdict[seq].seqlen() < maxseqlength:
            if len(seqdict[seq]) < maxseqlength:
                #ngaps = maxseqlength - seqdict[seq].seqlen()
                ngaps = maxseqlength - len(seqdict[seq])
                newnexusfile.write(f"{seq}     {seqdict[seq]}")
                for gaps in range(ngaps):
                    newnexusfile.write("-")
                newnexusfile.write("\n")
            else:
                newnexusfile.write(f"{seq}     {seqdict[seq]}\n")
        newnexusfile.write(";\n")
        newnexusfile.write("\nEND;")

def phylip_writer(inputfile, outputfile):
    """
    Takes the intermediate data from a file using the fileanalyser() function and creates a Phylip file.
    """
    seqdict = fileanalyser(inputfile)
    maxseqlength = maxseqlen(inputfile)
    with open(outputfile, "w") as newphylipfile:
        newphylipfile.write(f"{str(len(seqdict))} {str(maxseqlen(inputfile))}\n")
        for seq in seqdict:
            #if seqdict[seq].seqlen() < maxseqlength:
            if len(seqdict[seq]) < maxseqlength:
                #ngaps = maxseqlength - seqdict[seq].seqlen()
                ngaps = maxseqlength - len(seqdict[seq])
                newphylipfile.write(f"{seq}   {seqdict[seq]}")
                for gaps in range(ngaps):
                    newphylipfile.write("-")
                newphylipfile.write("\n")
            else:
                newphylipfile.write(f"{seq}   {seqdict[seq]}\n")

def converter(inputfile, outputfile):
    """
    Determines the output format and executes the adequate function to convert to it.
    """
    try:
        if outputfile.endswith(".fasta"):
            fasta_writer(inputfile, outputfile)
        elif outputfile.endswith(".nexus"):
            nexus_writer(inputfile, outputfile)
        elif outputfile.endswith(".phy"):
            phylip_writer(inputfile, outputfile)
        else:
            print("Output file does not have a valid extension! Try '.fasta', '.nexus' or '.phy'.", file=stderr)
            exit()
    except TypeError as err:
        print("You did not provide an input file!", file=stderr)
    except AttributeError as err:
        print("You did not provide an output file!", file=stderr)

converter(args.input, args.output)