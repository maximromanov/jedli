import re
import os
import time
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from operator import itemgetter
import random
import webbrowser
import sys
import tempfile
###
import json
import copy

from core_mining_functions import natural_sort, deNoise
import jedli_global
from jedli_global import static_files
import jedli_logger
from date_plot import make_grouped_date_graph


##############################
#      STATIC GLOBAL VARIABLES


header = open(os.path.join(static_files, "html_header.txt"), mode="r", encoding="UTF-8").read()
footer = open(os.path.join(static_files, "html_footer.txt"), mode="r", encoding="UTF-8").read()
shamelapage = '<a href="http://shamela.ws/browse.php/book-{}/page-{}" target="_blank">{}</a>'
shamelabook = '<a href="http://shamela.ws/index.php/book/{}" target="_blank">{}</a>'
waraqpage = '<a href="http://www.alwaraq.net/Core/AlwaraqSrv/bookpage?book={}&fkey=2&page={}&option=1" target="_blank">{}</a>'
waraqbook = '<a href="http://www.alwaraq.net/Core/waraq/coverpage?bookid={}" target="_blank">{}</a>'

juz = "الجزء:"
safha = "الصفحة:"
page_regex = r"%s \w+ ¦ %s \w+" % (juz, safha)

print = jedli_global.print

source_overview_link =  '<div id="top">\n'
source_overview_link += '  <a href="#results-overview">(Overview </a>\n'
source_overview_link += '  and'
source_overview_link += '  <a href="#graph"> graphs </a>\n'
source_overview_link += '  of the results at the bottom of the page)\n'
source_overview_link += '</div>\n'

default_colors = ["#FFFF00", "#00FF00", "#00CCFF", "#FF0000", "#FF99FF", "#33FFFF",
                  "#FFCC00", "#CC9900", "#CCCCCC", "#999999"]
default_colors_dic = {"#FFFF00" : "Yellow", "#00FF00" : "Lime",
                      "#00CCFF" : "Light Blue", "#FF0000" : "Red",
                      "#FF99FF" : "Pink", "#33FFFF" : "Turquoise",
                      "#FFCC00" : "Mustard", "#CC9900" : "Dark Gold",
                      "#CCCCCC" : "Gray80", "#999999": "Gray60"}

hidden_signs = ["$a", "$b", "$c", "$d", "$e", "$f", "$g", "$h", "$i", "$j", "$k", "$l", "$m",
                "$n", "$o", "$p", "$q", "$r", "$s", "$t", "$u", "$v", "$w", "$x", "$y", "$z"]





class Load_variables:
    """Contains the main variables shared by the main Jedli tools
    (currently Highlighter and Indexer/ContextSearch)"""
    
    def __init__(self, variables):
        """Initiate the class variables.
        variables is a list that contains the following elements:
            0 - sources:
            1 - output_folder: the path to the output folder
            2 - search_values: a list of dictionaries, one for every row in the search screen.
                   each dictionary contains the following elements:
                    dic["words"] = a list of search terms
                        (either, the words the user wrote in the input field,
                         or the words in the checklist she selected)
                    dic["words_regex"] = a list of regular expressions
                        (i.e., the search options applied to every search term)
                    dic["checklist_name"] = path to the checklist file
                        if the user selected any (if not: None)
                    dic["input"] = the literal content of the input field
                    dic["searchregex1"] = the regular expression prefixed to the search word
                    dic["searchregex2"] = the regular expression affixed to the search word
                    dic["and_or_not"] = Boolean operator ("AND", "OR", "NOT")
                    dic["alif_option"] = does Jedli have to disregard alif variations?(True or False)
                    dic["ta_marb_option"] = does Jedli have to disregard the difference
                       between ta marbuta and final ha(True or False)
                    dic["alif_maqs_option"] = does Jedli have to disregard the difference
                       between alif maqsura and final ya(True or False)
                    dic["simpleSearch"] = does Jedli hqve to disregard any letters before
                        and after the search word (True or False)
                    dic["prefixes"] = which combination of prefixes? (None or str)
                    dic["prefix_masdar"] = None or "m- in maṣdar, participles, nouns of instrument/place"
                    dic["prefix_perfect_i"] = None or "alif before perfect stem"
                    dic["prefix_article"] = None or "article al-"
                    dic["prefix_preposition"] = None or "prepositions ka-, bi- and li-"
                    dic["prefix_personal"] = None or "personal prefixes (verbs)"
                    dic["prefix_future"] = None or "future_particle sa-"
                    dic["prefix_lila"] = None or "affirmative/energetic particle la-; li- + jussive/subjunctive"
                    dic["prefix_conjunction"] = None or "conjunctions wa- and fa-"
                    dic["prefix_interr"] = None or "interrogative particle a-"
                    dic["suffixes"] = which combination of suffixes? (None or str)
                    dic["suffix_nisba"] = None or "nisba-ending -ī"
                    dic["suffix_case"] = None or "inflection suffixes for nouns/adjectives"
                    dic["suffix_verb_infl"] = None or "inflection suffixes for verbs"
                    dic["suffix_pronom"] = None or "suffixed pronouns"
                    """
        
        self.variables = variables
        self.NOT_repl_dic = {}
        self.NOT_repl_no = 0
        self.all_words = []
        self.all_words_regex = []
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.pth = self.tmp.name+".html"
        self.final_outcomes = ""
        self.last_search_time = time.time()
        self.start = time.time()
        self.and_or_not(variables)
        self.all_final_results_counter = 0
        self.sources = variables.sources
        self.output_folder = variables.output_folder
        #self.checklist_name = variables.search_values[0]["checklist_name"]
        self.results_dic = {}
        self.sources_dic = {}
        self.index_type = jedli_global.index_type
        self.get_first_checklist_name(variables)
        
        self.make_output_paths()


    def get_first_checklist_name(self, variables):
        self.checklist_name = ""
        for dic in variables.search_values:
            if "checklist_name" in dic:
                self.checklist_name = dic["checklist_name"]
                break


    def flatten(self, list_of_lists):
        """flatten a list of lists into a simple flat list.
        See https://stackoverflow.com/a/952952/4045481"""
        return [item for sublist in list_of_lists for item in sublist]
    

    def make_output_paths(self):
        """Make the paths for the main output directory, the data directory,
        the main html file and the json results file"""
        if jedli_global.ask_output_filename:
            self.new_file = asksaveasfilename(title= "Choose a name for the output file",
                                              initialdir=jedli_global.output_folder,
                                              filetypes=[("html files", ".html")])
            if not self.new_file.endswith(".html"):
                self.new_file += ".html"
            self.main_dir, self.base_filename = os.path.split(self.new_file)
            self.base_filename = os.path.splitext(self.base_filename)[0]
        else:
            if self.checklist_name is not None:
                self.base_filename = self.checklist_name.split("/")[-1].split(".")[0]
            else:
                self.base_filename = re.sub("\W+", "", self.words[0])
            self.main_dir = self.make_dir(jedli_global.output_folder, self.base_filename)
            
            if self.index_type == "Context Search":
                self.new_file = os.path.join(self.main_dir, "{}_in_context.html".format(self.base_filename)) 
            else:
                self.new_file = os.path.join(self.main_dir, "index_{}.html".format(self.base_filename))
            
        self.data_dir = self.make_dir(self.main_dir, "data")
        self.json_pth = os.path.join(self.data_dir, "{}_datecount.json".format(self.base_filename))
        self.graph_pth = os.path.join(self.data_dir, "{}_graph.html".format(self.base_filename))
        self.table_pth = os.path.join(self.data_dir, "{}_table.html".format(self.base_filename))
