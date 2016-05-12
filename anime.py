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

def isContainerLayer(layer):
    """Return True if the layer is a group or switch layer."""
    type = layer['type']
    return type == "GroupLayer" or type == "SwitchLayer"

def top_level_layer_names(groupLayer):
    layer_names = []
    for layer in groupLayer:
        layer_names.append(layer['name'])
    return layer_names

def all_layer_names(groupLayer):
    """Iterate a group or switch layer descending into sub groups and updating or
printing layers otherwise."""
    layer_names = []
    for layer in groupLayer:
        if isContainerLayer(layer):
            layer_names.extend(layer_names(layer['layers']))
        else:
            layer_names.append(layer['name'])
    return layer_names


def get_data(path):
    """Iterate the root project layers."""
    projectPath = path
    projectData = extractProject(projectPath)
    if len(projectData) > 0:
        return json.loads(projectData)


