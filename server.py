from sanic import Sanic
from sanic.response import HTTPResponse, html, redirect, raw
from sanic.request import Request

from wuolah_adblock.extract import extractImages
from wuolah_adblock.cleaned import createCleaned

app = Sanic("Wuolah-Adblock")

def readHTML(html_path: str):
    f = open(html_path)
    file_html = f.read()
    f.close()
    return file_html

@app.get("/")
async def home(request: Request)-> HTTPResponse:
    return html(readHTML('./templates/home.html'))

@app.post("clear")
async def clear(request: Request)-> HTTPResponse:
    if request.files.get('pdf') and request.files.get('pdf').type == 'application/pdf':
        pdf = request.files.get('pdf')
        images = extractImages(pdf.body)
        doc = createCleaned(images)
        return raw(doc.write(), content_type='application/pdf', headers={
            'Content-Disposition': 'attachment; filename="Wuolah-Limpio.pdf"'
        })
    return redirect('/error')

@app.get("/error")
async def error(request: Request) -> HTTPResponse:
    return html(readHTML('./templates/error.html'))

@app.get("/about")
async def about(request: Request) -> HTTPResponse:
    return html(readHTML('./templates/about.html'))

# Debug mode
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
