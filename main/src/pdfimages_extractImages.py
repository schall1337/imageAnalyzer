import subprocess

pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\python_modell_ba\\main\\resources\\same_pic_diff_sizes.pdf"

pathOfOutput = "..\\tmp\\image"

SCRIPT_NAME = "pdfimages_extractImages"

def extractImages():
    subprocessResult = runPdfimagesSubprocess()
    return validatePdfimagesResult(subprocessResult)


def runPdfimagesSubprocess():
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