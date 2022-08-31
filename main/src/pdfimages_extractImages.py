import subprocess

#pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\python_modell_ba\\main\\resources\\same_pic_diff_sizes.pdf"

pathOfOutput = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\tmp\\tmp"

SCRIPT_NAME = "pdfimages_extractImages"

def extractImages(pathOfPdf):
    subprocessResult = runPdfimagesSubprocess(pathOfPdf)
    return validatePdfimagesResult(subprocessResult)


def runPdfimagesSubprocess(pathOfPdf):
    return subprocess.run(["pdfimages", "-all", pathOfPdf, pathOfOutput], capture_output=True, text=True, check=True)


def validatePdfimagesResult(subprocessResult):
    try:
        if (subprocessResult.returncode != 0):
            raise Exception(
                "Error while running pdfimages as subprocess: '" + subprocessResult.stderr + "'. Script: " + SCRIPT_NAME)
    except Exception as e:
        print(e)
    else:
        return True