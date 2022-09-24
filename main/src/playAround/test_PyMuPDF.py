import fitz # PyMuPDF
import io
from PIL import Image

# open the file
pdf_file = fitz.open("C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\resources\\testdokumentBachelor.pdf")

# iterate over PDF pages
for page_index in range(len(pdf_file)):
    # get the page itself
    page = pdf_file[page_index]
    image_list = page.get_images()
    image_info = page.get_image_info(hashes=True, xrefs=True)
    print(image_info)
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page.get_images(), start=1):
        # get the XREF of the image
        xref = img[0]
        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]
        # load it to PIL
        image = Image.open(io.BytesIO(image_bytes))
        # save it to local disk
        image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))