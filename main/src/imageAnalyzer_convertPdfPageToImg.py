import fitz

def convertPdfPageToImg(pdfFile):
    doc = fitz.open(pdfFile)
    pdfPageImgList = []
    count = 0
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(dpi = 300)  # render page to an image
        count += 1
        
        fileName = "pdfImgPage-" + str(count) + ".png"
        pdfPageImg = {"page": count,
                      "fileName": fileName,
                      "mediaBox": {"width" : page.mediabox.width, "height" : page.mediabox.height},
                      "pixMap": {"width" : pix.width, "height" : pix.height},
                      "figures": []
                      }
        pdfPageImgList.append(pdfPageImg)
        pix.save("../../tmp/" + fileName)  # store image as a PNG
    return pdfPageImgList
