from imageAnalyzer_getImagesDetails import getImageDetailList
from imageAnalyzer_extractImage import extractImages
from imageAnalyzer_reverseImageSearch import reverseImageSearcher
from imageAnalyzer_getImageCoordinates import getImageCoordinates
from imageAnalyzer_checkImagePosition import isImageInsideBorder
from imageAnalyzer_extractExif import extractExif
from imageAnalyzer_convertPdfPageToImg import convertPdfPageToImg
from imageAnalyzer_deleteTmpFiles import deleteTmpFiles
from imageAnalyzer_layoutParser import getImagesFromLayoutParser
from imageAnalyzer_tesseract import extractWordsFromImage
from imageAnalyzer_calcQualityMetrics import calcQualityMetrics
from imageAnalyer_annotation import generateAnnotation
from imageAnalyzer_wordAnalysis import wordAnalysis
from imageAnalzyer_colorCheck import colorCheck
from imageAnalyzer_reportBuilder import createReport

import json

#pathOfPdf = "../resources/testdokumentBachelorCompressed.pdf"
pathOfPdf = "../resources/TestLibre.pdf"

# data retrieval
imageDetailList = getImageDetailList(pathOfPdf)
extractImages(imageDetailList, pathOfPdf)
getImageCoordinates(imageDetailList, pathOfPdf)
extractExif(imageDetailList)

pdfPagesAsImageList = convertPdfPageToImg(pathOfPdf)
getImagesFromLayoutParser(pdfPagesAsImageList)
extractWordsFromImage(pdfPagesAsImageList)

# data analysis
reverseImageSearcher(imageDetailList)
isImageInsideBorder(imageDetailList, pathOfPdf)
calcQualityMetrics(imageDetailList)

wordAnalysis(pdfPagesAsImageList)
colorCheck(pdfPagesAsImageList)

# data output (annotation in pdf)
generateAnnotation(pathOfPdf, imageDetailList, pdfPagesAsImageList)
createReport(imageDetailList, pdfPagesAsImageList)

deleteTmpFiles()

#print(json.dumps(pdfPagesAsImageList))
print("\n")
#print(json.dumps(imageDetailList))
print("End")
