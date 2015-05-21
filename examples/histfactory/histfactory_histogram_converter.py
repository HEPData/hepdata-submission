#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
histfactory_histogram_converter.py - Convert objects in root files to hepdata format.
Based on hepconverter, but with different format.

Todo:
Focus on histograms that inherit from TH1 (includes 2d and 3d histograms)
input is list of 3-tuples (ROOT files input file, path, histogram name)
Output yaml should have aggregate the histograms in one file with 3-tuple 
encoded before bin center, bin content, and bin error .


--- Supposedly recent dump from: python hepconverter.py -h
usage: hepconverter.py [-h] [-v] [-i INPUTFILES [INPUTFILES ...]]
                       [-g GROUP [GROUP ...]] [-y OVERLAY [OVERLAY ...]]
                       [-s SKIP [SKIP ...]] [-q ONLY [ONLY ...]]
                       [-r name xlow xhigh] [--float-format FLOATFMT]
                       [-o OUTPUT] [-z] [-n] [-e]
                       
Converts objects in root files to hepdata format.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version string
  -i INPUTFILES [INPUTFILES ...], --input INPUTFILES [INPUTFILES ...]
                        List of input files
  -g GROUP [GROUP ...], --group-suffixes GROUP [GROUP ...]
                        Group objects with the same name but different
                        suffixes together. Example: If input has x_sys and
                        x_stat and argument "-g sys stat" is given the code
                        will keep the 2 errors for each bin in a single
                        histogram.
  -y OVERLAY [OVERLAY ...], --overlay OVERLAY [OVERLAY ...]
                        Overlay multiple histograms/graphs on the same axes.
                        Example: if you have histograms called pT_MC and
                        pT_data and specify "-y MC data" then both will use a
                        common x axis. Note that "MC" and "data" can be
                        anywhere in the histogram names, as grouped suffixes
                        may also be specified (see the -g option).
  -s SKIP [SKIP ...], --skip SKIP [SKIP ...]
                        Skip any histogram whose name contains any of these
                        strings
  -q ONLY [ONLY ...], --test ONLY [ONLY ...]
                        Only process histograms whose names contain one of
                        these strings. Usually used for testing, hence the
                        name.
  -r name xlow xhigh, --range name xlow xhigh
                        Reject entries in histogram NAME outside range [xlow,
                        xhigh]. Can be used multiple times
  --float-format FLOATFMT
  -o OUTPUT, --output OUTPUT
                        Name of output data set
  -z, --zero            Supress entries with y-bin == 0
  -n, --nan             Supress entries containing NaN
  --inf                 Supress entries containing Inf
  -e, --supress-errors  Present results without errors
  
Happy converting!
---

