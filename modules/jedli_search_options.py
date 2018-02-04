import re
from tkinter import *
from tkinter import ttk

from core_mining_functions import deNoise
import jedli_global


class Search_options:

    def __init__(self):
## open the pop-up window
        self.top = Toplevel()
        self.top.title("Search options")
        self.top.columnconfigure(6, weight=1)

        self.defineVariables()
        self.makeButtons()
        self.setInitialSettings()
        self.getValuesAndDisplay()
## keep the pop-up running until it is destroyed:
        self.top.mainloop()

    def defineVariables(self):
## define the search options variables and set them to default value:
        self.searchregex1 = StringVar
        self.searchregex2 = StringVar

        self.contextvar = IntVar()
        self.search_option = IntVar()
        self.word_beginning = IntVar()
        self.pre_comb = IntVar()
        self.masdar = IntVar()
        self.perfect_i = IntVar()
        self.article = IntVar()
        self.preposition = IntVar()
        self.pers_pref = IntVar()
        self.future = IntVar()
        self.lila = IntVar()
        self.conjunction = IntVar()
        self.interr = IntVar()
        self.word_ending = IntVar()
        self.suf_comb = IntVar()
        self.nisba = IntVar()
        self.case = IntVar()
        self.verb_infl = IntVar()
        self.pronom = IntVar()
        self.alif = IntVar()
        self.ta_marbuta = IntVar()
        self.alif_maqs = IntVar()
        
        self.example_results = StringVar()
        self.example_results_NOT = StringVar()
        self.example_word = StringVar()
        self.example_text0="""كورة كوره وكورة فكورة أكورة أكوره وأكورة فأكورة وبكورة فبكورة ولكورة فلكورة وككورة فككورة والكورة فالكورة وبالكورة فبالكورة وللكورة فللكورة وكالكورة فكالكورة وكوره فكوره وبكوره فبكوره ولكوره فلكوره وككوره فككوره والكوره فالكوره وبالكوره فبالكوره وللكوره فللكوره وكالكوره فكالكوره وكورته فكورته وبكورته فبكورته ولكورته فلكورته وككورته فككورته كورت مذكورة ذكورته كذكوره"""
        self.example_text1 = """اشغل اشغلت اشغلنا اشغلوا أشغلوا أشغل تشغل يشغلون شغل وشغل فشغل وأشغل فأشغل وبشغل فبشغل ولشغل فلشغل وكشغل فكشغل والشغل فالشغل وبالشغل فبالشغل وللشغل فللشغل وكالشغل فكالشغل وشغله فشغله وبشغلها فبشغلي ولشغلنا فلشغلهما وكشغله فكشغله مشغل"""
        self.example_text2 = """أعلى أعلي وأعلى فأعلى اعلى أعلي وأعلى فأعلى وبأعلى بأعلى ولاعلى فلأعلى وكأعلى كأعلى والأعلى فالأعلى وبالأعلى فبالأعلى وللاعلى للأعلى وكالأعلى فكالأعلى واعلي فأعلي وبأعلي فبأعلي ولاعلي فلأعلي وكأعلي كاعلي والأعلي فالأعلي وبالأعلي فبالأعلي وللأعلي فللأعلي  وكالأعلي فكالأعلي وأعلاه فأعلاه وبأعلاه فبأعلاه ولأعلاه فلأعلاه وكأعلاه فكأعلاه أعلا اتفقواعلى"""
        self.example_options = ["كورة", "شغل", "أعلى"]
        self.example_dic = {"كورة":self.example_text0, "شغل":self.example_text1, "أعلى":self.example_text2}


        self.simpleSearch = jedli_global.simpleSearch
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
        
