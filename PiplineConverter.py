import os
import xml.etree.ElementTree as ET

from XmlWriter import XmlWriter
from TextExtractor import text_extractor
from os import listdir

base_path = "/root/sharedfolder/MAG_crawl/MAG_crawl_results/2020022908"
path_output = "/root/sharedfolder/MAG_crawl/MAG_crawl_results_format_converter"
filenames = listdir(base_path)
#output_file_names = set(listdir(path_output))
print(len(filenames))

for pdfmef_path in filenames:
    #print(pdfmef_path)
    #if pdfmef_path in output_file_names:
        #continue
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
    #path_algo = base_path + "/"+pdfmef_path+ "/" + pdfmef_path + ".algorithms"
    acad_paper = False
    try:
        parscit_input = ET.parse(path_parscit)
        #algo_input = ET.parse(path_algo)
        tei_input = ET.parse(path_full_text)
        root = parscit_input.getroot()
        #root_algo = algo_input.getroot()
        root_tei = tei_input.getroot()
        #print(root.tag, root_algo.tag, root_tei.tag)
        if root.tag != "error" and root_tei.tag != "error":
            acad_paper = True
    except:
        pass
    #print(success, acad_paper)
    if not success and acad_paper:
        #print('inside success and acad paper')
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

        f = open(file_3, "w")
        f.write(xmlWriter.get_file_info_string())
        f.close()

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

            textExtractor = text_extractor(file_4, path_full_text)
            textExtractor.main()

        except:
            pass
