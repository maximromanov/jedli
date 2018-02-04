import re
import os
from tkinter.filedialog import asksaveasfilename
from openpyxl import *

import jedli_global
from jedli_global import source_info_path, txt_path

print = jedli_global.print

def sourceUpdate():
    print("Checking the texts folder...")
    #load the shamela database to a list:
    shamela_database = []
    sources_wb=load_workbook(os.path.join(source_info_path, "source_info.xlsx"))
    sources_ws=sources_wb.active
    for row in sources_ws.rows:
        current_row=[]
        for cell in row:
            current_row.append(cell.value)
        shamela_database.append(current_row)

    #make a list of all the txt files in the txt_files directory:
    txt_files_in_directory = []
    for file in os.listdir(txt_path):
        if file.endswith(".txt"):
            txt_files_in_directory.append(file[:-4])

    # for every file in the directory, check if it is in the shamela database
    not_in_shamela = []
    in_directory = []
    for filename in txt_files_in_directory:
        x = [row for row in shamela_database if filename == str(row[4])]
        if x == []:
            not_in_shamela.append(filename)
            in_directory.append([filename, filename, "?", "?", filename])
        else:
            in_directory.append(x[0])

    print("You have currently %s text files in your text folder" % len(in_directory))

    sources_wb2=Workbook()
    sources_ws2=sources_wb2.active
    for element in in_directory:
        sources_ws2.append(element)
    sources_wb2.save(os.path.join(source_info_path, "sources_in_folder.xlsx"))

    print("Your list of sources has been updated")

