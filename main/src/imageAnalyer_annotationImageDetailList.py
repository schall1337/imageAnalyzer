import fitz

def generateAnnotationImageDetailList(pathOfPdf, imageDetailList):
    doc = fitz.open(pathOfPdf)
    for imageDetail in imageDetailList:
        outputTextList = []
        # coord
        topLeftX = imageDetail["coordinates"]["top_left"]["x"]
        topLeftY = imageDetail["coordinates"]["top_left"]["y"]
        bottomRightX = imageDetail["coordinates"]["bottom_right"]["x"]
        bottomRightY = imageDetail["coordinates"]["bottom_right"]["y"]
        # page
        page = doc[int(imageDetail["page"])-1]
        page.set_rotation(0)

        # annotation offset
        offset = 0

        # outputText
        outputTextList.append(getGeneralInformation(imageDetail))
        outputTextList.append(getBlockinessInformation(imageDetail))
        if(imageDetail["exif"]):
            outputTextList.append(getExifData(imageDetail["exif"]))
        
        if(imageDetail["imageAnalysis"]["reverseImageDetection"]["countPagesWithMatchingImages"]):
            outputTextList.append(getReverseImageSearchResults(imageDetail["imageAnalysis"]["reverseImageDetection"]))

        for output in outputTextList:
            rect = fitz.Rect(topLeftX + offset, topLeftY, bottomRightX, bottomRightY)
            page.add_text_annot(rect.tl, output)
            offset += 30

    doc.save("testAnnotation.pdf", deflate=False)
    doc.close()

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

def getBlockinessInformation(imageDetail):
    blockinessScore = int(imageDetail["imageAnalysis"]["qualityScore"])
    outputBlockiness = """
    Kompressionsinformation

    Der Blockartefaktescore gibt an, wie stark die Blockartefakte im Bild vertreten sind.
    Blockartefakte entstehen durch zu hohe Kompressionsraten. Der Score ist auf einer
    Skala von 1 bis 10 ausgelegt (1 sehr schlecht, 10 sehr gut).

    Blockartefaktescore: {blockinessScore}

    Hinweis:
    """.format(blockinessScore=blockinessScore)

    if blockinessScore < 6:
        outputBlockiness += """
        Der berechnete Score ist unter der Schwelle von '6'.
        Überprüfen Sie, ob offensichtliche Kompressionartefakte sichtbar sind.
        """
    else:
        outputBlockiness += """
        Der berechnete Score ist über der Schwelle von '6'.
        Es scheinen keine offensichtlichen Kompressionartefakte vorhanden zu sein.
        """
    
    return outputBlockiness

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
    
    if x_ppi < 300:
        allgemeineHinweise.append(
            "- Die horizontale Auflösung beträgt weniger als 300 ppi (Optimal min. 300 ppi)")
    
    if y_ppi < 300:
        allgemeineHinweise.append("- Die vertikale Auflösung beträgt weniger als 300 ppi (Optimal min. 300 ppi)")
    
    if groesse > 3000:
        allgemeineHinweise.append("- Bildgröße überschreitet 3 MB")
    
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