##        self.metadata_pth = os.path.join(self.data_dir, "{}_metadata.html".format(self.base_filename))


    def and_or_not(self, variables):
        """puts the search terms in lists, depending on the operator
        (AND, OR, NOT) the user selected"""
        
        # put the search terms from the first row in the user input
        # in the self.words and self_words_regex lists
        # and make empty lists for the AND and NOT words and regexes:

        self.words = variables.search_values[0]["words"].copy()
        self.words_regex = variables.search_values[0]["words_regex"].copy()
        self.AND_OR_dics = [variables.search_values[0]].copy()
        self.AND_words = []
        self.AND_words_regex = []
        self.NOT_words = []
        self.NOT_words_regex = []

        # loop through the values from all further rows in the user input
        # and add the words and regexes to the relevant lists:

        self.last_added = self.words

        for dic in variables.search_values[1:]:
            if dic["and_or_not"] == "AND":
                # NB: AND_words and AND_words_regex are lists of lists
                # because we want to allow users to define contexts with
                # numerous layers of AND words:
                # A in the context of B AND C
                # or A in the context of B OR C
                if jedli_global.index_type == "Index":
                    self.words += dic["words"]
                    self.words_regex += dic["words_regex"]
                    self.last_added = self.words
                else:
                    self.AND_OR_dics.append(dic)
                    self.AND_words_regex.append(dic["words_regex"])
                    self.AND_words.append(dic["words"])
                    self.last_added = self.AND_words

            elif dic["and_or_not"] == "NOT":
                # NB: NOT_words and NOT_words_regex are flat lists
                self.NOT_words_regex += dic["words_regex"]
                self.NOT_words += dic["words"]
                self.last_added = self.NOT_words
                
            elif dic["and_or_not"] == "OR":
                # add these words to the same list as the previous row
                if self.last_added == self.AND_words:
                    last = self.AND_words.pop()
                    self.AND_OR_dics.append(dic)
                    self.AND_words_regex.append(last+dic["words_regex"])
                    self.AND_words.append(last+dic["words"])
                elif self.last_added == self.NOT_words:
                    self.NOT_words_regex += dic["words_regex"]
                    self.NOT_words += dic["words"]
                else: 
                    self.words_regex += dic["words_regex"]
                    self.words += dic["words"]
                    self.AND_OR_dics.append(dic)
##        # make joint lists of the AND and OR categories
##        # (for use in the Highlighter and Indexer)
##        self.all_words = self.words + self.flatten(self.AND_words)
##        self.all_words_regex = self.words_regex + self.flatten(self.AND_words_regex)
##


    def keep_replacements(self, matchobj):
        """give the string matched by the regex a number,
        and store it in the self.NOT_repl_dic, so we can put the string back
        into the text later. Return the temporary replacement code repl"""
##            print(matchobj.group())
        self.NOT_repl_dic[self.NOT_repl_no] = matchobj.group(0)
        repl = "###REPL{}###".format(self.NOT_repl_no)
        self.NOT_repl_no += 1
        return repl  

    def replace_NOT_words(self, NOT_words_regex, text):
        """"temporarily replace the NOT words in the text with a code ###REPL\d+###"""
        not_regex = r"({})".format(r"|".join(NOT_words_regex))
        return re.sub(not_regex, self.keep_replacements, text)


    def replace_back(self, temp_text):
        """put the original NOT words back into the text"""
        def find_replacement(matchobj):
            return self.NOT_repl_dic[int(matchobj.group(1))]

        return re.sub("###REPL(\d+)###", find_replacement, temp_text) 

    def get_page_number(self, text, index_tuple, page_regex):
        """find the page number for the current search result"""
        
        b = text[index_tuple[1]:index_tuple[1]+6000]
        try:
            page_number = re.findall(page_regex, b)[0]
        except:
            page_number = "[no page number]"
        return page_number


    def link_page_number(self, page_number, source_id, all_page_numbers):
        """add a link to the full-text web page to the page number"""
        
        if page_number != "[no page number]": # add link to the Shamela page
            try:
                p = all_page_numbers.index(page_number)+1
                if "WARAQ" in source_id:
                    waraq_id = int(re.findall(r"\d+", source_id)[0])
                    page_number = waraqpage.format(waraq_id, p, page_number)
                else:
                    page_number = shamelapage.format(source_id, p, page_number)
            except:
                pass
        return page_number        


    def make_metadata(self, final=False):
        """Make html section with the metadata of the search"""
##        html = header
        html = '<div id="intro">Jedli {} metadata</div>\n<br/>\n'.format(jedli_global.index_type)

        if final:
            html += '<p class="ltr-text">Click <a href="{}">here</a> for an overview table of all searched sources and results</p>\n'.format(self.table_pth)
            html += '<p class="ltr-text">Click <a href="{}">here</a> for graphs of the results</p>\n'.format(self.graph_pth)
            html += '<p class="ltr-text">Search words: </p>\n'.format(self.graph_pth)

        html += '<div id="source_table">\n'
        html += '  <table>\n'

        # make table header row:
        html+= '    <tr>\n'
        html+= '      <th>operator</th>\n'
        if jedli_global.index_type == "Highlighter":
            html+= '      <th>highlight color</th>\n'
            html+= '      <th>hidden tag</th>\n'
        html+= '      <th>search word(s)</th>\n'
        html+= '      <th>checklist name</th>\n'
        html+= '      <th>search options</th>\n'
        if jedli_global.show_regex:
            html+= '      <th>regex used</th>\n'
        html+= '    </tr>\n'

        # fill the table:         
        for i, dic in enumerate(self.variables.search_values):
            html+= '    <tr>\n'
            if i > 0:
                html+= '      <td style="text-align:left">{}</td>\n'.format(dic["and_or_not"])
            else:
                html+= '      <td style="text-align:left">-</td>\n'
            if jedli_global.index_type == "Highlighter":
                html+= '      <td><span style="background-color: {0}">{0}</span></td>\n'.format(dic["color"])
                html+= '      <td>{}</td>\n'.format(dic["hidden_sign"])
            html+= '      <td>{}</td>\n'.format("<br/>".join(dic["words"]))
            if dic["checklist_name"]:
                html+= '      <td style="text-align:left">{}</td>\n'.format(dic["checklist_name"])
            else:
                html+= '      <td>--</td>\n'
            html+= '      <td style="text-align:left">{}</td>\n'.format(self.make_search_options_cell(dic))
            if jedli_global.show_regex:
                html+= '      <td>{}</td>\n'.format("<br/>".join(dic["words_regex"]))
            html+= '    </tr>\n'
        html += '  </table>\n'
        html += '</div>\n<br/>\n'

        if final:
            html += '<p class="ltr-text">Search date: {}</p>'.format(time.asctime( time.localtime(time.time()) ))

##        html += '  Click <a href="{}">here</a> for an overview of all sources searched<br/>\n'.format(self.table_pth)
##        html += '</div>'
##        html += '<div id="top"><a href="..\{}">back to overview</a></div><br/>\n'.format(os.path.split(self.new_file)[1])

