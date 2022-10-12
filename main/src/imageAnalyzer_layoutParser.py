import layoutparser as lp
from PIL import Image
import numpy as np


def getImagesFromLayoutParser(pdfPagesAsImageList):
    # precise modell
    """ model = lp.Detectron2LayoutModel('lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config', 
                                     extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                     label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}) """

    # efficient modell
    model = lp.EfficientDetLayoutModel(
        'lp://efficientdet/PubLayNet/tf_efficientdet_d0/config')

    path = "../../tmp/"
    for index_page, pdfImagePage in enumerate(pdfPagesAsImageList, start=1):
        pageWidth = pdfImagePage["pixMap"]["width"]
        pageHeight = pdfImagePage["pixMap"]["height"]
        percentageOfWidth = pageWidth * 0.15
        percentageOfHeight = pageHeight * 0.1

        borderBox = lp.elements.Rectangle(
            0 + percentageOfWidth, 0 + percentageOfHeight, pageWidth - percentageOfWidth, pageHeight - percentageOfHeight)

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
