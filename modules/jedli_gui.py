import re
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter.colorchooser import *
import time
import json
import webbrowser

from source_selection import Source_selection, Download
from jedli_search_options import Search_options
from jedli_logic import Highlighter, ContextSearch#, IndexGenerator
from core_mining_functions import ignore_interword_characters
import jedli_global
from jedli_global import html_path, check_path, saved_searches_path, doc_path
import sourceUpdate
import setDefaultValues
import jedli_EpubConverter
import jedli_logger

documentation_path = os.path.join(doc_path, "Jedli documentation.pdf")
about_path = os.path.join(doc_path, "About.txt")


start=time.time()

#print = jedli_global.print

class MainContainer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent) # do superclass init
        self.pack(fill=BOTH, expand=NO)
        self.parent=parent
        # the following function gets the height of the screen;
        # we limit the hight of the window to 90% of the screen.
        jedli_global.max_height = self.parent.winfo_screenheight()*0.88
        self.makeScrollBar()
        self.makeMenu()
        self.displayLogger()
        jedli_global.rClickbinder(self)
        sys.stdout = jedli_logger.RedirectLogging(jedli_global.logger.textf, 0)
        sys.stderr = jedli_logger.RedirectLogging(jedli_global.logger.textf, 1)

        
    def makeScrollBar(self):
        self.canvas=Canvas(self)
        jedli_global.frame=Frame(self.canvas)
        jedli_global.frame.pack(fill=BOTH, expand=NO)
        self.myscrollbar=Scrollbar(self,orient="vertical",
                                   command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set,
                              highlightthickness=0)

        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left", fill=BOTH, expand=NO)
        self.canvas.create_window((0,0),window=jedli_global.frame,anchor="nw")
        jedli_global.frame.bind("<Configure>",self.resizeFrame)

    def resizeFrame(self, event):
        height = 550+(len(jedli_global.search_rows)*35)
        if height > jedli_global.max_height:
            height = jedli_global.max_height
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=555,height=height)
    def makeMenu(self):
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load search parameters", command=self.loadSearch)
        filemenu.add_command(label="Save search parameters", command=self.saveSearch)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.parent.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        optionsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Load default settings",
                                command=setDefaultValues.loadDefaultValues)
        optionsmenu.add_command(label="Load and edit default settings",
                                command=setDefaultValues.setDefaultValues)
##        optionsmenu.add_command(label="Save current settings as default",
##                                command=lambda: self.hello(None))        
        menubar.add_cascade(label="Options", menu=optionsmenu)

        sourcemenu = Menu(menubar, tearoff=0)
        sourcemenu.add_command(label="Update source list", command=sourceUpdate.sourceUpdate)
        sourcemenu.add_command(label="Download sources from the Jedli website", command=Download)
        sourcemenu.add_command(label="Epub converter", command=jedli_EpubConverter.epubConverter)
        menubar.add_cascade(label="Sources", menu=sourcemenu)

        viewmenu = Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Display Jedli logger", command=self.displayLogger)
        menubar.add_cascade(label="View", menu=viewmenu)
        

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: self.hello(about_path))
        helpmenu.add_command(label="Help", command=lambda: self.hello(documentation_path))
        menubar.add_cascade(label="Help", menu=helpmenu)

    def hello(self, pth):
        try:
            webbrowser.open(pth)
        except:
            self.displayLogger()
            print("Under construction")
            print("This function will become available soon")
            #messagebox.showwarning("Under construction", "This function will become available soon")

    def displayLogger(self):
        if jedli_global.logger == None:
            jedli_global.logger = jedli_logger.Logger()
        else:
            jedli_global.logger.top.deiconify()
        
    def loadSearch(self):
        jedli_global.i_o_f.loadSearch()
        
    def saveSearch(self):
        jedli_global.i_o_f.saveSearch()
        
    def loadPreferences(self):
        setDefaultValues.SetDefaultValues.loadPreferences() # this does not work: "AttributeError: "function" object has no attribute "loadPreferences"" 
        
class Application(MainContainer):
    def __init__(self, parent=None):
        MainContainer.__init__(self, parent)
        #self.pack(fill=BOTH, expand=YES)
        self.make_frames()

    def make_frames(self):
        jedli_global.search_f = SearchTermsGUI(jedli_global.frame)
        jedli_global.i_o_f = InputOutputGUI()
        jedli_global.index_f = IndexGUI()
        jedli_global.highlight_f = HighlightGUI()
        jedli_global.context_f = ContextGUI()