##        html += footer
##        self.write_html(self.metadata_pth, html)
        return html


    def make_search_options_cell(self, dic):
        """Make the contents of a search options cell
        in the metadata table"""

        order_list = [
                      ("prefixes: ", ["simpleSearch", "prefixes", "prefix_masdar",
                                      "perfect_i", "prefix_article", "prefix_preposition",
                                      "prefix_personal", "prefix_future", "prefix_lila",
                                      "prefix_conjunction", "prefix_interr"]),
                      ("suffixes:", ["suffixes", "suffix_nisba", "suffix_case",
                                     "suffix_verb_infl", "suffix_pronom"]),
                      ("other options:", ["alif_option", "ta_marb_option",
                                          "alif_maqs_option"])
                      ]
        
        cell_html = ''
        for tup in order_list:
            list_html = ''
            for k in dic:    
                if k in tup[1]:
                    if dic[k]:
                        list_html += '    <li>{}</li>'.format(dic[k])
            if list_html:
                cell_html += tup[0] + '\n'
                cell_html += '  <ul>\n'
                cell_html += list_html
                cell_html += '  </ul>\n'
        return cell_html


    def make_dir(self, pref, suf):
        """Make a directory (if it does not exist yet)"""
        pth = os.path.join(pref, suf)
        if not os.path.exists(pth):
            os.mkdir(pth)
        return pth

    def write_html(self, pth, html):
        with open(pth, mode="w", encoding="utf-8") as outfile:
            outfile.write(html)
                


##################################
#          HIGHLIGHTER


        
        

class Highlighter(Load_variables):

    def make_random_color(self):
        """Creates a random color taking random hexadecimal values from 6 to D
        (not too dark, not too clear).
        NB: 0x is the prefix to write numbers in base-16 in C-based languages"""
        
        color = "#"
        for number in range(6):
            color += "%01x" % random.randint(6, 0xD)
        return color



    def colorpicker(self, dic):
        """Let the user pick the colour of her choice for the current checklist"""
        
        if dic["checklist_name"] is not None:
            head, tail = os.path.split(dic["checklist_name"])
            title_text = "Choose your color for checklist: %s" % tail
        else:
            title_text = "Choose your color for search term(s) %s: " % "-".join(dic["words"])
            
        self.color = askcolor(title = title_text)
        try:
            return str(self.color[1])
        except:
            print("***************************************")
            print("     User canceled color selection")
            print("Please click the Highlight button again")
            print("***************************************")

        


    def attribute_colors(self, AND_OR_dics):
        """Attribute colors and hidden signs to every set of search words.
        NOT words don't get colors and hidden signs;
        OR words get the same colors/hidden signs as the previous AND set
        Returns:
        * regexesPerColor: a dictionary that contains the following pairs
            - key: color (an html color code)
            - value: a list containing the following elements:
                0. a list of the regular expressions that should be highlighted in this color
                1. the name of the checklist (if any; otherwise: None)
                2. a list of the original words that form the basis of the regular expressions
                3. the hidden sign that will be attributed to this batch of words
        * regexes: a dictionary that contains the following pairs:
            - key: regex (a regular expression that should be highlighted)
            - value: a list containing the following elements:
                0. the color this regex should be highlighted in
                1. the name of the checklist the regex belongs to (if any; otherwise: None)
                2. the hidden sign that will be attributed to this regex
        """
        

        regexesPerColor = {}
        regexes = {}

        e=0
        for i, dic in enumerate(self.variables.search_values):
            if i != 0:
                if dic["and_or_not"] == "AND":
                    e+=1                
            words_regex = dic["words_regex"]
            hidden_sign = hidden_signs[e]
            
            if dic["and_or_not"] == "NOT":
                color = "--"
                hidden_sign = "--"
            else:
                # if the user indicated she wanted to choose the colours herself,
                # open the colorpicker and use the user-selected colours:

                if jedli_global.custom_colors == 1:
                    color = self.colorpicker(dic)
                    if not color:
                        return

                #if not, use the Jedli default colours:

                else: 
                    if e < len(default_colors):
                        color = default_colors[e]
                    else:
                        color = self.make_random_color()
            

            regexesPerColor[color] = [words_regex,
                                      dic["checklist_name"],
                                      dic["words"],
                                      hidden_sign
                                      ]
            for regex in words_regex:
                regexes[regex] = [color,
                                  dic["checklist_name"],
                                  hidden_sign
                                  ]
            self.variables.search_values[i]["color"] = color
            self.variables.search_values[i]["hidden_sign"] = hidden_sign
            

        return regexesPerColor, regexes
                        

    def prepare_text(self, source_pth):
        """open the text file, remove the noise
        and replace the line breaks with html line breaks"""
        
        with open(source_pth, mode="r", encoding="utf-8") as file:
            text = file.read()
            text = deNoise(text)
            text = re.sub("\n", "<br/>", text)
            text = re.sub("(<br/>){3}", "<br/>", text)
        return text


    def highlighter(self):
        """Main function of this class:
        highlight the relevant words in each of the texts.
        Every set of words is highlighted in a specific colour.
        Default colours can be used,
        or users can define their own colour scheme"""

        
        

        # attribute colours and hidden signs to every set of search terms:

        regexesPerColor, regexes = self.attribute_colors(self.AND_OR_dics)
        if regexesPerColor == None:
            return


        # START HIGHLIGHTING:

        for source in self.sources:

            # define the variables for the current source:
            
            self.start = time.time()
            
            source_author = source[0]
            
            source_name = source[1]
            print("Currently highlighting %s..." % source_name)
            short_source_name = self.shorten_name(source_name)
            source_fn = "{}_{}_highlighted.html".format(source_author, short_source_name)
            source_fn = re.sub("\s+", "_", source_fn)
            new_file = os.path.join(self.output_folder, source_fn)
            graph_pth = re.sub("\.html", "_chronoplot.html", new_file)
            graph_link = '<p class="ltr-text">Click <a href="{}">here</a> for a graph representing the distribution of the search words in the text</p>\n'.format(graph_pth)
            self.current_source = "".format(source_author, short_source_name)

            text = self.prepare_text(source[2])
            
            html_intro = '<div id="intro"> Jedli Highlighter:<br/>\n'
            html_intro += '  <h1>%s - %s</h1>\n' % (source_author, source_name)
            html_intro += '</div>\n'

            metadata = self.make_metadata()

            self.highlight_repl_no = 0
            self.highlight_dic ={}


            # temporarily replace the NOT words in the text with a code ###REPL\d+###
            
            if self.NOT_words_regex != []:
                text = self.replace_NOT_words(self.NOT_words_regex, text)


            # highlight every search word in the current source in its designated colour:
            # (making sure the longest regexes are treated first)

            for word_regex in sorted(regexes.keys(), key=len, reverse=True): 
                self.colorcode = regexes[word_regex][0]
                self.hidden_sign = regexes[word_regex][2]
                self.current_word_regex = word_regex
##                colorcode = regexes[word_regex][0]
##                hidden_sign = regexes[word_regex][2]
                word_regex = r"(%s)" % word_regex
