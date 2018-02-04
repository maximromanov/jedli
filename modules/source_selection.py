import re
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
import time
from openpyxl import *
import urllib.request
import urllib.parse
import shutil


import jedli_global
from jedli_global import txt_path, source_info_path, source_sel_path
import sourceUpdate


base_url = r"http://downloads.islamic-empire.uni-hamburg.de/texts/"

print = jedli_global.print

class Download:
    def __init__(self):
        self.window = Source_selection()
        self.sources = self.window.sourcefiles
        self.window.top.title("Select new sources to download")
        self.window.filterff.config(background="royal blue")
        self.window.filterf.config(background="royal blue")
        self.addButtons()
        self.addDownloads()
        self.window.top.wait_window()
        self.leave()
        
    def addButtons(self):
        self.window.addDownloadsB.grid_forget()
##        self.window.removeDownloadsB.grid_forget()
        self.window.savebutton.config(text="Name and download selection")
        self.window.confirmbutton.config(text="Download selection")
        for child in self.window.filterf.children.values():
            if child.winfo_class() == "Label":
                child.config(background="royal blue")

    def addDownloads(self):
        all_downloadable_sources = []
        self.sources_wb=load_workbook(os.path.join(source_info_path, "sources_available_for_download.xlsx"))
        self.sources_ws=self.sources_wb.active
        for row in self.sources_ws.rows:
            current_row=[]
            for cell in row:
                current_row.append(cell.value)
            all_downloadable_sources.append(current_row)
        print(len(all_downloadable_sources), "sources are available on the Jedli website")
        current_sources = self.window.primary_sources[:]
        self.window.primary_sources=[]
        for s in all_downloadable_sources:
            if s not in current_sources:
                self.window.primary_sources.append(s)
##        print(len(self.window.primary_sources))
        if self.window.primary_sources == []:
            self.window.primary_sources.append(("", "no new files available", "", "", ""))
        self.window.build_tree(self.window.tree1, self.window.primary_sources)

    

    def leave(self):
        to_be_downloaded = self.window.sourcefiles
        if len(to_be_downloaded)>1:
            print("now downloading %s files; this may take a while" % len(to_be_downloaded))
            
        failed = []
        downloaded = []
        i=0
        for x in to_be_downloaded:
            i+=1
            print("now downloading", x[1])
            print(len(self.window.sourcefiles)-i, "files to go")
            filename = os.path.basename(x[2])
            url = base_url+filename
            output_file = os.path.join(txt_path, filename)
            try:
                with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                downloaded.append(url)
            except Exception as e:
                print(url + " this one went wrong: %s" % e)
                failed.append(url)
        if downloaded != []:
            print("Your %s downloads are being added to your texts folder" % len(downloaded))
            sourceUpdate.sourceUpdate()
        else:
            print("No sources selected for download")
        if failed != []:
            print("Jedli was not able to download the following files:")
            for y in failed:
                print(y)
            
##            try:
##                ftp = FTP("speedtest.ftp.otenet.gr")
##                ftp.login("speedtest", "speedtest") # (username, password)
##                print(ftp.retrlines('LIST')) # prints a list of all the files in that directory
##                ftp.retrbinary('RETR test100k.db', open(output_file, 'wb').write)
##            except Exception as e:
##                print(str(e))
##                failed.append(url)
##        sourceUpdate.sourceUpdate()
##        print("Your downloads have been added to your list of files")
##        if failed != []:
##            print("Jedli was not able to download the following files:")
##            for y in failed:
##                print(y)
            
        
        


class Source_selection:
    def __init__(self):
        self.top = Toplevel()
        #self.top.title("Select sources")
        self.set_main_variables()
        self.make_frames()
        self.populate_frames()
        try:
            self.move_to_selected(jedli_global.selected_sources, self.tree2, self.tree1)
