#!/usr/bin/env python3
import argparse
from pathlib import Path
from wuolah_adblock.extract import extractImages
from wuolah_adblock.cleaned import createCleaned

cli = argparse.ArgumentParser()
cli.add_argument('-i', '--input', help='PDF path', required=True)
cli.add_argument('-o', '--output', default='Cleaned', help='Output pdf name')
cli.add_argument('--pdf', default=False, action="store_true", help="Store it as images instead of a pdf")
args = cli.parse_args()

f = open(args.input, 'rb')
pdf_bytes = f.read()
f.close()

images = extractImages(pdf_bytes)

if args.pdf:
    folder_out = f'./out/{args.output}'
    Path(folder_out).mkdir(parents=True, exist_ok=True)
    i = 0
    for img in images:
        with open(f'{folder_out}/{i}.{img["ext"]}', 'wb') as f:
            f.write(img['image'])
            i += 1
else:
    doc = createCleaned(images)
    doc.save(f'./out/{args.output}.pdf')
    doc.close()

print("DONE")
