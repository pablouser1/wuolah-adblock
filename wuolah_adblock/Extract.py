import fitz
from hashlib import md5


class Extract:
    @staticmethod
    def images(file_bytes, blacklist: list) -> list:
        whitelist_images = []
        # Open pdf
        dirty_doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in dirty_doc:
            images = page.get_images()
            for tmp_img in images:
                img = dirty_doc.extract_image(tmp_img[0])  # Image bytes
                checksum = md5(img['image']).hexdigest()
                if checksum not in blacklist:
                    whitelist_images.append(img)
        dirty_doc.close()
        return whitelist_images


def extractImages(file_bytes, blacklist: list) -> list:
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

            # Skip spam images
            if img["image"] not in blacklist:
                whitelist_images.append(img)
    dirty_doc.close()
    return whitelist_images