##            print(jedli_global.selected_sources)
        except:
            pass
        ####### does not work while wait_window is called:
        #self.top.wait_window(self.top)
        
        
    def set_main_variables(self):
        self.col_header = ["Author","Title","Genre","Date", "Id"]
        self.primary_sources = []
        self.sources_wb=load_workbook(os.path.join(source_info_path, "sources_in_folder.xlsx"))
        self.sources_ws=self.sources_wb.active
        for row in self.sources_ws.rows:
            current_row=[]
            for cell in row:
                current_row.append(cell.value)
            self.primary_sources.append(current_row)
        self.genres = list(set([x[2] for x in self.primary_sources]))
        self.user_selections = []
        for file in os.listdir(source_sel_path):
            if file.endswith(".txt"):
                self.user_selections.append(file[:-4])
        self.sourcefiles = []
        
    def make_frames(self):

        self.filterff=Frame(self.top) # this frame only serves to keep the filterf centered
        self.filterff.pack(side=TOP, fill="both", expand=True, padx=5, pady=5)
        self.filterff.config(background="light sea green") 
        self.filterf=Frame(self.filterff)
        self.filterf.pack(side=TOP, fill=Y)
        self.make_filterf()
        self.sourcef=Frame(self.top)
        self.sourcef.pack(side=LEFT, fill="both", expand=True, pady=10, padx=5)
        self.make_sourcef()
        self.transferf=Frame(self.top)
        self.transferf.pack(side=LEFT, pady=10, padx=5)
        self.make_transferf()
        self.selectedf=Frame(self.top)
        self.selectedf.pack(side=LEFT, fill="both", expand=True, pady=10, padx=5)
        self.make_selectedf()
        
    def make_filterf(self):
        self.filterf.config(background="light sea green")
        Label(self.filterf, text = "Filters:", background="light sea green").grid(row=0, column=0, padx=20, pady=5, sticky=W)
        Label(self.filterf, text = "Author: ", background="light sea green").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        Label(self.filterf, text = "Title: ", background="light sea green").grid(row=1, column=1, padx=5, pady=5, sticky=W)
        Label(self.filterf, text = "Genre: ", background="light sea green").grid(row=2, column=1, padx=5, pady=5, sticky=W)       
        Label(self.filterf, text = "Dates: between", background="light sea green").grid(row=3, column=1, padx=5, pady=5, sticky=W)
        Label(self.filterf, text = "My selections: ", background="light sea green").grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.author_entry = Entry(self.filterf, width=23)
        self.author_entry.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky=W)
        self.title_entry = Entry(self.filterf, width=23)
        self.title_entry.grid(row=1, column=2, columnspan=5, padx=5, pady=5, sticky=W)
        self.genre_box = ttk.Combobox(self.filterf, values=[1,2])
        self.genre_box.grid(row=2, column=2, columnspan=5, padx=5, pady=5, sticky=W)       
        self.start_date_entry = Entry(self.filterf, width=5)
        self.start_date_entry.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        Label(self.filterf, text = "and", background="light sea green").grid(row=3, column=3, padx=5, pady=5, sticky=W)
        self.end_date_entry = Entry(self.filterf, width=5)
        self.end_date_entry.grid(row=3, column=4, padx=5, pady=5, sticky=W)
        Label(self.filterf, text = "AH", background="light sea green").grid(row=3, column=5, padx=5, pady=5, sticky=W)        
        self.selection_box = ttk.Combobox(self.filterf, values=[1,2])
        self.selection_box.grid(row=4, column=2, columnspan=5, padx=5, pady=5, sticky=W)
        ttk.Button(self.filterf, text="Clear all", style="sea.TButton",
                   command=self.clear_all).grid(row=0, column=6, padx=5, pady=5, sticky=W)
        ttk.Button(self.filterf, text="Apply filters", style="sea.TButton",
                   command=self.apply_filters).grid(row=4, column=6, padx=5, pady=5, sticky=W)

    def make_sourcef(self):
# the code for the muticolumn listbox widget is based on:
# http://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        self.label1 = Label(self.sourcef, text="Select your sources:")
        self.label1.grid(row=0, column=0, sticky="n")
        self.tree1 = ttk.Treeview(self.sourcef, height=16,
                                  columns=self.col_header, show="headings")
        vsb = Scrollbar(self.sourcef, orient="vertical", command=self.tree1.yview)
        hsb = Scrollbar(self.sourcef, orient="horizontal", command=self.tree1.xview)
        self.tree1.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree1.grid(column=0, columnspan=2, row=1, sticky="nsew")
        vsb.grid(column=2, row=1, sticky="ns")
        hsb.grid(column=0, columnspan=3, row=2, sticky="ew")
        self.sourcef.grid_columnconfigure(0, weight=1)
        self.sourcef.grid_rowconfigure(0, weight=1)
        self.addDownloadsB = ttk.Button(self.sourcef, text="download additional sources", command=self.addDownloads)
        self.addDownloadsB.grid(column=0, row=3, pady=10)
