#!/usr/bin/env python
""" Print out the layers for an animeStudio file (.anime)
"""
import zipfile
import json

_styleIdToName = {}
_styleNameToPreferredId = {}
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

def write_anime_file(animeFile):
    writeProject(animeFile, _anime_studio_object)

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
    projectData = extract_project(projectPath)
    if len(projectData) > 0:
        return json.loads(projectData)


def findLayer(name, groupLayer, layersProcessed):
    for layer in groupLayer:
        uuid = layer['uuid']
        if (layer['name'].strip() == name) and uuid not in layersProcessed:
            layersProcessed[uuid] = True
            return layer

def getReplacementId(uuid):
    name = _styleIdToName[uuid]
    if name not in _styleNameToPreferredId:
        _styleNameToPreferredId[name] = uuid
        return uuid
    return _styleNameToPreferredId[name]


def processShapes(shapes):
    for shape in shapes:
        uuid = shape['inherited_style_uuid']
        replacementId = getReplacementId(uuid)
        if replacementId != uuid:
            shape['inherited_style_uuid'] = replacementId


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


def process_named_layers(path, named_layers):
    global _anime_studio_object
    """Iterate the root project layers."""
    projectPath = path
    projectData = extract_project(projectPath)
    if len(projectData) > 0:
        _anime_studio_object = json.loads(projectData)
        buildStyleLists()
        layers = _anime_studio_object['layers']
        layersProcessed = {}
        for layerName in named_layers:
            layerName = layerName.strip()
            layer = findLayer(layerName,layers, layersProcessed)
            if layer is not None:
                processLayer(layer)

