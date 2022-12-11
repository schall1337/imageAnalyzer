import fitz
import configparser

config = configparser.ConfigParser()
config.read('config-file.ini')

def generateAnnotation(pathOfPdf, imageDetailList, pdfPagesAsImageList):
    doc = fitz.open(pathOfPdf)

    generateAnnotationImageDetailList(imageDetailList, doc)
    generateAnnotationPdfPagesAsImageList(pdfPagesAsImageList, doc)

    doc.save("../../tmp/annotation.pdf", deflate=False)
    doc.close()

###PagesAsImageList
def generateAnnotationPdfPagesAsImageList(pdfPagesAsImageList, doc):

    for pdfImgPage in pdfPagesAsImageList:
        if pdfImgPage["figures"]:
            x_offset = 0
            y_offset = 30
            scalingFactor = pdfImgPage["pixMap"]["width"] / pdfImgPage["mediaBox"]["width"]
            docPage = doc[pdfImgPage["page"]-1]
            for figure in pdfImgPage["figures"]:
                outputTextList = []
                #coord
                topLeftX = figure["coordinates"][0][0] / scalingFactor
                topLeftY = figure["coordinates"][0][1] / scalingFactor
                bottomRightX = figure["coordinates"][2][0] / scalingFactor
                bottomRightY = figure["coordinates"][2][1] / scalingFactor
                
                ##outputText
                if figure["imageAnalysis"]["spellingErrors"]:
                    outputTextList.append(getspellingErrors(figure))
                
                if figure["imageAnalysis"]["minWordHeight"] is not None and figure["imageAnalysis"]["minWordHeight"] <= int(config['default']['min_pixel_height']):
                    outputTextList.append(getSmallCharacterInformation(figure, int(config['default']['min_pixel_height'])))

                if figure["imageAnalysis"]["isTooCloseToBorder"]:
                    outputTextList.append(getTooCloseToBorderInfo())
                
                if figure["imageAnalysis"]["color"]["background"]:
                    outputTextList.append(getColorAnalysis(figure["imageAnalysis"]["color"]))
                
                if figure["imageAnalysis"]["color_primitive"]:
                    outputTextList.append(getPrimitiveColorAnalysis(figure["imageAnalysis"]["color_primitive"]))

                for output in outputTextList:
                    rect = fitz.Rect(topLeftX + x_offset, topLeftY + y_offset, bottomRightX, bottomRightY)
                    docPage.add_text_annot(rect.tl, output)
                    x_offset += 30

def getColorAnalysis(colorData):
    farbtonHintergrund = colorData["background"][0]["farbton"]
    anteilHintergrund = colorData["background"][0]["anteil"]
    outputColorText = "Hinweise zur Farbwahl\n\n"
    outputColorText += "- Es wurde ein Hintergrund mit dem Farbton '{farbton}' erkannt ({anteil}% Anteil)\n\n".format(farbton = farbtonHintergrund, anteil =anteilHintergrund)
    for indistinctColor in colorData["indistinctColors"]:
        farbton = indistinctColor["farbton"]
        anteil = indistinctColor["anteil"]
        contrast = indistinctColor["wcgaContrast"]
        outputColorText += "- Es wurde der Farbton '{farbton}' im Bild erkannt ({anteil}% Anteil)\n".format(farbton=farbton, anteil=anteil)
        outputColorText += "- Der Kontrast der beiden Farben entspricht nach der WCAG Richtlinie einem Wert von '{contrast}', es sollte mindestens einen Wert von '3' haben\n".format(contrast=contrast)
        outputColorText += "- Weitere Informationen unter 'https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html'\n\n"
    outputColorText += "\nHinweis:\nDiese Farben haben einen niedrigen Kontrast zu einander und können nur schwer gelesen werden."
    return outputColorText

def getPrimitiveColorAnalysis(primColorData):
    farbtonHintergrund = primColorData["background"]
    outputColorText = "Hinweise zur Farbwahl\n\n"
    outputColorText += "- Es wurde ein Hintergrund mit dem RGB-Wert '{farbton}' erkannt\n\n".format(farbton = farbtonHintergrund)
    for indistinctColor in primColorData["indistinctColors"]:
        farbton = indistinctColor["color"]
        contrast = indistinctColor["contrast"]
        outputColorText += "- Es wurde der RGB-Wert '{farbton}' im Bild erkannt)\n".format(farbton=farbton)
        outputColorText += "- Der Kontrast der beiden Farben entspricht nach der WCAG Richtlinie einem Wert von '{contrast}', es sollte mindestens einen Wert von '3' haben\n\n".format(contrast=contrast)
    outputColorText += "- Weitere Informationen unter 'https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html'\n\n"
    outputColorText += "\nHinweis:\nDiese Farben haben einen niedrigen Kontrast zu einander und können nur schwer gelesen werden."
    return outputColorText

def getTooCloseToBorderInfo():
    outputTooCloseToBorder = "Hinweis zur Position\n\nEs wurde festgestellt, dass die Position des Bildes zu nah am Rand ist."
    return outputTooCloseToBorder


