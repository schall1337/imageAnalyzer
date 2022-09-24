from pdfimages_extractImages import extractImages
from pdfimages_getImagesDetails import getImageDetailList
from pdfimages_mapImagePathToDetails import mapImagePathToDetails
from pdfimages_reverseImageSearch import reverseImageSearcher
from pdfimages_getImageCoordinates import getImageCoordinates
from pdfimages_checkImagePosition import isImageInsideBorder
from pdfimages_deleteTmpFiles import deleteTmpFiles
from pdfimages_extractExif import extractExif

import json

pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\testdokumentBachelor.pdf"

extractImages(pathOfPdf)
imageDetailList = getImageDetailList(pathOfPdf)
imageDetailList = mapImagePathToDetails(imageDetailList)
#imageDetailList = reverseImageSearcher(imageDetailList)
imageDetailList = getImageCoordinates(imageDetailList, pathOfPdf)
imageDetailList = isImageInsideBorder(imageDetailList, pathOfPdf)
imageDetailList = extractExif(imageDetailList)

deleteTmpFiles()

print(json.dumps(imageDetailList))
