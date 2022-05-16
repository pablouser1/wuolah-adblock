#!/usr/bin/env python3
import argparse
from pathlib import Path
from wuolah_adblock.Blacklist import Blacklist
from wuolah_adblock.Extract import Extract
from wuolah_adblock.Build import Build

error = {
    'status': False,
    'message': None
}

cli = argparse.ArgumentParser()
cli.add_argument('input', help='PDF path')
cli.add_argument('--pdf', default=False, action="store_true", help="Store it as images instead of a pdf")

if __name__ == '__main__':
    args = cli.parse_args()
    blacklist = Blacklist.fromFile()
    path = Path(args.input)
    pdf_bytes = path.read_bytes()
    filename_clean = path.name.replace('wuolah-free-', '')
    images = Extract.images(pdf_bytes, blacklist)
    if len(images) > 0:
        if args.pdf:
            # Create pdf
            doc = Build.pdf(images)
            doc.save(f'./out/{filename_clean}.pdf')
            doc.close()
        else:
            # Create folder with all the images
            folder_out = f'./out/{filename_clean}'
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
        exit(1)

    print("DONE")
