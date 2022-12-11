import fitz
import configparser

def calcPdfBorder(pathOfPdf):
    config = configparser.ConfigParser()
    config.read('config-file.ini')
    doc = fitz.open(pathOfPdf)
    page = doc.load_page(2)
    rectPage = page.mediabox

    pageWidth = rectPage.width
    pageHeight = rectPage.height

    #1cm = 28px at 72 dpi
    cm_to_pixel = 28

    x_top_left = float(config['default']['border_left']) * cm_to_pixel
    y_top_left = float(config['default']['border_top']) * cm_to_pixel

    x_bottom_right = pageWidth - (float(config['default']['border_right']) * cm_to_pixel)
    y_bottom_right = pageHeight - (float(config['default']['border_bottom']) * cm_to_pixel)
    
    r1 = fitz.Rect(x_top_left , y_top_left,x_bottom_right,y_bottom_right)

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
    #doc.saveIncr()
    #doc.close()
    return coordBorder

def isImageInsideBorder(imageDetailList, pathOfPdf):

    coordBorder = calcPdfBorder(pathOfPdf)
    borderPointTopLeft = coordBorder["top_left"]
    borderPointBottomRight = coordBorder["bottom_right"]

    for imageDetail in imageDetailList:
        imagePointTopLeft = imageDetail["coordinates"]["top_left"]
        imagePointBottomRight = imageDetail["coordinates"]["bottom_right"]
        if not (borderPointTopLeft["x"] < imagePointTopLeft["x"] < borderPointBottomRight["x"] and borderPointTopLeft["y"] < imagePointTopLeft["y"] < borderPointBottomRight["y"]):
            imageDetail["imageAnalysis"]["isTooCloseToBorder"] = True
            continue

        if not (borderPointTopLeft["x"] < imagePointBottomRight["x"] < borderPointBottomRight["x"] and borderPointTopLeft["y"] < imagePointBottomRight["y"] < borderPointBottomRight["y"]):
            imageDetail["imageAnalysis"]["isTooCloseToBorder"] = True

    return imageDetailList

