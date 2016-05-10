#!/usr/bin/env python
""" Print out the layers for an animeStudio file (.anime)
"""
import argparse
import os
import anime

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

    # listLayersModule.iterateLayers(path)

    for name in anime.layer_names(anime.get_data(path)['layers']):
        print("layer name is ", name)

if __name__ == '__main__':
    perform()
