"""
NB: replaced matplotlib with plotly
"""

import json
from operator import itemgetter
import re
##import matplotlib
##from matplotlib import pyplot
##matplotlib.rc('font', family='Arial')

import plotly.offline as offline
import plotly.tools as ply_tools
import plotly.plotly as ply
import plotly.graph_objs as go


def load_json(pth):
    with open(pth, mode="r", encoding="utf-8") as file:
        return json.load(file)

def make_simple_date_graph(data):
    """graph the raw word count for every date"""
    pass

def make_relative_date_graph(data):
    """graph the relative word count for every date"""
    pass

##def draw_graph(data):
##    colours = ["blue", "green", "red", "yellow"]
##    pyplot.title("Relative frequency (occurences / 1.000.000 characters)")
##    for i, word in enumerate(sorted(data.keys())):
##        print(i)
##        pyplot.subplot(211+i)
##        pyplot.title(word)
####        g1 = []
####        g2 = []
####        for group in data[word]:
####            g1.append(group)
####            g2.append(data[word][group])
####        print(word)
####        print(g1)
####        print(g2)
####        pyplot.bar(g1, g2, width=10, color="blue")
##        pyplot.bar(list(data[word].keys()), list(data[word].values()),
##                   width=10, color="blue", align='center')
##    pyplot.show()

def draw_graph(data, json_path, relative):
    colours = ["blue", "green", "red", "yellow"]
    colours = ["#00CCFF", "#FF0000", "#FF99FF", "#33FFFF",
               "#FFCC00", "#CC9900", "#CCCCCC", "#999999",
               "#FFFF00", "#66FF00"]
    if relative:
        chart_title = "Relative frequency: occurences / 1.000.000 characters"
        yaxis_title = "Number of occurrences per 1.000.000 characters"
    else:
        chart_title = "Absolute frequency of the search words"
        yaxis_title = "Number of occurrences: absolute numbers"
        

    traces = []
    for i, word in enumerate(sorted(data.keys())):
        trace = go.Bar(x=list(data[word].keys()),
                       y=list(data[word].values()),
                       marker=dict(color=colours[i]),
                       name=word,
                       text=word
                       )
        traces.append(trace)
    layout = go.Layout(title = chart_title,
                   xaxis=dict(title="Date AH"),
                   yaxis=dict(title=yaxis_title))
    fig = go.Figure(data=traces, layout=layout)
    htmlfilepath = json_path[:-10]+"plot.html"
    if __name__ == "__main__":
        offline.plot(fig, filename=htmlfilepath)
    else:
        plot_html = offline.plot(fig, output_type="div")
##    with open(htmlfilepath) as file:
##        html = file.read()
##        plot_html = re.findall(r"<body>(.+)</body>", html, re.DOTALL)[0]
        return plot_html
        
def rounddown(value, base=50):
    """round any value down to the nearest base"""
    return value - value % base    


def make_grouped_date_graph(data, json_path, group, relative):
    """graph the word count; group dates by decade, century, etc."""
    graph_dic = {}
    group_len_dic = {}
    for textID in data:
        for word in data[textID]['results']:
            if word not in graph_dic:
                graph_dic[word] = {}
                group_len_dic[word] = {}
            # define the group (chronological bucket) into which the source belongs:
            date = int(data[textID]["source_date"])
            if date > 3000: # None dates will be displayed at 0
                date = 0
            current_group = rounddown(date, group)
            if current_group not in graph_dic[word]:
                graph_dic[word][current_group] = 0
                group_len_dic[word][current_group] = 0
                
            # add the data to the group_dic
            count = data[textID]["results"][word]["number_of_results"]
            graph_dic[word][current_group] += count
            if relative: 
                text_len = data[textID]["len"]
                group_len_dic[word][current_group] += text_len
                
    if relative:
        # divide the number of results for each groups by the
        # number of characters the texts of each group contain:
        for word in graph_dic:
            for group in graph_dic[word]:
                rel = graph_dic[word][group]/group_len_dic[word][group]
                graph_dic[word][group] = 1000000*rel
                

        
    plot_html = draw_graph(graph_dic, json_path, relative)
    return plot_html


##def make_grouped_date_graph(data, json_path, group, relative):
##    """graph the word count; group dates by decade, century, etc."""
##    graph_dic = {}
##    for word_regex, dic in data.items():
##        word = data[word_regex]["word"]
##        group_dic = {}
##        group_len_dic = {}
##        for textID in sorted(data[word_regex]['sources'],
##                             key=lambda x: data[word_regex]["sources"][x]["date"]):
##            
##            # define the group (chronological bucket) into which the source belongs:
##            date = int(data[word_regex]['sources'][textID]["date"])
##            if date > 3000: # None dates will be displayed at 0
##                date = 0
##            current_group = rounddown(date, group)
##            if current_group not in group_dic:
##                group_dic[current_group] = 0
##                group_len_dic[current_group] = 0
##                
##            # add the data to the group_dic
##            count = data[word_regex]['sources'][textID]["results_count"]
##            group_dic[current_group] += count
##            if relative: 
##                text_len = data[word_regex]['sources'][textID]["char_count"]
##                group_len_dic[current_group] += text_len
##                
##        if relative:
##            # divide the number of results for each groups by the
##            # number of characters the texts of each group contain:
##            for g in group_dic:
##                group_dic[g] = 1000000*group_dic[g]/group_len_dic[g]
##                
##        graph_dic[word] = group_dic
##        
##    plot_html = draw_graph(graph_dic, json_path, relative)
##    return plot_html

def main(json_path, grouped = False, relative = False):
    count_dic = load_json(json_path)
    for word_regex, dic1 in count_dic.items():
        print(word_regex)
        for source_id, dic2 in sorted(dic1["sources"].items()):
            print("  ", source_id, dic2["results_count"])
            
    if grouped != False:
        plot_html = make_grouped_date_graph(count_dic, json_path, grouped, relative)

        
        
if __name__ == "__main__":
##    json_path = r"C:\Users\ERC\Desktop\exe.win-amd64-3.4\search_results\index_أعيان_datecount.json"
##    json_path = r"C:\Users\ERC\Desktop\exe.win-amd64-3.4\search_results\index_مفاخر_datecount.json"
    json_path = r"C:\Program Files\Jedli-Windows\exe.win-amd64-3.4\search_results\index_البصرة_datecount.json"
    main(json_path, grouped = 50, relative = False)

