import fitz


def calcPdfBorder(pathOfPdf):
    doc = fitz.open(pathOfPdf)
    page = doc.load_page(0)
    rectPage = page.mediabox

    pageWidth = rectPage.width
    pageHeight = rectPage.height

    
    tenPercentOfWidth = pageWidth * 0.15
    tenPercentOfHeight = pageHeight * 0.1
    r1 = fitz.Rect(0 + tenPercentOfWidth , 0 + tenPercentOfWidth,pageWidth - tenPercentOfWidth,pageHeight-tenPercentOfHeight)

    coordBorder  = {
                "bottom_left": {"x" : r1.bottom_left.x, "y" : r1.bottom_left.y},
                "bottom_right": {"x" : r1.bottom_right.x, "y" : r1.bottom_right.y}, 
                "top_left": {"x" : r1.top_left.x, "y" : r1.top_left.y},
                "top_right": {"x" : r1.top_right.x, "y" : r1.top_right.y},
    }
    
    #shape = page.new_shape()
    #shape.draw_rect(r1)
    #shape.finish(width=0.3)
    #shape.commit()
    #doc.save("C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\coordTest2.pdf")

    return coordBorder

def isImageInsideBorder(imageDetailList, pathOfPdf):

    coordBorder = calcPdfBorder(pathOfPdf)
    borderPointTopLeft = coordBorder["top_left"]
    borderPointBottomRight = coordBorder["bottom_right"]

    for imageDetail in imageDetailList:
        imagePointTopLeft = imageDetail["coordinates"]["top_left"]
        imagePointBottomRight = imageDetail["coordinates"]["bottom_right"]
        if not (borderPointTopLeft["x"] < imagePointTopLeft["x"] < borderPointBottomRight["x"] and borderPointTopLeft["y"] < imagePointTopLeft["y"] < borderPointBottomRight["y"]):
            imageDetail["isTooCloseToBorder"] = True
            continue

        if not (borderPointTopLeft["x"] < imagePointBottomRight["x"] < borderPointBottomRight["x"] and borderPointTopLeft["y"] < imagePointBottomRight["y"] < borderPointBottomRight["y"]):
            imageDetail["isTooCloseToBorder"] = True

    return imageDetailList