Version: 0.0 rootconverter.py created: Thomas Burgess 17 Dec 2010
Version: 1.0 hepconverter.py Created: Thomas Burgess 30/1-2012
Version: 1.1 hepconverter.py Created: Mike Flowerdew 30/02/2012 (Basic functionality)
Version: 1.2 hepconverter.py Created: Mike Flowerdew 26/04/2012 (Groups and overlays)
Version: 2.0 hepconverter.py Created: Mike Flowerdew 19/05/2014 (Changed output formatting)
Version: 2.1 hepconverter.py Created: Mike Flowerdew 16/07/2014 (Added warnings for Inf and NaN values)
"""

#############################################################################
# Imports
import sys
from array import array
import itertools
import datetime

# Get ROOT, override pyroots command line, (ROOT > 5.24)
try:
    import ROOT
    ROOT.PyConfig.IgnoreCommandLineOptions = True
except Exception, e :
    print e
    raise Exception("ERROR, install python enabled ROOT >= v5.24 to use this package")

# Get element tree for xml handling (python 2.5+)
from xml.etree import ElementTree as etree

# Get argparse (python with argparse installed, or any 2.7+)
try:
    import argparse
except Exception, e:
    print e
    raise Exception("ERROR, run on lxplus with athena, install argparse, or just use python 2.7+ to use this package")

#############################################################################
# Global constants

allowedRootClasses = (
    "TH1",
    "TH1D",
    "TH1F",
    "TH1I",
    "TH1S",
    "TH2",
    "TH2D",
    "TH2F",
    "TH2I",
    "TH2S",
    "TProfile",
    "TProfile2D",
    "TGraph",
    "TGraph2D",
    "TGraphErrors",
    "TGraph2DErrors",
    "TGraphAsymmErrors"
)


def makeHepData(objlist, fmt, output):
    """Write information in HepData format.
    objlist is a list of dictionaries with the data to write.
    The first object in the list is "primary", and determines things
    like the axis titles and general descriptions.
    """

    def deROOTtitle(obj):
        """Removes ROOT's special syntax for a literal semicolon,
        needed for HTML tags"""
        return obj.GetTitle().replace("#;",";").replace("#semicolon",";")

    primary = objlist[0]
    nametowrite = primary["basename"]
    print "%s: Merging information from %i objects"%(primary["basename"],len(objlist))

    # Header information - unknown to this script, just a skeleton
    # See hepdata.cedar.ac.uk/resource/sample.input

    # Start a table
    output.write('\n\n*dataset:\n')
    output.write('*location: Figure GIVE FIGURE NUMBER\n')
    output.write('*dscomment: '+deROOTtitle(primary['obj'])+'\n')
    output.write('*reackey: P P --> GIVE THE PRODUCTION PROCESSES\n')
    output.write('*obskey: GIVE KEY FOR Y-AXIS VARIABLE\n')
    output.write('*qual: . : GIVE COLUMN EXPLANATIONS, IF YOU USED OVERLAYS\n')
    output.write('*qual: RE : P P --> GIVE THE PRODUCTION PROCESSES + DECAYS (IF RELEVANT)\n')
    output.write('*qual: SQRT(S) IN GEV : 8000.0\n')

    # Work out the axis titles
    # This is complicated, because any independent axis must be called "x"
    # and any dependent axis must be called "y", including all overlays
    xtitles = []
    ytitles = []
    for obj in objlist:
        for label in obj['labels']:
            # If this is an uncertainty, skip it
            if 'd' in label or 'low' in label or 'high' in label:
                continue

            if 'x' in label:
                xtitles.append(deROOTtitle(obj['obj'].GetXaxis()))

            elif 'y' in label:
                if obj['dim'] > 2:
                    # 3D object, this is "really" an x-axis
                    xtitles.append(deROOTtitle(obj['obj'].GetYaxis()))
                else:
                    ytitles.append(deROOTtitle(obj['obj'].GetYaxis()))

            elif 'z' in label:
                if obj['dim'] > 3:
                    # You never know ;)
                    xtitles.append(deROOTtitle(obj['obj'].GetZaxis()))
                else:
                    ytitles.append(deROOTtitle(obj['obj'].GetZaxis()))
                
    # Print the axis titles in HepData format
    output.write('*yheader: ')
    output.write(' : '.join(ytitles))
    output.write('\n*xheader: ')
    output.write(' : '.join(xtitles))
    output.write('\n')

    # Print the specification of the axis dimensions
    output.write('*data: ')
    output.write(' : '.join(['x' for x in xtitles] + ['y' for y in ytitles]))
    output.write('\n')

    for i in range(len(primary[primary['labels'][0]])):
        substrs = [''] # To ensure a space at the beginning
        for obj in objlist:
            # See if the bin exists
            try:
                didcentralvalue = False

                for ilabel,label in enumerate(obj['labels']):

                    value = ('{0:'+fmt+'}').format(obj[label][i])

                    if 'low' in label: # low edge of a bin
                        substrs.extend(['(BIN='+value, 'TO'])

                    elif 'high' in label: # high edge of a bin
                        substrs.extend([value+')'])
                    
                    elif label[-1] in '+-' or 'd' in label: # Asymmetric or symmetric uncertainty
                        
                        # Do we have details on the uncertainty? (do not print if this object also had the central value)
                        hasdetail = bool(obj['errordetail']) and not didcentralvalue
                        # Did the last entry already have an open bracket?
                        openbracket = '(' in substrs[-1]
                        # Is this a symmetric error?
                        symmetric = label[-1] not in '+-'
                        sign = '' if symmetric else label[-1]
                        
                        if symmetric and not hasdetail:
                            # Easy case, just get this out of the way
                            substrs.extend(['+-',value])
                            continue

                        # Here we either have details, and/or an asymmetric error
                        # All concatenated without spaces
                        thisstr = ''

                        # Write the first few characters
                        if sign is '-':
                            thisstr += ',' # Down error always follows an up error
                        elif hasdetail: # Only needs introduction if there's some detail
                            if openbracket: thisstr += ',' # Not the first in a list of errors
                            else: thisstr += '(' # First error in list
                            # Either way, we need to clarify what the error is
                            # Convention seems to be to capitalise it
                            thisstr += obj['errordetail'][0].upper()
                            thisstr += '='

                        # Display the numerical error value
                        thisstr += sign
                        thisstr += value

                        # Finish off description of systematic, if necessary
                        if len(obj['errordetail']) > 1:
                            thisstr += ':'
                            thisstr += '_'.join(obj['errordetail'][1:])
                        if hasdetail:
                            thisstr += ')'

                        # Is this a new systematic entry?
                        if openbracket or sign is '-':
                            substrs[-1] = substrs[-1].rstrip(')')
                            substrs[-1] += thisstr
                        else:
                            substrs.append(thisstr)

                    else: # Central value
                        if substrs[-1]:
                            substrs[-1] += ';'
                        substrs.append(value)
                        didcentralvalue = True

            except IndexError:
                print 'WARNING: Bin %i missing in object %s. This may indicate a problem with your input data'%(i,obj['name'])
#                 output.write('\t'.join([ '--' for l in obj['labels']] + ['']))
                substrs.extend(['--' for l in obj['labels']])
                raise

        output.write(' '.join(substrs))
        output.write(';\n')
    output.write('*dataend:\n')
    
def isnan(x):
    """
    return true if any of x is nan
    """
    return len(filter(lambda a: a != a, x)) != 0
        
def isinf(x):
    """
    return true if any of x is inf
    """
    return len(filter(lambda a: a == float('Inf'), x)) != 0
        
def cleanObjDict(objlist, cutZero = False, cutNaN = False, cutInf = False, cutXlow = 0, cutXhigh = 0 ):
    """
    clean out some entries in dict arrays
    """
    primary = objlist[0]
    bins = range(len(primary["x"])) # bin id's
    delbins = [] # bins to delete    
    for ibin in bins:
        if cutZero:
            deleteIt = True
            for obj in objlist:
                try:
                    try: nbin = obj["z"][ibin]
                    except KeyError: nbin = obj["y"][ibin]
                except IndexError:
                    print "WARNING: Bin %i missing in %s. Please double-check your input data"%(ibin,obj["name"])
                if nbin:
                    deleteIt = False
                    break
            if deleteIt:
                delbins += [ibin]
                continue
        if isnan([primary[label][ibin] for label in primary["labels"]] ):
            print "WARNING: NaN value found - please edit before uploading to HepData! (or remove with -n option)"
            if cutNaN:
                delbins += [ibin]
            continue
        if isinf([primary[label][ibin] for label in primary["labels"]] ):
            print "WARNING: Inf value found - please edit before uploading to HepData! (or remove with -inf option)"
            if cutInf:
                delbins += [ibin]
            continue
        if cutXlow < cutXhigh and (primary["x"][ibin] < cutXlow or primary["x"][ibin] > cutXhigh):
            delbins += [ibin]
            continue
    
    # Delete entries from each array with a label
    for obj in objlist:
        for label in obj["labels"]:
            for k in reversed(sorted(delbins)):
                try: obj[label].pop(k)
                except IndexError: # Missing bin, already printed a warning
                    pass

    if cutZero or cutNaN or cutInf or (cutXlow < cutXhigh):
        print "Removed ",
        if cutZero:
            print " : bins with 0 entries ",
        if cutNaN:
            print " : any NaN entries ",
        if cutInf:
            print " : any Inf entries ",
        if (cutXlow < cutXhigh):
            print " : any entries outside " + str(cutXlow) + " < x < " + str(cutXhigh),
        print
    
def extractRootObject(d):
    """
    extract and store root object data in a object dictionary d retrieved by getRootObjects

    Depending on what is available in the root objects different data and labels
    will be stored:
    * x, y - all objects
    * xlow, xhigh - histograms and graphs with errors in x
    * dy-, dy+ - histograms and graphs with errors in y    
    """
    name = d["name"]
    classname = d["class"]

    # Graphs
    if "TGraph" in classname:
        asymmerrors = "AsymmErrors" in classname
        bins = range(d["obj"].GetN())

        # Fill point values
        d["x"] = [d["obj"].GetX()[i] for i in bins]
        d["y"] = [d["obj"].GetY()[i] for i in bins]
        if d["dim"] > 2:
            d["z"] = [d["obj"].GetZ()[i] for i in bins]
           
        if not d["doerrors"]:

            d['labels'] = ['x','y']
            if d['dim'] > 2: d['labels'].append('z')

        else:

            # X errors
            d['labels'] = ['x']
            try:
                exlow = [d["obj"].GetErrorXlow(i) for i in bins]
                exhigh = [d["obj"].GetErrorXhigh(i) for i in bins]
            except AttributeError:
                exlow = [d["obj"].GetErrorX(i) for i in bins]
                exhigh = exlow
            # Check that errors are set
            if filter(None, exlow) or filter(None, exhigh):
                # Calculate bin start and end using asymmetric errors
                d["xlow"] = [d["x"][i] - exlow[i] for i in bins]
                d["xhigh"] = [d["x"][i] + exhigh[i] for i in bins]
                d['labels'].extend(['xlow','xhigh'])

            # Y errors
            d['labels'].append('y')
            equalErrors = False # Switch from a+b-c to a+-b notation
            try:
                eylow = [d["obj"].GetErrorYlow(i) for i in bins]
                eyhigh = [d["obj"].GetErrorYhigh(i) for i in bins]
                if eylow == eyhigh: equalErrors = True
            except AttributeError:
                eylow = [d["obj"].GetErrorY(i) for i in bins]
                eyhigh = eylow
                equalErrors = True
            # Check that errors are set
            if filter(None, eylow) or filter(None, eyhigh):
                if d["dim"] > 2:
                    d["ylow"] = [d["y"][i] - eylow[i] for i in bins]
                    d["yhigh"] = [d["y"][i] + eyhigh[i] for i in bins]
                    d['labels'].extend(['ylow','yhigh'])
                else:
                    if equalErrors:
                        d['dy'] = [e for e in eylow]
                        d['labels'].append('dy')
                    else:
                        d["dy-"] = [e for e in eylow]
                        d["dy+"] = [e for e in eyhigh]
                        d['labels'].extend(['dy+','dy-'])
            
            if d["dim"] > 2:
                # Z errors - always symmetric
                d['labels'].append('z')
                ez = [d["obj"].GetErrorZ(i) for i in bins]
                # Check that errors are set
                if filter(None, ez):
                    d['dz'] = [e for e in ez]
                    d['labels'].append('dz')


    # Histograms
    elif "TH" in classname or "TProfile" in classname:

        # Fill x-related quantities
        xaxis = d["obj"].GetXaxis()
        nx = xaxis.GetNbins()
        xbins = range(1, nx+1) # Removes under/overflow
        d["x"] = [xaxis.GetBinCenter(i) for i in xbins]
        d["xlow"] = [xaxis.GetBinLowEdge(i) for i in xbins]
        d["xhigh"] = [xaxis.GetBinUpEdge(i) for i in xbins]
        d['labels'] = ['x','xlow','xhigh'] if d['doerrors'] else ['x']

        if d["dim"] > 2:
            
            # Calculate how many y bins we have
            yaxis = d["obj"].GetYaxis()
            ny = yaxis.GetNbins()
            ybins = range(1, ny+1) # Removes under/overflow

            # Replicate the x axis info ny times
            d["x"] *= ny
            d["xlow"] *= ny
            d["xhigh"] *= ny

            # Fill y- and z-related quantities - each y result needs replication nx times
            if d['doerrors']:
                d['labels'].extend(['y','ylow','yhigh','z','dz'])
            else:
                d['labels'].extend(['y','z'])
            d["y"] = []
            d["ylow"] = []
            d["yhigh"] = []
            d["z"] = []
            d['dz'] = []
            for iy in ybins:
                d["y"] += [yaxis.GetBinCenter(iy)]*nx
                d["ylow"] += [yaxis.GetBinLowEdge(iy)]*nx
                d["yhigh"] += [yaxis.GetBinUpEdge(iy)]*nx
                for ix in xbins:
                    d["z"].append(d["obj"].GetBinContent(ix,iy))
                    d['dz'].append(d['obj'].GetBinError(ix,iy))
            # Check to see if z errors are good
            if not filter(None, d['dz']):
                del d['dz']
        else:
            # 1D: Fill y-related quantities
            if d['doerrors']:
                d['labels'].extend(['y','dy'])
            else:
                d['labels'].append('y')
            d["y"] = [d["obj"].GetBinContent(i) for i in xbins]
            d['dy'] = [d['obj'].GetBinError(i) for i in xbins]
            # Check to see if y errors are good
            if not filter(None, d['dy']):
                del d['dy']
    else:
        print "NOTICE: Parsing of ROOT class " + classname + " (" + name + ") not implemented"
        return
    print "Extracted " + classname + " " + name

    # Filter out labels we may have lost because the errors were zero
    d["labels"] = [l for l in d["labels"] if d.has_key(l)]

def getRootObjects(filenames, skip = None, only = None, doerrors = True):
    """
    get ROOT objects from file

    skips objects named anything contained in strings in skip list
    the only argument can be used to positively select particular histograms
    the ClassName of all objects is checked against allowedRootClasses

    result is a list with a dictionary for each object
    """

    files = [] # This is to return the files
               # (needed or root destroys objects on File destruction)
    rootobjs = [] # This is to return the list of objects

    # Loop over all files
    for filename in filenames:

        # Open file
        rootfile = ROOT.TFile.Open(filename, "READ")
        if rootfile.IsZombie():
            print "WARNING: Failed opening file \"", filename, "\", skipping to next file"
            continue
        files += [rootfile]

        # Loop over all keys in file
        for key in rootfile.GetListOfKeys():

            # Skip histograms associated with TGraph2D objects
            if key.GetName().endswith("_TG2Dhist"):
                continue

            # Get obj from file
            rootobj = rootfile.Get(key.GetName())

            # Check if object should be skipped
            if skip is not None:
                if len([s for s in skip if s in rootobj.GetName()]) > 0:
                    continue
            # Check if object should be included
            if only is not None:
                if len([o for o in only if o in rootobj.GetName()]) == 0:
                    continue

            # Ensure class is allowed
            if rootobj.ClassName() not in allowedRootClasses:
                continue

            # Add dictionary to object list
            rootobjs += [{
                    "file"  : filename,
                    "obj"   : rootobj.Clone(),
                    "name"  : rootobj.GetName(),
                    "class" : rootobj.ClassName(),
                    "dim"   : 3 if "2" in rootobj.ClassName() else 2,
                    "doerrors": doerrors,
                    "basename": rootobj.GetName(), # Base, minus suffixes
                    "errordetail": [], # Usually [] or ["DSYS"]
                    }]

            # Record if we should store errors
            if "TGraph" in rootobj.ClassName() and "Errors" not in rootobj.ClassName():
                rootobjs[-1]["doerrors"] = False
            
            # If it's a TGraph2D, retrieve the matching histogram
            if "TGraph2D" in rootobj.ClassName():
                hist = rootfile.Get(key.GetName()+"_TG2Dhist")
                if hist:
                    # Associate the histogram back with the graph
                    # We must remove the histogram from gDirectory to avoid ownership conflicts
                    hist.SetDirectory(0)
                    rootobjs[-1]["obj"].SetHistogram(hist)

    # Return objects and opened root file
    return rootobjs, files

def makeParser():
    """
    Define the command line argument parser used in main()
    """
    parser = argparse.ArgumentParser(
        description="""
           Converts objects in root files to
           hepdata format.""",
        epilog = "Happy converting!")
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = "%(prog)s 2.1",
        help = "Print version string")
    parser.add_argument(
        "-i", "--input",
        nargs = "+",
        dest = "inputfiles",
        help = "List of input files")
    parser.add_argument(
        "-g", "--group-suffixes",
        help = """
           Group objects with the same name but different suffixes together.
           Example: If input has x_sys and x_stat and argument "-g sys stat"
           is given the code will keep the 2 errors for each bin in a single
           histogram.""",
        nargs = "+",
        default = ["stat","dsys"],
        dest = "group")
#     parser.add_argument(
#         "-m", "--merge-groups",
#         action = "store_true",
#         help = """
#            Merge all y-errors in grouped together by adding errors in
#            quadrature. """,
#         dest = "merge") # Not implemented
    parser.add_argument(
        "-y", "--overlay",
        help = """
           Overlay multiple histograms/graphs on the same axes.
           Example: if you have histograms called pT_MC and pT_data
           and specify "-y MC data" then both will use a common x axis.
           Note that "MC" and "data" can be anywhere in the histogram names,
           as grouped suffixes may also be specified (see the -g option).""",
        nargs = "+",
        dest = "overlay")
    parser.add_argument(
        "-s", "--skip",
        nargs = "+",
        help = """Skip any histogram whose name contains any of these strings""",
        dest = "skip")
    parser.add_argument(
        "-q", "--test",
        nargs = "+",
        help = """
           Only process histograms whose names contain one of these strings.
           Usually used for testing, hence the name.
           """,
        dest = "only")
    parser.add_argument(
        "-r", "--range",
        nargs = 3,
        action = "append",
        metavar = ("name", "xlow", "xhigh"),
        help ="""
              Reject entries in histogram NAME outside range [xlow, xhigh].
              Can be used multiple times""",
        dest = "range")
