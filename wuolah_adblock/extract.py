import fitz
from wuolah_adblock.blacklist import getBlacklist

def extractImages(file_bytes, blacklist: list)-> list:
    """
    Extracts images not blacklisted from a pdf
    """
    whitelist_images = []
    # Open pdf
    dirty_doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in dirty_doc:
        # Get all images of page and try to save them
        images = page.get_images()
        for image in images:
            img = dirty_doc.extract_image(image[0])
            # Skip spammy images
            if img["image"] not in blacklist:
                whitelist_images.append(img)
    dirty_doc.close()
    return whitelist_images
