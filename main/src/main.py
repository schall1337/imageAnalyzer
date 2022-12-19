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
from imageAnalyzer_annotation import generateAnnotation
from imageAnalyzer_wordAnalysis import wordAnalysis
from imageAnalzyer_colorCheck import colorCheck
from imageAnalyzer_reportBuilder import createReport
from imageAnalyzer_colorCheckPrimitive import colorCheckPrimitive

import configparser
import sys

def run():

    deleteTmpFiles()
    # -------------data retrieval-------------
    imageDetailList = getImageDetailList(pathOfPdf)

    extractImages(imageDetailList, pathOfPdf)

    getImageCoordinates(imageDetailList, pathOfPdf)

    extractExif(imageDetailList)

    pdfPagesAsImageList = convertPdfPageToImg(pathOfPdf)

    getImagesFromLayoutParser(pdfPagesAsImageList)

    extractWordsFromImage(pdfPagesAsImageList)

    # -------------data analysis-------------

    reverseImageSearcher(imageDetailList)

    isImageInsideBorder(imageDetailList, pathOfPdf)

    calcQualityMetrics(imageDetailList)

    wordAnalysis(pdfPagesAsImageList)

    colorCheck(pdfPagesAsImageList)

    colorCheckPrimitive(pdfPagesAsImageList)

    # -------------data output (annotation in pdf)-------------
    generateAnnotation(pathOfPdf, imageDetailList, pdfPagesAsImageList)

    createReport(imageDetailList, pdfPagesAsImageList)

    if int(config['default']['debug_mode']) == 0:
        deleteTmpFiles()


if len(sys.argv) > 1:
    pathOfPdf = sys.argv[1]
    config = configparser.ConfigParser()
    config.read('config-file.ini')
    print("---start prototyp----")
    run()
    print("---end prototyp---")
else:
    print("no path provided")