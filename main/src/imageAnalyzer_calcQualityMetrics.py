import matlab.engine

def calcQualityMetrics(imageDetailList):
    eng = matlab.engine.start_matlab()

    for imageDetail in imageDetailList:
        fileName = "../../tmp/" + imageDetail["fileName"]

        blockinessScore = eng.jpeg_quality_score(fileName)
        imageDetail["imageAnalysis"]["blockinessScore"] = blockinessScore

        piqeScore = eng.piqe_score(fileName)
        imageDetail["imageAnalysis"]["piqeScore"] = piqeScore

    eng.quit()

    return imageDetailList