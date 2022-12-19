from haishoku.haishoku import Haishoku
import wcag_contrast_ratio as contrast

def colorCheckPrimitive(pdfPagesAsImageList):
    for pdfPage in pdfPagesAsImageList:
        for figure in pdfPage["figures"]:
            haishoku = Haishoku.loadHaishoku("../../tmp/"+figure["fileName"])
            dominantColor = haishoku.dominant
            palette = haishoku.palette
            figure["imageAnalysis"]["color_primitive"]["background"] = dominantColor
            for color in palette[1:]:
                wcagContrast = round(contrast.rgb(tuple(elem / 255 for elem in dominantColor), tuple(elem / 255 for elem in color[1])),2)
                if wcagContrast < 3:
                    colorInfo = {"color" : color[1], "contrast": wcagContrast}
                    figure["imageAnalysis"]["color_primitive"]["indistinctColors"].append(colorInfo)

