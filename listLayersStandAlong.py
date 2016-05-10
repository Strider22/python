#!/usr/bin/env python
""" Print out the layers for an animeStudio file (.anime)
"""
import zipfile
import json
import argparse
import os
import sys

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


def perform():
    parser = argparse.ArgumentParser(description="List the names of top layers "
                                                 "in an anime studio file.")
    parser.add_argument('anime_studio_file', help="Anime Studio file to list layers.")
    args = parser.parse_args()

    path = os.path.abspath(args.anime_studio_file)
    if not os.path.exists(path):
        parser.error("%s does not exist." % path)
    if not path.endswith(".anime"):
        parser.error("%s is not an Anime Studio (.anime) file." % path)

    iterateLayers(path)

if __name__ == '__main__':
    perform()
