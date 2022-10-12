from haishoku.haishoku import Haishoku
import colorsys


def colorCheck(pdfPagesAsImageList):
    # background white threshold
    hsv_white_lower_threshold = (0, 0, 0.96)
    hsv_white_upper_threshold = (1, 0.03, 1)
    # background yellow threshold
    hsv_yellow_lower_threshold = (0.15, 0.3, 0.95)
    hsv_yellow_upper_threshold = (0.18, 1, 1)

    for pdfPage in pdfPagesAsImageList:
        for figure in pdfPage["figures"]:
            haishoku = Haishoku.loadHaishoku("../../tmp/"+figure["fileName"])
            dominantColor = haishoku.dominant
            palette = haishoku.palette

            if isBetweenTreshold(dominantColor, hsv_white_lower_threshold, hsv_white_upper_threshold):
                for color in palette:
                    anteil = color[0]
                    rgb = color[1]
                    if anteil > 0 and isBetweenTreshold(color[1], hsv_yellow_lower_threshold, hsv_yellow_upper_threshold):
                        indistinctColor = {"anteil": anteil*100,
                                           "farbton": "Gelb",
                                           "rgb": rgb
                                           }
                        figure["imageAnalysis"]["color"]["indistinctColors"].append(
                            indistinctColor)

                if figure["imageAnalysis"]["color"]["indistinctColors"]:
                    background = {"anteil": palette[0][0]*100,
                    "farbton": "Weiß",
                    "rgb": palette[0][1]
                    }
                    figure["imageAnalysis"]["color"]["background"].append(background)
    
    return pdfPagesAsImageList

def isBetweenTreshold(color, lowerTreshold, upperTreshold):
    r, g, b = color
    hsv_color = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    fitsLowerTreshold = all(x >= y for x, y in zip(hsv_color, lowerTreshold))
    fitsUpperTreshold = all(x <= y for x, y in zip(hsv_color, upperTreshold))
    return fitsLowerTreshold and fitsUpperTreshold