##                text = re.sub(word_regex, '<span style="background-color: %s">' % colorcode
##                              +r'\1'+'</span><span class=hidden>%s</span>' % hidden_sign, text)
                text = self.highlight_word(word_regex, text)

            print("Timer: %s seconds" % (time.time()-self.start))


            # put the NOT words back into the text:

            if self.NOT_words_regex != []:
                text = self.replace_back(text)
            

            # write the highlighted text html file:
            
            with open(new_file, mode="w", encoding="UTF-8") as file:
                file.write(header+html_intro+text+graph_link+metadata+footer)


            # open the highlighted text in the browser:

            print("Your file is now opening in your browser")
            webbrowser.open(new_file)


            # make the chronoplot graph:

            plot_html = self.make_chronoplot(text, new_file)
            self.write_html(graph_pth, "<html>\n{}\n</html>".format(plot_html))


    def keep_track_of_highlights(self, matchobj):
        """give the string matched by the regex a number,
        and store it in the self.NOT_repl_dic, so we can put the string back
        into the text later. Return the temporary replacement code repl"""
##            print(matchobj.group())
        self.highlight_dic[self.highlight_repl_no] = self.current_word_regex
        repl = '<span style="background-color: %s">' % self.colorcode
        repl += matchobj.group(0)
        repl += '<a name="{}"></a>'.format(self.highlight_repl_no)
        repl += '</span><span class=hidden>%s</span>' % self.hidden_sign
        self.highlight_repl_no += 1
        return repl  


    def highlight_word(self, word_regex, text):
        return re.sub(word_regex, self.keep_track_of_highlights, text)



    def make_empty_indices_dic(self, text):
        """make an empty dictionary:
            * keys: set of search words (string)
            * values: a dictionary:
                * "words_regex": a list of the corresponding regexes
                * "list_indices": a list of tuples that mark the location of
                                  attestations of these search regexes in the text"""
        indices_dic = {}
        words = []
        words_regex = []
        for i, dic in enumerate(self.variables.search_values):
            if dic["and_or_not"] != "NOT":
                if dic["and_or_not"] != "OR":
                    if words_regex:
                        words = "-".join(words)
                        indices_dic[words] = {}
                        indices_dic[words]["words_regex"] = words_regex
                        indices_dic[words]["list_indices"] = []
                        indices_dic[words]["list_links"] = []
                        words_regex = []
                        words = []
                words += dic["words"]
                words_regex = dic["words_regex"]
        if words_regex:
            words = "-".join(words)
            indices_dic[words] = {}
            indices_dic[words]["words_regex"] = words_regex
            indices_dic[words]["list_indices"] = []
            indices_dic[words]["list_links"] = []
        return indices_dic

    def make_chronoplot(self, text, new_file):
        """prepare the data for the chronoplot"""

        indices_dic = self.make_empty_indices_dic(text)
        text_len = len(text)

        
        regex = r'<a name="(\d+)"></a>'
        for m in re.finditer(regex, text):
            no = int(m.group(1))
            word_regex = self.highlight_dic[no]
            for words in indices_dic:
                if word_regex in indices_dic[words]["words_regex"]:
                    indices_dic[words]["list_indices"].append(m.span())
                    indices_dic[words]["list_links"].append("""<a href="%s#%s"></a>""" %(new_file, no))
                    break
                    
        import chronoplot
        plot_html = chronoplot.chronoplot(text_len, indices_dic, self.graph_pth)
        return plot_html

    
##    def make_chronoplot(self, text):
##        """prepare the data for the chronoplot"""
##        indices_dic = {}
##        list_indices = []
##        words = ""
##        text_len = len(text)
##        for i, dic in enumerate(self.variables.search_values):
##            if dic["and_or_not"] != "NOT":
##                if dic["and_or_not"] != "OR":
##                    if list_indices:
##                        indices_dic[words] = list_indices
##                    list_indices = []
##                    words = ""
##                words = "-".join([words, ] + dic["words"])
##                ##### this doesn't work because the regexes is not the same as dic["words_regex"]
##                for word_regex in sorted(dic["words_regex"].keys(), key=len, reverse=True):
####                for word_regex in dic["words_regex"]:
##                    indices = [m.span() for m in re.finditer(word_regex, text)]
##                    list_indices += indices
##        if list_indices:
##            indices_dic[words] = list_indices
##        import chronoplot
##        plot_html = chronoplot.chronoplot(text_len, indices_dic, self.graph_pth)
##        return plot_html

    def shorten_name(self, name):
        """Shorten the source name for use in the filename"""
        try: 
            return "_".join(name.split()[:2])
        except IndexError:
            return name


##    def make_highlighter_metadata(self):
##
##        html += '<div id="source_table">\n'
##        html += '  <table>\n'
##
##        # make table header row:
##        html+= '    <tr>\n'
####        html+= '      <th>operator</th>\n'
##        html+= '      <th>search word(s)</th>\n'
##        html+= '      <th>checklist name</th>\n'
##        html+= '      <th>search options</th>\n'
##        if jedli_global.show_regex:
##            html+= '      <th>regex used</th>\n'
##        html+= '      <th>hidden tag</th>\n'
##        html+= '      <th>highlight colour</th>\n'
##        html+= '    </tr>\n'
##
##        # fill the table:         
##        for i, dic in enumerate(self.variables.search_values):
##            html+= '    <tr>\n'
##            if i > 0:
##                html+= '      <td style="text-align:left">{}</td>\n'.format(dic["and_or_not"])
##            else:
##                html+= '      <td style="text-align:left">-</td>\n'
##            html+= '      <td>{}</td>\n'.format("<br/>".join(dic["words"]))
##            if dic["checklist_name"]:
##                print(checklist)
##                html+= '      <td style="text-align:left">{}</td>\n'.format(dic["checklist_name"])
##            else:
##                html+= '      <td>--</td>\n'
##            html+= '      <td style="text-align:left">{}</td>\n'.format(self.make_search_options_cell(dic))
##            if jedli_global.show_regex:
##                html+= '      <td>{}</td>\n'.format("<br/>".join(dic["words_regex"]))
##            html+= '    </tr>\n'
##        html += '  </table>\n'
##        html += '</div>\n<br/>\n'
##
##        html += '<p class="ltr-text">Search date: {}</p>'.format(time.asctime( time.localtime(time.time()) ))
##
####        html += '  Click <a href="{}">here</a> for an overview of all sources searched<br/>\n'.format(self.table_pth)
####        html += '</div>'
####        html += '<div id="top"><a href="..\{}">back to overview</a></div><br/>\n'.format(os.path.split(self.new_file)[1])
##
####        html += footer
####        self.write_html(self.metadata_pth, html)
##        return html
        




#################################
#        CONTEXT SEARCH




