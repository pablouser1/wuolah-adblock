# Wuolah Adblock
Este programa elimina todos los anuncios de los pdfs de Wuolah, por ahora solo funciona con pdfs conteniendo imágenes

## Instalación
```bash
python -m pip install -r requirements.txt
```

## Cómo usar (CLI)
### Output en carpeta con fotos
```bash
python cli.py -i NAME.pdf -o OUTPUT_DIR
```
#### Output en pdf
```bash
python cli.py -i NAME.pdf -o PDF_NAME --pdf
```

## Cómo usar (Web)
Debug:
```bash
python server.py
```
Podrás acceder al servidor en http://localhost:8080

Release:
```bash
gunicorn -k uvicorn.workers.UvicornWorker server:app
```
Podrás acceder al servidor también en http://localhost:8080

También puedes acceder a la versión ya preparada en Heroku [aquí](https://wuolah-adblock.herokuapp.com)