## define location and commands of the buttons
    def makeButtons(self):

        self.simple_search = Radiobutton(self.top, text='Simple search: e.g. "فارس" will also find "الفارسي"',
                                    value=1, variable=self.search_option, command=self.Check_option)
        self.simple_search.grid(column=0, row=0, columnspan=3, sticky=W)
        self.restricted_search = Radiobutton(self.top, text="Restricted search",
                                        value=2, variable=self.search_option, command=self.Check_option)
        self.restricted_search.grid(column=0, row=1, columnspan=2, sticky=W)

        self.b_word_beginning = Checkbutton(self.top,
                                     text="Restrict word beginning",
                                     variable=self.word_beginning,
                                      command=self.Check_beginning)
        self.b_word_beginning.grid(column=1, row=2, sticky=W, padx=40, columnspan=5)

        self.b_strict_beginning = Radiobutton(self.top,
                         text="Super strict: allow no character before search word",
                         variable=self.pre_comb, value=0, command=self.Disable_prefixes)
        self.b_strict_beginning.grid(column=2, row=3, columnspan=2, sticky=W)
        self.b_all_prefs = Radiobutton(self.top,
                         text="All: allow all possible combinations of prefixes",
                         variable=self.pre_comb, value=1, command=self.Disable_prefixes)
        self.b_all_prefs.grid(column=2, row=4, columnspan=2, sticky=W)
        self.b_nom_prefs = Radiobutton(self.top,
                         text="Nominal: allow all possible combinations of prefixes before nouns and adjectives",
                         variable=self.pre_comb, value=2, command=self.Disable_prefixes)
        self.b_nom_prefs.grid(column=2, row=5, columnspan=2, sticky=W)
        self.b_verb_prefs = Radiobutton(self.top,
                         text="Verbal: allow all possible combinations of prefixes before verbs",
                         variable=self.pre_comb, value=3, command=self.Disable_prefixes)
        self.b_verb_prefs.grid(column=2, row=6, columnspan=2, sticky=W)
        self.b_custom_pref = Radiobutton(self.top,
                         text="Custom: allow combination of the following prefixes before search word:",
                         variable=self.pre_comb, value=4, command=self.Enable_prefixes)
        self.b_custom_pref.grid(column=2, row=7, columnspan=2, sticky=W)
        
        i = 8
        self.b_interr = Checkbutton(self.top, text="interrogative particle a-",
                               variable=self.interr, command=self.getValuesAndDisplay)
        self.b_interr.grid(column=3, row=i, sticky=W)
        self.b_conjunction = Checkbutton(self.top, text="conjunctions wa- and fa-",
                                  variable=self.conjunction, command=self.getValuesAndDisplay)
        self.b_conjunction.grid(column=3, row=i+1, sticky=W)
        self.b_lila = Checkbutton(self.top, text="affirmative/energetic particle la-, li- + jussive/subjunctive",
                               variable=self.lila, command=self.getValuesAndDisplay)
        self.b_lila.grid(column=3, row=i+2, sticky=W)
        self.b_future = Checkbutton(self.top, text="future particle sa-",
                               variable=self.future, command=self.getValuesAndDisplay)
        self.b_future.grid(column=3, row=i+3, sticky=W)
        self.b_preposition = Checkbutton(self.top, text="prepositions ka-, bi- and li-",
                                   variable=self.preposition, command=self.getValuesAndDisplay)
        self.b_preposition.grid(column=3, row=i+4, sticky=W)
        self.b_pers_pref = Checkbutton(self.top, text="personal prefixes (verbs)",
                               variable=self.pers_pref, command=self.getValuesAndDisplay)
        self.b_pers_pref.grid(column=3, row=i+5, sticky=W)
        self.b_article = Checkbutton(self.top, text="article al-",
                               variable=self.article, command=self.getValuesAndDisplay)
        self.b_article.grid(column=3, row=i+6, sticky=W)
        self.b_masdar = Checkbutton(self.top, text="m- in maṣdar, participles, nouns of instrument/place",
                               variable=self.masdar, command=self.getValuesAndDisplay)
        self.b_masdar.grid(column=3, row=i+7, sticky=W)
        self.b_perfect_i = Checkbutton(self.top, text="alif before perfect stem",
                               variable=self.perfect_i, command=self.getValuesAndDisplay)
        self.b_perfect_i.grid(column=3, row=i+8, sticky=W)


        self.j = i+9
        self.b_word_ending = Checkbutton(self.top,
                                     text="restrict word ending",
                                     variable=self.word_ending, command=self.Check_ending)
        self.b_word_ending.grid(column=1, row=self.j+1, sticky=W, padx=40, columnspan=2)

        self.b_strict_end = Radiobutton(self.top,
                         text="Super strict: allow no character after search word",
                         variable=self.suf_comb, value=0, command=self.Disable_suffixes)
        self.b_strict_end.grid(column=2, row=self.j+2, columnspan=2, sticky=W)
        self.b_all_suf = Radiobutton(self.top,
                         text="All: allow all possible combinations of suffixes",
                         variable=self.suf_comb, value=1, command=self.Disable_suffixes)
        self.b_all_suf.grid(column=2, row=self.j+3, columnspan=2, sticky=W)
        self.b_nom_suf = Radiobutton(self.top,
                         text="Nominal: all combinations of suffixes allowed after nouns and adjectives",
                         variable=self.suf_comb, value=2, command=self.Disable_suffixes)
        self.b_nom_suf.grid(column=2, row=self.j+4, columnspan=2, sticky=W)
        self.b_verb_suf = Radiobutton(self.top,
                         text="Verbal: all combinations of suffixes allowed after verbs",
                         variable=self.suf_comb, value=3, command=self.Disable_suffixes)
        self.b_verb_suf.grid(column=2, row=self.j+5, columnspan=2, sticky=W)
        self.b_custom_suf = Radiobutton(self.top,
                         text="Custom: allow combination of the following suffixes after search word:",
                         variable=self.suf_comb, value=4, command=self.Enable_suffixes)
        self.b_custom_suf.grid(column=2, row=self.j+6, columnspan=2, sticky=W)

        k = self.j+7
        self.b_nisba = Checkbutton(self.top, text="nisba ending -ī",
                                   variable=self.nisba, command=self.getValuesAndDisplay)
        self.b_nisba.grid(column=3, row=k, sticky=W)
        self.b_case = Checkbutton(self.top, text="inflection suffixes for nouns/adjectives",
                           variable=self.case, command=self.getValuesAndDisplay)
        self.b_case.grid(column=3, row=k+1, sticky=W)
        self.b_verb_infl = Checkbutton(self.top, text="inflection suffixes for verbs",
                                       variable=self.verb_infl, command=self.getValuesAndDisplay)
        self.b_verb_infl.grid(column=3, row=k+2, sticky=W)
        self.b_pronom = Checkbutton(self.top, text="suffixed pronouns",
                                    variable=self.pronom, command=self.getValuesAndDisplay)
        self.b_pronom.grid(column=3, row=k+3, sticky=W)

        ttk.Separator(self.top, orient=VERTICAL).grid(rowspan=30, row=0, column=5, sticky=NS, pady=5)

        l = k+5
        Label(self.top, text="Additional search options: ",
                   justify=LEFT, anchor=W).grid(column=6, row=0, columnspan=2, 
                                                sticky=W, padx=15)
        self.b_alif = Checkbutton(self.top, text="match any alif-hamza (ﭐأاإآ)",
                            variable=self.alif, command=self.getValuesAndDisplay)
        self.b_alif.grid(column=6, row=1, sticky=W, padx=15, columnspan=3)

        self.b_ta_marbuta = Checkbutton(self.top, text="hāʾ for tāʾ marbūṭa",
                            variable=self.ta_marbuta, command=self.getValuesAndDisplay)
        self.b_ta_marbuta.grid(column=6, row=2, sticky=W, padx=15, columnspan=3)
        self.b_alif_maqs = Checkbutton(self.top, text="match alif maqṣūra and yāʾ",
                            variable=self.alif_maqs, command=self.getValuesAndDisplay)
        self.b_alif_maqs.grid(column=6, row=3, sticky=W, padx=15, columnspan=3)

        Button(self.top, text="Show regexes and sample search >", command=self.unhideExampleFrame
               ).grid(column=6, row=7, columnspan=2, sticky=E, padx=15, pady=10)
        
        self.regex1_label = Label(self.top, wraplength=200, 
                                    text="The following regex will be prefixed to your search word(s): ")
        #self.regex1_label.grid(column=6, row=self.j+1, columnspan=2, sticky=W, padx=15)
        self.regex1_entry = Entry(self.top)
        #self.regex1_entry.grid(column=6, row=self.j+2, columnspan=2, sticky=EW, padx=15)
        self.regex2_label = Label(self.top, wraplength=200,
                                    text="The following regex will be suffixed to your search word(s): ")
        #self.regex2_label.grid(column=6, row=self.j+4, columnspan=2, sticky=W, padx=15)
        self.regex2_entry = Entry(self.top)
        #self.regex2_entry.grid(column=6, row=self.j+5, columnspan=2, sticky=EW, padx=15)

        self.OK_button = Button(self.top, text="OK", width=10, padx=10, pady=5,
                           command=self.close_search_options)
        self.OK_button.grid(column=6, row=self.j+5, sticky=SE, padx=10, pady=10, rowspan=2)

        ttk.Separator(self.top, orient=VERTICAL).grid(rowspan=30, row=0, column=8, sticky=NS, pady=5)

        self.regexframe = Frame(self.top)
        self.regexframe.grid(column=9, row=0, rowspan=30, sticky=NSEW)
