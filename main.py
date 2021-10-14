#!/usr/bin/env python3
import argparse
from os import listdir
from os.path import isfile, join
from pathlib import Path
import fitz

cli = argparse.ArgumentParser()
cli.add_argument('-i', '--input', help='PDF path', required=True)
cli.add_argument('-o', '--output', default='./out/Cleaned', help='Output folder')
args = cli.parse_args()
Path(args.output).mkdir(parents=True, exist_ok=True)

# Open pdf
dirty_doc = fitz.open(args.input)
# Blacklist images
blacklist = []
blacklist_files = [f for f in listdir('./blacklist') if isfile(join('./blacklist', f))]
# Read all images and append to list
for blacklist_file in blacklist_files:
    with open(f'./blacklist/{blacklist_file}', 'rb') as f:
        blacklist.append(f.read())

i = 0
for page in dirty_doc:
    # Get all images of page and try to save them
    images = page.get_images()
    for image in images:
        img = dirty_doc.extract_image(image[0])
        # Skip spammy images
        if img["image"] not in blacklist:
            with open(f'{args.output}/{i}.{img["ext"]}', 'wb') as f:
                f.write(img['image'])
                i += 1

dirty_doc.close()
