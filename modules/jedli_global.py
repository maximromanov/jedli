import sys
import inspect
import os
import re
#####################
from tkinter import *

version = 1.2

# frame names etc.
root = None
frame=None
i_o_f = None
search_f = None
index_f = None
highlight_f = None
context_f = None
first_row = None
search_rows = []
sources = None

# path names:
modules_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
base_path = os.path.dirname(modules_path)
check_path = os.path.join(base_path, "checklists")
html_path = os.path.join(base_path, "search_results")
settings_path = os.path.join(base_path, "settings")
static_files = os.path.join(settings_path, "static_files")
saved_searches_path = os.path.join(settings_path, "saved_searches")
prefs_path = os.path.join(settings_path, "user_preferences")
source_sel_path = os.path.join(settings_path, "source_selections")
txt_path = os.path.join(base_path, "texts")
epub_path = os.path.join(txt_path, "epub_files")
source_info_path = os.path.join(txt_path, "source_info")
doc_path = os.path.join(base_path, "documentation")

# main screen default settings:
and_or_not_default = "AND"
sources_default = []
output_default = html_path
output_folder = output_default
default_colors_default = 0
####index_context = 0
####context_context = "8"
search_context_words_before = 8
search_context_words_after = 6
output_context_words = 30
custom_colors = 0

max_height = 0

#search options default settings:
searchregex1 = ""
searchregex2 = ""
alif_option = 0
ta_marb_option = 0
alif_maqs_option = 0
contextvar = 0
search_option = 2
word_beginning = 1
pre_comb = 1
masdar = 0
perfect_i = 0
article = 0
preposition = 0
pers_pref = 0
future = 0
lila = 0
conjunction = 0
interr = 0
word_ending = 1
suf_comb = 0
nisba = 0
case = 0
verb_infl = 0
pronom = 0
alif = 0
ta_marbuta = 0
alif_maqs = 0
ignore_interword = True
print_sources = False

simpleSearch = None
prefixes = "all possible combinations of prefixes"
prefix_masdar = None
prefix_perfect_i = None
prefix_article = None
prefix_preposition = None
prefix_personal = None
prefix_future = None
prefix_lila = None
prefix_conjunction = None
prefix_interr = None
suffixes = "no suffixes allowed"
suffix_nisba = None
suffix_case = None
suffix_verb_infl = None
suffix_pronom = None 


# output variables:
one_output_file = False # True if all the data should be in one html file only
verbose = False
include_len_in_table = True # include the number of characters in every source in the source overview table
graph_buckets = 50 # group the texts by buckets of X years in the plot
ask_output_filename = False
results_per_page = 50
show_regex = False
index_type = None

# make a json file for the datecount function?
datecount_dump = True

logger = None
##print = None # necessary ?????

def print(*args):
    try:
        to_be_printed = ""
        for x in args:
            to_be_printed += " " + str(x)
        to_be_printed = to_be_printed[1:]
        to_be_printed = re.sub(r"  +", r" ", to_be_printed)
        to_be_printed += "\n"
        logger.textf.insert(END, to_be_printed)
        logger.textf.yview(END)
        logger.top.update()
        logger.top.update_idletasks()
    except:
        pass



def rClicker(e, readonly=False):
    ''' right click context menu for all Tk Entry and Text widgets
    see https://stackoverflow.com/a/4552646/4045481
    use self.textf.bind('<Button-3>',rClicker, add='')
    to bind the right-click menu to the self.texf widget
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Copy', lambda e=e: rClick_Copy(e)),
               ]
        if not readonly:
            nclst+=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

            

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print(' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r, readonly=False):
    '''alternative to binding the rClicker to every widget separately:
    make the rClicker available to every Entry/Text/Listbox/Label widget
    see https://stackoverflow.com/a/4552646/4045481
    use rClickbinder(self.top) to make the right-click menu available
    for all widgets in self.top
    '''
    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label', 'Combobox']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=lambda e: rClicker(e, readonly), add='')
##                         func=rClicker, add='')
    except TclError:
        print(' - rClickbinder, something wrong')
        pass
