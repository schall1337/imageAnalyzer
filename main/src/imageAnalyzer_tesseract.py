import cv2
from pytesseract import pytesseract
from pytesseract import Output


custom_psm_config = r'--psm 11'
path = "../../tmp/"

def extractWordsFromImage(pdfPagesAsImageList):
    count = 1
    for pdfPage in pdfPagesAsImageList:
        if len(pdfPage["figures"]) > 0:
            for figure in pdfPage["figures"]:
                figureImg = cv2.imread(path + figure["fileName"])
                figure_data = pytesseract.image_to_data(figureImg, output_type=Output.DICT, config = custom_psm_config, lang='deu')
                #filtered_list = filter(lambda x: len(x) > 3, figure_data['text'])
                for i, word in enumerate(figure_data["text"]):
                    if len(word) > 2:
                        textData = {
                            "text" : word,
                            "height" : figure_data['height'][i]
                        }
                        figure["textData"].append(textData)
                        x,y,w,h = figure_data['left'][i],figure_data['top'][i],figure_data['width'][i],figure_data['height'][i]
                        cv2.rectangle(figureImg,(x,y),(x+w,y+h),(0,255,0),1)
                cv2.imwrite(path + "ocrImage_" + str(count) + ".png", figureImg)
                count += 1