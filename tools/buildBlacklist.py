import hashlib
from os.path import dirname
from sys import argv
from glob import glob

HASH_FILENAME = dirname(__file__) + '/../data/blacklist.txt'

if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception('You need to pass an image directory')
    IMG_DIR = argv[1]

    hashes_f = open(HASH_FILENAME, 'a')
    files = glob(IMG_DIR + '/*')
    for filename in files:
        with open(filename, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            hashes_f.write(f'{md5}\n')
    hashes_f.close()