class ContextSearch(Load_variables):


    def AND_search(self, AND_words_list, AND_words_regex_list, input_result):
        """return a list of the AND_words that were found in the input_result context"""
        
        hits = []
        for f, word in enumerate(AND_words_list):
            regex = AND_words_regex_list[f]
            if re.findall(regex, input_result):
                hits.append((word, regex))
        return hits


    def getContext(self, index_tuple, context_tup, text, text_length):
        """get a substring from the text, dependent on:
        * index_tuple: the start and end point of the regex match in the text
        * context: the number of charachters the desired substring should have
        * text: the full string from which the substring should be extracted
        * text_length: the number of characters in the text string"""
        
        if len(context_tup) == 1:
            context_before = context_tup[0]
            context_after = context_tup[0]
        else:
            context_before = context_tup[0]
            context_after = context_tup[1]
        if index_tuple[0] < context_before:
            a = text[0:index_tuple[1]+context_after]
        elif index_tuple[1] > text_length - context_after:
            a = text[index_tuple[0]-context_before:]
        else:
            a = text[index_tuple[0]-context_before:index_tuple[1]+context_after]
        # Trim off the partial words at the beginning and end of the search result:
        if a.count(" ") > 2:
            while a[0] != " ":
                a = a[1:]
            while a[-1] != " ":                
                a = a[:-1]
        return a

    def output_or_not(self, array_or_string):
        """Check if an array or string is empty,
        and if the user indicates she wants to have
        empty result sets in the output"""
        
        outputThis = True
        if len(array_or_string) == 0:
            if jedli_global.verbose == False:
                outputThis = False
        return outputThis



    def del_keys(self, input_dic, key_list):
        """deletes all keys in the key_list from a dictionary.
        Recursively goes through nested dictionaries"""
        copy_dic = input_dic.copy()
        for key in copy_dic.keys(): #Used as iterator to avoid the 'DictionaryHasChanged' error
            if key in key_list:
                del input_dic[key]
            else:
                if isinstance(copy_dic[key], dict):
                    self.del_keys(input_dic[key], key_list)
        return input_dic

    def json_dump_results(self, fp, results_dic):
        """dump the results as a json file for use in the datecount function.
        The dumped dictionary is a copy of the results_dic, from which
        the html-formatted results and the total number of results are removed"""
        
        result_count = self.del_keys(copy.deepcopy(results_dic), ["total", "html"])    
        with open(fp, mode="w", encoding="UTF-8") as file:
            json.dump(result_count, file)


    def make_source_ref(self, source_id, source_name):
        """make a link to the full text web page for the current source"""
        
        if "WARAQ" in source_id:
            waraq_id = int(re.findall(r"\d+", source_id)[0])
            source_ref = waraqbook.format(waraq_id, source_name)
        else:
            source_ref = shamelabook.format(source_id, source_name)
        return source_ref


    def formatResults(self, context, search_results, words_regex, AND_words_regex):
        """Add the page number, formatting and highlighting to the search result"""
        
        # Combine page numbers and results:

        outcomes = ""
        previous_source = 0
        for page_number, result, index_tuple, hits, source_id in search_results:
            source_name = self.sources_dic[source_id]["source_name"]
            author = self.sources_dic[source_id]["author"]
            source_ref = self.make_source_ref(source_id, source_name)
            if source_id != previous_source:
                outcomes += '<a name="{}"></a>'.format(source_id)
                previous_source = source_id
            outcomes += "  <h1>{} - {} : {}\n  </h1>\n".format(author, source_ref, page_number)
            if context != 0:
                outcomes += "  <h1>{}\n  </h1><br/>\n".format(result)

        # highlight the search words:

        outcomes = self.highlight_results(outcomes, words_regex, AND_words_regex)
        
        # do some final formatting of the whitespace:
        
        outcomes = re.sub(r"\n+\W+\n+", "</br>", outcomes)
        outcomes = re.sub(r"\s{8,}", " ", outcomes)
        return outcomes


    def highlight_results(self, outcomes, words_regex, AND_words_regex):
        """highlight the search terms in the results"""
        
        # first, highlight the AND_words (if any):
        
        e = 1
        for regex_list in AND_words_regex:
            for regex in regex_list:
                head = '<span style="background-color: {}">'.format(default_colors[e])
                tail = '</span><span class=hidden>{}</span>'.format(hidden_signs[e])
                outcomes = re.sub(r"(%s)" % regex, head+r'\1'+tail, outcomes)
            e+=1

        # then, highlight the main search word(s): 
        for regex in words_regex:
            head = '<span style="background-color: #FFFF00">'
            tail = '</span><span class=hidden>$a</span>'
            outcomes = re.sub(r"(%s)" % regex, head+r'\1'+tail, outcomes)
        return outcomes


    def format_final_indexfile(self):
        """rearrange the results, sorted per search word, not per source"""
        
        final_outcomes = ''
        for word_regex, source_dic in sorted(self.results_dic.items(), key=lambda item: item[1]["word"]):
            word = self.results_dic[word_regex]["word"]
            final_outcomes += '''<div id="intro">Index for the word %s\n</div>\n''' % (word)
            final_outcomes += '''<div id="index">\n''' 
            if jedli_global.verbose:
                final_outcomes += '''  <p class="ltr-text">You have searched with this regex:
                                    %s\n  </p>\n''' % (word_regex)
            total_count = 0
            for element in sorted(self.sources, key=itemgetter(3)): # order the sources by date
                source_name = element[1]
                source = element[2]
                source_id = os.path.splitext(os.path.basename(element[2]))[0]
                try:
                    final_outcomes += '<br/><br/><br/>\n'.join(source_dic["sources"][source_id]["html"])
                except:
                    if jedli_global.verbose:
                        print("No results for {} in text no. {}".format(word, source_id))
                try:
                    total_count += self.results_dic[word_regex]["sources"][source_id]["results_count"]
                except:
                    if jedli_global.verbose:
                        print("No results for {} in {}".format(word, source_id))
            final_outcomes += '<br/><br/>\n  <p class="ltr-text">The Indexer found \
                                  {} results in total for the word {}'.format(total_count, word)
            if jedli_global.verbose:
                final_outcomes += 'using search term {}\n  </p>\n'.format(word_regex)
            final_outcomes+= '\n</div><br/><br/><br/>\n'
            self.results_dic[word_regex]["total"] = total_count
        return final_outcomes


    def make_source_table_header(self, current_results):
        """Make the header of the sources table"""
        table_header = '    <tr>\n'
        table_header+= '      <th>Source_id</th>\n'
        table_header+= '      <th>Source_name</th>\n'
        table_header+= '      <th>Author</th>\n'
        if jedli_global.include_len_in_table:
            table_header+= '      <th>Number of characters</th>\n'
        table_header+= '      <th>Date AH</th>\n'
        for word in sorted(current_results):
            table_header += '      <th>{}</th>\n'.format(word)
        table_header += '   </tr>\n'
        return table_header


    def make_source_table_body(self, sources_dic):
        """make the source table body"""
        table_body = ""
        for source_id, source_dic in sorted(sources_dic.items(), key=lambda item: item[1]["source_date"]):
            
            try:
                source_date = int(source_dic["source_date"])
                if  source_date > 3000:
                    source_date = "(no date)"
            except:
                source_date = "(no date)"
                
            table_body += '    <tr>\n'
            table_body += '      <td>{}</td>\n'.format(source_id)
            table_body += '      <td>{}</td>\n'.format(source_dic["source_name"])
            table_body += '      <td>{}</td>\n'.format(source_dic["author"])
            if jedli_global.include_len_in_table:
                table_body+= '      <td>{}</td>\n'.format(source_dic["len"])
            table_body += '      <td>{}</td>\n'.format(source_date)
            for word, word_dic in sorted(source_dic["results"].items()):
                no_of_results = word_dic["number_of_results"]
                first_result_page = word_dic["first_result_page"]
                if first_result_page:
                    # add a link to the file that contains the first result of this source:
                    fp = "{}_{}_{}.html#{}".format(self.base_filename, word,
                                                   first_result_page, source_id)
                    table_body += '      <td><a href="{}">{}</a></td>\n'.format(fp, no_of_results)
                else:
                    table_body += '      <td>{}</td>\n'.format(no_of_results)
            table_body += '    </tr>\n'
        return table_body


    def make_source_table_totals(self, current_results):
        """make the last line of the source table, containing the totals"""
        totals_row =  '    <tr>\n'
        totals_row += '      <td></td>\n'
        totals_row += '      <td></td>\n'
        totals_row += '      <td></td>\n'
        if jedli_global.include_len_in_table:
            totals_row += '      <td></td>\n'
        totals_row += '      <td>TOTALS:</td>\n'
        for word, dic in sorted(current_results.items()):
            totals_row += '      <td>{}</td>\n'.format(dic["total_results_count"])
        totals_row += '    </tr>\n'
        return totals_row


    def output_source_table(self, sources_dic, current_results):
        """make a html table that contains an overview of all the results"""

        # make the intro matter:
        sources_html = '<a name="results-overview"></a>'
        sources_html+= '<div id="intro">List of all sources searched: \n</div>\n'
        overview_link = '<div id="top"><a href="..\{}">back to overview</a></div><br/>\n'.format(os.path.split(self.new_file)[1])
        graph_link = '<div id="top">Click <a href="{}">here</a> for a graph of the results</div>\n'.format(self.graph_pth)
        sources_html+= overview_link
        sources_html+= graph_link + '<br/>'

        # make the table:
        sources_html+= '<div id="source_table">\n'
        sources_html+= '  <table>\n'
        table_header = self.make_source_table_header(current_results)
        table_body = self.make_source_table_body(sources_dic)
        totals_row = self.make_source_table_totals(current_results)
        if len(sources_dic) < 15:
            sources_html += table_header + table_body + totals_row
        else: # repeat the totals_row at the beginning of the table
            sources_html += table_header + totals_row + table_body + totals_row
        sources_html += '  </table>\n'
        sources_html += '</div>\n<br/>\n'

        # add the outro matter:
        sources_html+= graph_link
        sources_html += overview_link
        
        return sources_html


    def make_range(self, first, current, last,
                   extra=1, before=5, after=5, max_no=20):
        """Make a range of the result pages.
        If there are more pages than max_no, get the range
        from x before and y after the current page number;
        making sure that the range does not go below 0
        and not higher than the last page number.
        Since range does not include the final number,
        an extra can be added if necessary"""
        if last < max_no:
            return range(first, last+extra)
        else:
            if current-first < before:
                return range(first, current+after+extra)
            elif last-current < after:
                return range(current-before, last+extra)
            else:
                return range(current-before, current+after+extra)
            
        
    
    def make_result_page_links(self, current_results, word, current_page, last_page,
                               final=False, pagetype=None, before=5, after=5, max_no=20):
        """make the links that refer from the overview page to the results pages"""

        if last_page > 0: # if there are any results:
            link_dummy = '<a href="{}_{}_{}.html">{}</a> '
            if not pagetype: # if temporary result: current page number should not get a link
                myrange = self.make_range(1, current_page, last_page, extra=0)
            elif pagetype == "final_results":
                myrange = self.make_range(1, current_page, last_page, extra=1)
            elif pagetype == "overview":
                myrange = range(1, last_page+1)
                link_dummy = '<a href="data/{}_{}_{}.html">{}</a> '

            # add the 'first page' and 'previous page' links
            # (only for results files, not for overview files)
            if pagetype != "overview":
                page_links = '<div id="top"> '
                if last_page > max_no:
                    page_links += '<a href="{}_{}_{}.html">first page</a> '.format(self.base_filename,
                                                                                      word, 1)
                if current_page > 1:
                    page_links += '<a href="{}_{}_{}.html">previous page</a> '.format(self.base_filename,
                                                                                      word, current_page-1)
                if last_page > max_no:
                    if current_page > before:
                        page_links += '... '
            else:
                page_links = ''
                
            # add links for every page in myrange:
            for x in myrange:
                page_link = link_dummy.format(self.base_filename, word, x, x)
                page_links += page_link

            # add current page number without a link for non-final result pages
            if not pagetype: 
                page_links += str(current_page) 

            # add the 'next page' and 'last page' links
            # (only for results files, not for overview files)
            if pagetype != "overview":
                if last_page > max_no:
                    if last_page-current_page > after:
                        page_links += '... '

                if not final:
                    page_links += ' <a href="{}_{}_{}.html">next page</a>'.format(self.base_filename,
                                                                                  word, current_page+1)
                else:
                    if last_page != current_page:
                        page_links += ' <a href="{}_{}_{}.html">next page</a>'.format(self.base_filename,
                                                                                      word, current_page+1)                        
                if final:
                    if last_page > max_no:
                        if last_page != current_page: 
                            page_links += ' <a href="{}_{}_{}.html">last page</a> '.format(self.base_filename,
                                                                                          word, last_page) 
        else:
            if final:
                page_links = ' no results found\n'
            else:
                page_links = ' no results found yet\n'
       
        if pagetype != "overview":
            page_links += '</div>\n'

        return page_links
    

    def make_overview_page(self, current_results, final=False):
        """make the outline of the overview page"""
        html = header
        html += '<div id="intro">Jedli Context Search results</div>\n'
        for word in current_results:
            current_page = current_results[word]["current_page"]
            #html += '<p>{}: {}</p>\n'.format(word, self.make_result_page_links(current_results, word, pagetype="overview", final=final))
            page_links = self.make_result_page_links(current_results, word, current_page,
                                                     current_page, final, pagetype="overview")
            html += '<p>{}: {}</p>\n'.format(word, page_links)

        if not final:
            html += '\n<div id="top">This is a temporary page, created while Jedli is searching.'
            html += '   Press F5 to update the results</div>\n'

        if final:
            self.metadata = self.make_metadata(final)
        html += self.metadata

        html += footer
        self.write_html(self.new_file, html)


    def make_temp_result_page(self, word, current_page, page_links):
        """Make an empty page that is the target of the "next page" link
        on the current results page. This page has to be deleted if it does
        not contain results after Jedli finished the search"""
        html = header
        html += '<div id="intro">Jedli Context Search results for the word {}</div>\n'.format(word)
        html += '<a name="page_links_top">{}\n</a><br/>\n'.format(page_links)
        html += '\n<div id="top">This is a temporary page, created while Jedli is searching.'
        html += '   Press F5 to update the results</div>\n'
        html += footer
        pth = os.path.join(self.data_dir, "{}_{}_{}.html".format(self.base_filename, word, current_page+1))
        self.write_html(pth, html)

    def remove_temp_page(self, word, last_page):
        """remove the empty temp pages that were created
        as target of the "next page" links on every current results page"""
        to_be_removed_fn = self.base_filename+"_{}_{}.html".format(word, last_page+1)
        to_be_removed_fp = os.path.join(self.data_dir, to_be_removed_fn)
        try:
            os.remove(to_be_removed_fp)
        except:
