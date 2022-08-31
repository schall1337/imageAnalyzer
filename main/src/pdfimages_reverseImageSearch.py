imagePath = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\imageAnalyzer\\main\\tmp\\"

def reverseImageSearcher(imageDetailList):
    for imageDetail in imageDetailList:
        reverseImageDetails = detect_web(imagePath + imageDetail["fileName"])
        imageDetail["reverseImageDetection"] = reverseImageDetails
    return imageDetailList

def detect_web(path):
    """Detects web annotations given an image."""
    from google.cloud import vision
    import io
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Schall\\Documents\\Bachelorarbeit\\key_api_google\\api_google_key.json"
    client = vision.ImageAnnotatorClient()

    reverseImageDetails = {
        "countPagesWithMatchingImages" : "",
        "pagesWithMatchingImages": []   
    }

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.pages_with_matching_images:

        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))
        reverseImageDetails["countPagesWithMatchingImages"] = len(annotations.pages_with_matching_images)

        for page in annotations.pages_with_matching_images:
            detailEntity = {
                "pageUrl": "",
                "fullMatchingImages": [],
                "partiallyMatchingImages": []
            }
            print('\n\tPage url   : {}'.format(page.url))
            detailEntity["pageUrl"] = page.url
            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
                    detailEntity["fullMatchingImages"].append(image.url)

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))

                for image in page.partial_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
                    detailEntity["partiallyMatchingImages"].append(image.url)
            reverseImageDetails["pagesWithMatchingImages"].append(detailEntity)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return reverseImageDetails
