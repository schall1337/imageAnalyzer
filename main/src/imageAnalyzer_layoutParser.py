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
    for index_page, pdfImagePage in enumerate(pdfPagesAsImageList):

        imagePil = Image.open(path + pdfImagePage["fileName"]).convert('RGB')
        image = np.array(imagePil)


        layout = model.detect(image)

        #lp.draw_box(image, layout, box_width=3)

        figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])


        for index_block, block in enumerate(figure_blocks):
            segment_image = (block
                       .pad(left=15, right=15, top=15, bottom=5)
                       .crop_image(image))
            path = "../../tmp/"
            fileName = "page_"+ str(index_page) +"_block_" + str(index_block) + ".png"
            block = {"fileName": fileName,
                     "coordinates": block.points.tolist()
                     }
            pdfImagePage["figures"].append(block)

            im = Image.fromarray(segment_image)
            im.save(path + fileName)
            
    return pdfPagesAsImageList
