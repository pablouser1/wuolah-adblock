from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, raw
from sanic.exceptions import InvalidUsage

from wuolah_adblock.extract import extractImages
from wuolah_adblock.cleaned import createCleaned
from wuolah_adblock.blacklist import getBlacklist

blacklist = getBlacklist()

app = Sanic("Wuolah-Adblock")
app.static('/', './templates/home.html',  name='home')
app.static('/about', './templates/about.html', name='about')

@app.post("/clear", error_format="html")
async def clear(request: Request)-> HTTPResponse:
    if request.files.get('pdf') and request.files.get('pdf').type == 'application/pdf':
        pdf = request.files.get('pdf')
        images = extractImages(pdf.body, blacklist)
        if len(images) > 0:
            doc = createCleaned(images)
            out = doc.write()
            doc.close()
            return raw(out, content_type='application/pdf', headers={
                'Content-Disposition': 'attachment; filename="Wuolah-Limpio.pdf"'
            })
        raise InvalidUsage('No se ha podido extraer ninguna imagen. ¿El documento realmente contiene imágenes incrustadas?')
    raise InvalidUsage("Ha habido un error al procesar la solicitud. ¿Has elegido un archivo pdf válido?")

# Debug mode
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
