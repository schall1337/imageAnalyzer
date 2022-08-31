import fitz

#pathOfPdf = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\coordTest.pdf"


def getImageCoordinates(imageDetailList, pathOfPdf):
    doc = fitz.open(pathOfPdf)
    for imageDetail in imageDetailList:
        page = doc.load_page(int(imageDetail["page"]) - 1)
        rect = page.get_image_rects(int(imageDetail["object"]))[0]
        coord = {
            "bottom_left": {"x" : rect.bottom_left.x, "y" : rect.bottom_left.y},
            "bottom_right": {"x" : rect.bottom_right.x, "y" : rect.bottom_right.y},
            "top_left": {"x" : rect.top_left.x, "y" : rect.top_left.y},
            "top_right": {"x" : rect.top_right.x, "y" : rect.top_right.y},
            "width": rect.width,
            "height": rect.height
        }
        imageDetail["coordinates"] = coord
    return imageDetailList
