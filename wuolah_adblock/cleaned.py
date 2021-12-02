import fitz

def createCleaned(whitelist_images: list)-> fitz.Document:
    """
    Create a new pdf from images
    """
    doc = fitz.open()
    i = 0
    for whitelist_image in whitelist_images:
        img = fitz.open(stream=whitelist_image['image'], filetype=whitelist_image['ext'])
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = fitz.open("pdf", pdfbytes)
        page = doc.new_page(width = rect.width, height = rect.height)
        page.show_pdf_page(rect, imgPDF, 0)
        imgPDF.close()
    
    return doc