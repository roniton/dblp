import os
import xml.parsers.expat
from html.parser import HTMLParser

unescape = HTMLParser().unescape

class DBLPXMLParser:
    def __init__(self, *args, **kargs):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.handleStartElement
        self.parser.EndElementHandler = self.handleEndElement
        self.parser.CharacterDataHandler = self.handleCharData
        self.line_count = None
        self.xmlFile = None
        self.csvFile = None
        self.temp_article = None
        self.tag = None

    def setXMLFile(self, file):
        self.xmlFile = file

    def setCSVFile(self, file):
        self.csvFile = file

    def init(self):
        print("Initiating...")
        self.line_count = self.__count_lines()

    def __count_lines(self):
        if self.xmlFile != None:
            for i, l in enumerate(self.xmlFile):
                pass
            self.xmlFile.seek(0)
            return i + 1

    def get_progress(self):
        current_line = self.parser.CurrentLineNumber
        return float(current_line)/float(self.line_count)

    def parse_file(self):
        self.init()
        self.parser.ParseFile(self.xmlFile)

    def handleCharData(self, data):
        if not self.temp_article:
            return

        if not data:
            return

        if self.tag == "title":
            self.temp_article.title += data
        elif self.tag == "year":
            self.temp_article.year += data
        elif self.tag == "journal":
            self.temp_article.journal += data
        elif self.tag in ("sup", "sub", "i", "tt"):
            self.temp_article.title += data

    def handleStartElement(self, name, attrs):
        if not name:
            return

        name = name.lower()

        if name == "article":
            self.temp_article = Article(attrs['key'])
        
        self.tag = name

    def handleEndElement(self, name):
        if not name or not self.temp_article:
            return

        name = name.lower()

        if name == "title" and self.temp_article:
            self.temp_article.title = unescape(self.temp_article.title)
        elif name == "year" and self.temp_article:
            self.temp_article.year = self.temp_article.year
        elif name == "journal" and self.temp_article:
            self.temp_article.journal = unescape(self.temp_article.journal)
        elif name == "article" and self.temp_article:            
            self.processElement(self.temp_article.key+';'+self.temp_article.title.replace('\n', '').replace('\r', '')+';'+self.temp_article.journal.replace('\n', '').replace('\r', '')+';'+self.temp_article.year.replace('\n', '').replace('\r', '')) 
            print('Progress:', round(self.get_progress() * 100.0, 2), '% - type: ', name, ' Line: ', self.parser.CurrentLineNumber)
        elif name in ("www", "phdthesis", "inproceedings", "incollection", "proceedings", "book", "mastersthesis"):
            print('Progress:', round(self.get_progress() * 100.0, 2), '% - type: ', name, ' Line: ', self.parser.CurrentLineNumber)

    def processElement(self, data):
        fout = open(self.csvFile, 'a')
        print(data, end="\n", file=fout)
        fout.close()

class Article:
    def __init__(self, key):
        self.key = key
        self.title = ''
        self.year = ''
        self.journal = ''

if __name__ == '__main__':
    xmldblp = 'dblp.xml'
    csvdblp = 'parsed_dblp.csv'

    if not os.path.isfile(xmldblp):
        print("Error")
        exit(0)

    if os.path.isfile(csvdblp):
        os.remove(csvdblp)

    with open(xmldblp, "rb") as file:
        parser = DBLPXMLParser()
        parser.setXMLFile(file)
        parser.setCSVFile(csvdblp)
        parser.parse_file()