##        self.removeDownloadsB = ttk.Button(self.sourcef, text="remove downloadable sources", command=self.addDownloads)
##        self.removeDownloadsB.grid(column=1, row=3, pady=10)
        self.loadSourcesB = ttk.Button(self.sourcef, text="load saved selection", command=self.loadSelection)
        self.loadSourcesB.grid(column=1, row=3, pady=10)


    def make_transferf(self):
        Button(self.transferf, text = ">>", width=6,
               command=lambda: self.move_to_selected(self.tree1.get_children(), self.tree2, self.tree1)).pack(side=TOP, padx=5)
        Button(self.transferf, text = ">", width=6,
               command=lambda: self.move_to_selected(self.tree1.selection(), self.tree2, self.tree1)).pack(side=TOP, padx=5, pady=10)
        Button(self.transferf, text = "<", width=6,
               command=lambda: self.move_to_selected(self.tree2.selection(), self.tree1, self.tree2)).pack(side=TOP, padx=5, pady=10)
        Button(self.transferf, text = "<<", width=6,
               command=lambda: self.move_to_selected(self.tree2.get_children(), self.tree1, self.tree2)).pack(side=TOP, padx=5)
        
    def make_selectedf(self):
        Label(self.selectedf, text="You have selected these sources: ").grid(row=0, column=0, sticky="n")
        self.tree2 = ttk.Treeview(self.selectedf, height=15, columns=self.col_header, show="headings")
        vsb = Scrollbar(self.selectedf, orient="vertical", command=self.tree2.yview)
        hsb = Scrollbar(self.selectedf, orient="horizontal", command=self.tree2.xview)
        self.tree2.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree2.grid(column=0, columnspan=2, row=1, sticky="nsew")
        vsb.grid(column=2, row=1, sticky="ns")
        hsb.grid(column=0, columnspan=3, row=2, sticky="ew")
        self.savebutton=ttk.Button(self.selectedf, text="Save selection for later",
               command=lambda widget="save": self.leave(widget))
        self.savebutton.grid(column=0, row=3, pady=10)
        self.confirmbutton = ttk.Button(self.selectedf, text="Confirm selection",
               command=lambda widget="ok": self.leave(widget))
        self.confirmbutton.grid(column=1, row=3, pady=10)
        self.selectedf.grid_columnconfigure(0, weight=1)
        self.selectedf.grid_rowconfigure(0, weight=1)

    def populate_frames(self):
        self.build_tree(self.tree1, self.primary_sources)
        self.build_tree(self.tree2, [])
        self.genre_box.config(values=self.genres)
        self.selection_box.config(values=self.user_selections)

    def build_tree(self, tree, source_list):
##        print(source_list)

        for col in self.col_header:
            tree.heading(col, text=col.title(),
                              command=lambda col=col: self.sortby(tree, col, 0))
            # adjust the column's width to the header string:
        tree.delete(*tree.get_children())

        for item in source_list:
            tree.insert("", "end", values=item)
        tree.column("Author", width=140, anchor="e")
        tree.column("Title", width=140, anchor="e")
        tree.column("Genre", width=100, anchor="e")
        tree.column("Date", width=40, anchor="e")
        tree.column("Id", minwidth=0, width=0, stretch=0)


    def get_selected_sources(self, my_sel):
        #make a dictionary that has the text ids as keys, and the source info as values:
        primary_sources_dict = {str(array[4]):array for array in self.primary_sources}

        #open the file that contains the paths of the selected texts:
        if not my_sel.endswith(".txt"):
            my_sel += ".txt"
        path=os.path.join(source_sel_path, my_sel)
        with open(path, encoding="utf-8-sig", mode="r") as file:
            source_paths=file.read().splitlines()
            
        #get the relevant source information from the primary_sources_dict:
        sources = []
        for source_path in source_paths:
            identifier = os.path.splitext(os.path.basename(source_path))[0]
            if identifier in primary_sources_dict:
                sources.append(primary_sources_dict[identifier])
        return sources


