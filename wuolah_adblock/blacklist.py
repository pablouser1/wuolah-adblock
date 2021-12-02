from os import listdir
from os.path import isfile, join

def getBlacklist()-> list:
    # Blacklist images
    blacklist = []
    blacklist_files = [f for f in listdir('./blacklist') if isfile(join('./blacklist', f))]
    # Read all images and append to list
    for blacklist_file in blacklist_files:
        with open(f'./blacklist/{blacklist_file}', 'rb') as f:
            blacklist.append(f.read())
    
    return blacklist
