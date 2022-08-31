import subprocess
import re

#pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\python_modell_ba\\main\\resources\\same_pic_diff_sizes.pdf"
SCRIPT_NAME = "pdfimages_getImagesDetails"

def getImageDetailList(pathOfPdf):
    subprocessResult = runPdfimagesSubprocess(pathOfPdf)
    if validatePdfimagesResult(subprocessResult):
        pdfimagesResultList = subprocessResult.stdout
        imageResults = getResultAsJsonArray(pdfimagesResultList)
        return imageResults


def runPdfimagesSubprocess(pathOfPdf):
    return subprocess.run(["pdfimages", "-list", pathOfPdf], capture_output=True, text=True, check=True)


def validatePdfimagesResult(subprocessResult):
    try:
        if (subprocessResult.returncode != 0):
            raise Exception(
                "Error while running pdfimages as subprocess: '" + subprocessResult.stderr + "'. Script: " + SCRIPT_NAME)
    except Exception as e:
        print(e)
    else:
        return True


def getResultAsJsonArray(pdfimagesResult):
    imageResultsAsJsonArray = []
    lines = pdfimagesResult.splitlines()
    # skip header (line 0) and separator (line 1) to start dire with result
    # TODO check if line exists
    if len(lines) > 1:
        for line in lines[2:]:
            imageValueArray = line.split()
            imageResultsAsJsonArray.append(
                mapResultToJson(imageValueArray))
    return imageResultsAsJsonArray


def mapResultToJson(imageValueArray):
    imageDetails = convertSizeToMegabyte(imageValueArray[14])
    imageModell = {
        "page": imageValueArray[0],
        "num": imageValueArray[1],
        "type": imageValueArray[2],
        "width": imageValueArray[3],
        "height": imageValueArray[4],
        "color": imageValueArray[5],
        "comp": imageValueArray[6],
        "bpc": imageValueArray[7],
        "enc": imageValueArray[8],
        "interp": imageValueArray[9],
        "object": imageValueArray[10],
        "ID": imageValueArray[11],
        "x-ppi": imageValueArray[12],
        "y-ppi": imageValueArray[13],
        "size": imageDetails,
        "ratio": imageValueArray[15],
        "fileName": "",
        "reverseImageDetection": "",
        "coordinates": "",
        "isTooCloseToBorder": False
    }
    return imageModell

#helper class
def convertSizeToMegabyte(imageSize):
    #example "80.4K"
    #get unit from string
    unit = "".join(re.split("[^a-zA-Z]*", imageSize))
    #get float from string
    value = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", imageSize)[0])
    
    details = {
        "unit": "megabytes",
        "size": ""
    }

    match unit:
        case 'B':
            details["size"] =  value / 1000000
        case 'K':
            details["size"] = value / 1000
        case 'M':
            details["size"] = value
        case 'G':
            details["size"] = value * 1000

    return details