#     parser.add_argument(
#         "--file-format",
#         choices = ("aida", "flat", "hep", "plot", "pyroot","root",
#                    "yoda", "mpl", "jhepwork", "all"),
#         dest = "format",
#         nargs = "+",
#         default = ["all"],
#         help = """
#             Format of output files to produce.
#             Files will be named output.format
#             (with output from -o option)""") # Limited implementation
    parser.add_argument(
        "--float-format",
        dest = "floatfmt",
        default = "1.4g")
    parser.add_argument(
        "-o", "--output",
        dest = "output",
        default = sys.stdout,
        help = "Name of output data set")
    parser.add_argument(
        "-z", "--zero",
        action = "store_true",
        dest = "zero",
        help = "Supress entries with y-bin == 0")
    parser.add_argument(
        "-n", "--nan",
        action = "store_true",
        dest = "nan",
        help = "Supress entries containing NaN")
    parser.add_argument(
        "--inf",
        action = "store_true",
        dest = "inf",
        help = "Supress entries containing Inf")
    parser.add_argument(
        "-e", "--supress-errors",
        action = "store_true",
        dest = "noerrors",
        help = "Present results without errors")

    return parser

def checkConsistency(ref, target):
    """
    Checks for consistency between reference and target.
    Number of x/y bins and compatibility of values.
    """
    # Check dimensionality
    if ref["dim"] != target["dim"]:
        print "ERROR: Objects of different dimensionality cannot be combined:",
        print ref["class"],"is dimension",ref["dim"],
        print "while",target["class"],"is dimension",target["dim"]
        return False
    # Check class types: this is only a warning
    if ref["class"] != target["class"]:
        print "WARNING: Objects not of same type! This may indicate an error:",
        print ref["name"],"is a",ref["class"],
        print "while",target["name"],"is a",target["class"]
    # Check number of points - at the moment, just a warning
    if len(ref["x"]) != len(target["x"]):
        print "WARNING: Objects with different numbers of bins:",
        print ref["name"],"has",len(ref["x"]),"bins",
        print "while",target["name"],"has",len(target["x"]),"bins"
    # Before checking x values, work out what tolerance to apply
    # This assumes one characteristic scale for all x values
    xrange = max(ref["x"]) - min(ref["x"])
    if not xrange:
        print "ERROR: All x values are the same in",ref["name"]
        return False
    xtolerance = xrange/1e6 # Easily within double precision
    # Check x values
    haveError = False
    for x1,x2 in zip(ref["x"],target["x"]):
        if abs(x1-x2) > xtolerance:
            print "ERROR: x values do not match:",x1,x2
            haveError = True
    if haveError:
        print "ERROR: Inconsistent x binning for",ref["name"],"and",target["name"]
        return False
    if ref["dim"] > 2:
        # Before checking y values, work out what tolerance to apply
        # This assumes one characteristic scale for all y values
        yrange = max(ref["y"]) - min(ref["y"])
        if not yrange:
            print "ERROR: All y values are the same in",ref["name"]
            return False
        ytolerance = yrange/1e6 # Easily within double precision
        # Check y values
        haveError = False
        for y1,y2 in zip(ref["y"],target["y"]):
            if abs(y1-y2) > ytolerance:
                print "ERROR: y values do not match:",y1,y2
                haveError = True
        if haveError:
            print "ERROR: Inconsistent y binning for",ref["name"],"and",target["name"]
            return False

    # If we get here, we had warnings at worst
    return True