##        self.regex1_label = Label(self.regexframe, wraplength=200, 
##                                    text="The following regex will be prefixed to your search word(s): ")
##        self.regex1_label.grid(column=0, row=0, columnspan=3, sticky=W, padx=15)
##        self.regex1_entry = Entry(self.regexframe)
##        self.regex1_entry.grid(column=0, row=1, columnspan=3, sticky=EW, padx=15, pady=5)
##        self.regex2_label = Label(self.regexframe, wraplength=200,
##                                    text="The following regex will be suffixed to your search word(s): ")
##        self.regex2_label.grid(column=0, row=2, columnspan=3, sticky=W, padx=15, pady=5)
##        self.regex2_entry = Entry(self.regexframe)
##        self.regex2_entry.grid(column=0, row=3, columnspan=3, sticky=EW, padx=15)
        Label(self.regexframe, wraplength=200,
              text = "Show example results for your search options with one of these words:"
              ).grid(column=0, row=4, columnspan=3, padx=5, pady=5)
        i=0
        for element in self.example_options:
            Radiobutton(self.regexframe, text=element, variable=self.example_word,value=element, 
                        command=self.exampleSearch).grid(row=5, column = i)
            i+=1
        Label(self.regexframe, wraplength=200, textvariable=self.example_results
              ).grid(column=0, row=6, columnspan=3, padx=5, pady=10)
        Label(self.regexframe, wraplength=200,
              text = "The following words would not be included in the results:"
              ).grid(column=0, row=7, columnspan=3, padx=5)
        Label(self.regexframe, wraplength=200, textvariable=self.example_results_NOT
              ).grid(column=0, row=8, columnspan=3, padx=5)
        Button(self.regexframe, text="OK", width=10, padx=10, pady=5, command=self.close_search_options
               ).grid(column=0, row=10, columnspan=3, padx=10, pady=10, sticky=SE)
        self.regexframe.grid_remove()