##            print("file path not found:", to_be_removed_fp)
            pass
        
        
    def output_result_page(self, current_results, word, current_page,
                           final=False, pagetype=None, last_page=0):
        """make the html page for a section of the results"""
           
        overview_link = '<div id="top"><a href="..\{}">back to overview</a></div><br/>\n'.format(os.path.split(self.new_file)[1])
        
        page_links = self.make_result_page_links(current_results, word, current_page,
                                                 last_page, final, pagetype)

        # make a temp file that is the target for the "next" link in the page
        if not final:
            self.make_temp_result_page(word, current_page, page_links + '</div>\n')

        # format the current results:
        results_string = self.formatResults(jedli_global.output_context_chars,
                                            current_results[word]["results"],
                                            self.words_regex, self.AND_words_regex)
        if self.NOT_words_regex != []:
           results_string = self.replace_back(results_string)
        
        # build the html:
        html = header
        html += '<div id="intro">Jedli Context Search results for the word {}</div>\n'.format(word)
        html += overview_link
        html += '<a name="page_links_top">{}\n</a><br/>\n'.format(page_links)
        html += '<div id="index">\n'
        html += results_string
        html += '\n</div>\n'
        html += '<a name="page_links_bottom">{}\n</a>'.format(page_links)
        html += overview_link
        html += footer
        
        # write the html file:
        pth = os.path.join(self.data_dir, "{}_{}_{}.html".format(self.base_filename, word, current_page))
        self.write_html(pth, html)


    def finalize_page_refs(self, current_results, final=True):
        """After the last results have been written to the results files,
        add the page links to all pages to the result files"""
        for word in current_results:
            last_page = current_results[word]["current_page"]
            self.remove_temp_page(word, last_page)
