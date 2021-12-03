from typing import Union
from sanic import Sanic
from sanic.response import HTTPResponse, redirect, raw
from sanic.request import Request

from wuolah_adblock.extract import extractImages
from wuolah_adblock.cleaned import createCleaned

app = Sanic("Wuolah-Adblock")

app.static('/', './templates/home.html',  name='home')
app.static('/about', './templates/about.html', name='about')
app.static('/error', './templates/error.html', name='error')

@app.post("clear")
async def clear(request: Request)-> HTTPResponse:
    if request.files.get('pdf') and request.files.get('pdf').type == 'application/pdf':
        pdf = request.files.get('pdf')
        images = extractImages(pdf.body)
        doc = createCleaned(images)
        return raw(doc.write(), content_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="Wuolah-Limpio.pdf"'
        })
    return redirect('/error', status=500)

# Debug mode
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