## group the buttons in lists:
        self.beg_end = [[self.b_word_beginning, self.word_beginning],
                        [self.b_word_ending,self.word_ending]]
        self.radio_pre = [self.b_strict_beginning, self.b_all_prefs, self.b_nom_prefs,
                          self.b_verb_prefs, self.b_custom_pref]
        self.radio_suf = [self.b_strict_end, self.b_all_suf, self.b_nom_suf,
                          self.b_verb_suf, self.b_custom_suf]
        self.check_pre = [[self.b_masdar, self.masdar], [self.b_perfect_i, self.perfect_i],
                          [self.b_article, self.article], [self.b_preposition, self.preposition],
                          [self.b_pers_pref, self.pers_pref], [self.b_future, self.future],
                          [self.b_lila, self.lila], [self.b_conjunction, self.conjunction],
                          [self.b_interr, self.interr]]
        self.check_suf = [[self.b_nisba, self.nisba], [self.b_case, self.case],
                          [self.b_verb_infl, self.verb_infl], [self.b_pronom, self.pronom]]
        self.check_add = [[self.b_alif, self.alif], [self.b_ta_marbuta, self.ta_marbuta],
                          [self.b_alif_maqs, self.alif_maqs]]

    def unhideExampleFrame(self):
        self.regexframe.grid()
        self.OK_button.grid_remove()
        self.regex1_label.grid(column=6, row=self.j+1, columnspan=2, sticky=W, padx=15)
        self.regex1_entry.grid(column=6, row=self.j+2, columnspan=2, sticky=EW, padx=15)
        self.regex2_label.grid(column=6, row=self.j+4, columnspan=2, sticky=W, padx=15)
        self.regex2_entry.grid(column=6, row=self.j+5, columnspan=2, sticky=EW, padx=15)



    def setInitialSettings(self):