##            self.remove_temp_page(word, -1) # remove a 0 page, if one was made
            for x in range(1, last_page+1):
                fn = self.base_filename+"_{}_{}.html".format(word, x)
                current_file = os.path.join(self.data_dir, fn)
                with open(current_file, mode="r", encoding="utf-8") as f:
                    html = f.read()

                    new_links = self.make_result_page_links(current_results, word, x,
                                                       last_page, final, pagetype="final_results")

                    # remove the link to the current page
                    current_p = r'<a href="{}">{}</a>'.format(fn, x)
                    #new_links = re.sub(current_p, str(x), new_links)
                    new_links = new_links.replace(current_p, str(x))
                    
                    html = re.sub('(<a name="page_links_\w+">).+', r'\1 {}</div>\n'.format(new_links), html)
                with open(current_file, mode="w", encoding="utf-8") as f:
                    f.write(html)
        
        
    





    def contextSearch(self):
        print("Conducting the context search...")

        # INITIALIZE CONTEXT SEARCH VARIABLES:

##        v = Load_variables(variables)
##        ####v.define_context(jedli_global.context_context)
##        v.results_dic = {}
##        v.sources_dic = {}

##        self.make_output_paths()
        self.metadata = self.make_metadata()


        # CONDUCT THE CONTEXT SEARCH:

        # loop through the selected sources:
        
        source_counter=0
##        print(variables.sources[0])
        current_results = {word: {"results" : [],
                                  "results_count" : 0,
                                  "current_page" : 0,
                                  "total_results_count" : 0
                                  } for word in self.words}
        for element in sorted(self.sources, key=itemgetter(3)): # sort sources by date
            
            # initialize the variables for the current source:
            
            to_do = len(self.sources) - source_counter
##            print("%s sources to go..." % to_do)
            all_results=[]
            author = element[0]
            source_name = element[1]
            source = element[2]
            source_id = os.path.splitext(os.path.basename(element[2]))[0]
            source_date = element[3]

            print("Now indexing text no {} - {}...".format(source_id, source_name))
##            print("Currently processing %s in %s..." % (self.words[0], os.path.basename(source)))
            if source_counter%10 == 0:
                print("{} source(s) to go".format(to_do))

            with open(source, mode="r", encoding="utf-8") as source_file:
                text = source_file.read()
                text = deNoise(text)
            L = len(text)
            all_page_numbers = re.findall(page_regex, text)

            self.sources_dic[source_id] = {}
            self.sources_dic[source_id]["source_name"] = source_name
            self.sources_dic[source_id]["author"] = author
            self.sources_dic[source_id]["source_date"] = source_date
            self.sources_dic[source_id]["len"] = L
            self.sources_dic[source_id]["results"] = {}
            


            # replace the NOT words in the text with a temporary code:

            if self.NOT_words_regex != []:
                text = self.replace_NOT_words(self.NOT_words_regex, text)
                    

            # loop through the first set of search words:

            word_counter=0            
            for word in self.words: 
                
                # initialize the variables for the current search word:
                
                word_regex = self.words_regex[word_counter]
                result_counter = 0
                incl_NOT_words = 0
                self.sources_dic[source_id]["results"][word] = {}
                self.sources_dic[source_id]["results"][word]["first_result_page"] = None
                                
                if jedli_global.one_output_file:
                    if word_regex not in self.results_dic:
                        self.results_dic[word_regex] = {}
                        self.results_dic[word_regex]["word"] = word
                        self.results_dic[word_regex]["sources"] = {}

                    word_intro = '<div id="intro">%s for the word %s\n</div>\n' % (self.index_type, word) 
                    word_intro += '<div id="index">\n'
                    if jedli_global.verbose:
                        word_intro += '  <p class="ltr-text">You have searched \
                                       with this regex: %s\n  </p>\n' % (word_regex)
                
                # find all indices (locations of all attestations of the search regex in the text):

                indices = [m.span() for m in re.finditer(word_regex, text)]

                # loop through all results and search for AND_words in the user-defined context:
               

                current_outcomes = ""
                search_results = []
                for index_tuple in indices:  
                    
                    # for each result, get the words around it:
                    
                    search_context_tup = (jedli_global.search_context_chars_before, jedli_global.search_context_chars_after)
                    search_context = self.getContext(index_tuple, search_context_tup, text, L)
                    output_context = self.getContext(index_tuple, [jedli_global.output_context_chars, ], text, L)
                    output_context = output_context.replace(search_context,
                                                            "<strong>{}</strong>".format(search_context))

                    # Conduct Context Search (if it applies)
                    
                    include_in_index = True
                    all_hits = []
                    hits = []
                    if self.index_type == "Context Search":
                        
                        if "###REPL" in search_context: # remove the results that had any of the NOT words in them