def findGroups(names, groups):
    """
    for names A_a, A_b, B_a, B_b, C (C is ungrouped) and groups a, b
    return dict of "A":["A_a", "A_b"], "B":["B_a", "B_b"], "C":["C"]
    """
    grp = {}

    if groups and len(groups) > 1:
        for g in groups:
            # Loop over all objects in this group
            for n in [n for n in names if n.endswith("_"+g)]:
                # Get name string
                name = [n.rpartition("_"+g)[0].strip()]
                if name == [] or name == [""]: continue
                name = name[0]
                # Append full name to groups dict
                if name in grp:
                    grp[name] += [n]
                else:
                    grp[name] = [n]
                # Remove this item from further consideration
                names.remove(n)

    # Add in remaining names (or all names if groups is not defined)
    for n in names:
        grp[n] = [n]

    return grp

def groupObjects(rootobjs, groups):
    """
    Make rootobjs into a richer structure, by grouping together
    related histograms/graphs defined by the groups parameter.
    rootobjs: a list of dictionaries from getROOTObjs()
    groups: a dictionary of lists from findGroups()
    returns: a list of lists of dictionaries, defined by groups
    """
    if not groups:
        return [[o] for o in rootobjs]

    result = []
    for obj in rootobjs:
        hname = obj["name"]
        for basename,groupednames in groups.items():
            if hname == groupednames[0]:
                # We have the first histogram of a group
                thisgroup = [obj]
                # Loop through the rest of the group and find the objects!
                for othername in groupednames[1:]:
                    otherobjs = [item for item in rootobjs if item["name"]==othername]
                    try: assert len(otherobjs) == 1
                    except AssertionError:
                        if otherobjs: print "Error: %i group-level matches for %s"%(len(otherobjs),othername)
                        else: print "Error: No histogram %s found to group with %s"%(othername,hname)
                        raise
                    # Check that the object is compatible with the first
                    if checkConsistency(obj, otherobjs[0]):
                        # This is a secondary histogram: only activate the errors:
                        otherobjs[0]["labels"] = [l for l in otherobjs[0]["labels"] if 'd' in l]
                        thisgroup.append(otherobjs[0])
                    else:
                        print "ERROR: Objects do not match, will not be combined!"
                        print "ERROR:",obj["name"],otherobjs[0]["name"]
                # Set the basenames appropriately, removing suffixes
                # Record the suffix separately
                for obj2 in thisgroup:
                    obj2["basename"] = basename
                    # hname is basename+'_'+groupname, where groupname can be split using underscores
                    obj2["errordetail"] = obj2['name'].replace(basename,'').split('_')[1:]

                # Append this object list to result, and skip to the next item
                result.append(thisgroup)
                break

    return result

