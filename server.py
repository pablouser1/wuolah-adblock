from bottle import Bottle, request, response, HTTPError, static_file
from os.path import splitext
from io import BytesIO

from wuolah_adblock.Blacklist import Blacklist
from wuolah_adblock.Extract import Extract
from wuolah_adblock.Build import Build

app = Bottle()

blacklist = Blacklist.fromFile()

@app.get('/')
def home():
    return static_file('home.html', './views')

@app.post('/clear')
def clear():
    pdf = request.files.get('pdf')
    if pdf and pdf.content_type == 'application/pdf':
        filename_clean = pdf.filename.replace('wuolah-free-', '')
        # Saving file to BytesIO
        file_bytes = BytesIO()
        pdf.save(file_bytes)
        # Extract images from document (and ignore images from blacklist)
        images = Extract.images(file_bytes, blacklist)
        if len(images) > 0:
            # Make pdf with cleaned images
            doc = Build.pdf(images)
            out = doc.write()
            response.set_header('Content-Type', 'application/pdf')
            response.set_header('Content-Disposition', f'attachment; filename="{filename_clean}"')
            # Close everything
            doc.close()
            file_bytes.close()
            return out
        return HTTPError(400, 'No se ha podido extraer ninguna imagen. ¿El documento realmente contiene imágenes incrustadas?')
    return HTTPError(400, "Ha habido un error al procesar la solicitud. ¿Has elegido un archivo pdf válido?")

# Debug mode
if __name__ == "__main__":
    app.run(debug=True, reloader=True)
