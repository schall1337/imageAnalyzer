from exif import Image

def extractExif(imageDetailList):
    tmp = "../../tmp/"
    for imageDetail in imageDetailList:
        if imageDetail["imageExt"] == "jpeg":
            with open(tmp + imageDetail["fileName"], 'rb') as image_file:
                image = Image(image_file)
                if image.has_exif:
                    exifData = {}
                    keys = image.get_all()
                    for key in keys:
                        exifData[key] = image[key]
                    imageDetail["exif"] = exifData
    return imageDetailList



        