import os
import xml.etree.ElementTree as ET

from XmlWriter import XmlWriter
from TextExtractor import text_extractor
from os import listdir

base_path = "/root/sharedfolder/citeseer_results/2019090800"
path_output = "/root/sharedfolder/citeseer_results/format_converter_results"
filenames = listdir(base_path)


for pdfmef_path in filenames:
    path_academic_filter = base_path+"/"+pdfmef_path+"/"+pdfmef_path+".academic_filter"
    success = False
    try:
        acad = open(path_academic_filter)
        success = True
    except:
        pass

    path_full_text = base_path+"/"+pdfmef_path+"/"+pdfmef_path+".tei"
    path_parscit =  base_path+"/"+pdfmef_path+"/"+pdfmef_path+".cite"
    path_met = base_path + "/" + pdfmef_path + "/" + pdfmef_path + ".met"
    path_txt =  base_path + "/" + pdfmef_path + "/" + pdfmef_path + ".txt"

    acad_paper = False
    try:
        parscit_input = ET.parse(path_parscit)
        root = parscit_input.getroot()
        if root.tag != "error":
            acad_paper = True
    except:
        pass

    if not success and acad_paper:
        filename, extension = os.path.splitext(path_full_text)
        #filename, extension = os.path.splitext(filename)
        filename, extension = os.path.split(filename)

        final_path = path_output + '/' + extension
        if not os.path.exists(final_path):
            os.mkdir(final_path)

        file_1 = final_path + '/' + extension + '.header'
        file_2 = final_path+'/'+extension+'.parscit'
        file_3 = final_path+'/'+extension+'.file'
        file_4 = final_path+'/'+extension+'.txt'
        fh = open(file_1,'w')
        fh1 = open(file_2,'w')
        fh2 = open(file_3,'w')

        xmlWriter = XmlWriter(path_full_text,path_output,path_parscit,path_met)
        xmlWriter.main()

        ET.ElementTree(xmlWriter.get_file_info_root()).write(file_3,encoding='UTF-8',xml_declaration=True)
        ET.ElementTree(xmlWriter.get_header_root()).write(file_1)
        ET.ElementTree(xmlWriter.get_parscit_root()).write(file_2)

        fh.close()
        fh1.close()
        fh2.close()

        try:
            f = open(path_met, "r")
            copy = open(final_path+'/'+extension+'.met', "wt")
            for line in f:
                copy.write(line)
            f.close()
            copy.close()
        except:
            pass

        try:
            f = open(path_txt, "r")
            copy = open(final_path+'/'+extension+'.txt', "wt")
            for line in f:
                copy.write(line)
            f.close()
            copy.close()

            oldFileName, extension = os.path.splitext(path_txt)
            keyword = 'REFERENCES'
            with open(path_txt, 'r') as fh:
                text_split = fh.read().split(keyword)

            with open(oldFileName + '.body', 'w') as fh:
                fh.write(text_split[0] + keyword)

            with open(oldFileName + '.cite', 'w') as fh:
                fh.write(keyword.join(text_split[1:]))

        except:
            textExtractor = text_extractor(file_4,path_full_text)
            textExtractor.main()