##        print(time.time()-start)


class MakeSearchRows(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.checklist = None
        self.and_not = None
        self.search_options = None
        self.inp = None
        self.and_or_not = StringVar()
        self.and_or_not.set(jedli_global.and_or_not_default)
        
        #search options
        self.searchregex1 = None
        self.searchregex2 = None
        self.alif_option = None
        self.simpleSearch = None
        self.ta_marb_option = None
        self.alif_maqs_option = None
        self.prefixes = jedli_global.prefixes
        self.prefix_masdar = jedli_global.prefix_masdar
        self.prefix_perfect_i = jedli_global.prefix_perfect_i
        self.prefix_article = jedli_global.prefix_article
        self.prefix_preposition = jedli_global.prefix_preposition
        self.prefix_personal = jedli_global.prefix_personal
        self.prefix_future = jedli_global.prefix_future
        self.prefix_lila = jedli_global.prefix_lila
        self.prefix_conjunction = jedli_global.prefix_conjunction
        self.prefix_interr = jedli_global.prefix_interr
        self.suffixes = jedli_global.suffixes
        self.suffix_nisba = jedli_global.suffix_nisba
        self.suffix_case = jedli_global.suffix_case
        self.suffix_verb_infl = jedli_global.suffix_verb_infl
        self.suffix_pronom = jedli_global.suffix_pronom
        
    def createRows(self, row_no, frame):
        if row_no > 0:
             
            self.and_b = Radiobutton(frame, text="AND", indicatoron=0,
                                     variable=self.and_or_not, value="AND")
            self.and_b.grid(column=0, row=row_no, padx=5, pady=5)
            self.or_b = Radiobutton(frame, text="OR", indicatoron=0,
                                     variable=self.and_or_not, value="OR")
            self.or_b.grid(column=1, row=row_no, padx=5, pady=5)
            self.not_b = Radiobutton(frame, text="NOT", indicatoron=0,
                                     variable=self.and_or_not, value="NOT")
            self.not_b.grid(column=2, row=row_no, padx=5, pady=5)
        self.input1 = Entry(frame, width=25)
        self.input1.grid(column=3, row=row_no, padx=5, pady=5)
        self.checklist_b = ttk.Button(frame, text="select checklist", style="sea.TButton",
               command=self.askCheckList).grid(column=5, row=row_no, padx=5, pady=5, sticky=NE)     
        self.search_options_b = ttk.Button(frame, text="search options", style="sea.TButton",
               command=self.searchOptions).grid(column=6, row=row_no, padx=5, pady=5, sticky=NE)


    def askCheckList(self):
        self.checklist = askopenfilename(title="Choose a checklist",
                               initialdir=check_path, filetypes = [("text files", ".txt")])
        if len(self.checklist) > 0:   
            if self.checklist != self.input1.get():            
                self.input1.delete(0, END)
                self.input1.insert(0, self.checklist.split("/")[-1])
            else:
                self.input1.insert(0, self.checklist.split("/")[-1])
        return self.checklist

    def searchOptions(self):
        options = Search_options()
        self.search_options = True
        self.searchregex1 = options.searchregex1
        self.searchregex2 = options.searchregex2
        self.alif_option = options.alif_option
        self.ta_marb_option = options.ta_marb_option
        self.alif_maqs_option = options.alif_maqs_option
        self.simpleSearch = options.simpleSearch
        self.prefixes = options.prefixes
        self.prefix_masdar = options.prefix_masdar
        self.prefix_perfect_i = options.prefix_perfect_i
        self.prefix_article = options.prefix_article
        self.prefix_preposition = options.prefix_preposition
        self.prefix_personal = options.prefix_personal
        self.prefix_future = options.prefix_future
        self.prefix_lila = options.prefix_lila
        self.prefix_conjunction = options.prefix_conjunction
        self.prefix_interr = options.prefix_interr
        self.suffixes = options.suffixes
        self.suffix_nisba = options.suffix_nisba
        self.suffix_case = options.suffix_case
        self.suffix_verb_infl = options.suffix_verb_infl
        self.suffix_pronom = options.suffix_pronom


    def alifs(self, word):
        A = ["ا", "آ", "إ", "أ"]
        for x in A:
            word = re.sub(x, "X", word)
        word = re.sub("X", "[اإآأ]", word)
        return(word)

    def apply_options(self, word):
        if self.alif_option:
            word = self.alifs(word)
        if jedli_global.ignore_interword == True:
            word = ignore_interword_characters(word)
        
        # the following makes sure that the final ha and the construct form
        # of ta marbuta are also taken into account (but not a ta not followed by a suffix):
        if self.ta_marb_option:
             word = re.sub(r"[ةه]\b", r"(?:ة|ه|(?:%s\B))" % "ت", word)
        else:
            word = re.sub("ة", r"(?:ة|(?:%s\B))" % "ت", word)
        # the following makes sure that the final ya and the construct form
        # of alif maqsura (= alif) are also taken into account
        # (but not an alif not followed by a suffix):
        if self.alif_maqs_option:
            word = re.sub(r"[يى]\b", r"(?:ى|ي|(?:%s\B))" % "ا", word)
        else:
            word = re.sub("ى", r"(?:ى|(?:%s\B))" % "ا", word)
        regex1 = self.searchregex1
        regex2 = self.searchregex2

        try:
            word = regex1+word+regex2
        except TypeError:
            regex1 = r"\b(?:ا|أ|و|ف|ل|س|ت|ي|ن|إ|م|ك|ب){0,6}"
            regex2 = r"\b"
            word = regex1+word+regex2
        return(word)


class SearchTermsGUI(Frame):
    def __init__(self, parent=None):        
        Frame.__init__(self)
        self.frame = ttk.Frame(jedli_global.frame)
        self.frame.configure(style = "roundedFrameSea", padding=10)
        self.frame.pack(expand=YES, fill=BOTH)
        Label(self.frame, text="Search term(s): ", bg="light sea green", fg="white").grid(
            row=0, column=0, columnspan=3, padx=5, pady=5)
        self.addFirstRow()
        self.add_more = ttk.Button(self.frame, text="Add more search words",
               command=self.addNewRow, style="sea.TButton")
        self.add_more.grid(column=3, row=self.m+1, padx=5, pady=5)
        self.count = len(self.rows)               

    def addFirstRow(self):
        self.rows = []
        self.m = len(self.rows)
        jedli_global.first_row=MakeSearchRows()
        jedli_global.first_row.createRows(0, self.frame)
        jedli_global.search_rows = []
        jedli_global.search_rows.append(jedli_global.first_row)
        self.rows.append(jedli_global.first_row)


    def addNewRow(self):
        self.m=len(self.rows)
        self.new_row = MakeSearchRows()        
        self.rows.append(self.new_row)
        jedli_global.search_rows.append(self.new_row)        
        self.new_row.createRows(self.m, self.frame)
        self.add_more.grid(column=3, row=self.m+1, padx=5, pady=5)

##    UNUSED??
##    def askCheckList(self):
##        MakeSearchRows.askCheckList(self)
##
##    def searchOptions(self):
##        MakeSearchRows.searchOptions(self)
##        
##    def saveInput(self, m):
##        MakeSearchRows.saveInput(self)
        
            

class InputOutputGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self)
        self.frame = ttk.Frame(jedli_global.frame)
        self.frame.configure(style = "roundedFrameSea", padding=10)
        self.frame.pack(expand=YES, fill=BOTH)
        self.createButtons()
        self.setDefaultValues()
        
        
    def createButtons(self):
        Label(self.frame, text="Input and Output",bg="light sea green", fg="white").grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        Label(self.frame, text="Source(s) to be searched: ",bg="light sea green").grid(
            row=1, column=0, columnspan=3, padx=5, pady=5, sticky=NW)
        Label(self.frame, text="Output folder: ",bg="light sea green").grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        self.col_header=["Author", "Title"]
        self.sources_t = ttk.Treeview(self.frame, height=10, columns=self.col_header, show="headings")
        vsb = Scrollbar(self.frame, orient="vertical", command=self.sources_t.yview)
        hsb = Scrollbar(self.frame, orient="horizontal", command=self.sources_t.xview)
        self.sources_t.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sources_t.grid(column=1, columnspan=5, row=2, sticky="nsew")
        vsb.grid(column=6, row=2, rowspan=2, sticky="wns")
        hsb.grid(column=1, columnspan=5, row=3, sticky="ew")

        self.output_entry = Entry(self.frame, width=45)        
        self.output_entry.grid(row=4, column=2, columnspan=2, padx=5, pady=5)
        ttk.Button(self.frame, text="select source(s)", command=self.selectSources,
               width=20, style="sea.TButton").grid(row=1,
                column=2, columnspan=3, padx=5, pady=10)
        ttk.Button(self.frame, text="change output folder", command=self.outputFolder,
               width=20, style="sea.TButton").grid(row=4,
                column=4, columnspan=3, padx=5, pady=10, sticky=NW)
        m=0


    def build_tree(self, source_list):
        for col in self.col_header:
            self.sources_t.heading(col, text=col.title(),
                              command=lambda col=col: self.sortby(self.sources_t, col, 0))
            # adjust the column's width to the header string:
        self.sources_t.delete(*self.sources_t.get_children())            

        for item in source_list:
            self.sources_t.insert("", "end", values=item)
        self.sources_t.column("Author", width=140)
        self.sources_t.column("Title", width=240)

    def setDefaultValues(self):
        self.output_entry.delete(0,END)
        self.output_entry.insert(0, jedli_global.output_default)
        self.output_entry.configure(fg="grey")
        self.build_tree(jedli_global.sources_default)
        
    def selectSources(self):
        ssl=Source_selection()
        ssl.top.title("Select your sources")
        ssl.top.wait_window()
        
        all_sources=ssl.sourcefiles
        
        if len(all_sources) == 0:
          print("No sources selected")  
        elif len(all_sources) < 20:
            print("You have selected the following sources:")
            for x in all_sources:
                print("%s - %s \n(%s)" % (x[0], x[1], os.path.basename(x[2])))
        else:
            print("You have selected the following sources:")
            for x in all_sources[:20]:
                print("%s - %s \n(%s)" % (x[0], x[1], os.path.basename(x[2])))
            try:
                print("and %s more sources" % (len(all_sources)-20))
            except:
                print("Total: %s" % len(all_sources))
        self.sources = set(all_sources)
        self.sources = list(self.sources)
        self.build_tree(self.sources)
        jedli_global.sources = self.sources

                
    def outputFolder(self):
        self.output_folder=askdirectory(title="""Choose a directory to save your
                                        output html file""", initialdir=jedli_global.output_default)
        jedli_global.output_folder = self.output_folder
        self.output_entry.delete(0,END)
        self.output_entry.insert(0, jedli_global.output_folder)
        self.output_entry.configure(fg="black")
        
    def saveSearch(self):
        filename = asksaveasfilename(title= "Choose a name for your search criteria",
                                     initialdir=saved_searches_path,
                                     filetypes=[("json files", ".json")])
        if filename.endswith(".json") is not True:
            filename+=".json"
        values = GetValues()
        values.getValues()
        file = open(filename, mode="w", encoding="utf-8")
        json.dump(values.values_to_be_saved, file, ensure_ascii=False)
        file.close()
    
    def loadSearch(self):
        ### open the document that contains the saved search settings:
        filename=askopenfilename(title="Choose your saved search file",
                                 initialdir=saved_searches_path,
                                 filetypes=[("json files", ".json")])
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                values = json.load(file)
            for value in values:
                pass
            
        except:
            #print("no file selected")
            pass

        ### set the settings:
        jedli_global.sources = values[0]
        jedli_global.i_o_f.build_tree(values[0])
        jedli_global.output_folder = values[1]

        self.output_entry.delete(0,END)
        self.output_entry.insert(0, jedli_global.output_folder)
        self.output_entry.configure(fg="black")

        for row in jedli_global.search_f.rows:
            row.input1.delete(0, END)
        e=0
        for dic in values[2]:
            if e > (len(jedli_global.search_f.rows)-1):
                jedli_global.search_f.addNewRow()
            else:
                pass
            jedli_global.search_f.rows[e].searchregex1 = dic["searchregex1"]
            jedli_global.search_f.rows[e].searchregex2 = dic["searchregex2"]
            jedli_global.search_f.rows[e].alif_option = dic["alif_option"]
            jedli_global.search_f.rows[e].ta_marb_option = dic["ta_marb_option"]
            jedli_global.search_f.rows[e].alif_maqs_option = dic["alif_maqs_option"]
            try:
                jedli_global.search_f.rows[e].simpleSearch = dic["simpleSearch"]
                jedli_global.search_f.rows[e].prefixes = dic["prefixes"]
                jedli_global.search_f.rows[e].prefix_masdar = dic["prefix_masdar"]
                jedli_global.search_f.rows[e].prefix_perfect_i = dic["perfect_i"]
                jedli_global.search_f.rows[e].prefix_article = dic["prefix_article"]
                jedli_global.search_f.rows[e].prefix_preposition = dic["prefix_preposition"]
                jedli_global.search_f.rows[e].prefix_personal = dic["prefix_personal"]
                jedli_global.search_f.rows[e].prefix_future = dic["prefix_future"]
                jedli_global.search_f.rows[e].prefix_lila = dic["prefix_lila"]
                jedli_global.search_f.rows[e].prefix_conjunction = dic["prefix_conjunction"]
                jedli_global.search_f.rows[e].prefix_interr = dic["prefix_interr"]
                jedli_global.search_f.rows[e].suffixes = dic["suffixes"]
                jedli_global.search_f.rows[e].suffix_nisba = dic["suffix_nisba"]
                jedli_global.search_f.rows[e].suffix_case = dic["suffix_case"]
                jedli_global.search_f.rows[e].suffix_verb_infl = dic["suffix_verb_infl"]
                jedli_global.search_f.rows[e].suffix_pronom = dic["suffix_pronom"]        

            except:
                jedli_global.search_f.rows[e].simpleSearch = None
                jedli_global.search_f.rows[e].prefixes = None
                jedli_global.search_f.rows[e].prefix_masdar = None
                jedli_global.search_f.rows[e].prefix_perfect_i = None
                jedli_global.search_f.rows[e].prefix_article = None
                jedli_global.search_f.rows[e].prefix_preposition = None
                jedli_global.search_f.rows[e].prefix_personal = None
                jedli_global.search_f.rows[e].prefix_future = None
                jedli_global.search_f.rows[e].prefix_lila = None
                jedli_global.search_f.rows[e].prefix_conjunction = None
                jedli_global.search_f.rows[e].prefix_interr = None
                jedli_global.search_f.rows[e].suffixes = None
                jedli_global.search_f.rows[e].suffix_nisba = None
                jedli_global.search_f.rows[e].suffix_case = None
                jedli_global.search_f.rows[e].suffix_verb_infl = None
                jedli_global.search_f.rows[e].suffix_pronom = None        
            
            if dic["checklist_name"] is None:
                try:
                    jedli_global.search_f.rows[e].input1.insert(0, "-".join(dic["words"]))
                except TypeError:
                    jedli_global.search_f.rows[e].input1.insert(0, dic["words"])
            else:
                jedli_global.search_f.rows[e].input1.insert(0, dic["checklist_name"].split("/")[-1])
                jedli_global.search_f.rows[e].checklist = dic["checklist_name"]
            e +=1


class IndexGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self)
        self.frame = ttk.Frame(jedli_global.frame)
        self.frame.configure(style = "roundedFrameOlive", padding=10)
        self.frame.pack(side=LEFT, expand="yes", fill="both")
        self.make_index_buttons()

    def make_index_buttons(self):
        ttk.Button(self.frame, text="index it!", command=self.index_generator,
                   style="olive.TButton").pack(pady=5)
##        self.output_context_entry = Entry(self.frame, textvariable=jedli_global.output_context_words, width=5,
##                                   justify=RIGHT)
##        self.output_context_entry.pack(side=LEFT)
##        self.output_context_entry.insert(0, jedli_global.output_context_words)
##        Label(self.frame, text=" words of context", bg="DarkOliveGreen3").pack(side=LEFT, padx=5)

        Label(self.frame, text="Output context: ", bg="DarkOliveGreen3").pack(side=LEFT, padx=1)
        self.context_entry = Entry(self.frame, textvariable=jedli_global.output_context_words,
                                          width=5,justify=RIGHT)
        self.context_entry.pack(side=LEFT)
        self.context_entry.insert(0, jedli_global.output_context_words)
        Label(self.frame, text=" words", bg="DarkOliveGreen3").pack(side=LEFT, padx=1)

     
    def other_terms_than_NOT_words(self, variables):
        """Return True if at least one of the search terms is not a NOT word"""
        for dic in variables.search_values:
            if dic["and_or_not"] == "AND" or dic["and_or_not"] == "OR":
                return True

    def define_context_chars(self, words_context):
        """the user indicates the number of words of context she wants.
        This function converts this number of words to a number of characters"""
        if 0 < words_context < 3:
            char_context = (words_context*5)+5
        else:
            char_context = words_context*5
        return char_context

    def index_generator(self):
