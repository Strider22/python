#!/usr/bin/env python
"""anime_util - Manipulate a .anime file
Commands are list, extract, and update.
list prints the paths of image and audio layers.
extract saves the Project.animeproj to a desired location.
update replaces existing paths with the one supplied.
anime_util.py -h |command| for help.
"""
import zipfile
import json
import argparse
import os
import sys


def processNamedLayers(path):
    """Iterate the root project layers."""
    projectPath = path
    print(projectPath)
    projectData = extractProject(projectPath)
    if len(projectData) > 0:
        jsonData = json.loads(projectData)
        layers = jsonData['layers']
        for layer in layers:
            layer['name'] = "Squigly"
            print(layer['name'])
    writeProject("modifiedByPython.anime", json.dumps(jsonData))

def extractProjectFile(animeFile, projectFilepath = None):
    """Iterate Project.animeproj to projectFilePath."""
    jsonData = extractProject(animeFile)
    if len(jsonData) > 0:
        jsonData = json.loads(jsonData)
        if projectFilepath:
            output = file(projectFilepath, 'wb')
        else:
            output = file('Project.animeproj', 'wb')
        json.dump(jsonData, output, sort_keys=False, indent=4)
    else:
        parser.error("Project.animeproj is empty")



def extractProject(animeFile):
    """Return the Project.animeproj extracted from a zip file as a string."""
    zf = zipfile.ZipFile(animeFile)
    for filename in [ 'Project.animeproj' ]:
        data = zf.read(filename)
    return data

def writeProject(animeFile, projectData):
    """Write data back into Project.animeproj in a zip file"""
    zf = zipfile.ZipFile(animeFile, mode="w")
    zf.writestr('Project.animeproj', projectData)

def perform():
    projectData = extractProject("Colors3.anime")
    if len(projectData) > 0:
        jsonData = json.loads(projectData)
        writeProject("testWriteModified.anime", json.dumps(jsonData))

if __name__ == '__main__':
    perform()
