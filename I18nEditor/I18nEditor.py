from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
import json

class I18nEditor(object):
    def __init__(self):
        self.form = Tk()
        self.filename = ''
        self.keys = []
        self.values = {}
        self.dicts = {}
        self.texts = {}
        self.languages = []

        self.form.title('i18n Editor')
        self.form.resizable(0,0)

        screen_width = self.form.winfo_screenwidth()
        screen_height = self.form.winfo_screenheight()

        #size = tuple(int(_) for _ in self.form.geometry().split('+')[0].split('x'))
        x = int((screen_width - 600)/2)
        y = int((screen_height - 450)/2)

        self.form.geometry('{}x{}+{}+{}'.format(600, 450, x, y))

        self.frame = Frame(self.form)
        self.frame.place(anchor=NW,x=50,y=0, relx=0.20)

        self.lbox = Listbox(self.form, height=600, width=25)
        self.lbox.bind('<<ListboxSelect>>', self.onselect)
        self.lbox.pack(side="left")
        self.lbox.pack(expand=0)

        lblkey = Label(self.frame, text="Key")
        lblkey.grid(row=0, column=0)

        self.textKey = StringVar()
        self.txtKey = Entry(self.frame, width=50, textvariable=self.textKey)
        self.txtKey.grid(row=0,column=1, columnspan=5)

        self.btnSelect = Button(self.frame, text="Select i18n folder", command=self.loadFils)
        self.btnSelect.grid(row=3,column=0)

        self.btnClear = Button(self.frame, text="Clear", command=self.clear, width=10)
        self.btnClear.grid(row=3, column=1)

        self.btnUpdate = Button(self.frame, text="Update Key", command=self.update)
        self.btnUpdate.grid(row=3, column=2)

        self.btnAdd = Button(self.frame, text="Add Key", command=self.addKey, width=10)
        self.btnAdd.grid(row=3, column=3)

        self.btnSaveFiles = Button(self.frame, text="Save Files", command=self.saveFiles, width=10)
        self.btnSaveFiles.grid(row=3, column=4)
        

    def clear(self):
        self.textKey.set('')
        for lang in self.languages:
            self.texts[lang].set('')

    def update(self):
        k = self.textKey.get()
        for lang in self.languages:
            self.dicts[lang][k] = self.texts[lang].get()

    def addKey(self):
        k = self.textKey.get()
        self.lbox.insert(0, k)
        for lang in self.languages:
            self.dicts[lang][k] = self.texts[lang].get()

        self.clear()

    def saveFiles(self):
        files = os.listdir(self.filename)
        for lang in self.languages:
            with open(self.filename+'/'+lang+'.json','w', encoding="utf-8") as file:
                json.dump(self.dicts[lang], file, ensure_ascii=False)
        

        messagebox.showinfo("Done", "File Saved Successfully")

    def onselect(self,evt):
        # Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.textKey.set(value)
        for lang in self.languages:
            self.texts[lang].set(self.dicts[lang][value])
        

    def read_files(self,folder):
        files = os.listdir(folder);
        self.languages = [f.split('.')[0] for f in files]
        for i in range(len(files)):
            fi = files[i]
            lang = fi.split('.')[0]
            lbl = Label(self.frame, text="Value {}".format(lang), )
            lbl.grid(row=1+i, column=0)

            text = StringVar()
            txt = Entry(self.frame, width=50, textvariable=text)
            txt.grid(row=1+i,column=1, columnspan=5)
            self.texts[lang] = text

            file = open(folder+'/'+fi,'r', encoding="utf-8")
            dict = json.loads(file.read())
            self.keys = list(dict.keys())
            self.values[lang] = list(dict.values())
            self.dicts[lang] = dict

        l = len(self.languages)
        self.btnSelect.grid(row=l+2,column=0)
        self.btnClear.grid(row=l+2, column=1)
        self.btnUpdate.grid(row=l+2, column=2)
        self.btnAdd.grid(row=l+2, column=3)
        self.btnSaveFiles.grid(row=l+2, column=4)
        
        for i,item in enumerate(self.keys):
            self.lbox.insert(1,item)

    def loadFils(self):
        self.filename = filedialog.askdirectory()
        print(self.filename)
        self.read_files(self.filename)

if __name__ == "__main__":
    I18nEditor().form.mainloop()