"""
print a frequency list of all (Arabic) words in a directory
the program sorts the words in descending order and writes them to a file
For every word, the file contains:
1. its rank
2. how many times it is present in the corpus
3. the number of times it features in the text per 1.000 words

Takes more than 10 minutes to run this over the entire Shamela corpus on my laptop
=> save dictionaries as a json file, and check if the same group of text has
   already been treated? Or just wait until we built the database...

Problems:
* make_html takes a really long time!
  =>Much faster when not making the entire file in memory before writing it
* html file of the entire Shamela corpus becomes really big: 300+ MB
"""

import os
import re
import regex
from collections import defaultdict
from operator import itemgetter
from core_mining_functions import deNoise
import time
import webbrowser
import json


from jedli_global import static_files, output_folder
header = open(os.path.join(static_files, "html_header.txt"), mode="r", encoding="UTF-8").read()
footer = open(os.path.join(static_files, "html_footer.txt"), mode="r", encoding="UTF-8").read()


def open_file(pth):
    with open(pth, mode="r", encoding="utf-8-sig") as file:
        return file.read()


##def make_html(intro, dic, word_count, rank_dict):
##    print(3)
##    header_list = ['Rank', 'Word', 'Frequency',
##                   'Relative Frequency (attestations per 1000 words)']
##    html = intro + make_table_intro()
##    html += make_table_header(header_list)
##    for word, freq in sorted(dic.items(), key=itemgetter(1), reverse=True):
##        html += make_table_row([rank_dict[freq], word, freq, freq/word_count*1000])
##    html += '  </table>\n'
##    html += '</div>\n'
##    html += footer
##    return html

def make_html(intro, dic, word_count, rank_dict, pth):
    print(3)
    header_list = ['Rank', 'Word', 'Frequency',
                   'Relative Frequency (attestations per 1000 words)']
    html = intro + make_table_intro()
    html += make_table_header(header_list)
    with open(pth, mode="w", encoding="utf-8") as outfile:
        outfile.write(html)
        for word, freq in sorted(dic.items(), key=itemgetter(1), reverse=True):
            outfile.write(make_table_row([rank_dict[freq], word, freq, freq/word_count*1000]))
        html = '  </table>\n'
        html += '</div>\n'
        html += footer
        outfile.write(html)


def write_file(html, pth):
    print("writing...")
    with open(pth, mode="w", encoding="utf-8") as outfile:
        outfile.write(html)            

def delete_page_numbers(text):
    return re.sub("(?:{}|{}): \w+".format("الجزء", "الصفحة"), "", text)

def splitText(text):
##    split_text = text.split()
##    split_text = re.split("\s", text) # useless: includes punctuation etc.
##    split_text = re.findall("\w+", text) # quite good but includes non-Arabic words
    split_text = regex.findall("\p{Arabic}+", text) # same time, but has only Arabic words
    return split_text

def clean_text(text):
    text = deNoise(text)
    #text = delete_page_numbers(text)
    text = re.sub("\d+", "", text)
    return text

def get_frequencies(split_text, word_count=0, count_dict={}, text_len=0):
    """add the words from the split_text to the count_dic
    and add the number of words to the word_count"""
    if not text_len:
        text_len = len(split_text)
    word_count += text_len
    for word in split_text:
        count_dict[word] += 1
    return word_count, count_dict


def get_rank(count_dict, x):
    i=len(count_dict)
    for key, val in sorted(count_dict.items(), key=lambda item:item[1]):
        i-=1
        if key == x:
            return i

def make_rank_dict(count_dict):
    """make a dictionary that contains the rank of every value
    in the count_dict"""
    
    last_val = None
    rank_dict = {}
    i = 1
    for key, val in sorted(count_dict.items(), key=lambda item:item[1], reverse=True):
        if last_val != val:
            last_val = val
            rank_dict[val] = i
            i += 1
    return rank_dict
        
def filter_words_to_count(words_to_count, count_dict, rank_dict):
    """make a list of tuples that contains only
    the results of the selected words/regexes.
    Tuples:
      0 - regex
      1 - total number of times the regex is attested
      2 - a dictionary containing the results of all words that match the regex:
            * word: number of results"""
    ##selected_words = {}
    selected_words = []
    all_words = " ".join(count_dict.keys()) # make a searchable string of all words in the dictionary
    for regex in words_to_count:
        count = 0
        count_d = {}
        all_hits = re.findall(r"\b{}\b".format(regex), all_words)
        for x in all_hits:
            count += count_dict[x]
            count_d[x] = count_dict[x]
