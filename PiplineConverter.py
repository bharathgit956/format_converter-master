import os
import xml.etree.ElementTree as ET

from XmlWriter import XmlWriter
from TextExtractor import text_extractor


class PipelineConverter:
    path = ''

    def __init__(self, path):
        self.path = path

    path2 = "/Users/bharath971/Documents/Acads/citeseerx docs/pdfmef-extraction-sample-output/" \
            "tei_processFulltextDocument/10.1.1.324.1892.tei.xml"
    path3 = "/Users/bharath971/Documents/Acads/citeseerx docs/perl-extraction-sample-output"

    filename, extension = os.path.splitext(path2)
    filename, extension = os.path.splitext(filename)
    filename, extension = os.path.split(filename)

    final_path = path3 + '/' + extension
    if not os.path.exists(final_path):
        os.mkdir(final_path)

    file_1 = final_path + '/' + extension + '.header'
    file_2 = final_path+'/'+extension+'.parscit'
    file_3 = final_path+'/'+extension+'.xml'
    file_4 = final_path+'/'+extension+'.txt'
    fh = open(file_1,'w')
    fh1 = open(file_2,'w')
    fh2 = open(file_3,'w')

    xmlWriter = XmlWriter(path2)
    xmlWriter.main()

    ET.ElementTree(xmlWriter.get_xml_root()).write(file_3)
    ET.ElementTree(xmlWriter.get_header_root()).write(file_1)
    ET.ElementTree(xmlWriter.get_parscit_root()).write(file_2)

    fh.close()
    fh1.close()
    fh2.close()

    text_extractor = text_extractor(file_4,path2)
    text_extractor.main()