##        jedli_global.search_context_words = 0
##        jedli_global.search_context_chars = 0
        jedli_global.search_context_chars_before = 0
        jedli_global.search_context_chars_after = 0
        jedli_global.search_context_words_before = 0
        jedli_global.search_context_words_after = 0
        jedli_global.output_context_words = int(self.context_entry.get())
        jedli_global.output_context_chars = self.define_context_chars(jedli_global.output_context_words)

        jedli_global.index_type = "Index"
        variables = GetValues()
        variables.getValues()
        if variables.sources == None or variables.sources == []:
            try:
                messagebox.showwarning("Index Generator", "You have not selected a source")
            except:
                #self.displayLogger()
                print("******************************")
                print("You have not selected a source")
                print("******************************")
        elif variables.search_values == []:
            try:
                messagebox.showwarning("Index Generator", "You have not selected any search word")
            except:
                #self.displayLogger()
                print("*************************************")
                print("You have not provided any search word")
                print("*************************************")
        elif not self.other_terms_than_NOT_words(variables):
                print("************************************************************")
                print("          You have only provided NOT words")
                print("Please add search terms or select another operator (AND, OR)")
                print("*************************************************************")   
        else:
            #IndexGenerator().indexGenerator(variables)
            #ContextSearch().contextSearch(variables)
            c = ContextSearch(variables)
            c.contextSearch()

class HighlightGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self)
        self.frame = ttk.Frame(jedli_global.frame)
        self.frame.configure(style = "roundedFrameOlive", padding=10)
        self.frame.pack(side=LEFT, expand="yes", fill="both")
        self.make_highlight_buttons()

    def make_highlight_buttons(self):
        ttk.Button(self.frame, text="highlight it!", style="olive.TButton",
                   command=self.highlighter).pack(pady=5)
        self.checkvar = IntVar()
        self.checkvar.set(jedli_global.default_colors_default)
        self.context_button = Checkbutton(self.frame, variable=self.checkvar,
                                          text="choose custom colours",bg="DarkOliveGreen3")
        self.context_button.pack(side=LEFT, padx=5)


    def other_terms_than_NOT_words(self, variables):
        """Return True if at least one of the search terms is not a NOT word"""
        for dic in variables.search_values:
            if dic["and_or_not"] == "AND" or dic["and_or_not"] == "OR":
                return True

            
    def highlighter(self):
##        self.colourcheck=self.checkvar.get()
        jedli_global.custom_colors = self.checkvar.get()
        variables = GetValues()
        variables.getValues()

        if variables.sources == None or variables.sources == []:
            try:
                messagebox.showwarning("Highlighter", "You have not selected a source")
            except:
                #self.displayLogger()
                print("******************************")
                print("You have not selected a source")
                print("******************************")            
        elif variables.search_values == []:
            try:
                messagebox.showwarning("Highlighter", "You have not selected any search word")
            except:
                #self.displayLogger()
                print("*************************************")
                print("You have not provided any search word")
                print("*************************************")
        elif not self.other_terms_than_NOT_words(variables):
                print("************************************************************")
                print("          You have only provided NOT words")
                print("Please add search terms or select another operator (AND, OR)")
                print("*************************************************************")   
        else:
            #Highlighter().highlighter(variables)
            h = Highlighter(variables)
            jedli_global.index_type = "Highlighter"
            h.highlighter()


