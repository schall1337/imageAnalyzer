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

import timeit

import json
import configparser

CSV_TEST = "getRasterMetaData,extractRasterImgs,getRasterImgCoord,extractEXIF,convertPdfPageToRasterImg,getImgsFromLayoutParser,getWordsFromImgs,reverseImageSearcher,checkIfRasterImgIsInsideBorder,calcQualityMetrics,wordAnalysis,colorCheck,colorCheckPrimitive,generateAnnotation,generateReport,deleteTmpFiles,fullExeTime\n"

#TEST RUNS OF 5 CAN TAKE WITH TOTAL EXECUTION TIME OF 30 SEC ALREADY 2:30 MIN
TEST_RUNS = 5

def helperCsvAddLine(start_time):
    global CSV_TEST 
    CSV_TEST += str(timeit.default_timer()- start_time) +","

def helperCsvEndLine():
    global CSV_TEST 
    CSV_TEST += "\n"

def testPrototyp():
    config = configparser.ConfigParser()
    config.read('config-file.ini')

    pathOfPdf = "../resources/testdokumentBachelorCompressed.pdf"
    #pathOfPdf = "../resources/Bachelorarbeit_Daniel_Schall.pdf"

    # data retrieval
    start_prototyp = timeit.default_timer()
    start_time = timeit.default_timer()
    imageDetailList = getImageDetailList(pathOfPdf)
    helperCsvAddLine(start_time)
    print("imageDetailList: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    extractImages(imageDetailList, pathOfPdf)
    helperCsvAddLine(start_time)
    print("extractImages: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    getImageCoordinates(imageDetailList, pathOfPdf)
    helperCsvAddLine(start_time)
    print("getImageCoordinates: {}".format(
        timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    extractExif(imageDetailList)
    helperCsvAddLine(start_time)
    print("extractExif: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    pdfPagesAsImageList = convertPdfPageToImg(pathOfPdf)
    helperCsvAddLine(start_time)
    print("convertPdfPageToImg: {}".format(
        timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    getImagesFromLayoutParser(pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("getImagesFromLayoutParser: {}".format(
        timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    extractWordsFromImage(pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("extractWordsFromImage: {}".format(
        timeit.default_timer() - start_time))

    # data analysis
    start_time = timeit.default_timer()
    #reverseImageSearcher(imageDetailList)
    helperCsvAddLine(start_time)
    print("reverseImageSearcher: {}".format(
        timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    isImageInsideBorder(imageDetailList, pathOfPdf)
    helperCsvAddLine(start_time)
    print("isImageInsideBorder: {}".format(
        timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    calcQualityMetrics(imageDetailList)
    helperCsvAddLine(start_time)
    print("calcQualityMetrics: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    wordAnalysis(pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("wordAnalysis: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    colorCheck(pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("colorCheck: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    colorCheckPrimitive(pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("colorCheckPrimitive: {}".format(
        timeit.default_timer() - start_time))

    # data output (annotation in pdf)
    start_time = timeit.default_timer()
    generateAnnotation(pathOfPdf, imageDetailList, pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("generateAnnotation: {}".format(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    createReport(imageDetailList, pdfPagesAsImageList)
    helperCsvAddLine(start_time)
    print("createReport: {}".format(timeit.default_timer() - start_time))

    if int(config['default']['debug_mode']) == 0:
        start_time = timeit.default_timer()
        deleteTmpFiles()
        helperCsvAddLine(start_time)
        print("deleteTmpFiles: {}".format(timeit.default_timer() - start_time))

    helperCsvAddLine(start_prototyp)
    print("full time: {}".format(timeit.default_timer() - start_prototyp))
    helperCsvEndLine()

timeit.timeit(testPrototyp, number = TEST_RUNS)
print(CSV_TEST )
f = open("../../output/timingResults.csv","w")
f.write(CSV_TEST)
f.close()

# print(json.dumps(pdfPagesAsImageList))
# print(json.dumps(imageDetailList))
# print("\n")
# print("End")
