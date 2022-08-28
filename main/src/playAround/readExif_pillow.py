import os
from PIL import Image, ExifTags

pil_img = Image.open("C:\\Users\\Schall\\Documents\\Bachelorarbeit\\python_modell_ba\\image1_1.jpeg")
exif = {ExifTags.TAGS[k]: v for k, v in pil_img.getexif().items() if k in ExifTags.TAGS}
print(exif)