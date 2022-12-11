from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

from reportlab.platypus import Table

from reportlab.platypus import TableStyle
from reportlab.lib import colors

import configparser

import fitz


def createReport(imageDetailList, pdfPagesAsImageList):

    config = configparser.ConfigParser()
    config.read('config-file.ini')

    reportData = {
        "layoutParserSize": 0,
        "internalPDFSize": 0,
        "jpegFormat": 0,
        "lowPPI": 0,
        "closeToBorder": 0,
        "jpegQualityScore": 0,
        "spellingErrors": 0,
        "metaData": 0,
        "webDetection": 0,
        "smallFontSize": 0,
        "bigImgSize": 0,
        "lowContrast": 0
    }

    reportData["internalPDFSize"] = len(imageDetailList)

    for img in imageDetailList:
        if img["imageExt"] == "jpg" or img["imageExt"] == "jpeg":
            reportData["jpegFormat"] += 1

        if int(img["x-ppi"]) < int(config['default']['min_ppi']) or int(img["y-ppi"]) < int(config['default']['min_ppi']):
            reportData["lowPPI"] += 1

        if img["exif"]:
            reportData["metaData"] += 1

        if img["imageAnalysis"]["jpegQualityScore"] < int(config['default']['jpeg_quality_score']):
            reportData["jpegQualityScore"] += 1

        if img["imageAnalysis"]["reverseImageDetection"] and img["imageAnalysis"]["reverseImageDetection"]["countPagesWithMatchingImages"]:
            reportData["webDetection"] += 1

        if img["size"]["size"] > int(config['default']['max_image_size']):
            reportData["bigImgSize"] += 1

    for page in pdfPagesAsImageList:
        for img in page["figures"]:
            reportData["layoutParserSize"] += 1

            if img["imageAnalysis"]["spellingErrors"]:
                reportData["spellingErrors"] += 1

            if img["imageAnalysis"]["minWordHeight"] is not None and img["imageAnalysis"]["minWordHeight"] <= int(config['default']['min_pixel_height']):
                reportData["smallFontSize"] += 1

            if img["imageAnalysis"]["isTooCloseToBorder"]:
                reportData["closeToBorder"] += 1

            if img["imageAnalysis"]["color"]["background"] and img["imageAnalysis"]["color"]["indistinctColors"]:
                reportData["lowContrast"] += 1

    tableData = [
        ['Report der automatischen Bildqualitätsanalyse', '', ''],
        ['Merkmal', 'Wert', 'Hinweis'],
        ['1. Bilder entdeckt (Layout Parser)', reportData['layoutParserSize'],
         'Können sowohl Rastergrafiken als auch\nVektorgrafiken sein'],
        ['2. Bilder entdeckt (Analyse PDF Struktur)',
         reportData['internalPDFSize'], 'Nur Rastergrafiken'],
        ['3. Bilder im JPEG Format', reportData["jpegFormat"],
            'Können aufgrund von Kompressionen\neine geringe Qualität aufweisen'],
        ['4. Bilder mit weniger als '+config['default']['min_ppi']+' PPI', reportData['lowPPI'],
            'Empfohlene Anzahl für Printmedien'],
        ['5. Bilder zu nah am Rand', reportData['closeToBorder'],
            'Werden ggf. nicht vollständig gedruckt'],
        ['6. Bilder mit hohen Anteil\n    an Blockartefakten', reportData['jpegQualityScore'],
            'Bildqualität kann durch Blackartefakte\nstark eingeschränkt sein'],
        ['7. Bilder mit Rechtschreibfehlern', reportData['spellingErrors'],
            'Überprüfen Sie die annotierten Bilder\nauf Rechtschreibfehler'],
        ['8. Bilder mit Metadaten', reportData['metaData'],
            'Metadaten können sensible Informationen\nenhalten (GPS Koordinaten etc.)'],
        ['9. Bilder im Internet gefunden', reportData['webDetection'],
            'Beachten Sie eine richtige Quellenangabe'],
        ['10. Bilder mit kleiner Schriftgröße (< '+config['default']['min_pixel_height']+'px)', reportData['smallFontSize'],
         'Beachten Sie eine adequate Schriftgröße\nfür eine bessere Leserlichkeit'],
        ['11. Bilder mit hoher Dateigröße (> '+config['default']['max_image_size']+' KB)', reportData['bigImgSize'],
         'Vielzahl an großen Bildern\nkann die PDF Dateigröße sehr groß\nwerden lassen'],
        ['12. Bilder mit geringem Farbkontrast (< 3 nach WCAG Standard)',
         reportData['lowContrast'], "Achten Sie auf eine gute Farbwahl"]
    ]

    fileName = '../../tmp/report.pdf'

    pdf = SimpleDocTemplate(
        fileName,
        pagesize=A4
    )

    table = Table(tableData)

    # add style
    style = TableStyle([
        ('SPAN', (0, 0), (2, 0)),
        ('BACKGROUND', (0, 0), (2, 0), colors.lightgrey),
        ('BACKGROUND', (0, 1), (2, 1), colors.silver),
        ('BACKGROUND', (0, 2), (0, -1), colors.beige),
        ('BACKGROUND', (1, 2), (1, -1), colors.ivory),
        ('BACKGROUND', (2, 2), (2, -1), colors.whitesmoke),


        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (2, 1), 'CENTER'),
        ('ALIGN', (1, 2), (2, -1), 'CENTER'),
        ('ALIGN', (0, 2), (0, -1), 'LEFT'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LINEBELOW', (0, 3), (-1, 3), 2, colors.black),
        

    ])
    table.setStyle(style)

    # Add red/green colors

    for i in range(4, len(tableData)):
        if tableData[i][1] == 0:
            ts = TableStyle(
                [('BACKGROUND', (1, i), (1, i), colors.palegreen)]
            )
            table.setStyle(ts)
        else:
            ts = TableStyle(
                [('BACKGROUND', (1, i), (1, i), colors.salmon)]
            )
            table.setStyle(ts)

    # Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('GRID', (0, 1), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(ts)

    elems = []
    elems.append(table)

    pdf.build(elems)

    #attach report and annotation together
    docReport = fitz.open(fileName)
    docAnnotation = fitz.open("../../tmp/annotation.pdf")
    docReport.insert_pdf(docAnnotation)
    docReport.save("../../output/bildanalyse_report.pdf")
    docReport.close()
    docAnnotation.close()