### Button-operated methods:
    def loadSelection(self):
        my_sel = askopenfilename(title="Select saved text selection",
                               initialdir=source_sel_path, filetypes = [("text files", ".txt")])
##        #make a dictionary that has the text ids as keys, and the source info as values:
##        primary_sources_dict = {str(array[4]):array for array in self.primary_sources}
##
##        #open the file that contains the paths of the selected texts:
##        if not my_sel.endswith(".txt"):
##            my_sel += ".txt"
##        path=os.path.join(source_sel_path, my_sel)
##        with open(path, encoding="utf-8-sig", mode="r") as file:
##            source_paths=file.read().splitlines()
##            
##        #get the relevant source information from the primary_sources_dict:
##        sources = []
##        for source_path in source_paths:
##            identifier = os.path.splitext(os.path.basename(source_path))[0]
##            if identifier in primary_sources_dict:
##                sources.append(primary_sources_dict[identifier])
        self.top.tkraise() # bring the Select sources window back into focus
        sources = self.get_selected_sources(my_sel)
        self.filtered_sources = self.filter_sources(sources)
        self.build_tree(self.tree1, self.filtered_sources)

    def addDownloads(self):
        dwnl = Download()

    def numericData2(self, dt):
        try:
            dt=int(dt)
        except:
            numeric_part = re.findall("\d+", dt)
            if dt[0] == "ق":
                dt=int(numeric_part[0])*100
            elif numeric_part != []:
                dt=int(numeric_part[0])
            else:
                if dt=="معاصر":
                    dt=9998
                else:
                    dt=9999
        return dt

    def numericData(self, data):
        data = [list(i) for i in data]
        for x in data:
            dt = x[0]
            x[0] = self.numericData2(dt)
        return data

    def sortby(self, tree, col, descending):
        # sort tree contents when a column header is clicked on:
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        # if the data to be sorted is numeric change to float:
        if data[0][0].isdigit():
            #print(data[0][0])
            data = self.numericData(data)
        else:
            if data[-1][0][-1].isdigit():
                data = self.numericData(data)            
                
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], "", ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))
        
    def clear_all(self):
        for x in [self.author_entry, self.title_entry, self.genre_box,
                  self.start_date_entry, self.end_date_entry, self.selection_box]:
            x.delete(0, END)
        self.build_tree(self.tree1, self.primary_sources)
            
    def apply_filters(self):
        my_sel = self.selection_box.get()
        if my_sel == "":
            sources = self.primary_sources
        else:
            sources = self.get_selected_sources(my_sel)
