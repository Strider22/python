#!/usr/bin/env python
"""renameStyles - Renames duplicate styles in an anime studio file.
renameStyles.py -h |command| for help.
"""
import zipfile
import json
import argparse
import os
import sys

_anime_studio = None


def extract_project(animeFile):
    """Return the Project.animeproj extracted from a zip file as a string."""
    zf = zipfile.ZipFile(animeFile)
    for filename in ['Project.animeproj']:
        data = zf.read(filename)
    return data


def writeProject(animeFile, projectData):
    """Write data back into Project.animeproj in a zip file"""
    zf = zipfile.ZipFile(animeFile, mode="w")
    zf.writestr('Project.animeproj', projectData)


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
    parser = argparse.ArgumentParser(description="Renames duplicate styles. _Does not_ "
                                                 "take layer order into consideration.")
    parser.add_argument('input_anime_studio_file', help="The original Anime Studio file")
    parser.add_argument('output_anime_studio_file', help="The Anime Studio file with styles renamed.")
    args = parser.parse_args()

    # Check input file
    input_path = os.path.abspath(args.input_anime_studio_file)
    if not os.path.exists(input_path):
        parser.error("%s does not exist." % input_path)
    if not input_path.endswith(".anime"):
        parser.error("%s is not an Anime Studio (.anime) file." % input_path)

    # Check output file
    output_path = os.path.abspath(args.output_anime_studio_file)
    if os.path.exists(output_path):
        parser.error("%s already exists. Please select a separate file." % output_path)
    if not output_path.endswith(".anime"):
        parser.error("%s is not an Anime Studio (.anime) file." % output_path)

    rename_styles(input_path)
    writeProject(output_path, json.dumps(_anime_studio))

if __name__ == '__main__':
    perform()