def getSmallCharacterInformation(figure, MIN_CHAR_HEIGHT):
    outputSmallCharacterInfo = "Hinweis zur Schriftgröße\n\nEs wurden Wörter mit sehr kleiner Schriftgröße erkannt.\n\n"
    
    for word in figure["textData"]:
        if word["height"] <= MIN_CHAR_HEIGHT:
            #ocr wurde bei 144dpi durchgeführt, standard anzeige ist 72dpi, deswegen durch 2 teilen
            #1px = 0.75pt
            outputSmallCharacterInfo += "- '" + word["text"] + ", Höhe: ~" + str(word["height"]/2) + "px bzw. ~" + str(word["height"]/2*0.75) + "pt\n"
    
    outputSmallCharacterInfo += "\nDie angegebenen Werte sind für 72 DPI berechnet"
    outputSmallCharacterInfo += "\nEs empfiehlt sich eine Größe von min. 8pt"
    return outputSmallCharacterInfo

def getspellingErrors(figure):
    outputSpellingError = "Rechtschreibfehler bzw. unbekannte Wörter\n"

    for spellingError in figure["imageAnalysis"]["spellingErrors"]:
        outputSpellingError+="- '" + spellingError+"'\n"
    
    outputSpellingError+= "\nHinweis: Wörter können aufgrund von schlechter Bildqualität oder zu kleiner Schrift falsch erkannt werden."
    return outputSpellingError

###imageDetailList Annotation
def generateAnnotationImageDetailList(imageDetailList, doc):

    for imageDetail in imageDetailList:
        outputTextList = []
        # coord
        topLeftX = imageDetail["coordinates"]["top_left"]["x"]
        topLeftY = imageDetail["coordinates"]["top_left"]["y"]
        bottomRightX = imageDetail["coordinates"]["bottom_right"]["x"]
        bottomRightY = imageDetail["coordinates"]["bottom_right"]["y"]
        # page
        docPage = doc[int(imageDetail["page"])-1]
        docPage.set_rotation(0)

        # annotation offset
        x_offset = 0

        # outputText
        outputTextList.append(getGeneralInformation(imageDetail))
        outputTextList.append(getJpegQualityScoreInformation(imageDetail))
        outputTextList.append(getPiqeInformation(imageDetail))
        if imageDetail["exif"]:
            outputTextList.append(getExifData(imageDetail["exif"]))
        
        if imageDetail["imageAnalysis"]["reverseImageDetection"] and imageDetail["imageAnalysis"]["reverseImageDetection"]["countPagesWithMatchingImages"]:
            outputTextList.append(getReverseImageSearchResults(imageDetail["imageAnalysis"]["reverseImageDetection"]))

        for output in outputTextList:
            rect = fitz.Rect(topLeftX + x_offset, topLeftY, bottomRightX, bottomRightY)
            docPage.add_text_annot(rect.tl, output)
            x_offset += 30

def getPiqeInformation(imageDetail):
    piqeScore = int(imageDetail["imageAnalysis"]["piqeScore"])
    output = """
    PIQE Score (Perception-based Image QUality Evaluator)

    Der PIQE Score gibt die Verzerrung eines Bildes aufgrund von Blockartefakte
    und Gaußsches Rauschen an.
    Je höher der Score, desto schlechter ist die Qualität des Bildes.
    Werte unter 50 werden als gut wahrgenommen.

    PIQE Score: {piqeScore}

    Weitere Informationen unter
    https://de.mathworks.com/help/images/ref/piqe.html
    oder
    https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7084843
    """.format(piqeScore=piqeScore)

    return output

def getReverseImageSearchResults(reverseSearchDetails):
    outputReverse = """Ergebnisse der Bildsuche

    Das Bild wurde auf min. {count} Seiten gefunden.
    Nachfolgend werden die einzelnen Seiten aufgezeigt\n.
    """.format(count = reverseSearchDetails["countPagesWithMatchingImages"])

    for page in reverseSearchDetails["pagesWithMatchingImages"]:
        if page["fullMatchingImages"]:
            for fullyMatch in page["fullMatchingImages"]:
                outputReverse += fullyMatch + "\n"
        if page["partiallyMatchingImages"]:
            for partialMatch in page["partiallyMatchingImages"]:
                outputReverse += partialMatch + "\n"
    return outputReverse


def getExifData(imageDetailExif):
    outputExif = "Metadaten\n"
    if "image_description" in imageDetailExif:
        outputExif+= "Titelbeschreibung: " + imageDetailExif["image_description"]+ "\n"
    if "artist" in imageDetailExif:
        outputExif+= "Author: " + imageDetailExif["artist"] +"\n"
    if "copyright" in imageDetailExif:
        outputExif+= "Copyright: " + imageDetailExif["copyright"] +"\n"
    if "gps_latitude" in imageDetailExif:
        outputExif+= "GPS Latitude: " + str(imageDetailExif["gps_latitude"][0]) + " " + str(imageDetailExif["gps_latitude"][1]) + " " + str(imageDetailExif["gps_latitude"][2]) +"\n"
    if "gps_longitude" in imageDetailExif:
        outputExif+= "GPS Longitude: " + str(imageDetailExif["gps_longitude"][0]) + " " + str(imageDetailExif["gps_longitude"][1]) + " " + str(imageDetailExif["gps_longitude"][2]) +"\n"
    
    return outputExif

