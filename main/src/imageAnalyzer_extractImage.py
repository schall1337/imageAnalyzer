import fitz # PyMuPDF
import io
from PIL import Image

def extractImages(imageDetailList, pdfFile):
    pdf_file = fitz.open(pdfFile)

    for image_index, image in enumerate(imageDetailList, start=0):
        base_image = pdf_file.extract_image(int(image["object"]))
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        imagePIL = Image.open(io.BytesIO(image_bytes))
        imageName = f"MuPDF_image{image_index}.{image_ext}"
        image["fileName"] = imageName
        #imagePIL.save("../../tmp/" + open(imageName, "wb"))
        imagePIL.save("../../tmp/" + imageName)

    return imageDetailList

    