##                    selected_words[regex] = {}
##                    selected_words[regex]["count"] = count
##                    selected_words[regex]["count_d"] = count_d
        selected_words.append((regex, count, count_d))
    return selected_words

def make_table_header(header_list):
    table_header= '    <tr>\n'
    for h in header_list:
        table_header+= '      <th>{}</th>\n'.format(h)
    table_header+= '    </tr>\n'
    return table_header

def make_table_row(row_list): 
    row = '    <tr>\n'
    for r in row_list:
        row+= '      <td>    {}</td>\n'.format(r)
    row+= '    </tr>\n'
    return row

def make_table_intro():
    intro= '<div id="source_table">\n'
    intro+= '  <table>\n'
    return intro
    

def write_selected_words_intro(selected_words, word_count, rank_dict):
    intro = header + '<div id="intro">Frequency list: Selected words: \n</div>\n'
    intro+= make_table_intro()
    header_list = ['Rank', 'Word', 'Frequency',
                   'Relative Frequency (attestations per 1000 words)']
    intro += make_table_header(header_list)
    for tup in sorted(selected_words, key=itemgetter(1), reverse=True):
        intro+= make_table_header(["", tup[0], tup[1], tup[1]/word_count*1000])
        for word, freq in sorted(tup[2].items(), key=lambda item:item[1], reverse=True):
            intro += make_table_row([rank_dict[freq], word, freq, freq/word_count*1000]) 
    intro += '  </table>\n'
    intro += '</div><br/><br/><br/>\n'
    intro += '<div id="intro">Frequency list: All words: \n</div>\n'
    #print(intro)
    return intro

def make_json_dump(count_dict, word_count, rank_dict):
    outfilepath = os.path.join(output_folder, "frequency_dic_{}.json".format(len(count_dict)))
    with open(outfilepath, mode="w", encoding="utf-8") as file:
        json.dump({"count_dict" : count_dict,
                   "word_count" : word_count,
                   "rank_dict" : rank_dict},
                  file)

def main(source_list, words_to_count= [""], outfilepath=""):

    start = time.time()
    count_dict = defaultdict(int)
    source_dict = {}
    word_count = 0
    
    for filepath in source_list:
        text = open_file(filepath)
        text = clean_text(text)
        split_text = splitText(text)
        text_len = len(split_text)
        source_dict[filepath] = text_len
        word_count, count_dict = get_frequencies(split_text, word_count,
                                                 count_dict, text_len)
    rank_dict = make_rank_dict(count_dict)        
    if words_to_count:
        selected_words = filter_words_to_count(words_to_count, count_dict, rank_dict)
        intro = write_selected_words_intro(selected_words, word_count, rank_dict)
    else:
        selected_words = None
        intro = header + '<div id="intro">Frequency list\n</div>\n'

    if not outfilepath:
        outfilepath = os.path.join(output_folder, "frequency_list.html")
    make_html(intro, count_dict, word_count, rank_dict, outfilepath)
    print("{} seconds; {} words in corpus".format(time.time() - start, word_count))
    #write_file(html, outfilepath)
    webbrowser.open('file://' + os.path.realpath(outfilepath))
    return count_dict, word_count, rank_dict, selected_words


if __name__ == "__main__":
    directory = r"C:\Users\ERC\Desktop\exe.win-amd64-3.4\texts"
    directory = r"C:\Users\ERC\Documents\Peter\computer_stuff\frequency_lists\test_folder"
    directory = r"D:\ERC\computer_stuff\frequency_lists\test_folder"
    directory = r"C:\Program Files\Jedli-Windows\exe.win-amd64-3.4\texts"

    source_list = []
    for f in os.listdir(directory):
        #print(f)
        if f.endswith(".txt"):
            source_list.append(os.path.join(directory, f))

    main(source_list,
         words_to_count=["الله", "[وبف]*?البصرة", "الكوفة", "قاضي"])
    #main(source_list, words_to_count=["الصفحة"])


    

    




