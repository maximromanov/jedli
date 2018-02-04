"""make a scatter/line plot that represents
the distribution of the sets of search words
within the text.

Problems:
1. the scatter plot has more batches than it is supposed to have
2. the result is not clear; looks like a confetti bomb
"""

import plotly.graph_objs as go
import plotly.offline as offline


def define_batch(text_len, batches):
    """This function can be used in two ways:
    1. to define how large a batch is for a text of a given text_len
    and a batches number of batches
    2. to define into which batch a position inside the text falls"""
    return int((text_len - (text_len % batches)) / batches)

def chronoplot(text_len, indices_dic, outputfp, batches=100, write_file=False):
    """make a scatter/line plot that represents
    the distribution of the sets of search words
    within the text."""

    batch_size = define_batch(text_len, batches)
    scatter_dic = {}
    line_dic = {}
##    for i, lst in sorted(indices_dic.items()):
    for i, dic in sorted(indices_dic.items()):
        print(i)
        batches_dic = {x:[] for x in range(batches+1)}
        x = [] # will contain the data for the x axis for this set of search words
        y = [] # will contain the data for the y axis for this set of search words
        links = []
##        for tup in lst:
        for e, tup in enumerate(dic["list_indices"]):
            #print(tup, text_len)
            its_batch = define_batch(tup[0], batch_size)
            pos_in_batch = tup[0] % batch_size
            x.append(its_batch)
            y.append(pos_in_batch)
            links.append(dic["list_links"][e])
            try:
                batch_list = batches_dic[its_batch]
                batch_list.append(pos_in_batch)
                batches_dic[its_batch] = batch_list
            except:
                print('batch', its_batch, 'not in batches_dic')
        scatter_dic[i] = {}
        scatter_dic[i]["x"] = x
        scatter_dic[i]["y"] = y
        scatter_dic[i]["links"] = links
        line_dic[i] = batches_dic

    data = []
##    links_annotations = []
    for i, dic in sorted(scatter_dic.items()):
        trace = go.Scatter(x=dic["x"], y=dic["y"],
                           mode="markers", name=i, yaxis="y1")
##        for e in range(len(dic["x"])):
##            links_annotations.append(dict(x=dic["x"][e], y=dic["y"][e],
##                                          text=dic["links"][e],
##                                          showarrow=False,
##                                          xanchor="center",
##                                          yanchor="center"))
        data.append(trace)

    
    

    for i, dic in sorted(line_dic.items()):
        val_len = [len(val)
                   for key, val in sorted(dic.items())]
        trace = go.Scatter(x=sorted(dic.keys()), y=val_len,
                           mode="lines", name=i, yaxis="y2")
        data.append(trace)
        
    layout = go.Layout(yaxis=dict(title="location of attestations in batches"),
                       yaxis2=dict(title="number of attestations per batch",
                                   side="right", overlaying="y"),
##                       annotations=links_annotations
                       )
    fig = go.Figure(data=data, layout=layout)
    if write_file:
        offline.plot(fig, filename=outputfp)
    else:
        plot_html = offline.plot(fig, output_type="div")
        return plot_html
        


##    for i, dic in sorted(line_dic.items()):
##        val_len = [len(val) for key, val in sorted(dic.items())]
##        trace = go.Bar(x=sorted(dic.keys()), y=val_len)
##        data.append(trace)
##        layout = go.Layout()
##        fig = go.Figure(data=data, layout=layout)
##        offline.plot(fig, filename='bartest.html')
    
    
    
        
