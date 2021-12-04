#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from wuolah_adblock.extract import extractImages
from wuolah_adblock.cleaned import createCleaned
from wuolah_adblock.blacklist import getBlacklist

error = {
    'status': False,
    'message': None
}

cli = argparse.ArgumentParser()
cli.add_argument('-i', '--input', help='PDF path', required=True)
cli.add_argument('-o', '--output', default='Cleaned', help='Output pdf name')
cli.add_argument('--pdf', default=False, action="store_true", help="Store it as images instead of a pdf")
args = cli.parse_args()

f = open(args.input, 'rb')
pdf_bytes = f.read()
f.close()
blacklist = getBlacklist()
images = extractImages(pdf_bytes, blacklist)
if len(images) > 0:
    if args.pdf:
        # Create pdf
        doc = createCleaned(images)
        doc.save(f'./out/{args.output}.pdf')
        doc.close()
    else:
        # Create folder with all the images
        folder_out = f'./out/{args.output}'
        Path(folder_out).mkdir(parents=True, exist_ok=True)
        i = 0
        for img in images:
            with open(f'{folder_out}/{i}.{img["ext"]}', 'wb') as f:
                f.write(img['image'])
                i += 1
else:
    error['status'] = True
    error['message'] = 'The cleaned PDF document could not be created. Maybe you used a document that did not contain images?'

# Throw error if any
if error['status']:
    print(f'There was an error: {error["message"]}')
    sys.exit(1)

print("DONE")
