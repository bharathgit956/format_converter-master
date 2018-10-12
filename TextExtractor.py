import xml.etree.ElementTree as ET
import os


class text_extractor:
    def __init__(self, file_path, extraction_path):
        self.file_path = file_path
        self.extraction_path = extraction_path

    def titleAndAuthorExtraction(self, childs, fh):
        for child in childs:
            if child.tag == '{http://www.tei-c.org/ns/1.0}titleStmt':
                try:
                    #print(child[0].text)
                    fh.write(child[0].text +'\n')
                except:
                    pass
            elif child.tag == '{http://www.tei-c.org/ns/1.0}sourceDesc':
                for ch in child[0][0]:
                    self.authorExtraction(ch,fh)
                pass

    def authorExtraction(self, childs,fh):
        for author in childs:
            if author.tag == '{http://www.tei-c.org/ns/1.0}email':
                #print(author.text)
                fh.write(author.text+'\n')
            else:
                s = ""
                for name in author:
                    s = s + name.text + " "
                #print(s)
                fh.write(s+'\n')



    def abstractExtraction(self, childs, fh):
        for child in childs:
            if child.tag == '{http://www.tei-c.org/ns/1.0}abstract':
                try:
                    #print(child[0].text)
                    fh.write(child[0].text)
                except:
                    pass
        fh.write('\n')


    def parseHeaderInformation(self,tag,fh):
        for childs in tag:
            if childs.tag == '{http://www.tei-c.org/ns/1.0}fileDesc':
                self.titleAndAuthorExtraction(childs,fh)

            elif childs.tag == '{http://www.tei-c.org/ns/1.0}profileDesc':
                self.abstractExtraction(childs,fh)


    def extractBibilography(self, c, count, fh):
        s = ""
        for childs in c:
            if childs.tag == '{http://www.tei-c.org/ns/1.0}analytic':
                for child in childs:
                    if child.tag == '{http://www.tei-c.org/ns/1.0}title':
                        try:
                            s = s + child.text + " ,"
                        except:
                            pass
                    if child.tag == '{http://www.tei-c.org/ns/1.0}author':
                        for ch in child:
                            for c in ch:
                                s = s + c.text + " "
                            s = s + ","
            if childs.tag == '{http://www.tei-c.org/ns/1.0}monogr':
                for ch in childs:
                    if ch.tag == '{http://www.tei-c.org/ns/1.0}title' or ch.tag == '{http://www.tei-c.org/ns/1.0}editor':
                        try:
                            s = s + ch.text + " ,"
                        except:
                            pass
                    if ch.tag == '{http://www.tei-c.org/ns/1.0}meeting':
                        pass
                    if ch.tag == '{http://www.tei-c.org/ns/1.0}imprint':
                        for c in ch:
                            if c.tag == '{http://www.tei-c.org/ns/1.0}publisher':
                                s = s + c.text + " ,"
                            if 'when' in c.attrib.keys():
                                s = s + c.attrib['when']+" "
            if childs.tag == '{http://www.tei-c.org/ns/1.0}note':
                    s = s + childs.text

        #print(str(count) + "." + s)
        fh.write(str(count) + "." + s)


    def extractAcknowledgement(self, child):
        pass


    def extractAnnex(self, child):
        pass


    def extractReferences(self, child, fh):
        for ch in child:
            #print("REFERENCES")
            fh.write("REFERENCES")
            count = 0
            for c in ch:
                count = count + 1
                fh.write('\n')
                self.extractBibilography(c, count, fh)
        pass


    def parseTextInformation(self,tag,fh):
        for childs in tag:
            if childs.tag == '{http://www.tei-c.org/ns/1.0}body':
                for child in childs:
                    for ch in child:
                        try:
                            #print(ch.text)
                            fh.write(ch.text+'\n')
                        except:
                            pass
            elif childs.tag == '{http://www.tei-c.org/ns/1.0}back':
                for child in childs:
                    if child.attrib['type'] == 'acknowledgement':
                        self.extractAcknowledgement(child)
                    elif child.attrib['type'] == 'annex':
                        self.extractAnnex(child)
                    elif child.attrib['type'] == 'references':
                        self.extractReferences(child,fh)


    def main(self):
        tree = ET.parse(self.extraction_path)
        root = tree.getroot()
        fh = open(self.file_path,'w')
        for childs in root:
            if childs.tag == '{http://www.tei-c.org/ns/1.0}teiHeader':
                self.parseHeaderInformation(childs,fh)
            elif childs.tag == '{http://www.tei-c.org/ns/1.0}text':
                self.parseTextInformation(childs,fh)
        fh.close()
        self.getBodyandCite(self.file_path)


    def getBodyandCite(self, path):

        oldFileName, extension = os.path.splitext(path)
        keyword = 'REFERENCES'
        with open(path, 'r') as fh:
            text_split = fh.read().split(keyword)

        with open(oldFileName + '.body', 'w') as fh:
            fh.write(text_split[0]+keyword)

        with open(oldFileName + '.cite', 'w') as fh:
            fh.write(keyword.join(text_split[1:]))