def addOverlays(rootobjs, overlay, suffixes):
    """Create overlay structure for histograms sharing a common x (and y) axis.
    rootobjs: a list of list of dictionaries (output of groupObjects())
    overlay: a list of strings to look for: overlay histograms that differ only by these strings
    suffixes: a list of suffixes that may differ between overlaid histograms
    """
    if not overlay or len(overlay) < 2:
        return rootobjs
    result = []

    for objects in rootobjs:
        obj = objects[0]
        hname = obj["name"]
        hbasename = obj["basename"]
        if overlay[0] in hname:
            # This is the first of a set with a common x axis
            # We don't want to treat this specially until we know the other overlays are there
            try:
                tmplist = objects[:]
                for otherkey in overlay[1:]:
                    # Enforce strict key matching, but ignore suffixes
                    otherobjs = []
                    for s in suffixes+[""] if suffixes else [""]:
                        othername = hbasename.replace(overlay[0],otherkey)
                        if s: othername = "_".join([othername,s])
                        otherobjs = [items for items in rootobjs if othername in [i["name"] for i in items]]
                        if otherobjs:
                            print "Found match to",othername
                            break # Avoids multiple matches to the same list
                    try: assert len(otherobjs) == 1
                    except AssertionError:
                        if otherobjs: print "Error: %i matches for %s"%(len(otherobjs),hbasename.replace(overlay[0],otherkey))
                        else: print "WARNING: No histogram %s found to overlay with %s"%(hbasename.replace(overlay[0],otherkey),hname)
                        raise
                    # Check to see if the binning is consistent (it's enough to check the first one)
                    if checkConsistency(tmplist[0], otherobjs[0][0]):
                        tmplist.extend(otherobjs[0])
                    else:
                        print "ERROR: Objects do not match, will not be combined!"
                        print "ERROR:",tmplist[0]["name"],otherobjs[0][0]["name"]
                # Modify the basename to remove the overlay markers
                basename = hbasename.replace(overlay[0],"").strip("_")
                for otherobj in tmplist:
                    otherobj["basename"] = basename
                # Remove labels for independent axes
                for otherobj in tmplist[len(objects):]:
                    indeplabel = "z" if otherobj["dim"]==3 else "y"
                    otherobj["labels"] = [l for l in otherobj["labels"] if indeplabel in l]
                result.append(tmplist)
            except AssertionError:
                # This means we couldn't find all matches
                # just append the object on its own
                result.append(objects)
            pass
        else:
            # Check to see if this has *any* distinguishing features
            if not [ol for ol in overlay if ol in hname]:
                # It stands alone
                result.append(objects)

    return result

