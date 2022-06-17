import fitz


class Build:
    @staticmethod
    def pdf(whitelist_images: list) -> fitz.Document:
        """
        Create a new pdf from images
        """
        doc = fitz.open()
        doc.set_metadata({
            'creator': 'Wuolah (https://wuolah.com)',
            'producer': 'wuolah-adblock (https://github.com/pablouser1/wuolah-adblock)'
        })
        for whitelist_image in whitelist_images:
            img = fitz.open(stream=whitelist_image['image'], filetype=whitelist_image['ext'])
            rect = img[0].rect
            pdfbytes = img.convert_to_pdf()
            img.close()
            imgPDF = fitz.open("pdf", pdfbytes)
            page = doc.new_page(width=rect.width, height=rect.height)
            page.show_pdf_page(rect, imgPDF, 0)
            imgPDF.close()

        return doc
