#!/usr/bin/env python
"""Extract To JSON ? Takes 1 or more .anime file and converts it to JSON
extract_to_json.py <.anime files>
"""
import os
import os.path
import json
import shutil
import sys
import zipfile


def ExtractToJSON(animepath, beautify=True):
    if (not os.path.exists(animepath)):
       print 'ERROR: %s does not exist' % animepath
       return

    # Get the folder and the file name for the path
    folder, animefilename = os.path.split(animepath)
    print 'Extracting from ' + animefilename + '...'

    # Open the .anime file
    with zipfile.ZipFile(animepath) as zip_file:

        # Iterate over all of the items in the zip file
        for item in zip_file.namelist():
            filename = os.path.basename(item)
            # skip everything except the .animeproj file, which is JSON
            if filename != 'Project.animeproj':
                continue
            # Create the extracted .json path name
            filename, ext = os.path.splitext(animefilename)
            filename += '.json'
            jsonpath = os.path.join(folder, filename)
            # Load the JSON from the zip file and dump it beautified to the .json path
            source = zip_file.open(item)
            if (beautify):
                json_obj = json.load(source)
                json.dump(json_obj, file(jsonpath, "wb"), sort_keys=False)
            else:
                shutil.copyfileobj(source, file(jsonpath, "wb"))
def Usage():
    print ('%s <.anime files> ? Extract .anime to JSON') % os.path.basename(sys.argv[0])

def perform():
    numArgs = len(sys.argv)
    if numArgs == 1:
        Usage()
        return
    for animepath in sys.argv[1:]:
        ExtractToJSON(os.path.normpath(animepath))

if __name__ == '__main__':
    perform()
