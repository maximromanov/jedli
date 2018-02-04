import sys
import inspect
import os

### check if the folders are in the Python path:
### see http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
base_path = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if base_path not in sys.path:
    sys.path.insert(0, base_path)
module_path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"modules")))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from tkinter import *
from tkinter import ttk

from modules.jedli_gui import Application



frameBorderSea2_data = """
R0lGODlhQABAANUAAAAAAP///6SipJyanJSSlIyKjISChPz6/PTy9Ozq7OTi5Nza3NTS1MzKzMTC
xLy6vLSytKyqrCCyqnx+fKSmpJyenJSWlIyOjPz+/PT29Ozu7OTm5Nze3NTW1MzOzMTGxLy+vLS2
tKyurP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACMALAAAAABAAEAAAAa6wJFw
SCwaj8ikcslsOp/QqHRKrVqv2KxRwu16v+CwGEwdm89obzTNbpOd7ni8Ka+3mfb8eanvj5V+gV+A
goWEhYGHiH2Ki3mNjnWQkXNJlHqTl2yZmmicnWafoGKio29Ipm6lqV2rrBKurLGps6a1o7eguZ27
mr2Xv5TBkcOOxYvHiMmGlq+ezc6h0NGk09SnR9d/1tqt3N2w39184N7LfnTlT+Br12WvWvHy8/T1
9vf4+fr7/P3+8kEAADs="""

frameBorderOlive2_data="""
R0lGODlhQABAANUAAAAAAP///6SipJyanJSSlIyKjISChPz6/PTy9Ozq7OTi5Nza3NTS1MzKzMTC
xLy6vLSytKyqrHx+fKSmpJyenJSWlIyOjPz+/PT29Ozu7OTm5Nze3NTW1MzOzMTGxLy+vLS2tKyu
rKLNWv///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACMALAAAAABAAEAAAAa6wJFw
SCwaj8ikcslsOp/QqHRKrVqv2KxRxO16v+CwGEwdm89obzTNbpOd7ni8Ka+3mfb8eanvj5V+gV+A
goWEhYGHiH2Ki3mNjnWQkXNJlHqTl2yZmmicnWafoGKio29Ipm6lqV2rrCKurLGps6a1o7eguZ27
mr2Xv5TBkcOOxYvHiMmGlq+ezc6h0NGk09SnR9d/1tqt3N2w39184N7LfnTlT+Br12WvWvHy8/T1
9vf4+fr7/P3+8kEAADs="""




def main():

    root = Tk()
    root.title("jedli")
    root.wm_iconbitmap(bitmap = "jedli_logo1.ico")
    hs = root.winfo_screenheight()
    ws = root.winfo_screenwidth()
    # define the location of the jedli windows on the computer screen:
    w=570
    h=580
    x = (ws/2) - (w+20)
##    y =(hs/2) - (h/2)
    y = 0
    root.geometry('+%d+%d' % (x, y))
    root.resizable(0,0)

    # the following block of code defines the rounded frames of the GUI
    img1 = PhotoImage("frameBorderSea", data=frameBorderSea2_data)
    img2 = PhotoImage("frameBorderOlive", data=frameBorderOlive2_data)
    style = ttk.Style()
    style.element_create("roundedFrameSea", "image", "frameBorderSea",
                         border=16, sticky="nsew")
    style.layout("roundedFrameSea", [("roundedFrameSea", {"sticky": "nsew"})])
    style.element_create("roundedFrameOlive", "image", "frameBorderOlive",
                         border=16, sticky="nsew")
    style.layout("roundedFrameOlive", [("roundedFrameOlive", {"sticky": "nsew"})])
    # this sets the outline of the Button to the same color as the frames:
    style.configure("sea.TButton", background="light sea green")
    style.configure("olive.TButton", background="DarkOliveGreen3")
    
    Application(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
