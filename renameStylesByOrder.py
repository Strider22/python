#!/usr/bin/env python
"""renameStylesByOrder - Resolves duplicate styles in an anime studio file.
createLayerOrderFile.py should have been run first to create the layer order file.
renameStylesByOrder.py -h |command| for help.
"""

import zipfile
import json
import argparse
import os
import sys

_styleIdToName = {}
_styleIdToStyle = {}
_processed_styles = {}
_anime_studio_object = None


def extract_project(animeFile):
    """Return the Project.animeproj extracted from a zip file as a string."""
    zf = zipfile.ZipFile(animeFile)
    for filename in [ 'Project.animeproj' ]:
        data = zf.read(filename)
    return data


def writeProject(animeFile, projectData):
    """Write data back into Project.animeproj in a zip file"""
    zf = zipfile.ZipFile(animeFile, mode="w")
    zf.writestr('Project.animeproj', projectData)

def findLayer(name, groupLayer, layersProcessed):
    for layer in groupLayer:
        uuid = layer['uuid']
        if (layer['name'].strip() == name) and uuid not in layersProcessed:
            layersProcessed[uuid] = True
            return layer

def check_style_name(uuid):
    name = _styleIdToName[uuid]
    if name not in _processed_styles:
        _processed_styles[name] = 1
    else:
        _styleIdToStyle[uuid]['name'] = name + " " + str(_processed_styles[name])
        _processed_styles[name] += 1

def processShapes(shapes):
    for shape in shapes:
        uuid = shape['inherited_style_uuid']
        check_style_name(uuid)


def processLayer(layer):
    if 'mesh' in layer and 'shapes' in layer['mesh']:
        processShapes(layer['mesh']['shapes'])
    if 'layers' in layer:
        for layer in layer['layers']:
            processLayer(layer)


def buildStyleLists() :
    for style in _anime_studio_object['styles']:
        uuid = style['uuid']
        name = style['name']
        _styleIdToName[uuid] = name
        _styleIdToStyle[uuid] = style


def processNamedLayers(path, file):
    global _anime_studio_object
    """Iterate the root project layers."""
    projectPath = path
    projectData = extract_project(projectPath)
    if len(projectData) > 0:
        _anime_studio_object = json.loads(projectData)
        buildStyleLists()
        layers = _anime_studio_object['layers']
        layersProcessed = {}
        for layerName in file.xreadlines():
            layerName = layerName.strip()
            layer = findLayer(layerName,layers, layersProcessed)
            if layer is not None:
                processLayer(layer)
        file.close()


def perform():
    parser = argparse.ArgumentParser(description="Renames duplicate styles. _Does_ "
                                                 "take layer order into consideration.")
    parser.add_argument('layer_order_file', help="File containing the input file and the preferred layer order. "
                                                 "Created by running createLayerOrderFile.py.")
    parser.add_argument('output_anime_studio_file', help="Output Anime Studio file that will contain "
                                                         "the resolved styles.")
    # parser.add_argument('--overwrite', help="Use if you want to overwrite the output if it exists.")

    args = parser.parse_args()

    # Check input file
    input_path = os.path.abspath(args.layer_order_file)
    if not os.path.exists(input_path):
        parser.error("%s does not exist." % input_path)

    # Check output file
    output_path = os.path.abspath(args.output_anime_studio_file)
    if os.path.exists(output_path):
        parser.error("%s already exists. Please select a separate file." % output_path)
    if not output_path.endswith(".anime"):
        parser.error("%s is not an Anime Studio (.anime) file." % output_path)

    layer_order_file = open(input_path, "r")
    anime_studio_file = layer_order_file.readline().rstrip('\n')

    processNamedLayers(anime_studio_file, layer_order_file)
    writeProject(output_path, json.dumps(_anime_studio_object))

if __name__ == '__main__':
    perform()
