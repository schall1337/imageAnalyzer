import matlab.engine


def calcBlockiness(imageDetailList):
    eng = matlab.engine.start_matlab()

    for imageDetail in imageDetailList:
        qualityScore = eng.jpeg_quality_score("../../tmp/" + imageDetail["fileName"])
        imageDetail["imageAnalysis"]["qualityScore"] = qualityScore
    
    eng.quit()

    return imageDetailList