# This is the basic Jedli Indexer function without Graphical User Interface

# The first section (after the imports) contains variables that have to be filled in by the user
# The second section contains regular expressions for search options
# The third section contains the main mechanics of the function

# Comments are preceded by 1 hashtag, important user-defined variables by 3

import re
from core_mining_functions import deNoise
import os
from os import listdir
import os.path
from os.path import join, isfile 
import time
import inspect
modules_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
base_path = os.path.dirname(modules_path)

txt_path = join(base_path, 'texts')
html_path = join(base_path, 'html_files')
check_path = join(base_path, 'checklists')
static_files = join(html_path, 'static_files')


#######################################
# Section 1: parameters and variables 


### provide the paths/filenames, incl. extensions of your sources, as strings:
sources = []
for filename in os.listdir(txt_path):
    sources.append(os.path.join(txt_path, filename))
# you can also search the full txt_files directory by uncommenting the following line of code:
#sources = [join(txt_path, file) for file in os.listdir(txt_path) if file.endswith(".txt")]

### write the words you want to make an index for, as strings (""), separated by commas, between the brackets: 
#words = ["متيجة", "كوفة"]
words = []

### OR: provide the path/filename, incl. extension, of your checklist
checklist = r"L:\Islamic_Empire\DataMining\checklists\ChecklistfarsShort.txt" 

### write how many words of context you would like to get before and after your search word (as a string):
context = "25" 

### write the path to the directory where you want to save the output file:
output_path = r"L:\Islamic_Empire\DataMining\html_files"



#####################################################
# Section 2: Regular expressions for search options: 

def apply_search_options(word):
    
    ### write the regular expression you want to include before your search word(s):
    regex1 = r"\b[وفبال]{0,4}"
    ### write the regular expression you want to include after your search word(s):
    regex2 = r"\b"
    ### if you want to cancel out different combinations of alif and hamza, set alifs to 1
    alifs = 1
    ### if you want to cancel out the difference between ta marbuta and ha' 
    ### at the end of a word, set ta_marb to 1:
    ta_marb = 1
    ### if you want to cancel out the difference between ya' and alif maqsura
    ### at the end of a word, set alif_maqs to 1:
    alif_maqs = 1



    if alifs == 1:
        A = ["ا", "آ", "إ", "أ"]
        for x in A:
            word = re.sub(x, "X", word)
        word = re.sub("X", "[اإآأ]", word)
    if ta_marb == 1:
        word = re.sub(r"[ةه]\b", r"[ةه]", word)
    if alif_maqs == 1:
        word = re.sub(r"[يى]\b", r"[يى]", word)
    word = regex1 + word + regex2
    return(word)

    
##############################################
# Section 3: the Highlighter function proper 


juz = 'الجزء:'
safha = 'الصفحة:'
page_regex = r'%s \w+ ¦ %s \w+' % (juz, safha)

if checklist != "":
    try:
        checklist = open(checklist, mode="r", encoding="utf-8-sig").read()
    except:
        checklist = open(checklist, mode="r", encoding="utf-16").read()
    words = checklist.splitlines()


if int(context) < 3:
    context = int(context)*5+5
else:
    context = int(context)*5

final_outcomes = ""    
start = time.time()

number_of_results_per_source = []
for source in sources:
    if source.endswith(".txt"):
        print(source)
        number_of_all_results = 0
        with open(source, mode="r", encoding="utf-8") as file:
            text= file.read()
        text = deNoise(text)
        L = len(text)
        for word in words:
            word_regex = apply_search_options(word)

            search_results = []
            indices = [m.span() for m in re.finditer(word_regex, text)]
            number_of_all_results += len(indices)
        number_of_results_per_source.append([number_of_all_results,
                                            source, number_of_all_results/L])

for item in sorted(number_of_results_per_source):
    print(item[0], item[1], item[2])

##for word in words:
##    outcomes = '</p><p class="ltr-text">'
##    word_regex = apply_search_options(word)
##    outcomes += "This is an index for the word %s <br/>You have searched with this regex: %s" % (word, word_regex)
##    for source in sources:
##        print("Currently indexing %s in %s..." % (word, source))
##        text = open(source, mode="r", encoding="utf-8").read()
##        text = deNoise(text)
##        L = len(text)
##        
##        search_results = []
##        indices = [m.span() for m in re.finditer(word_regex, text)]
##        outcomes += '<br/></p><p class="ltr-text"><br/>The Indexer found %s results in %s' % (len(indices), source)
##       
##        for x,y in indices:
##            if x < context:
##                a = text[0:y+context]
##            elif y > L-context:
##                a = text[x-context:]
##            else:
##                a = text[x-context:y+context]
##            b = text[y:y+6000]
##            #trim off the partial words at the beginning and end of the search result:
##            if a.count(" ") > 2:
##                while a[0] != " ":
##                    a = a[1:]
##                while a[-1] != " ":                
##                    a = a[:-1]
##            
##            try:
##                page_number = re.findall(page_regex, b)[0]
##            except:
##                page_number = "[no page number]"
##            result = [page_number, a]
##            search_results.append(result)
##        print(time.time()-start)
##
##        outcomes2 = ""
##        if context == 0:
##            for page_number, x in search_results:
##                outcomes2 += page_number+'<br/>'
##        else:
##            for page_number, x in search_results:
##                outcomes2 += page_number+': <br/>'+x+'<br/><br/>'
##
##        outcomes = outcomes+"</p><p><br/><br/>"+outcomes2+"<br/><br/><br/>"
##        outcomes = re.sub(r"\\n", " ", outcomes)
##    regex3 = "(\w*"+word+"\w*)"
##    outcomes = re.sub(regex3, '<span style="background-color: #00ff00">'+r"\1"+"</span>", outcomes)
##    final_outcomes+= outcomes+"<br/><br/><br/>"

end = time.time()
print("Indexing time: "+str(end-start))

##header = open(join(static_files, 'html_header.txt'), mode="r", encoding="UTF-8").read()
##footer = open(join(static_files, 'html_footer.txt'), mode="r", encoding="UTF-8").read()
##
##new_file = join(output_path, 'index_'+words[0]+".html")
##file = open(new_file, mode="w", encoding="UTF-8")
##file.write(header+final_outcomes+footer)
##file.close()
##print("Your file is now opening in your browser")
##
##os.system(new_file)







