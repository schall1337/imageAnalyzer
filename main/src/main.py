from imageAnalyzer_getImagesDetails import getImageDetailList
from imageAnalyzer_extractImage import extractImages
from imageAnalyzer_reverseImageSearch import reverseImageSearcher
from imageAnalyzer_getImageCoordinates import getImageCoordinates
from imageAnalyzer_checkImagePosition import isImageInsideBorder
from imageAnalyzer_extractExif import extractExif
from imageAnalyzer_convertPdfPageToImg import convertPdfPageToImg
from imageAnalyzer_deleteTmpFiles import deleteTmpFiles
from imageAnalyzer_layoutParser import getImagesFromLayoutParser

import json

pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\testdokumentBachelorCompressed.pdf"

imageDetailList = getImageDetailList(pathOfPdf)
extractImages(imageDetailList, pathOfPdf)
#imageDetailList = reverseImageSearcher(imageDetailList)
imageDetailList = getImageCoordinates(imageDetailList, pathOfPdf)
imageDetailList = isImageInsideBorder(imageDetailList, pathOfPdf)
imageDetailList = extractExif(imageDetailList)
pdfPagesAsImageList = convertPdfPageToImg(pathOfPdf)
pdfPagesAsImageList = getImagesFromLayoutParser(pdfPagesAsImageList)



#deleteTmpFiles()

print(json.dumps(pdfPagesAsImageList))
#print(json.dumps(imageDetailList))