class ContextGUI(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.frame = ttk.Frame(jedli_global.frame)
        self.frame.configure(style = "roundedFrameOlive", padding=10)
        self.frame.pack(side=LEFT, expand="yes", fill="both")
        self.make_context_buttons()

    def make_context_buttons(self):
##        ttk.Button(self.frame, text="context search", style="olive.TButton",
##                   command=self.contextSearch).pack(pady=5)
##        
##        Label(self.frame, text="Search context: ", bg="DarkOliveGreen3").pack(side=LEFT, padx=5)
##        ####self.entryvar = StringVar()
##        self.search_context_entry = Entry(self.frame, textvariable=jedli_global.search_context,
##                                   width=5, justify=RIGHT)
##        self.search_context_entry.pack(side=LEFT)
##        self.search_context_entry.insert(0, jedli_global.search_context)
##        Label(self.frame, text=" words", bg="DarkOliveGreen3").pack(side=LEFT, padx=5)
##
##        Label(self.frame, text="Output context: ", bg="DarkOliveGreen3").pack(side=LEFT, padx=5)
##        self.output_context_entry = Entry(self.frame, textvariable=jedli_global.output_context,
##                                          width=5,justify=RIGHT)
##        self.output_context_entry.pack(side=LEFT)
##        self.output_context_entry.insert(0, jedli_global.output_context)
##        Label(self.frame, text=" words", bg="DarkOliveGreen3").pack(side=LEFT, padx=5)

        ttk.Button(self.frame, text="context search", style="olive.TButton",
                   command=self.contextSearch).grid(row=0, column=0,
                                                    sticky="n", columnspan=3)

        Label(self.frame, text="Words before: ",
              bg="DarkOliveGreen3").grid(row=1, column=0, sticky="w")
        self.search_context_before_entry = Entry(self.frame, width=5, justify=RIGHT,
                                   textvariable=jedli_global.search_context_words_before)
        self.search_context_before_entry.grid(row=1, column=1, sticky="w")
        self.search_context_before_entry.insert(0, jedli_global.search_context_words_before)

        Label(self.frame, text="Words after: ",
              bg="DarkOliveGreen3").grid(row=2, column=0, sticky="w")
        self.search_context_after_entry = Entry(self.frame, width=5, justify=RIGHT,
                                   textvariable=jedli_global.search_context_words_after)
        self.search_context_after_entry.grid(row=2, column=1, sticky="w")
        self.search_context_after_entry.insert(0, jedli_global.search_context_words_after)

        Label(self.frame, text="Output context: ",
              bg="DarkOliveGreen3").grid(row=3, column=0, sticky="w")
        self.output_context_entry = Entry(self.frame, width=5,justify=RIGHT,
                                          textvariable=jedli_global.output_context_words)
        self.output_context_entry.grid(row=3, column=1, sticky="w")
        ####self.output_context_entry.insert(0, jedli_global.output_context_words)
        Label(self.frame, text=" words",
              bg="DarkOliveGreen3").grid(row=3, column=2, sticky="w")


    def other_terms_than_NOT_words(self, variables):
        """Return True if at least one of the search terms is not a NOT word"""
        for dic in variables.search_values:
            if dic["and_or_not"] == "AND" or dic["and_or_not"] == "OR":
                return True
        

    def define_context_chars(self, words_context):
        """the user indicates the number of words of context she wants.
        This function converts this number of words to a number of characters"""
        if 0 < words_context < 3:
            char_context = (words_context*5)+5
        else:
            char_context = words_context*5
        return char_context


        
    def contextSearch(self):
        #jedli_global.context_context = self.entryvar.get()
        jedli_global.search_context_words_before = int(self.search_context_before_entry.get())
        jedli_global.search_context_chars_before = self.define_context_chars(jedli_global.search_context_words_before)
        jedli_global.search_context_words_after = int(self.search_context_after_entry.get())
        jedli_global.search_context_chars_after = self.define_context_chars(jedli_global.search_context_words_after)
        
        jedli_global.output_context_words = int(self.output_context_entry.get())
        jedli_global.output_context_chars = self.define_context_chars(jedli_global.output_context_words)

        jedli_global.index_type = "Context Search"
        
        variables = GetValues()
        variables.getValues()
        if variables.sources == None or variables.sources == []:
            try:
                messagebox.showwarning("Context Search", "You have not selected a source")
            except:
                #self.displayLogger()
                print("******************************")
                print("You have not selected a source")
                print("******************************")
        elif variables.search_values == []:
            try:
                messagebox.showwarning("Context Search", "You have not selected any search word")
            except:
                #self.displayLogger()
                print("*************************************")
                print("You have not provided any search word")
                print("*************************************")
        elif not self.other_terms_than_NOT_words(variables):
                print("************************************************************")
                print("          You have only provided NOT words")
                print("Please add search terms or select another operator (AND, OR)")
                print("*************************************************************")            
        elif len(variables.search_values) < 2:
            try:
                messagebox.showwarning("Context Search", "Please select second (set of) search word(s)")
            except:
                #self.displayLogger()
                print("****************************************************")
                print("  You have provided only 1 (set of) search word(s)")
                print("   Please click the Add more search words button")
                print("And add search terms that define the desired context")
                print("****************************************************")
        else:
            #ContextSearch().contextSearch(variables)
            c = ContextSearch(variables)
            c.contextSearch()


class GetValues:
    """Get the values from the user input fields in Jedli's main screen. 
    These values are saved as variables in the instance of this class,
    which can then be passed on to other classes.
    """
    
    def getValues(self):
        self.search_values = []

        # Get the values from every row in the search terms frame:
        
        for r in jedli_global.search_rows:
            dic = {}
            inp=r.input1.get()
            check_spaces = re.match(r"^\s+$", inp)
            if check_spaces is not None:
                inp=None
            if inp=="":
                inp=None
            if inp is not None and inp.endswith("txt") is False:
                r.checklist=None
                
            if inp == None:
                continue
            else:
                if r.checklist is None:
                    words = inp
                    words = words.split("-")
                elif inp == r.checklist.split("/")[-1]:
                    try:
                        words = open(r.checklist, mode="r", encoding="utf-16").read().splitlines()
                    except:
                        words = open(r.checklist, mode="r", encoding="utf-8-sig").read().splitlines()
                else:
                    words = inp
                
                words_regex = []
                for word in words:
                    word = word.strip()
                    word_regex=r.apply_options(word)
                    words_regex.append(word_regex)
##                print("Regular expressions: ")
##                for w in words_regex:
##                    print(w)

                
                dic["words"] = words
                dic["words_regex"] = words_regex
                dic["checklist_name"] = r.checklist
                dic["input"] = inp
                dic["searchregex1"] = r.searchregex1
                dic["searchregex2"] = r.searchregex2
                dic["alif_option"] = r.alif_option
                dic["ta_marb_option"] = r.ta_marb_option
                dic["alif_maqs_option"] = r.alif_maqs_option
                dic["and_or_not"] = r.and_or_not.get()
                dic["simpleSearch"] = r.simpleSearch
                dic["prefixes"] = r.prefixes
                dic["prefix_masdar"] = r.prefix_masdar
                dic["perfect_i"] = r.prefix_perfect_i
                dic["prefix_article"] = r.prefix_article
                dic["prefix_preposition"] = r.prefix_preposition
                dic["prefix_personal"] = r.prefix_personal
                dic["prefix_future"] = r.prefix_future
                dic["prefix_lila"] = r.prefix_lila
                dic["prefix_conjunction"] = r.prefix_conjunction
                dic["prefix_interr"] = r.prefix_interr
                dic["suffixes"] = r.suffixes
                dic["suffix_nisba"] = r.suffix_nisba
                dic["suffix_case"] = r.suffix_case
                dic["suffix_verb_infl"] = r.suffix_verb_infl
                dic["suffix_pronom"] = r.suffix_pronom             
                              
                self.search_values.append(dic)


        

        # Get the values from the Input and Output frame

        try:
            self.output_folder = jedli_global.output_folder
        except:
            print("no specific output folder selected; default output folder is", html_path)
            self.output_folder = html_path
            
        try:
            self.sources = jedli_global.sources
        except:
            self.sources = []
            popup = Toplevel()
            Label(popup, text = "You have not selected any source").pack(padx=5, pady=15)
            ttk.Button(popup, text="OK", command=lambda: popup.destroy()).pack(pady=15)

        self.values_to_be_saved = [self.sources,
                                   self.output_folder, self.search_values]