#############################################################################
# Main function
def main(args = sys.argv[1:]):
    """
    rootconverter.py main function
    """

    ####### PARSE AND CHECK OPTIONS
    parser = makeParser()

    # Print help and quit if there are no arguments
    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    # Parse arguments
    parse = parser.parse_args(args)

    # Check input file option
    if parse.inputfiles == None:
        parser.print_usage()
        print "ERROR: you need to specify some input files"
        exit(2)

    # Check range option
    try:
        if not parse.range == None:
            [(float(r[1]), float(r[2])) for r in parse.range]
    except Exception, e:
        parser.print_usage()
        print e
        print "ERROR: Range arguments 2 and 3 must be numeric!"
        exit(3)

    # Check float format
    try:
        ("{0:"+parse.floatfmt+"}").format(3.14)
    except Exception, e:
        parser.print_usage()
        print e
        print "ERROR: Float format argument not valid, try for example 1.3e"
        exit(4)

    # Get the root objects from inputfiles
    rootobjs, rootfiles = getRootObjects(parse.inputfiles, parse.skip, parse.only, not parse.noerrors)
    if len(rootobjs) == 0:
        print "ERROR: no valid root objects found in input files!"
        exit(6)

    # Extract the root data from each object
    for rootobj in rootobjs:
        extractRootObject(rootobj)

    # Grouping goes here
    # if parse.group is not None and len(parse.group) > 1:
    groups = findGroups([r["name"] for r in rootobjs], parse.group)
    from pprint import pprint
    print "Groups:"
    pprint(groups)
    rootobjs = groupObjects(rootobjs, groups)

    # Overlays happen here
    rootobjs = addOverlays(rootobjs, parse.overlay, parse.group)

    # Open output file(s)
    try: hepfile = open(parse.output + ".hep.dat", "w")
    except TypeError: hepfile = parse.output # Probably stdout

    # Write header
    hepfile.write('*author: AAD\n')
    hepfile.write('*reference: ARXIV:XXXX : 2014\n')
    hepfile.write('*reference: CERN-PH-EP-XXXX-XX : 2014\n')
    hepfile.write('*reference: GIVE JOURNAL CITATION (IF KNOWN) : 2014\n')
    hepfile.write('*reference: http://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-XXXX-XXX/ : 2014\n')
    hepfile.write('*doi: GIVE DOI\n')
    today = datetime.date.today()
    hepfile.write('*status: Encoded %i %s %i by ATLAS\n'%(today.day,today.strftime('%B').upper(),today.year))
    hepfile.write('*experiment: CERN-LHC-ATLAS\n')
    hepfile.write('*detector: ATLAS\n')
    hepfile.write('*inspireId: GIVE INSPIRE ID\n')
    hepfile.write('*cdsId: GIVE CDS ID\n')
    hepfile.write('*durhamId: \n')
    hepfile.write('*title: INSERT TITLE\n')
    hepfile.write('*comment: CERN-LHC. INSERT ABSTRACT\n')

    # Remove bad entries from each object
    for rootobjlist in rootobjs:
        xlow = 0
        xhigh = 0
        if parse.range is not None:
            if parse.range[0][0] in rootobj["name"]:
                xlow = float(parse.range[0][1])
                xhigh = float(parse.range[0][2])
        cleanObjDict(
            rootobjlist,
            cutZero = parse.zero,
            cutNaN = parse.nan,
            cutInf = parse.inf,
            cutXlow = xlow,
            cutXhigh = xhigh)
        try:
            makeHepData(rootobjlist, parse.floatfmt, hepfile)
        except NameError: pass

    # Write footer
    hepfile.write('*E\n')
    print "DONE."
    hepfile.close()

# Ensure main is called by default
if __name__ == "__main__":
    main()
