import enchant
spellChecker = enchant.Dict("de_DE_frami")


def wordAnalysis(pdfPagesAsImageList):
    for pdfPage in pdfPagesAsImageList:
        for figure in pdfPage["figures"]:
            minWordHeight = None
            for text in figure["textData"]:
                #spellCheck
                if not spellChecker.check(text["text"]):
                    figure["imageAnalysis"]["spellingErrors"].append(text["text"])
                #height
                if not minWordHeight:
                    minWordHeight = text["height"]
                elif text["height"] < minWordHeight:
                    minWordHeight = text["height"]
            if minWordHeight:
                figure["imageAnalysis"]["minWordHeight"] = minWordHeight
                
    return pdfPagesAsImageList




