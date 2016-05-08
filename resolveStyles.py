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

_styleIdToName = {}
_styleNameToPreferredId = {}
_anime_studio = None


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

# def printLayerInfo(layer):
#     """Print the path of an image or audio layer."""
#     if layer.has_key('mesh'):
#         mesh = layer['mesh']
#         if mesh.has_key('shapes'):
#             for shape in mesh['shapes']:
#                 shape['inherited_style_uuid'] = 5
#                 print "sytle:", shape['inherited_style_uuid']

# def updateLayerInfo(layer, update):
#     """Replace the path of an image or audio layer."""
#     if layer.has_key('image_path'):
#         path = layer['image_path']
#         layer['image_path'] = path.replace(update[0], update[1])
#     if layer.has_key('audio_path'):
#         path = layer['audio_path']
#         layer['audio_path'] = path.replace(update[0], update[1])

# def isContainerLayer(layer):
#     """Return True if the layer is a group or switch layer."""
#     type = layer['type']
#     return type == "GroupLayer" or type == "SwitchLayer"

def findLayer(name, groupLayer, layersProcessed):
    for layer in groupLayer:
        uuid = layer['uuid']
        if (layer['name'] == name) and not layersProcessed.has_key(uuid):
            layersProcessed[uuid]= True
            return layer

def getReplacementId(uuid):
    name = _styleIdToName[uuid]
    style_id = _styleNameToPreferredId[name]
    if style_id is not None:
        return style_id
    _styleNameToPreferredId[name] = uuid
    return uuid

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
    for style in _anime_studio['styles']:
        uuid = style['uuid']
        name = style['name']
        _styleIdToName[uuid] = name
        if name not in _styleNameToPreferredId:
            _styleNameToPreferredId[name] = uuid


def processNamedLayers(path, file):
    global _anime_studio
    """Iterate the root project layers."""
    projectPath = path
    projectData = extract_project(projectPath)
    if len(projectData) > 0:
        _anime_studio = json.loads(projectData)
        buildStyleLists()
        layers = _anime_studio['layers']
        layersProcessed = {}
        for layerName in file.xreadlines():
            layerName = layerName.rstrip()
            layer = findLayer(layerName,layers, layersProcessed)
            if layer is not None:
                processLayer(layer)
        file.close()


# def readSingleFile(evt) :
#             var f = evt.target.files[0];
#         if (f) {
#         var reader = new FileReader();
#         reader.onload = function (e) {
#         var contents = e.target.result;
#         buildLayerList(contents);
#         buildStyleLists();
#         };
#         reader.readAsText(f);
#         }
#         }

        # var myButton = new Button({
        #     label: "Get list order",
        #     onClick: function () {
        #         _wishlist.getAllNodes().forEach(function (node) {
        #         _orderedLayerList.push(node.innerHTML);
        # });
        # dom.byId("results").innerHTML = string;
        # showLayers(__anime_studio.layers, "");
        # processNamedLayers();
        # showLayers(__anime_studio.layers, "");
        # showDiv("result", string);
        # downloadJSON();
        # }
        # }, "btn").startup();


# def showJSON(text) :
#             __anime_studio = JSON.parse(text);
#         string = "";
#
#         showStyles(__anime_studio.styles);
#         buildStyleNameToIdsList();
#         //        listDuplicates();
#         //        addButton("Style1",{r:1,g:0,b:0},{b:1,r:1,g:1});
#         //        addButton("Style 2",{r:0,g:1,b:0},{b:.5,r:.5,g:1});
#         //        showLayers(obj.layers,"");
#         //            addDuplicateStyleButtons(_styleNameToIds, __anime_studio.styles);
#         //        showDiv("result", stringFromList(topLayersHavingStyle(obj.layers,this.styleWithMaxDuplicates)));
#         //        showDiv("result", string);
#         }
#
#
#
# def (list) :
# var string = "";
# for (var i = 0; i < list.length; i++) {
# string += list[i] + "<br>";
# }
# return string;
# }