def getJpegQualityScoreInformation(imageDetail):
    jpegQualityScore = int(imageDetail["imageAnalysis"]["jpegQualityScore"])
    outputJpegQualityScore = """
    Kompressionsinformation

    Der JPEG-Qualityscore gibt an, wie stark Kompressionsartefakte im Bild vertreten sind.
    Kompressionsartefakte entstehen durch zu hohe Kompressionsraten. Der Score ist auf einer
    Skala von 1 bis 10 ausgelegt (1 sehr schlecht, 10 sehr gut).

    JPEG-Qualityscore: {jpegQualityScore}

    Hinweis:
    """.format(jpegQualityScore=jpegQualityScore)

    if jpegQualityScore < int(config['default']['jpeg_quality_score']):
        outputJpegQualityScore += """
        Der berechnete Score ist unter der Schwelle von """+config['default']['jpeg_quality_score']+""".
        Überprüfen Sie, ob offensichtliche Kompressionartefakte sichtbar sind.
        """
    else:
        outputJpegQualityScore += """
        Der berechnete Score ist über der Schwelle von """+config['default']['jpeg_quality_score']+""".
        Es scheinen keine offensichtlichen Kompressionartefakte vorhanden zu sein.
        """
    
    return outputJpegQualityScore

def getGeneralInformation(imageDetail):
    dateiendung = imageDetail["imageExt"].upper()
    breite = int(imageDetail["width"])
    hoehe = int(imageDetail["height"])
    farbraum = imageDetail["color"]
    x_ppi = int(imageDetail["x-ppi"])
    y_ppi = int(imageDetail["y-ppi"])
    groesse = imageDetail["size"]["size"]
    groessenEinheit = imageDetail["size"]["unit"]
    angezeigteBreite = int(imageDetail["coordinates"]["width"])
    angezeigteHoehe = int(imageDetail["coordinates"]["height"])

    isTooCloseToBorder = imageDetail["imageAnalysis"]["isTooCloseToBorder"]

    outputAllgemein = """
    Bildinformationen:
    Dateiendung: {dateiendung}
    Original Breite: {breite} px
    Original Höhe: {hoehe} px
    Gerenderte Breite: {angezeigteBreite} px
    Gerenderte Höhe: {angezeigteHoehe} px
    Farbraum: {farbraum}
    Horizontale Auflösung: {x_ppi} ppi
    Vertikale Auflösung: {y_ppi} ppi
    Größe: {groesse} {groessenEinheit}
    """.format(dateiendung=dateiendung, breite=breite, hoehe=hoehe, farbraum=farbraum, x_ppi=x_ppi, y_ppi=y_ppi, groesse=groesse, groessenEinheit=groessenEinheit, angezeigteBreite=angezeigteBreite, angezeigteHoehe=angezeigteHoehe)

    allgemeineHinweise = []

    if dateiendung == "JPEG" or dateiendung =="JPG":
        allgemeineHinweise.append(
            "- Bei der Benutztung des JPEG-Formats kann es zu hohen Qualitätsverlusten kommen")
    
    if x_ppi < int(config['default']['min_ppi']):
        allgemeineHinweise.append(
            "- Die horizontale Auflösung beträgt weniger als " + config['default']['min_ppi'] + " ppi (Optimal min. 300 ppi)")
    
    if y_ppi < int(config['default']['min_ppi']):
        allgemeineHinweise.append("- Die vertikale Auflösung beträgt weniger als " + config['default']['min_ppi'] +" ppi (Optimal min. 300 ppi)")
    
    if groesse > int(config['default']['max_image_size']):
        allgemeineHinweise.append("- Bildgröße überschreitet " + config['default']['max_image_size'] +" MB")
    
    if angezeigteBreite > breite:
        allgemeineHinweise.append("- Gerenderte Breite ist größer als originale Breite (Bild ggf. unscharf)")
    
    if angezeigteHoehe > hoehe:
        allgemeineHinweise.append("- Gerenderte Höhe ist größer als originale Höhe (Bild ggf. unscharf)")
    
    if angezeigteBreite < breite:
        allgemeineHinweise.append("- Gerenderte Breite ist kleiner als originale Breite (Details ggf. schwer erkennbar)")
    
    if angezeigteHoehe < hoehe:
        allgemeineHinweise.append("- Gerenderte Höhe ist kleiner als originale Höhe (Details ggf. schwer erkennbar)")
    
    if isTooCloseToBorder:
        allgemeineHinweise.append("- Position des Bildes ist ggf. zu nah am Rand (Bild wird ggf. unvollständig gedruckt)")

    if len(allgemeineHinweise) > 0:
        outputAllgemein += "\nAllgemeine Hinweise:\n"
        for hinweise in allgemeineHinweise:
            outputAllgemein+=hinweise+"\n"


    return outputAllgemein
