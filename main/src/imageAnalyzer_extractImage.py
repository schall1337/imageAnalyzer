import fitz # PyMuPDF

def extractImages(imageDetailList, pdfFile):
    pdf_file = fitz.open(pdfFile)

    for image_index, image in enumerate(imageDetailList, start=0):
        base_image = pdf_file.extract_image(int(image["object"]))
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        image["imageExt"] = image_ext
        imageName = f"MuPDF_image{image_index}.{image_ext}"
        image["fileName"] = imageName
        out = open("../../tmp/" + imageName, "wb")
        out.write(image_bytes)
        out.close()
    
    pdf_file.close()

    return imageDetailList

    