# def showLayers(layers, path) :
# var layerPath = "";
# for (var i = 0; i < layers.length; i++) {
# var layer = layers[i];
# if ("" === path) layerPath = layer.name;
# else layerPath = path + "\\" + layer.name;
# string += layerPath + " - " + layer.uuid + "<br>";
# if (layer.mesh && layer.mesh.shapes) showShapes(layer.mesh.shapes);
# if (layer.layers) {
# showLayers(layer.layers, layerPath);
# }
# }
# }
# def showShapes(shapes) :
# shapes.forEach(function(shape){
#     string += "shape style - " + shape.inherited_style_uuid + "<br>";
# });
# }
#
# def topLayersHavingStyle(layers, style) :
# var topLayersHavingStyle = [];
# var layerPath = "";
# for (var i = 0; i < layers.length; i++) {
# var layer = layers[i];
# if (layerHasStyle(layer, style)) topLayersHavingStyle.push(layer.name);
# }
# return topLayersHavingStyle;
# }
#
# def layerHasStyle(layer, styleName) :
# if (!layer.mesh || !layer.mesh.shapes) return false;
# var shapes = layer.mesh.shapes;
# for (var i = 0; i < shapes.length; i++) {
# var shape = shapes[i];
# if (styleName == styleList[shape.inherited_style_uuid]) return true;
# }
# if (layer.layers) {
# for (i = 0; i < layer.layers.length; i++) {
# if (layerHasStyle(layer.layers[i], styleName))return true;
# }
# }
# return false;
# }
#
#
#
# def rgbColor(color) :
# return "rgb(" + Math.trunc(color.r * 255) + "," + Math.trunc(color.g * 255) + "," + Math.trunc(color.b * 255) + ")";
# }

# def addDuplicateStyleButtons(duplicateStyles, styles) :
# for (var propertyName in duplicateStyles) {
# var styleList = duplicateStyles[propertyName];
# for (var i = 0; i < styleList.length; i++) {
# var styleIndex = styleList[i];
# addStyleButton(styles[styleIndex]);
# }
# }
# }
#
#
# def addStyleButton(style) :
# //Create an input type dynamically.
# var element = document.createElement("BUTTON");
# element.innerHTML = style.name; // Really? You want the default value to be the type string?
# element.style.borderColor = rgbColor(style.line_color.val[0]);
# element.style.backgroundColor = rgbColor(style.fill_color.val[0]);
# element.onclick = function () { // Note this is a function
# alert(style.uuid);
# };
#
# var foo = document.getElementById("duplicates");
# //Append the element in page (in span).
# foo.appendChild(element);
# }

# def listDuplicates() :
# var string = "Style with max duplicates is " + _styleWithMaxDuplicates + "<br>";
# for (var propertyName in _styleNameToIds) {
# var style = _styleNameToIds[propertyName];
# string += propertyName + " - ";
# for (var i = 0; i < style.length; i++) {
# string += style[i] + "; ";
# }
# string += " <br>";
# }
# showDiv("duplicates", string);
# }
#
# def showStyles(styles) :
# for (var i = 0; i < styles.length; i++) {
# string += styles[i].name + " - " + styles[i].uuid + "<br>";
# }
# }
#
# def showDiv(divName, result) :
# document.getElementById(divName).innerHTML = result;
# }

def rename_styles(path):
    global _anime_studio
    processed_styles = {}
    project_data = extract_project(path)
    if len(project_data) > 0:
        _anime_studio = json.loads(project_data)
    else:
        return
    for style in _anime_studio['styles']:
        name = style['name']
        if name not in processed_styles:
            processed_styles[name] = 1
        else:
            style['name'] = name + " " + str(processed_styles[name])
            processed_styles[name] += 1


def perform():
    global _rename
    parser = argparse.ArgumentParser()
    parser.add_argument('layerOrderFile', help="File containing the preferred layer order ")
    parser.add_argument('--rename', help="Specify if you want to rename rather than replace duplicate style", action="store_true")
    args = parser.parse_args()
    order_file = open(args.layerOrderFile, "r")
    path = order_file.readline().rstrip('\n')
    if args.rename:
        rename_styles(path)
    else:
        processNamedLayers(path, order_file)
    writeProject("modifiedFile.anime", json.dumps(_anime_studio))

if __name__ == '__main__':
    perform()
