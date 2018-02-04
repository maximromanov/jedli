import re
import zipfile
import codecs
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import os
#from os.path import join
import time
from bs4 import BeautifulSoup

from jedli_global import txt_path, epub_path


def epubConverter():

        filenames = askopenfilenames(title="Choose one or more epub files to be converted",
                                       initialdir=epub_path, filetypes = [("epub files", ".epub")])        
        alpha = time.time()


        failed = []
        for file in filenames:
                start = time.time()
                if file.endswith(".epub"):
                        try:
                            print("Converting %s to .txt..." % os.path.basename(file))
                            fh = zipfile.ZipFile(file)
                            file=file.split("/")
                            file = file[-1][:-5]

                            list_names = []
                            for info in fh.infolist():
                                if info.filename.endswith("html"):
                                        list_names.append(info.filename)
                            numbers = re.compile("\d+")
                            good_list = []
                            for element in list_names:
                                last_part = os.path.split(element)[1]
                                number = re.findall(numbers, last_part)
                                try:
                                    number = number[0]
                                except IndexError:
                                    continue
                                e = 5
                                while len(number) < e:
                                    number = "0"+number
                                good_list.append((number, element))
                            good_list = sorted(good_list)
                            text=""

                            for html in good_list[:8000]:
                                data = fh.read(html[1])
                                data = codecs.decode(data, "utf-8")
                                text += data
                                
                            intro = fh.read("OEBPS/xhtml/info.xhtml")
                            intro= codecs.decode(intro, "utf-8")
                            text = intro + "\n\n" + text

                            s = text.split("<?xml")
                            s = s[1:]
                            new_text = ""
                            for el in s:
                                el = "<?xml"+el
                                line_break = r"<br />"
                                el = re.sub(line_break, "\n", el)
                                soup=BeautifulSoup(el)
                                soup.title.decompose()
                                t=" ".join(soup.strings)
                                t=re.sub(" +", " ", t)
                        #        t = soup.get_text()
                                new_text+=t

                            new_text = re.sub("(?: ?\n){3,}", "\n", new_text)

                            soup=BeautifulSoup(intro)
                            pp = soup.find_all("span", class_="info-item")
                            t = ""
                            for p in pp:
                                t+=" ".join(p.strings)+"\n"
                            new_text = t+"\n\n----------\n\n\n"+new_text

                            juz = "الجزء:"
                            safha = "الصفحة:"
                            page_regex = juz + r" \w+ ¦ " + safha + r" \w+"

                            new_text = re.sub(r"(%s)" % page_regex, r"\n\1\n\n\n", new_text)
                            file=os.path.join(txt_path, file)
##                            print(file)
                            with open(file+".txt", mode="w", encoding="utf-8") as txt_file:
                                txt_file.write(new_text)
                            end = time.time()
                            print("Conversion took %s seconds" % (end-start))
                        except Exception as e:
                                messagebox.showwarning("Epub converter", "Conversion of %s failed!! %s" % (file, str(e)))
                                failed.append(file)
                else:
                        messagebox.showwarning("Epub converter", "You have not selected an epub file")

        end = time.time()            
        print("total time: %s" % (end-alpha))
        if failed != []:
                print("conversions failed: ")
                for x in failed:
                    print(x)
        

if __name__ == "__main__":
    epubConverter()
