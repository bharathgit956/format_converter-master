import xml.etree.ElementTree as ET
import os




class XmlWriter:

    def __init__(self, file_path, final_path,path_parscit,path_met):
        self.final_path = final_path
        self.file_path = file_path
        self.path_parscit = path_parscit
        self.path_met = path_met
        print(file_path)
        tree = ET.parse(self.file_path)
        self.parscit_input = ET.parse(self.path_parscit)
        self.root = tree.getroot()
        self.newRoot = ET.Element("document")
        self.newRoot.set('id', 'unset')
        self.header_root = None
        self.file_info_root = None
        #self.header_root.set('id', 'unset')
        self.parscit_root = self.parscit_input.getroot()[0]
        self.intent = ""
        self.version=""



    def titleAndAuthorExtraction(self, childs):
        file_info = self.newRoot.find("fileInfo")
        conversionTrace = file_info.find('conversionTrace')
        if conversionTrace != "":
            algorithm = ET.SubElement(self.newRoot, "algorithm", name=conversionTrace.text, version=self.version)
        else:
            algorithm = ET.SubElement(self.newRoot, "algorithm", name='"SVM HeaderParse', version='0.2')

        title = ET.SubElement(algorithm, "title")
        authors = ET.SubElement(algorithm, "authors")

        if conversionTrace != "":
            self.header_root = ET.Element("algorithm", name=conversionTrace.text, version=self.version)
        else:
            self.header_root = ET.Element("algorithm", name="SVM HeaderParse", version="0.2")


        title_header = ET.SubElement(self.header_root, "title")
        authors_header = ET.SubElement(self.header_root, "authors")


        for child in childs:
            if child.tag == 'titleStmt':
                try:
                    #print(child[0].text)
                    title.text = child[0].text
                    title_header.text = child[0].text
                except:
                    pass

            elif child.tag == 'sourceDesc':
                try:
                    for ch in child[0][0]:
                        if ch.tag == 'author':
                            self.authorExtraction(ch, authors,authors_header)
                except:
                    pass


    def authorExtraction(self, childs, authors,authors_header):
        authorXml = ET.SubElement(authors, "author")
        authorXml_header = ET.SubElement(authors_header, "author")
        for author in childs:
            if 'persName' in author.tag:
                s = ""
                for ch in author:
                    try:
                        s = s + ch.text + " "
                    except:
                        pass
                name = ET.SubElement(authorXml, "name")
                name_header = ET.SubElement(authorXml_header, "name")
                name.text = s
                name_header.text = s
            elif author.tag == 'email':
                try:
                    email = ET.SubElement(authorXml, "email")
                    email.text = author.text
                    email_header = ET.SubElement(authorXml_header, "email")
                    email_header.text = author.text
                except:
                    pass
            elif author.tag == 'affiliation':
                s1 = ""
                for ch in author:
                    if ch.tag == 'address':
                        s = ""
                        for c in ch:
                            try:
                                s = s + c.text + " "
                            except:
                                pass
                        address = ET.SubElement(authorXml, "address")
                        address.text = s
                        address_header = ET.SubElement(authorXml_header, "address")
                        address_header.text = s
                    else:
                        try:
                            s1 = s1 + ch.text + " "
                        except:
                            pass
                affiliation = ET.SubElement(authorXml, "affiliation")
                affiliation.text = s1
                affiliation_header = ET.SubElement(authorXml_header, "affiliation")
                affiliation_header.text = s1

    def abstractExtraction(self, childs):
        algorithm = self.newRoot.find("algorithm")
        abstract = ET.SubElement(algorithm, "abstract")
        #algorithm_header = self.header_root.find("algorithm")
        abstract_header = ET.SubElement(self.header_root, "abstract")
        for child in childs:
            if child.tag == 'abstract':
                temp_str = ""
                if child.text and child.text != "\n":
                    temp_str = temp_str + child.text
                else:
                    for ch in child:
                        try:
                            for c in ch:
                                temp_str = temp_str+ " " + c.text
                        except:
                            pass
                abstract.text = temp_str
                abstract_header.text = temp_str

    def parseHeaderInformation(self, tag):
        for childs in tag:
            if childs.tag == 'encodingDesc':
                self.conversationTraceExtractor(childs)

            elif childs.tag == 'fileDesc':
                self.titleAndAuthorExtraction(childs)

            elif childs.tag == 'profileDesc':
                self.abstractExtraction(childs)
        algorithm = self.newRoot.find("algorithm")
        date = ET.SubElement(algorithm, "date")
        date_header = ET.SubElement(self.header_root, "date")
        ch = tag.find('fileDesc')
        for child in ch:
            if child.tag == 'publicationStmt':
                for c in child:
                    if c.tag == 'date':
                        try:
                            #print(child[0].text)
                            date.text = c.text
                            date_header.text = c.text
                        except:
                            date.text = " "
                            date_header.text = " "
                            pass
        validHeader = ET.SubElement(algorithm, "validHeader")
        validHeader.text = "1"
        validHeader_header = ET.SubElement(self.header_root, "validHeader")
        validHeader_header.text = "1"

    def extractRawString(self, c):
        s = ""
        for childs in c:
            if childs.tag == 'analytic':
                for child in childs:
                    if child.tag == 'title':
                        try:
                            s = s + child.text + " ,"
                        except:
                            pass
                    if child.tag == 'author':
                        for ch in child:
                            for c in ch:
                                s = s + c.text + " "
                            s = s + ","
            if childs.tag == 'monogr':
                for ch in childs:
                    if ch.tag == 'title' or ch.tag == 'editor':
                        try:
                            s = s + ch.text + " ,"
                        except:
                            pass
                    if ch.tag == 'meeting':
                        pass
                    if ch.tag == 'imprint':
                        for c in ch:
                            if c.tag == 'publisher':
                                s = s + c.text + " ,"
                            if 'when' in c.attrib.keys():
                                s = s + c.attrib['when'] + " "
            if childs.tag == 'note':
                s = s + childs.text
        return s

    def extractBibilography(self, c, count, citationList, citationList_parscit):
        s = ""
        s1 = self.extractRawString(c)
        citation = ET.SubElement(citationList, "citation", valid="true")
        title = ET.SubElement(citation, "title")
        authors = ET.SubElement(citation, "authors")
        #citation_parscit = ET.SubElement(citationList_parscit, "citation", valid="true")
        #title_parscit = ET.SubElement(citation_parscit, "title")
        #authors_parscit = ET.SubElement(citation_parscit, "authors")
        for childs in c:
            if childs.tag == 'analytic':
                for child in childs:
                    if child.tag == 'title':
                        try:
                            title.text = child.text
                            #title_parscit.text = child.text
                        except:
                            pass
                    if child.tag == 'author':
                        for ch in child:
                            name = ""
                            for c in ch:
                                name = name + c.text + " "
                            ET.SubElement(authors, "author").text = name
                            #ET.SubElement(authors_parscit, "author").text = name
            if childs.tag == 'monogr':
                for ch in childs:
                    if ch.tag == 'title':
                        try:
                            if ch.attrib['level'] == "j":
                                ET.SubElement(citation, "journal").text = ch.text
                                #ET.SubElement(citation_parscit, "journal").text = ch.text

                        except:
                            pass
                    if ch.tag == 'editor':
                        try:
                            s = s + ch.text + " ,"
                        except:
                            pass
                    if ch.tag == 'meeting':
                        pass
                    if ch.tag == 'imprint':
                        for c in ch:
                            if c.tag == 'publisher':
                                s = s + c.text + " ,"
                            if 'when' in c.attrib.keys():
                                ET.SubElement(citation, "date").text = c.attrib['when']
                                #ET.SubElement(citation_parscit, "date").text = c.attrib['when']
                            if 'volume' in c.attrib.keys():
                                ET.SubElement(citation, "volume").text = c.attrib['volume']
                                #ET.SubElement(citation_parscit, "volume").text = c.attrib['volume']
            if childs.tag == 'note':
                try:
                    ET.SubElement(citation, "note").text = childs.text
                    #ET.SubElement(citation_parscit, "note").text = childs.text
                except:
                    pass
        ET.SubElement(citation, "marker").text = str(count) + "."
        ET.SubElement(citation, "rawString").text = s1
        #ET.SubElement(citation_parscit, "marker").text = str(count) + "."
        #ET.SubElement(citation_parscit, "rawString").text = s1

    def extractAcknowledgement(self, child):
        pass

    def extractAnnex(self, child):
        pass

    def extractReferences(self, child):
        for child in self.parscit_input.getroot():
            ET.Element.append(self.newRoot, child)
        '''
        if self.ident != "" and self.version != "":
            algorithm = ET.SubElement(self.newRoot, "algorithm", name=self.ident, version=self.version)
        else:
            algorithm = ET.SubElement(self.newRoot, "algorithm", name="ParsCit", version="1.0")

        citationList = ET.SubElement(algorithm, "citationList")
        if self.ident != "" and self.version != "":
            algorithm_parscit = ET.SubElement(self.parscit_root, "algorithm", name=self.ident, version=self.version)
        else:
            algorithm_parscit = ET.SubElement(self.parscit_root, "algorithm", name="ParsCit", version="1.0")
        citationList_parscit = ET.SubElement(algorithm_parscit, "citationList")
        for ch in child:
            #print("REFERENCES")
            count = 0
            for c in ch:
                count = count + 1
                self.extractBibilography(c, count, citationList, citationList_parscit)
        pass
        '''

    def parseTextInformation(self, tag):
        for childs in tag:
            if childs.tag == 'back':
                for child in childs:
                    if child.attrib['type'] == 'acknowledgement':
                        self.extractAcknowledgement(child)
                    elif child.attrib['type'] == 'annex':
                        self.extractAnnex(child)
                    elif child.attrib['type'] == 'references':
                        self.extractReferences(child)

    def createFileInfo(self):
        file_info = ET.SubElement(self.newRoot, "fileInfo")
        filename, extension = os.path.splitext(self.file_path)
        filename, extension = os.path.splitext(filename)
        filename, extension = os.path.split(filename)

        final_path = self.final_path + '/' + extension

        file_1 = final_path + '/' + extension + '.pdf'
        file_2 = final_path + '/' + extension + '.body'
        file_3 = final_path + '/' + extension + '.cite'

        ET.SubElement(file_info, "repository").text = "rep1"
        ET.SubElement(file_info, "filePath").text = file_1
        ET.SubElement(file_info, "bodyFile").text = file_2
        ET.SubElement(file_info, "citeFile").text = file_3
        ET.SubElement(file_info, "conversionTrace").text = ""
        self.file_info_root = ET.Element("conversionTrace")
        self.file_info_root.text = ""

        check_sums = ET.SubElement(file_info, "checkSums")
        check_sums_file = self.file_info_root.Element("checkSums")
        check_sum = ET.SubElement(check_sums, "checkSum")
        check_sum_file = ET.SubElement(check_sums_file, "checkSum")

        ET.SubElement(check_sum, "fileType").text = "pdf"
        ET.SubElement(check_sum_file, "fileType").text = "pdf"
        try:
            met_input = ET.parse(self.path_met)
            root_met = met_input.getroot()
            for child in root_met:
                if child.tag == "SHA1":
                    ET.SubElement(check_sum, "sha1").text = child.text
                    ET.SubElement(check_sum_file, "sha1").text = child.text
        except:
            ET.SubElement(check_sum, "sha1").text = ""




    def main(self):
        self.createFileInfo()
        for childs in self.root:
            if childs.tag == 'teiHeader':

                self.parseHeaderInformation(childs)
            elif childs.tag == 'text':
                self.parseTextInformation(childs)

    def get_xml_root(self):
        return self.indent(self.newRoot)

    def get_file_info_root(self):
        return self.indent(self.file_info_root)

    def get_header_root(self):
        return self.indent(self.header_root)

    def get_parscit_root(self):
        return self.indent(self.parscit_root)


    def indent(self, elem, level=0):
        i = "\n"
        j = "\n"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem

    def conversationTraceExtractor(self, childs):
        for child in childs:
            for ch in child:
                if ch.tag == 'application':
                    try:
                        file_info = self.newRoot.find("fileInfo")
                        conversionTrace = file_info.find('conversionTrace')
                        conversionTrace_file = self.file_info_root.find('conversionTrace')
                        conversionTrace.text = ""+ch.attrib['ident'] + " "+ch.attrib['version']
                        conversionTrace_file.text = conversionTrace.text
                        self.ident = ch.attrib['ident']
                        self.version = ch.attrib['version']
                    except:
                        pass

