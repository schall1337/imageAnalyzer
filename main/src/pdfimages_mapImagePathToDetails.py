from os import listdir
from os.path import isfile, join

tmpPath = "..\\tmp"
SCRIPT_NAME = "pdfimages_mapImagePathToDetails"

def mapImagePathToDetails(imageDetailList):
    imageFileNames = [f for f in listdir(tmpPath) if isfile(join(tmpPath, f))] 
    if len(imageFileNames) == len(imageDetailList):
        for index, imageDetail in enumerate(imageDetailList):
            imageDetail["fileName"] = imageFileNames[index]
            print(imageDetail)
    else:
        raise Exception("imageDetailList length = '" + len(imageDetailList) + "' != imageFileNamesList = '" + len(imageFileNames) + "'. Script: " + SCRIPT_NAME)
    return imageDetailList





