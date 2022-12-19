import layoutparser as lp
from PIL import Image
import numpy as np
import configparser


def getImagesFromLayoutParser(pdfPagesAsImageList):

    config = configparser.ConfigParser()
    config.read('config-file.ini')

    # efficient modell
    model = lp.EfficientDetLayoutModel(
        'lp://efficientdet/PubLayNet/tf_efficientdet_d0/config')

    path = "../../tmp/"
    for index_page, pdfImagePage in enumerate(pdfPagesAsImageList, start=1):
        pageWidth = pdfImagePage["pixMap"]["width"]
        pageHeight = pdfImagePage["pixMap"]["height"]
        #percentageOfWidth = pageWidth * 0.15
        #percentageOfHeight = pageHeight * 0.1

        # 1cm = 56px at 144 dpi
        cm_to_pixel = 56

        x_top_left = float(config['default']['border_left']) * cm_to_pixel
        y_top_left = float(config['default']['border_top']) * cm_to_pixel

        x_bottom_right = pageWidth - \
            (float(config['default']['border_right']) * cm_to_pixel)
        y_bottom_right = pageHeight - \
            (float(config['default']['border_bottom']) * cm_to_pixel)

        borderBox = lp.elements.Rectangle(
            x_top_left, y_top_left, x_bottom_right, y_bottom_right)

        pdfPageAsImg = Image.open(
            path + pdfImagePage["fileName"]).convert('RGB')
        image = np.array(pdfPageAsImg)
        pdfPageAsImg.close()

        layout = model.detect(image)

        imageLayout = lp.draw_box(image, layout, box_width=3)

        imageLayout.save(path + "detectedLayoutPage_" +
                         str(index_page) + ".png")

        figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])

        for index_block, block in enumerate(figure_blocks, start=1):
            paddedBlock = block.pad(left=20, right=20, top=20, bottom=10)
            segment_image = (paddedBlock.crop_image(image))

            fileName = "page_" + str(index_page) + \
                "_block_" + str(index_block) + ".png"

            blockData = {"fileName": fileName,
                         "coordinates": paddedBlock.points.tolist(),
                         "textData": [],
                         "imageAnalysis": {
                             "spellingErrors": [],
                             "minWordHeight": None,
                             "isTooCloseToBorder": False,
                             "color": {
                                 "background": [],
                                 "indistinctColors": []
                             },
                             "color_primitive": {
                                "background": "",
                                "indistinctColors": []
                             }
                         }
                         }
            if not block.is_in(borderBox):
                blockData["imageAnalysis"]["isTooCloseToBorder"] = True

            pdfImagePage["figures"].append(blockData)

            im = Image.fromarray(segment_image)
            im.save(path + fileName)
            im.close()

    return pdfPagesAsImageList
