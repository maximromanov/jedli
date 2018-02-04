from tkinter import *
from tkinter import ttk
import logging
import jedli_global


class Logger:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("Jedli logger")
        ws = self.top.winfo_screenwidth()
        hs = self.top.winfo_screenheight()
        w = 500
        h = 600
        x = (ws/2) + 5
##        y = (hs/2) - (h/2)
        y = 0
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.top.protocol('WM_DELETE_WINDOW', self.hideWindow)
        self.mainframe = Canvas(self.top, borderwidth=0, width=500, height=600)
        self.mainframe.pack(fill=BOTH, expand=1)
        self.make_text_frame()
        jedli_global.rClickbinder(self.top, readonly=True)

    def hideWindow(self):
        self.top.withdraw()
        
    def make_text_frame(self):
        self.tf = Frame(self.mainframe)
        self.tf.pack(fill=BOTH, expand=1)
        scrollbar=Scrollbar(self.tf)
        self.textf = Text(self.tf, wrap=WORD, width=60, height=40,
                          foreground="blue", yscrollcommand=scrollbar.set)
        self.textf.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.pack(side=LEFT, fill=Y)
        scrollbar.config(command=self.textf.yview)
        
        self.textf.tag_config("blackLetters", foreground="black")
        self.textf.tag_config("redLetters", foreground="red")

        introText = "This is the Jedli logger. Here you can follow what the program is doing.\n\n\n"
        self.textf.insert(END,introText)
        self.textf.tag_add("blackLetters", 1.0, INSERT)
        self.textf.bind('<Button-3>',lambda e: jedli_global.rClicker(e, True), add='')

    
class RedirectLogging(logging.Handler):
    """ Used to redirect logging output to the widget passed in parameters """
    """ based on http://stackoverflow.com/questions/14883648/redirect-output-from-python-logger-to-tkinter-widget """
    def __init__(self, widget, color_var):
        logging.Handler.__init__(self)
        self.console = widget
        self.color_var = color_var

    def write(self,string):     
        try:
            self.console.mark_set("start-mark", INSERT) #set a mark at the insert position
            self.console.mark_gravity("start-mark", LEFT) #keep it to the left of the text that is going to be inserted
            self.console.insert(END, string)
            if self.color_var == 1:
                self.console.tag_add("redLetters", "start-mark", INSERT)
            self.console.mark_unset("start-mark") #remove the mark
            self.console.yview(END)
##        except:
##            pass
        except Exception as e:
            print("LOGGING ERROR!", e)

#### For some reason, the print function does not work properly from
#### the jedli_logger file (crashes all the time),
#### but it works fine from jedli_global
## def print(*args):
##    try:
##        to_be_printed = " PRINT!"
##        for x in args:
##            to_be_printed += " " + str(x)
##        to_be_printed = to_be_printed[1:]
##        to_be_printed += "\n"
##        jedli_global.logger.textf.insert(END, to_be_printed)
##        jedli_global.logger.textf.yview(END)
##        jedli_global.logger.top.update()
##        jedli_global.logger.top.update_idletasks()
##    except Exception as e:
##        print("LOGGING ERROR!", e)

def main(): 
    root = Tk()
    Button(text="launch shell", command=shell).pack()
    root.mainloop()


def main2(): 
    root = Tk()
    Button(text="launch shell", command=Logger()).pack()
    root.mainloop()

if __name__ == "__main__":
    Logger()