## setting initial values:
        self.contextvar.set(jedli_global.contextvar)
        self.search_option.set(jedli_global.search_option)
        self.word_beginning.set(jedli_global.word_beginning)
        self.pre_comb.set(jedli_global.pre_comb)
        self.masdar.set(jedli_global.masdar)
        self.perfect_i.set(jedli_global.perfect_i)
        self.article.set(jedli_global.article)
        self.preposition.set(jedli_global.preposition)
        self.pers_pref.set(jedli_global.pers_pref)
        self.future.set(jedli_global.future)
        self.lila.set(jedli_global.lila)
        self.conjunction.set(jedli_global.conjunction)
        self.interr.set(jedli_global.interr)
        self.word_ending.set(jedli_global.word_ending)
        self.suf_comb.set(jedli_global.suf_comb)
        self.nisba.set(jedli_global.nisba)
        self.case.set(jedli_global.case)
        self.verb_infl.set(jedli_global.verb_infl)
        self.pronom.set(jedli_global.pronom)
        self.alif.set(jedli_global.alif)
        self.ta_marbuta.set(jedli_global.ta_marbuta)
        self.alif_maqs.set(jedli_global.alif_maqs)
        self.example_word.set("كورة")
        



## hiding the custom fields for the initial view:
        for x, y in self.check_pre:
            x.grid_remove()
        for x, y in self.check_suf:
            x.grid_remove()
        
##        self.search_option.set(2)
##        self.pre_comb.set(1)
##        self.suf_comb.set(0)
##        for x,y in self.beg_end:
##            y.set(1)
##        for a in [self.check_pre, self.check_suf, self.check_add]:
##            for x,y in a:
##                y.set(0)


