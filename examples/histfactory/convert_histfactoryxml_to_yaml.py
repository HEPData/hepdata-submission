#!/usr/bin/env python
"""
Code to convert HistFactory XML into YAML for HepData, 
including the actual histogram contents using (modified) heprootconverter.


Requirements:
    PyXML
    PyYaml

---------------
Author: Kyle Cranmer 
Version 1.0 - May 20, 2015: based on convertyaml_map.py 
and heprootconverter.py by Thomas Burgess and Mike Flowerdew


"""

import sys, string, re, types
import yaml

from xml.dom import minidom
from xml.dom import Node


#
# Convert an XML document (file) to YAML and write it to stdout.
#
def convertXml2Yaml(inFileName):
    doc = minidom.parse(inFileName)
    root = doc.childNodes[-1]
    # Convert the DOM tree into "YAML-able" data structures.
    out = convertXml2YamlAlternate(root)
    # Ask YAML to dump the data structures to a string.
    outStr = yaml.safe_dump(out,default_flow_style=False)
    # Write the string to stdout.
    sys.stdout.write(outStr)

# not used, this peforms a canonical XML->YAML conversion. 
def convertXml2YamlAux(obj):
    objDict = {}
    # Add the element name.
    objDict['name'] = obj.nodeName
    # Convert the attributes.
    attrs = obj.attributes
    if attrs.length > 0:
        attrDict = {}
        for idx in range(attrs.length):
            attr = attrs.item(idx)
            attrDict[attr.name] = attr.value
        objDict['attributes'] = attrDict
    # Convert the text.
    text = []
    for child in obj.childNodes:
        if child.nodeType == Node.TEXT_NODE and \
            not isAllWhiteSpace(child.nodeValue):
            text.append(child.nodeValue)
    if text:
        textStr = "".join(text)
        objDict['text'] = textStr
    # Convert the children.
    children = []
    for child in obj.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            obj = convertXml2YamlAux(child)
            children.append(obj)
    if children:
        objDict['children'] = children
    return objDict


# this one is used, a little more readible, less verbose
def convertXml2YamlAlternate(obj, inputFile='',histoPath='', histoName='',explicitHistograms=True):
    objDict = {}
    # Add the element name.
    #objDict[obj.nodeName] = obj.nodeName
    # Convert the attributes.
    objName = obj.nodeName
    attrs = obj.attributes
    attrDict = {}
    if attrs.length > 0:
        for idx in range(attrs.length):
            attr = attrs.item(idx)
            attrDict[attr.name] = attr.value
            if attr.name=='InputFile':
                inputFile = attr.value
            if attr.name=='HistoPath':
                histoPath = attr.value
            if attr.name=='HistoName':
                histoName = attr.value
        if objName=='HistoSys':
            convertHistogram(inputFile,histoPath, attrDict['HistoNameHigh'])
            convertHistogram(inputFile,histoPath, attrDict['HistoNameLow'])
        if explicitHistograms:
            if not attrDict.has_key('InputFile'):
                attrDict['InputFile']=inputFile
            if not attrDict.has_key('HistoPath'):
                attrDict['HistoPath']=histoPath
            if not attrDict.has_key('HistoName'):
                attrDict['HistoName']=histoName


    # convert thie histogram
    nodesWithHistograms=['Data', 'Sample']
    if nodesWithHistograms.count(objName):
        convertHistogram(inputFile,histoPath, histoName)


        #objDict['attributes'] = attrDict
    # Convert the text.
    text = []
    for child in obj.childNodes:
        if child.nodeType == Node.TEXT_NODE and \
            not isAllWhiteSpace(child.nodeValue):
            text.append(child.nodeValue)
    if text:
        textStr = "".join(text)
        attrDict['text'] = textStr
    # Convert the children.
    children = []
    for child in obj.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            obj = convertXml2YamlAlternate(child,inputFile=inputFile, histoPath=histoPath, histoName=histoName)
            children.append(obj)
    if children:
        attrDict['children'] = children
    objDict[objName] = attrDict
    return objDict

#
# Utility functions.
#
def convertHistogram(inputFile='', histoPath='', histoName=''):
    print "# converting histogram,  %s, %s, %s" %(inputFile, histoPath, histoName)

def addLevel(level, out):
    for idx in range(level):
        out.append('    ')


NonWhiteSpacePattern = re.compile('\S')

def isAllWhiteSpace(text):
    if NonWhiteSpacePattern.search(text):
        return 0
    return 1


def main():
    args = sys.argv[1:]
    inFileName = args[0]
    convertXml2Yaml(inFileName)


if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')

