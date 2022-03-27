from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, raw
from sanic.exceptions import InvalidUsage

from wuolah_adblock.Blacklist import Blacklist
from wuolah_adblock.Extract import Extract
from wuolah_adblock.Build import Build

app = Sanic('Wuolah-Adblock')
app.ctx.blacklist = Blacklist.fromFile()
app.static('/', './templates/home.html',  name='home')

@app.post("/clear", error_format="html")
async def clear(request: Request)-> HTTPResponse:
    pdf = request.files.get('pdf')
    if pdf and pdf.type == 'application/pdf':
        filename_clean = pdf.name.replace('wuolah-free-', '')
        images = Extract.images(pdf.body, app.ctx.blacklist)
        if len(images) > 0:
            doc = Build.pdf(images)
            out = doc.write()
            doc.close()
            return raw(out, content_type='application/pdf', headers={
                'Content-Disposition': f'attachment; filename="{filename_clean}"'
            })
        raise InvalidUsage('No se ha podido extraer ninguna imagen. ¿El documento realmente contiene imágenes incrustadas?')
    raise InvalidUsage("Ha habido un error al procesar la solicitud. ¿Has elegido un archivo pdf válido?")

# Debug mode
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