## automatically disable and enable radiobuttons and checkbuttons if needed:
    def Check_option(self):
        if self.search_option.get() == 1:
            self.Disable_restricted()
        else:
            self.Enable_restricted()
    def Disable_restricted(self):
        for x,y in self.beg_end:
            x.configure(state="disabled")
            x.update()
            y.set(0)
        self.Disable_beginning()
        self.Disable_ending()
    def Enable_restricted(self):
        for x,y in self.beg_end:
            x.configure(state="disabled")
            x.update()
            y.set(1)
        self.restricted_search.configure(state="normal")
        self.restricted_search.update()
        self.Enable_beginning()
        self.Enable_ending()

    def Check_beginning(self):
        if self.word_beginning.get() == 1:
            self.Enable_beginning()
        else:
            self.Disable_beginning()
    def Enable_beginning(self):
        self.pre_comb.set(1)
        for x in self.radio_pre:
            x.configure(state="normal")
            x.update()
        self.getValuesAndDisplay()
    def Disable_beginning(self):
        self.Disable_prefixes()
        for x in self.radio_pre:
            x.configure(state="disabled")
            x.update()
        self.pre_comb.set(0)
        self.getValuesAndDisplay()


    def Enable_prefixes(self):
        for x,y in self.check_pre:
            x.grid()
            x.configure(state="normal")
            x.update()
        self.getValuesAndDisplay()
    def Disable_prefixes(self):
        for x, y in self.check_pre:
            x.grid_remove()
            x.configure(state="disabled")
            x.update()
            y.set(0)
        self.getValuesAndDisplay()

    def Check_ending(self):
        if self.word_ending.get() == 1:
            self.Enable_ending()
        else:
            self.Disable_ending()
        self.getValuesAndDisplay()
    def Enable_ending(self):
        self.suf_comb.set(0)
        for x in self.radio_suf:
            x.configure(state="normal")
            x.update()
        self.getValuesAndDisplay()
    def Disable_ending(self):
        self.Disable_suffixes()
        for x in self.radio_suf:
            x.configure(state="disabled")
            x.update()
        self.suf_comb.set(0)
        self.getValuesAndDisplay()

    def Enable_suffixes(self):
        for x, y in self.check_suf:
            x.grid()
            x.configure(state="normal")
            x.update()
        self.getValuesAndDisplay()
    def Disable_suffixes(self):
        for x, y in self.check_suf:
            x.grid_remove()
            x.configure(state="disabled")
            x.update()
            y.set(0)
        self.getValuesAndDisplay()

