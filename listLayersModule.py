#!/usr/bin/env python
""" Print out the layers for an animeStudio file (.anime)
"""
import zipfile
import json

def extractProject(animeFile):
    """Return the Project.animeproj extracted from a zip file as a string."""
    zf = zipfile.ZipFile(animeFile)
    for filename in [ 'Project.animeproj' ]:
        data = zf.read(filename)
    return data

def printLayerInfo(layer):
    """Print the path of an image or audio layer."""
    print layer['name']

def isContainerLayer(layer):
    """Return True if the layer is a group or switch layer."""
    type = layer['type']
    return type == "GroupLayer" or type == "SwitchLayer"

def iterateContainerLayer(groupLayer):
    """Iterate a group or switch layer descending into sub groups and updating or
printing layers otherwise."""
    for layer in groupLayer:
        if isContainerLayer(layer):
            iterateContainerLayer(layer['layers'])
        else:
            printLayerInfo(layer)

def iterateLayers(path):
    """Iterate the root project layers."""
    projectPath = path
    projectData = extractProject(projectPath)
    if len(projectData) > 0:
        jsonData = json.loads(projectData)
        layers = jsonData['layers']
        iterateContainerLayer(layers)


