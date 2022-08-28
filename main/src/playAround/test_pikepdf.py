from pikepdf import Pdf, PdfImage

filename = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\python_modell_ba\\main\\src\\pdf_metadata.pdf"
example = Pdf.open(filename)

for i, page in enumerate(example.pages):
    for j, (name, raw_image) in enumerate(page.images.items()):
        image = PdfImage(raw_image)
        out = image.extract_to(fileprefix=f"{filename}-page{i:03}-img{j:03}")
        # Optional: print info about image
        w = raw_image.stream_dict.Width
        h = raw_image.stream_dict.Height
        f = raw_image.stream_dict.Filter
        size = raw_image.stream_dict.Length

print(f"Wrote {name} {w}x{h} {f} {size:,}B {image.colorspace} to {out}")