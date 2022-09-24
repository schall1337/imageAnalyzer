from exif import Image
import os
import json

def extractExif(imageDetailList):
    cwd = os.getcwd()
    tmp = "\\main\\tmp\\"
    for imageDetail in imageDetailList:
        with open(cwd + tmp + imageDetail["fileName"], 'rb') as image_file:
            image = Image(image_file)
            if image.has_exif:
                exifData = {}
                keys = image.get_all()
                for key in keys:
                    exifData[key] = image[key]
                #imageDetail["exif"] = json.dumps(exifData)
                imageDetail["exif"] = exifData
    return imageDetailList



        