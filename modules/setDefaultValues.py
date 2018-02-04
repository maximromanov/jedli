import os.path
from os.path import join 
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import time
import json

from jedli_search_options import Search_options
from source_selection import Source_selection
import jedli_global
from jedli_global import prefs_path



class SetDefaultValues:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("Set Default Values")
        self.set_main_variables()
        self.make_frame()
        self.populate_frame()
#        self.top.wait_window(self.top)
        
    def set_main_variables(self):
        self.prefs_file = ""
        self.and_or_not = StringVar()
        self.color = IntVar()
        self.verbose = BooleanVar()
        self.print_sources = BooleanVar()
        self.ignore_interword = BooleanVar()

    def make_frame(self):
        i=0
        Label(self.top, text="Select your default output folder: "
              ).grid(row=i+0,column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Button(self.top, text="Select folder", command=self.askFolder, width=16
               ).grid(row=i+0, column=2, padx=5, pady=5, columnspan=4, sticky=W)
        Label(self.top, text="Select your default search options: "
              ).grid(row=i+1, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Button(self.top, text="Search options", command=self.selectSearchOptions, width=16
               ).grid(row=i+1, column=2, padx=5, pady=5, columnspan=4, sticky=W)
        Label(self.top, text="Select your default Boolean operator for search words: "
              ).grid(row=i+2, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        self.and_b = Radiobutton(self.top, text="AND", indicatoron=0,
                                 variable=self.and_or_not, value="AND")
        self.and_b.grid(row=i+2, column=2, padx=5, pady=5, sticky=W)
        self.or_b = Radiobutton(self.top, text="OR", indicatoron=0,
                                 variable=self.and_or_not, value="OR")
        self.or_b.grid(row=i+2, column=3, padx=5, pady=5, sticky=W)
        self.not_b = Radiobutton(self.top, text="NOT", indicatoron=0,
                                 variable=self.and_or_not, value="NOT")
        self.not_b.grid(row=i+2, column=4, padx=5, pady=5, sticky=W)
        Label(self.top, text="Select your default source selection: "
              ).grid(row=i+3, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Button(self.top, text="Select sources", command=self.selectSources, width=16
               ).grid(row=i+3, column=2, padx=5, pady=5, columnspan=4, sticky=W)
        self.col_header=["Author", "Title"]
        self.sources_t = ttk.Treeview(self.top, height=10, columns=self.col_header, show="headings")
        vsb = Scrollbar(self.top, orient="vertical", command=self.sources_t.yview)
        hsb = Scrollbar(self.top, orient="horizontal", command=self.sources_t.xview)
        self.sources_t.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.sources_t.grid(column=1, columnspan=3, row=i+4, sticky="nsew")
        vsb.grid(column=4, row=i+4, rowspan=2, sticky="wns")
        hsb.grid(column=1, columnspan=3, row=i+5, sticky="ew")
        self.build_tree(jedli_global.sources_default)
        Label(self.top, text="Choose user-defined colors for highlighting: "
              ).grid(row=i+6, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Checkbutton(self.top, variable=self.color
                    ).grid(row=i+6, column=2, padx=5, pady=5, sticky=W)
        Label(self.top, text="Context to be searched before the main search word (Context Search): "
              ).grid(row=i+7, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        self.search_context_before_entry = Entry(self.top, width=5)
        self.search_context_before_entry.grid(row=i+7, column=2, padx=5, pady=5, sticky=W)
        Label(self.top, text="words"
              ).grid(row=i+7, column=3, pady=5, sticky=W, columnspan=2)
        Label(self.top, text="Context to be searched after the main search word (Context Search): "
              ).grid(row=i+8, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        self.search_context_after_entry = Entry(self.top, width=5)
        self.search_context_after_entry.grid(row=i+8, column=2, padx=5, pady=5, sticky=W)
        Label(self.top, text="words"
              ).grid(row=i+8, column=3, pady=5, sticky=W, columnspan=2)
        Label(self.top, text="Context to be displayed in output: "
              ).grid(row=i+9, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        self.output_context_entry = Entry(self.top, width=5)
        self.output_context_entry.grid(row=i+9, column=2, padx=5, pady=5, sticky=W)
        Label(self.top, text="words"
              ).grid(row=i+9, column=3, pady=5, sticky=W, columnspan=2)
        Label(self.top, text="Include texts in output even if there were no results: "
              ).grid(row=i+10, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Checkbutton(self.top, variable=self.verbose
                    ).grid(row=i+10, column=2, padx=5, pady=5, sticky=W)
        Label(self.top, text="Ignore punctuation, footnote markings etc.: "
              ).grid(row=i+11, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Checkbutton(self.top, variable=self.ignore_interword
                    ).grid(row=i+11, column=2, padx=5, pady=5, sticky=W)        
        Label(self.top, text="Display list of searched texts in search results: "
              ).grid(row=i+12, column=0, padx=5, pady=5, sticky=W, columnspan=2)
        Checkbutton(self.top, variable=self.print_sources
                    ).grid(row=i+12, column=2, padx=5, pady=5, sticky=W)
        
        Button(self.top, text="Load preferences", command=self.loadPreferencesToEdit
               ).grid(row=i+13, column=0, padx=5, pady=15, sticky=W, columnspan=2)
        Button(self.top, text="Save and set preferences", command=self.savePreferences
               ).grid(row=i+13, column=2, padx=5, pady=15, sticky=W, columnspan=4)


    def populate_frame(self):
        self.and_or_not.set(jedli_global.and_or_not_default)
        self.build_tree(jedli_global.sources_default)
        self.color.set(jedli_global.default_colors_default)
        self.search_context_before_entry.delete(0, END)
        self.search_context_before_entry.insert(0, jedli_global.search_context_words_before)
        self.search_context_after_entry.delete(0, END)
        self.search_context_after_entry.insert(0, jedli_global.search_context_words_after)
        self.output_context_entry.delete(0, END)
        self.output_context_entry.insert(0, jedli_global.output_context_words)
        self.ignore_interword.set(jedli_global.ignore_interword)
        self.print_sources.set(jedli_global.print_sources)
        
    
        
    def askFolder(self):
        resp = askdirectory(initialdir=jedli_global.output_default,
                            title="Choose a directory to save your \
                                   output html files", parent=self.top)
        if resp != "":
            jedli_global.output_default = resp
        else:
            print("you have not selected a folder")

    def selectSources(self):
        ssl=Source_selection()
        ssl.top.wait_window()
        all_sources=ssl.sourcefiles
        self.sources = set(all_sources)
        self.sources = list(self.sources)
##        print("self.sources1", self.sources)
        jedli_global.sources = self.sources
        jedli_global.sources_default = self.sources
        self.build_tree(self.sources)
        print("finished selecting sources")
        
    def selectSearchOptions(self):
        sO = Search_options()
        jedli_global.alif = sO.alif_option
        jedli_global.ta_marbuta = sO.ta_marb_option
        jedli_global.alif_maqs = sO.alif_maqs_option
        jedli_global.contextvar = sO.contextvar_sel
        jedli_global.search_option = sO.search_option_sel
        jedli_global.word_beginning = sO.word_beginning_sel
        jedli_global.pre_comb = sO.pre_comb_sel
        jedli_global.masdar = sO.masdar_sel
        jedli_global.perfect_i = sO.perfect_i_sel
        jedli_global.article = sO.article_sel
        jedli_global.preposition = sO.preposition_sel
        jedli_global.pers_pref = sO.pers_pref_sel
        jedli_global.future = sO.future_sel
        jedli_global.lila = sO.lila_sel
        jedli_global.conjunction = sO.conjunction_sel
        jedli_global.interr = sO.interr_sel
        jedli_global.word_ending = sO.word_ending_sel
        jedli_global.suf_comb = sO.suf_comb_sel
        jedli_global.nisba = sO.nisba_sel
        jedli_global.case = sO.case_sel
        jedli_global.verb_infl = sO.verb_infl_sel
        jedli_global.pronom = sO.pronom_sel
        
    def build_tree(self, source_list):
##        print(source_list)
        for col in self.col_header:
            self.sources_t.heading(col, text=col.title(),
                              command=lambda col=col: self.sortby(self.sources_t, col, 0))
        self.sources_t.delete(*self.sources_t.get_children())
        for item in source_list:
            self.sources_t.insert("", "end", values=item)
        self.sources_t.column("Author", width=140)
        self.sources_t.column("Title", width=240)


    def loadPreferences(self, filename=None):
        if filename:
            self.prefs_file = filename
        else:
            self.prefs_file = askopenfilename(title= "Choose your preferences file",
                                          initialdir=prefs_path, parent=self.top,
                                          filetypes=[("json files", ".json")])
##        try:
        with open(self.prefs_file, mode="r", encoding="utf-8") as file:
            settings_to_be_loaded = json.load(file)
##            print(settings_to_be_loaded)
        # load settings to global:
        jedli_global.output_folder=settings_to_be_loaded[0]
        jedli_global.search_context_words_before=settings_to_be_loaded[1] 
        jedli_global.and_or_not_default=settings_to_be_loaded[2]
        jedli_global.output_default=settings_to_be_loaded[3] 
        jedli_global.sources_default=settings_to_be_loaded[4]
        jedli_global.default_colors_default=settings_to_be_loaded[5] 
        jedli_global.search_context_words_after=settings_to_be_loaded[6]
        jedli_global.max_height=settings_to_be_loaded[7] 
        jedli_global.searchregex1=settings_to_be_loaded[8]
        jedli_global.searchregex2=settings_to_be_loaded[9] 
        jedli_global.alif_option=settings_to_be_loaded[10]
        jedli_global.ta_marb_option=settings_to_be_loaded[11] 
        jedli_global.alif_maqs_option=settings_to_be_loaded[12]
        jedli_global.search_option=settings_to_be_loaded[13] 
        jedli_global.word_beginning=settings_to_be_loaded[14]
        jedli_global.pre_comb=settings_to_be_loaded[15] 
        jedli_global.masdar=settings_to_be_loaded[16]
        jedli_global.perfect_i=settings_to_be_loaded[17]
        jedli_global.article=settings_to_be_loaded[18] 
        jedli_global.preposition=settings_to_be_loaded[19]
        jedli_global.pers_pref=settings_to_be_loaded[20]
        jedli_global.future=settings_to_be_loaded[21] 
        jedli_global.lila=settings_to_be_loaded[22]
        jedli_global.conjunction=settings_to_be_loaded[23]
        jedli_global.interr=settings_to_be_loaded[24] 
        jedli_global.word_ending=settings_to_be_loaded[25]
        jedli_global.suf_comb=settings_to_be_loaded[26]
        jedli_global.nisba=settings_to_be_loaded[27] 
        jedli_global.case=settings_to_be_loaded[28]
        jedli_global.verb_infl=settings_to_be_loaded[29]
        jedli_global.pronom=settings_to_be_loaded[30] 
        jedli_global.alif=settings_to_be_loaded[31]
        jedli_global.ta_marbuta=settings_to_be_loaded[32]
        jedli_global.alif_maqs=settings_to_be_loaded[33]
        #jedli_global.output_context=settings_to_be_loaded[34]
        jedli_global.output_context_words=settings_to_be_loaded[34]
        jedli_global.verbose=settings_to_be_loaded[35]
        jedli_global.ignore_interword=settings_to_be_loaded[36]
        jedli_global.print_sources=settings_to_be_loaded[37]
        print("preferences loaded")
            
            
##        except:
##            print("Loading preferences failed")
##            pass
##            messagebox.showwarning("Load preferences",
##                                   "No file selected. Please try again",
##                                   parent=self.top)
    def loadPreferencesToEdit(self):
        self.loadPreferences(None)
        
        self.and_or_not.set(jedli_global.and_or_not_default)
        self.build_tree(jedli_global.sources_default)
        self.color.set(jedli_global.default_colors_default)
        self.search_context_before_entry.delete(0, END)
        self.search_context_before_entry.insert(0, jedli_global.search_context_words_before)
        self.search_context_after_entry.delete(0, END)
        self.search_context_after_entry.insert(0, jedli_global.search_context_words_after)
        

    def savePreferences(self):
        jedli_global.and_or_not_default = self.and_or_not.get()
        jedli_global.default_colors_default = self.color.get()
        jedli_global.search_context_words_before = self.search_context_before_entry.get()
        jedli_global.search_context_words_after = self.search_context_after_entry.get()
        jedli_global.output_context = int(self.output_context_entry.get())
        jedli_global.verbose = self.verbose.get()
        jedli_global.ignore_interword = self.ignore_interword.get()
        jedli_global.print_sources = self.print_sources.get()
        
        prefs = [jedli_global.output_folder, jedli_global.search_context_words_before,
        jedli_global.and_or_not_default, jedli_global.output_default,
        jedli_global.sources_default, jedli_global.default_colors_default,
        jedli_global.search_context_words_after, jedli_global.max_height,
        jedli_global.searchregex1, jedli_global.searchregex2,
        jedli_global.alif_option, jedli_global.ta_marb_option,
        jedli_global.alif_maqs_option, jedli_global.search_option,
        jedli_global.word_beginning, jedli_global.pre_comb,
        jedli_global.masdar, jedli_global.perfect_i, jedli_global.article,
        jedli_global.preposition, jedli_global.pers_pref, jedli_global.future,
        jedli_global.lila, jedli_global.conjunction, jedli_global.interr,
        jedli_global.word_ending, jedli_global.suf_comb, jedli_global.nisba,
        jedli_global.case, jedli_global.verb_infl, jedli_global.pronom,
        jedli_global.alif, jedli_global.ta_marbuta, jedli_global.alif_maqs,
        jedli_global.output_context, jedli_global.verbose,
        jedli_global.ignore_interword, jedli_global.print_sources]

        filename = asksaveasfilename(title= "Choose a name for your search criteria",
                                     initialfile=self.prefs_file, initialdir=prefs_path,
                                     filetypes=[("json files", ".json")], parent=self.top)
        if filename == "":
            pass
##            messagebox.showwarning("Save preferences",
##                                   "No file name entered. Please try again",
##                                   parent=self.top)
        else:
            if filename.endswith(".json") is not True:
                filename+=".json"
            print("Saving the following preferences in "+filename)
            print(prefs)
            with open(filename, mode="w", encoding="utf-8") as file:
                json.dump(prefs, file, ensure_ascii=False)
            self.loadPreferences(filename)
            self.leave()


    def adjustMainWindowSettings(self):
        jedli_global.sources = jedli_global.sources_default
        jedli_global.output_folder = jedli_global.output_default
        jedli_global.i_o_f.setDefaultValues()
        jedli_global.i_o_f.build_tree(jedli_global.sources_default)
        jedli_global.index_f.context_entry.delete(0,END)
        jedli_global.index_f.context_entry.insert(0, jedli_global.output_context_words)
        jedli_global.highlight_f.checkvar.set(jedli_global.default_colors_default)
        jedli_global.context_f.search_context_before_entry.delete(0,END)
        jedli_global.context_f.search_context_before_entry.insert(0, str(jedli_global.search_context_words_before))
        jedli_global.context_f.search_context_after_entry.delete(0,END)
        jedli_global.context_f.search_context_after_entry.insert(0, str(jedli_global.search_context_words_after))
        jedli_global.context_f.output_context_entry.delete(0,END)
        jedli_global.context_f.output_context_entry.insert(0, jedli_global.output_context_words)

    def leave(self):
        self.adjustMainWindowSettings()
        self.top.destroy()
            

def loadDefaultValues():
    prefs_file = askopenfilename(title= "Choose your preferences file",
                                 initialdir=prefs_path, parent=None,
                                 filetypes=[("json files", ".json")])
##    print(prefs_file)
##    try:
    with open(prefs_file, mode="r", encoding="utf-8") as file:
        settings_to_be_loaded = json.load(file)
##        print(settings_to_be_loaded)
        # load settings to global:
    jedli_global.output_folder=settings_to_be_loaded[0]
    jedli_global.search_context_words_before=settings_to_be_loaded[1] 
    jedli_global.and_or_not_default=settings_to_be_loaded[2]
    jedli_global.output_default=settings_to_be_loaded[3] 
    jedli_global.sources_default=settings_to_be_loaded[4]
    jedli_global.default_colors_default=settings_to_be_loaded[5] 
    jedli_global.search_context_words_after=settings_to_be_loaded[6]
    jedli_global.max_height=settings_to_be_loaded[7] 
    jedli_global.searchregex1=settings_to_be_loaded[8]
    jedli_global.searchregex2=settings_to_be_loaded[9] 
    jedli_global.alif_option=settings_to_be_loaded[10]
    jedli_global.ta_marb_option=settings_to_be_loaded[11] 
    jedli_global.alif_maqs_option=settings_to_be_loaded[12]
    jedli_global.search_option=settings_to_be_loaded[13] 
    jedli_global.word_beginning=settings_to_be_loaded[14]
    jedli_global.pre_comb=settings_to_be_loaded[15] 
    jedli_global.masdar=settings_to_be_loaded[16]
    jedli_global.perfect_i=settings_to_be_loaded[17]
    jedli_global.article=settings_to_be_loaded[18] 
    jedli_global.preposition=settings_to_be_loaded[19]
    jedli_global.pers_pref=settings_to_be_loaded[20]
    jedli_global.future=settings_to_be_loaded[21] 
    jedli_global.lila=settings_to_be_loaded[22]
    jedli_global.conjunction=settings_to_be_loaded[23]
    jedli_global.interr=settings_to_be_loaded[24] 
    jedli_global.word_ending=settings_to_be_loaded[25]
    jedli_global.suf_comb=settings_to_be_loaded[26]
    jedli_global.nisba=settings_to_be_loaded[27] 
    jedli_global.case=settings_to_be_loaded[28]
    jedli_global.verb_infl=settings_to_be_loaded[29]
    jedli_global.pronom=settings_to_be_loaded[30] 
    jedli_global.alif=settings_to_be_loaded[31]
    jedli_global.ta_marbuta=settings_to_be_loaded[32]
    jedli_global.alif_maqs=settings_to_be_loaded[33]
    jedli_global.output_context_words=settings_to_be_loaded[34]
    try:
        jedli_global.verbose=settings_to_be_loaded[35]
        jedli_global.ignore_interword=settings_to_be_loaded[36]
        jedli_global.print_sources=settings_to_be_loaded[37]
    except:
        pass
    print("settings loaded")
##    except:
##        print("problem loading settings")
##        pass
##        messagebox.showwarning("Load preferences",
##                               "No file selected. Please try again",
##                               parent=None)
    jedli_global.sources = jedli_global.sources_default
    jedli_global.output_folder = jedli_global.output_default
    jedli_global.i_o_f.setDefaultValues()
    jedli_global.i_o_f.build_tree(jedli_global.sources_default)
    jedli_global.index_f.context_entry.delete(0,END)
    jedli_global.index_f.context_entry.insert(0, jedli_global.output_context_words)
    jedli_global.highlight_f.checkvar.set(jedli_global.default_colors_default)
    jedli_global.context_f.search_context_before_entry.delete(0,END)
    jedli_global.context_f.search_context_before_entry.insert(0, str(jedli_global.search_context_words_before))
    jedli_global.context_f.search_context_after_entry.delete(0,END)
    jedli_global.context_f.search_context_after_entry.insert(0, str(jedli_global.search_context_words_after))


def setDefaultValues():
    SetDefaultValues()

def main(): 
    root = Tk()
    Button(text="Display Default Values Window", command=setDefaultValues).pack()
    Button(text="Open Default Values selector", command=loadDefaultValues).pack()
    
    style = ttk.Style()
    style.configure("sea.TButton", background="light sea green")
    root.mainloop()

if __name__ == "__main__":
    main()
