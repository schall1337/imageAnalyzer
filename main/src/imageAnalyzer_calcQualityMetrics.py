import matlab.engine
import math

def calcQualityMetrics(imageDetailList):
    eng = matlab.engine.start_matlab()

    for imageDetail in imageDetailList:
        fileName = "../../tmp/" + imageDetail["fileName"]

        jpegQualityScore = eng.jpeg_quality_score(fileName)

        if math.isnan(float(jpegQualityScore)):
            jpegQualityScore = 0

        imageDetail["imageAnalysis"]["jpegQualityScore"] = jpegQualityScore

        piqeScore = eng.piqe_score(fileName)
        imageDetail["imageAnalysis"]["piqeScore"] = piqeScore

    eng.quit()

    return imageDetailList