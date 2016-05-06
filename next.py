#!/usr/bin/env python
"""anime_util ­ Manipulate a .anime file
Commands are list, extract, and update.
list prints the paths of image and audio layers.
extract saves the Project.animeproj to a desired location.
update replaces existing paths with the one supplied.
anime_util.py ­h |command| for help.
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
def writeProject(animeFile, projectData):
"""Write data back into Project.animeproj in a zip file"""
zf = zipfile.ZipFile(animeFile, mode="w")
zf.writestr('Project.animeproj', projectData)
def printLayerInfo(layer):
"""Print the path of an image or audio layer."""
if layer.has_key('image_path'):
print "image:", layer['image_path']
if layer.has_key('audio_path'):
print "audio:", layer['audio_path']
def updateLayerInfo(layer, update):
"""Replace the path of an image or audio layer."""
if layer.has_key('image_path'):
path = layer['image_path']
layer['image_path'] = path.replace(update[0], update[1])
if layer.has_key('audio_path'):
path = layer['audio_path']
layer['audio_path'] = path.replace(update[0], update[1])
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
if update:
updateLayerInfo(layer, update)
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
if update:
writeProject(projectPath, json.dumps(jsonData))
iterateContainerLayer(layers)
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
def perform():
parser = argparse.ArgumentParser(description="Open a .anime file and print
and/or update the paths of image and audio layers")
subParsers = parser.add_subparsers(help="commands", dest="command")
parser_list = subParsers.add_parser("list", help="list image and audio paths in
Anime Studio file (.anime).")
parser_list.add_argument('path', help="path to Anime Studio file")
parser_extract = subParsers.add_parser("extract", help="extract
Project.animeproj from Anime Studio file (.anime).")
parser_extract.add_argument('path', help="path to Anime Studio file")
parser_extract.add_argument('projectFile', metavar='project file', help="path to
save Anime Studio project file")
parser_extract.add_argument('­b', '­­beautify', action="store_true", help="beautify
the project file")
parser_update = subParsers.add_parser("update", help="update image and
audio paths in Anime Studio file (.anime).")
parser_update.add_argument('existing', help="existing path(s) in file")
parser_update.add_argument('new', help="path to replace existing path(s) with")
parser_update.add_argument('path', help="path to Anime Studio file")
args = parser.parse_args()
path = os.path.abspath(args.path)
if not os.path.exists(path):
parser.error("%s does not exist." % path)
if not path.endswith(".anime"):
parser.error("%s is not an Anime Studio (.anime) file." % path)
updateInfo = None
if args.command == "update":
updateInfo = (args.existing, args.new)
if args.command == "extract":
extractProjectFile(path, os.path.abspath(args.projectFile))
else:
iterateLayers(path, update=updateInfo)
if __name__ == '__main__':
perform()
