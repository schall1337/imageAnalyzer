import enchant
spellChecker = enchant.Dict("de_DE_frami")

def spellCheck(pdfPagesAsImageList):
    for pdfPage in pdfPagesAsImageList:
        for figure in pdfPage["figures"]:
            for text in figure["textData"]:
                if not spellChecker.check(text["text"]):
                    figure["imageAnalysis"]["spellingErrors"].append(text["text"])
    return pdfPagesAsImageList




