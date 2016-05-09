#!/usr/bin/env python
""" Creates a layer order file that is to be used with
resolveStyles.py or renameStylesByOrder.py
The layer order controls style preference.
"""
import zipfile
import json
import argparse
import os
import sys
_output_file = None

def extractProject(animeFile):
    """Return the Project.animeproj extracted from a zip file as a string."""
    zf = zipfile.ZipFile(animeFile)
    for filename in [ 'Project.animeproj' ]:
        data = zf.read(filename)
    return data

def printLayerInfo(layer):
    """Print the path of an image or audio layer."""
    _output_file.write(layer['name'] + "\n")

def isContainerLayer(layer):
    """Return True if the layer is a group or switch layer."""
    type = layer['type']
    return type == "GroupLayer" or type == "SwitchLayer"

def iterateContainerLayer(groupLayer, update=None):
    """Iterate a group or switch layer descending into sub groups and updating or
printing layers otherwise."""
    for layer in groupLayer:
        if isContainerLayer(layer):
            iterateContainerLayer(layer['layers'], update)
        else:
            printLayerInfo(layer)

def iterateLayers(path, update=None):
    """Iterate the root project layers."""
    projectPath = path
    projectData = extractProject(projectPath)
    if len(projectData) > 0:
        jsonData = json.loads(projectData)
        layers = jsonData['layers']
        iterateContainerLayer(layers, update)


def perform():
    global _output_file
    parser = argparse.ArgumentParser(description="Creates a layer order file, allowing the "
                                                 "user to specify layer order needed for"
                                                 "resolving duplicate styles in resovleStyles.py.")
    parser.add_argument('anime_studio_file', help="Anime Studio file")
    parser.add_argument('layer_order_file', help="layer order file")
    args = parser.parse_args()

    path = os.path.abspath(args.anime_studio_file)
    if not os.path.exists(path):
        parser.error("%s does not exist." % path)
    if not path.endswith(".anime"):
        parser.error("%s is not an Anime Studio (.anime) file." % path)

    output_path = os.path.abspath(args.layer_order_file)
    if os.path.exists(output_path):
        parser.error("%s already exists. Please select another name." % path)

    _output_file = open(output_path,"w")
    _output_file.write(path + "\n")
    iterateLayers(path)

if __name__ == '__main__':
    perform()
