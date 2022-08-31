from pdfimages_extractImages import extractImages
from pdfimages_getImagesDetails import getImageDetailList
from pdfimages_mapImagePathToDetails import mapImagePathToDetails
from pdfimages_reverseImageSearch import reverseImageSearcher
from pdfimages_getImageCoordinates import getImageCoordinates
from pdfimages_checkImagePosition import isImageInsideBorder


pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\coordTest.pdf"
#imageDetailList = None
extractImages(pathOfPdf)
imageDetailList = getImageDetailList(pathOfPdf)
imageDetailList = mapImagePathToDetails(imageDetailList)
#imageDetailList = reverseImageSearcher(imageDetailList)
imageDetailList = getImageCoordinates(imageDetailList, pathOfPdf)
imageDetailList = isImageInsideBorder(imageDetailList, pathOfPdf)

print(imageDetailList)


""" import os
cwd = os.getcwd()

print(cwd) """