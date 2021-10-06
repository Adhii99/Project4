# 1. Please read :
# https://docs.python.org/3/library/tkinter.html
# for documentation on how to create GUI

# import libraries
from tkinter import *
import urllib3
from bs4 import BeautifulSoup
from nltk import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize


class Window(Frame):
    """ Class to handle window"""
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Clean Text GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        self.content = []

        # creating a buttons, entry, textbox instance
        self.entry_url = Entry(width=50)
        self.entry_url.insert(0, "https://en.wikipedia.org/wiki/Semantic_network")
        self.get_url = Button(self, text="Get URL", command=self.client_get_url)
        self.text_pro= Button(self, text="Text processor", command=self.client_text_processor)
        self.save_button = Button(self, text="Save", command=self.client_save)
        self.quitButton = Button(self, text="Exit", command=self.client_exit)
        self.t = Text(self, width=45, height=22)
        # placing the button on my window
        self.quitButton.place(x=400, y=260)
        self.get_url.place(x=400, y=20)
        self.entry_url.place(x=5, y=20)
        self.text_pro.place(x=400,y=90)
        self.save_button.place(x=400, y=160)
        self.t.place(x=5, y=40)


    def client_exit(self):
        """Exit function"""
        exit()
    def client_text_processor(self):
        self.t.delete(1.0, END)
        stemmer = PorterStemmer()
        word = []
        self.t.insert("end", "No. of sentences: "+str(len(self.content)))
        self.t.insert("end", " \nNormal words : ")
        for sent in self.content:
            word.extend(word_tokenize(sent))
        self.t.insert("end",str(word))
        self.t.insert("end", " \nStemmed words : ")
        stemmed_words = [stemmer.stem(i) for i in word]
        self.t.insert("end", " \nStemmed words : " + str(stemmed_words))



    def client_save(self):
        file = open("url_file.txt", "w+")
        file.write(" Text in https://en.wikipedia.org/wiki/Semantic_network :")
        for w in self.content:
            file.write(w)
        file.close()

    def client_get_url(self):
        """ Clean text operations """
        url = self.entry_url.get()
        http = urllib3.PoolManager()
        page = http.request('GET', url)
        soup = BeautifulSoup(page.data, "html.parser")
        self.t.delete(1.0, END)
        for p in soup.find_all('p'):
            self.t.insert("end", p.text)
            self.content.append(p.text)


root = Tk()

# size of the window
root.geometry("500x400")

app = Window(root)
root.mainloop()