##            #make a dictionary that has the text ids as keys, and the source info as values:
##            primary_sources_dict = {str(array[4]):array for array in self.primary_sources}
##
##            #open the file that contains the paths of the selected texts:
##            path=os.path.join(source_sel_path, "%s.txt" % my_sel)
##            with open(path, encoding="utf-8-sig", mode="r") as file:
##                source_paths=file.read().splitlines()
##                
##            #get the relevant source information from the primary_sources_dict:
##            sources = []
##            for source_path in source_paths:
##                identifier = os.path.splitext(os.path.basename(source_path))[0]
##                if identifier in primary_sources_dict:
##                    sources.append(primary_sources_dict[identifier])
                    
        self.filtered_sources = self.filter_sources(sources)
        self.build_tree(self.tree1, self.filtered_sources)
        
                    
    def get_filter_data(self):
        self.author_filter=self.author_entry.get()
        self.title_filter=self.title_entry.get()
        self.genre_filter=self.genre_box.get()
        self.date_filter_1=self.start_date_entry.get()
        self.date_filter_2=self.end_date_entry.get()
        
    def filter_string(self, filters, string): 
        filters = filters.split(" ")
        a = 0
        for f in filters:
            # el = apply_search_options(f)
            
            try: 
                if re.search(str(f), str(string)):
                    a+= 1
            except:
                continue
        if a >= len(filters):
            return(True)

    def filter_sources(self, source_list):
        filtered_sources = source_list
        self.get_filter_data()

        if self.author_filter != "":
            self.author_filter = jedli_global.first_row.alifs(self.author_filter)
            self.author_filter = re.sub(r"[يى]\b", r"[يى]", self.author_filter)
            temp_list = [source for source in filtered_sources if self.filter_string(self.author_filter, source[0])==True]
            filtered_sources = temp_list
        if self.title_filter != "":
            self.author_filter = jedli_global.first_row.alifs(self.author_filter)
            self.author_filter = re.sub(r"[يى]\b", r"[يى]", self.author_filter)
            temp_list = [source for source in filtered_sources if self.filter_string(self.title_filter, source[1])==True]
            filtered_sources = temp_list        
        if self.genre_filter != "":
            self.author_filter = jedli_global.first_row.alifs(self.author_filter)
            self.author_filter = re.sub(r"[يى]\b", r"[يى]", self.author_filter)
            temp_list = [source for source in filtered_sources if self.filter_string(self.genre_filter, source[2])==True]
            filtered_sources = temp_list
        if self.date_filter_1 != "":
            temp_list = []
            for source in filtered_sources:
                try:
                    source_date = re.findall("\d+", str(source[3]))[0]
                    if int(self.date_filter_1) < int(source_date):
                        temp_list.append(source)
                except:
                    continue
#            temp_list = [source for source in filtered_sources if int(self.date_filter_1) < int(source[3])]
            filtered_sources = temp_list
        if self.date_filter_2 != "":
            temp_list = []
            for source in filtered_sources:
                try:
                    source_date = re.findall("\d+", str(source[3]))[0]
                    if int(self.date_filter_2) > int(source_date):
                        temp_list.append(source)
                except:
                    continue
#            temp_list = [source for source in filtered_sources if int(self.date_filter_2) > int(source[3])]
            filtered_sources = temp_list
        return(filtered_sources)
    
    def move_to_selected(self, selection, dest, origin):
        if dest == self.tree2:
            c=dest.get_children()
            already_in_tree=[]
            for x in c:
                already_in_tree.append(dest.set(x))
        for s in selection:
            if dest == self.tree1:
                origin.delete(s)
            else:
                item=origin.set(s)
                if item not in already_in_tree:
                    already_in_tree.append(item)
        if dest == self.tree2:
            self.new_list =[]
            for item in already_in_tree:
                item=[item["Author"],item["Title"],item["Genre"],item["Date"], item["Id"]]
                self.new_list.append(item)

            self.build_tree(dest, self.new_list)


    def leave(self, widget):
        c=self.tree2.get_children()
        jedli_global.selected_sources = c
        sourcefile_list=[]
        save_list = []
        for x in c:
            source_id = self.tree2.set(x)["Id"]
            title = self.tree2.set(x)["Title"]
            author = self.tree2.set(x)["Author"]
            date = self.numericData2(self.tree2.set(x)["Date"])
            sourcefile_list.append((author, title, os.path.join(txt_path, "%s.txt" % source_id), date))
            save_list.append(os.path.join(txt_path, "%s.txt" % source_id))
            
        
        if widget == "save":
            filename = asksaveasfilename(title="Give your selection a name",
                                         initialdir=source_sel_path,
                                         filetypes=[("text files", ".txt")])
            if filename.endswith(".txt") is False:
                filename+=".txt"
            with open(filename, mode="w", encoding="utf-8") as new_file:
                sourcefiles="\n".join(save_list)
                new_file.write(sourcefiles)
        self.sourcefiles = sourcefile_list
        #print(self.sourcefiles)
        self.top.destroy()
            
        
def source_selection():
    Source_selection()

def download():
    sourceUpdate.sourceUpdate()
    Download()

def main(): 
    root = Tk()
    Button(text="Select Sources", command=source_selection).pack()
    Button(text="Download", command=download).pack()
    style = ttk.Style()
    style.configure("sea.TButton", background="light sea green")
    root.mainloop()


if __name__ == "__main__":
    main()