## build the prefix and suffix regexes:
    def getValues(self):
        regex1 = ""
        regex2 = ""

        if self.search_option.get() == 1: #simple search
            self.simpleSearch = True
            regex1 = "\w*?"
            regex2 = "\w*?"
        elif self.search_option.get() == 2: #restricted search
            if self.word_beginning.get() == 1:
                if self.pre_comb.get() == 1: #all possible prefixes
                    prefs = "ا|أ|و|ف|ل|س|ت|ي|ن|إ|م|ك|ب"
                    regex1 = "(?:%s){0,6}" % prefs
                    self.prefixes = "all possible combinations of prefixes"
                elif self.pre_comb.get()== 2: # all possible nominal prefixes
                    prefs = "ا|أ|و|ف|ل|س|ك|ب"
                    regex1 = "(?:%s){0,6}" % prefs
                    self.prefixes = "all possible combinations of nominal prefixes"
                elif self.pre_comb.get()== 3: # all possible verbal prefixes
                    prefs = "ا|أ|و|ف|ل|س|ت|ي|ن|إ|م"
                    regex1 = "(?:%s){0,6}" % prefs
                    self.prefixes = "all possible combinations of verbal prefixes"
                elif self.pre_comb.get()== 4: # combination of specific prefixes
                    if self.masdar.get() == 1:
                        self.prefix_masdar = "m- in maṣdar, participles, nouns of instrument/place"
                        if self.perfect_i.get() == 1:
                            regex1 = "(?:م|ا|إ)?"+regex1
                            self.prefix_perfect_i = "alif before perfect stem"
                        else:
                            regex1 = "م?"+regex1
                    else:
                        if self.perfect_i.get() == 1:
                            self.prefix_perfect_i = "alif before perfect stem"
                            regex1 = "(?:ا|إ)?"+regex1
                    if self.article.get() == 1:
                        self.prefix_article = "article al-"
                        if self.preposition.get() == 1:
                            self.prefix_preposition = "prepositions ka-, bi- and li-"
                            if self.pers_pref.get() == 1:
                                regex1 = "(?:ب|ل|ك|أ|ا|ت|ي|ن)?"+"(?:ال|لل)?"+regex1
                            else:
                                regex1 = "(?:ب|ل|ك)?"+"(?:ال|لل)?"+regex1
                        else:
                            regex1 = "(?:ال)?"+regex1
                    else:
                        if self.preposition.get() == 1:
                            self.prefix_preposition = "prepositions ka-, bi- and li-"
                            if self.pers_pref.get() == 1:
                                regex1 = "(?:ب|ل|ك|أ|ا|ت|ي|ن)?"+regex1
                            else:
                                regex1 = "(?:ب|ل|ك)?"+regex1
                    if self.pers_pref.get() == 1:
                        self.prefix_personal = "personal prefixes (verbs)"
                        if self.article.get() == 0:
                            if self.preposition.get() == 0:
                                regex1 = "(?:أ|ا|ت|ي|ن)?"+regex1
                    if self.future.get() == 1:
                        self.prefix_future = "future_particle sa-"
                        regex1 = "س?"+regex1
                    if self.lila.get() == 1:
                        self.prefix_lila = "affirmative/energetic particle la-; li- + jussive/subjunctive"
                        regex1 = "ل?"+regex1
                    if self.conjunction.get() == 1:
                        self.prefix_conjunction = "conjunctions wa- and fa-"
                        regex1 = "(?:ف|و){0,1}"+regex1
                    if self.interr.get() == 1:
                        self.prefix_interr = "interrogative particle a-"
                        regex1 = "(?:أ|ا)?"+regex1                        
                regex1 = r"\b"+regex1
            else:
                self.prefixes = "no prefixes allowed"
            if self.word_ending.get() == 1: #restrict word ending
                if self.suf_comb.get() == 1: # all possible suffixes
                    self.suffixes = "all possible combinations of suffixes"
                    sufs = "و|ن|ه|ى|ا|تما|ها|نا|ت|تم|هم|كم|ة|كما|تمو|كن|هما|ي|وا|ني|ات|هن|تن|ك|تا"
                    regex2 = "(?:%s){0,4}" % sufs
                elif self.suf_comb.get()== 2: # all possible nominal suffixes
                    self.suffixes = "all possible combinations of nominal suffixes"
                    sufs = "و|ن|ه|ى|ا|ها|ت|تم|هم|كم|ة|كما|كن|هما|ي|ات|هن|تن|ك|تا"
                    regex2 = "(?:%s){0,4}" % sufs
                elif self.suf_comb.get()== 3: # all possible verbal suffixes
                    self.suffixes = "all possible combinations of verbal suffixes"
                    sufs = "و|ن|ه|ى|ا|تما|ها|نا|ت|تم|هم|كم|كما|تمو|كن|هما|ي|وا|ني|ات|هن|تن|ك|تا"
                    regex2 = "(?:%s){0,4}" % sufs
                elif self.suf_comb.get()== 4: # combination of specific suffixes
                    if self.nisba.get() == 1:
                        self.suffix_nisba = "nisba-ending -ī"
                        regex2 = regex2+"ي?"
                    if self.case.get() == 1:
                        self.suffix_case = "inflection suffixes for nouns/adjectives"
                        sufs = "ة|ان|ين|ون|ي|ا|و|ات|تا|تي|تان|تين"
                        regex2 = regex2+"(?:%s){0,1}" % sufs
                    if self.verb_infl.get() == 1:
                        self.suffix_verb_infl = "inflection suffixes for verbs"
                        regex2 = regex2+"(?:ت|ا|ي|و|ات|ن|تم|تمو|تما|تن|تا|نا|وا)?"
                    if self.pronom.get() == 1:
                        self.suffix_pronom = "suffixed pronouns"
                        regex2 = regex2+"(?:ني|ي|نا|ك|كم|كما|كن|ه|ها|هم|هن|هم)?"
                else:
                    self.suffixes = "no suffixes allowed"
                regex2 = regex2+r"\b"
            
                


        self.searchregex1 = regex1
        self.searchregex2 = regex2
        self.searchregexes = (regex1, regex2)

        self.contextvar_sel = self.contextvar.get()
        self.search_option_sel = self.search_option.get()
        self.word_beginning_sel = self.word_beginning.get()
        self.pre_comb_sel = self.pre_comb.get()
        self.masdar_sel = self.masdar.get()
        self.perfect_i_sel = self.perfect_i.get()
        self.article_sel = self.article.get()
        self.preposition_sel= self.preposition.get()
        self.pers_pref_sel = self.pers_pref.get()
        self.future_sel = self.future.get()
        self.lila_sel = self.lila.get()
        self.conjunction_sel = self.conjunction.get()
        self.interr_sel = self.interr.get()
        self.word_ending_sel = self.word_ending.get()
        self.suf_comb_sel = self.suf_comb.get()
        self.nisba_sel = self.nisba.get()
        self.case_sel = self.case.get()
        self.verb_infl_sel = self.verb_infl.get()
        self.pronom_sel = self.pronom.get()
        self.alif_option = self.alif.get()
        self.ta_marb_option = self.ta_marbuta.get()
        self.alif_maqs_option = self.alif_maqs.get()
        if self.alif.get():
            self.alif_option = "any alif-hamza combination"
        if self.ta_marbuta.get():
            self.ta_marb_option = "final hā’ = tā’ marbūṭa"
        if self.alif_maqs.get():
            self.alif_maqs_option = "final yā’ = alif maqṣūra"


    def alifs(self, word):
        A = ["ا", "آ", "إ", "أ"]
        for x in A:
            word = re.sub(x, "X", word)
        word = re.sub("X", "[اإآأ]", word)
        return(word)

    def apply_options(self, word):
        if self.alif_option:
            word = self.alifs(word)
        # the following makes sure that the final ha and the construct form
        # of ta marbuta are also taken into account (but not a ta not followed by a suffix):
        if self.ta_marb_option:
             word = re.sub(r"[ةه]\b", r"(?:ة|ه|(?:%s\B))" % "ت", word)
        else:
            word = re.sub("ة", r"(?:ة|(?:%s\B))" % "ت", word)        
        if self.alif_maqs_option:
            #word = re.sub(r"[يى]\b", r"[يى]", word)
            word = re.sub(r"[يى]\b", r"(?:ى|ي|(?:%s\B))" % "ا", word)
        else:
            word = re.sub("ى", r"(?:ى|(?:%s\B))" % "ا", word)
        regex1 = self.searchregex1
        regex2 = self.searchregex2
        return(word)
        
    def exampleSearch(self):
        word= self.example_word.get()
