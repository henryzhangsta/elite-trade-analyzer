import csv

class CSVLoader(object):
    def __init__(self, headerfile):
        with open(headerfile) as f:
            self.header = self.parse_header(f.read())

    def parse_header(self, header_data):
        return header_data.split(',')

    def unicode_re_encoder(self, unicode_data):
        for line in unicode_data:
            yield line.encode('utf-8')

    def load(self, sc, filename):
        return sc.textFile(filename)

    def loadMap(self, sc, filename):
        return self.load(sc, filename).mapPartitions(self.mapper)

    def mapper(self, lines):
        reader = csv.DictReader(self.unicode_re_encoder(lines), fieldnames=self.header)
        return list(reader)
