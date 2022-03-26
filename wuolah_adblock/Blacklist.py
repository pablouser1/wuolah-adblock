class Blacklist:
    BLACKLIST_FILE = './data/blacklist.txt'
    @staticmethod
    def fromFile()-> list:
        hashes = []
        with open(Blacklist.BLACKLIST_FILE) as f:
            data = f.read()
            hashes = data.splitlines()

        return hashes