##        print(word)
        example_text=self.example_dic[word]
        example_list = example_text.split(" ")
        word= self.searchregex1+word+self.searchregex2
        word= self.apply_options(word)
        example_search = re.findall(word, example_text)
        self.example_results.set(" ".join(example_search))
        
        not_found = []
        for word in example_list:
            if word not in example_search:
                not_found.append(word)
        self.example_results_NOT.set(" ".join(not_found))
        
    def getValuesAndDisplay(self):
        self.getValues()
        self.displaySearchregexes()
        self.exampleSearch()
##        print("self1", self.searchregex1)
##        print("global1", jedli_global.searchregex1)
##        print("self2", self.searchregex2)
##        print("global2", jedli_global.searchregex2)

    def displaySearchregexes(self):
        self.regex1_entry.delete(0, END)
        self.regex1_entry.insert(0, self.searchregex1)
        self.regex2_entry.delete(0, END)
        self.regex2_entry.insert(0, self.searchregex2)

    def close_search_options(self):
        self.getValues()
##        print("self1", self.searchregex1)
##        print("global1", jedli_global.searchregex1)
##        print("self2", self.searchregex2)
##        print("global2", jedli_global.searchregex2)
##        if self.searchregex1 != jedli_global.searchregex1:
##            self.searchregex1 = jedli_global.searchregex1
##        if self.searchregex2 != jedli_global.searchregex2:
##            self.searchregex2 = jedli_global.searchregex2
##        print("self1", self.searchregex1)
##        print("global1", jedli_global.searchregex1)
##        print("self2", self.searchregex2)
##        print("global2", jedli_global.searchregex2)
        print("prefix regex:", self.searchregex1)
        print("suffix regex:", self.searchregex2)
        self.top.quit()
        self.top.destroy()
        
#Search_options()