##                            print("###REPL")
                            include_in_index = False
                            incl_NOT_words += 1
                        else:
                            # check for every set of AND_words if at least one AND_word appears in the set: 
                            for AND_index, AND_list in enumerate(self.AND_words):
                                hits = self.AND_search(AND_list,
                                                        self.AND_words_regex[AND_index],
                                                        search_context)

                                # remove from the results if one of the AND_lists does not produce results
                                if hits: 
                                    all_hits.append(hits)
                                else:
                                    include_in_index = False
                                    break

                    if include_in_index:
                        # find the page number for the current search result:
                        page_number = self.get_page_number(text, index_tuple, page_regex)
                        page_number = self.link_page_number(page_number, source_id, all_page_numbers)

                        # store the results:
                        ####result = [page_number, a, index_tuple, all_hits]
                        result = [page_number, output_context, index_tuple, all_hits, source_id]
                        current_results[word]["results_count"] = current_results[word]["results_count"]+1
                        current_results[word]["total_results_count"] = current_results[word]["total_results_count"]+1
                        if jedli_global.one_output_file:
                            search_results.append(result)
                        else:
                            current_results[word]["results"].append(result)


                            # output if this is the first result for a word,
                            # or if the number of results per page has been reached
                            if current_results[word]["current_page"] == 0:
                                # if these are the first results for this search word, open the temp page 1
                                current_results[word]["current_page"] = 1
                                self.output_result_page(current_results, word,
                                                        current_results[word]["current_page"])
                                self.make_overview_page(current_results)
                                
                            elif current_results[word]["results_count"] == jedli_global.results_per_page:
                                self.output_result_page(current_results, word,
                                                        current_results[word]["current_page"],
                                                        last_page=current_results[word]["current_page"])
                                self.make_overview_page(current_results)
                                if not self.sources_dic[source_id]["results"][word]["first_result_page"]:
                                    self.sources_dic[source_id]["results"][word]["first_result_page"] = current_results[word]["current_page"]
                                # reset the variables: 
                                current_results[word]["results_count"] = 0
                                current_results[word]["results"] = []
                                current_results[word]["current_page"] = current_results[word]["current_page"]+1
                            if not self.sources_dic[source_id]["results"][word]["first_result_page"]:
                                self.sources_dic[source_id]["results"][word]["first_result_page"] = current_results[word]["current_page"]                             
                        result_counter += 1

                if self.output_or_not(search_results):

                    # make a link to the full text web page for the current source:
                    
                    source_ref = self.make_source_ref(source_id, source_name)


                    # write the number of results for this word in this source:
                    
                    if jedli_global.one_output_file:
                        current_outcomes += '<br/><br/>\n  <p class="ltr-text">The Indexer found %s results \
                                         for the word %s in\n  </p>\n' % (len(indices), word)
                        current_outcomes += '  <h1>%s - %s\n  </h1>\n' % (author, source_ref)
                        if self.index_type == "Context Search":
                            if self.NOT_words: 
                                current_outcomes += '  <p class=ltr-text>Of these, %s were disqualified because an unwanted word \
                                                     was found in the context.\n  </p>\n' % (incl_NOT_words)
                                current_outcomes += '  <p class=ltr-text>Of the remaining results, %s were found \
                                                     in the desired context:\n  </p><br/><br/>\n' % len(search_results)
                            else:
                                current_outcomes += '  <p class=ltr-text>Of these, %s were found \
                                                     in the desired context:\n  </p><br/><br/>\n' % len(search_results)
                            

                        # format the results (highlighting, title formatting):

                            current_outcomes += self.formatResults(jedli_global.output_context_chars,
                                                                   search_results,
                                                                   self.words_regex, self.AND_words_regex)

                        # put the NOT words back into the result text: 

                        if self.NOT_words_regex != []:
                            if jedli_global.one_output_file:
                                current_outcomes = self.replace_back(current_outcomes)
                                


                        # add the results for this source to the html string for temp output:
                        
                        self.final_outcomes+= word_intro+current_outcomes+"\n"


                        # add the results to the results_dic (for the eventual final output): 
                        
                        if source_id not in self.results_dic[word_regex]["sources"]:
                            self.results_dic[word_regex]["sources"][source_id] = {}
                        else:
                            print("SOURCE ALREADY IN results_dic[word_regex]!!")
                        self.results_dic[word_regex]["sources"][source_id]["date"] = source_date
                        self.results_dic[word_regex]["sources"][source_id]["source_name"] = source_name
                        self.results_dic[word_regex]["sources"][source_id]["author"] = author
                        self.results_dic[word_regex]["sources"][source_id]["html"] = []
                        self.results_dic[word_regex]["sources"][source_id]["html"].append(current_outcomes)
                        self.results_dic[word_regex]["sources"][source_id]["results_count"] = len(search_results)
                        self.results_dic[word_regex]["sources"][source_id]["char_count"] = len(text)

                else:
                    pass
                if jedli_global.one_output_file:
                    if "</div>" not in self.final_outcomes[-10:]:
                        self.final_outcomes+= '</div>\n'

                self.sources_dic[source_id]["results"][word]["number_of_results"] = result_counter

                # update the user about the progress
                # and write the temporary results html file:
                # (after every tenth source)

                if word_counter%10 == 0:
                    if jedli_global.one_output_file:
                        with open(self.pth, mode="w", encoding="utf-8") as f:
                            temp = "This is a temporary file, created while the Indexer is still working. \
                                      Press F5 to refresh the file with the latest results"
                            f.write(header+self.final_outcomes+temp+footer)
                    else:
                        if current_results[word]["results"]:
                            self.output_result_page(current_results, word,
                                                    current_results[word]["current_page"],
                                                    last_page=current_results[word]["current_page"])
                        self.make_overview_page(current_results)

                    # open the temp file if it is not yet open:
                    
                    if source_counter == 0 and word_counter == 0:
                        if jedli_global.one_output_file:
                            webbrowser.open('file:///' + self.pth)
                        else:
                            webbrowser.open(self.new_file)
                        print("""A temporary file is now opening in your browser 
                                 while the Indexer continues working.
                                 In your browser, press F5 to refresh.
                                 The final file will open as soon as the Indexer is finished.""")
                        
                word_counter+=1


            # prepare the string for the final results html file: 
            
            if jedli_global.one_output_file:
                if "</div>" not in self.final_outcomes[-10:]:
                    self.final_outcomes+= "</div><br/><br/><br/>\n"
            
            source_counter+=1

        print("Total indexing time: %s seconds" % (time.time()-self.start))


        # write and open the final results html file:
        plot_html = '<a name="graph"></a>'
        overview_link = '<div id="top"><a href="..\{}">back to overview</a></div><br/>\n'.format(os.path.split(self.new_file)[1])
        plot_html+= overview_link

        plot_html += make_grouped_date_graph(self.sources_dic, self.json_pth,
                                             jedli_global.graph_buckets, True)
        plot_html += "\n" + make_grouped_date_graph(self.sources_dic, self.json_pth,
                                                    jedli_global.graph_buckets, False)
        plot_html+= overview_link
##        print(plot_html[:150])

        if jedli_global.one_output_file:
            final_outcomes = self.format_final_indexfile()

        table_html = self.output_source_table(self.sources_dic, current_results)

        if jedli_global.one_output_file:
    ##        if jedli_global.print_sources == True:
            final_outcomes = source_overview_link + final_outcomes

            with open(self.new_file, mode="w", encoding="UTF-8") as file:
                    file.write(header+final_outcomes+table_html+plot_html+footer)
        else:
            self.write_html(self.table_pth, header+table_html+footer)
            self.write_html(self.graph_pth, '<html>\n<body>\n'+plot_html+footer)
            for word in current_results:
                if current_results[word]["results"]:
                    self.output_result_page(current_results, word,
                                            current_results[word]["current_page"],
                                            last_page=current_results[word]["current_page"])
            self.make_overview_page(current_results, final=True)
            self.finalize_page_refs(current_results, final=True)

        webbrowser.open(self.new_file)
            
        print("The final results file is now opening in your browser")

        ###
        if jedli_global.datecount_dump:
            self.json_dump_results(self.json_pth, self.results_dic)



