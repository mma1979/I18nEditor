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
        self.valuesAr = []
        self.valuesEn = []
        self.dictAr = {}
        self.dictEn = {}
    

        self.form.title('i18n Editor')
        self.form.resizable(0,0)

        screen_width = self.form.winfo_screenwidth()
        screen_height = self.form.winfo_screenheight()

        #size = tuple(int(_) for _ in self.form.geometry().split('+')[0].split('x'))
        x = int((screen_width - 600)/2)
        y = int((screen_height - 450)/2)

        self.form.geometry('{}x{}+{}+{}'.format(600, 450, x, y))

        frame = Frame(self.form)
        frame.place(anchor=NW,x=50,y=0, relx=0.20)

        self.lbox = Listbox(self.form, height=600, width=25)
        self.lbox.bind('<<ListboxSelect>>', self.onselect)
        self.lbox.pack(side="left")
        self.lbox.pack(expand=0)

        lblkey = Label(frame, text="Key")
        lblkey.grid(row=0, column=0)


        self.textKey = StringVar()
        self.txtKey = Entry(frame, width=50, textvariable=self.textKey)
        self.txtKey.grid(row=0,column=1, columnspan=5)


        lblAr = Label(frame, text="Value AR", )
        lblAr.grid(row=1, column=0)

        self.textAr = StringVar()
        self.txtAr = Entry(frame, width=50, textvariable=self.textAr)
        self.txtAr.grid(row=1,column=1, columnspan=5)

        lblEn = Label(frame, text="Value EN")
        lblEn.grid(row=2, column=0)

        self.textEn = StringVar()
        self.txtEn = Entry(frame, width=50, textvariable=self.textEn)
        self.txtEn.grid(row=2,column=1, columnspan=5)

        self.btnSelect = Button(frame, text="Select i18n folder", command=self.loadFils)
        self.btnSelect.grid(row=3,column=0)

        self.btnClear = Button(frame, text="Clear", command=self.clear, width=10)
        self.btnClear.grid(row=3, column=1)

        self.btnUpdate = Button(frame, text="Update Key", command=self.update)
        self.btnUpdate.grid(row=3, column=2)

        self.btnAdd = Button(frame, text="Add Key", command=self.addKey, width=10)
        self.btnAdd.grid(row=3, column=3)

        self.btnSaveFiles = Button(frame, text="Save Files", command=self.saveFiles, width=10)
        self.btnSaveFiles.grid(row=3, column=4)


    def clear(self):
        self.textKey.set('')
        self.textAr.set('')
        self.textEn.set('')


    def update(self):
        k = self.textKey.get()
        self.dictAr[k] = self.textAr.get()
        self.dictEn[k] = self.textEn.get()

    def addKey(self):
        k = self.textKey.get()
        self.lbox.insert(0, k)
        self.dictAr[k] = self.textAr.get()
        self.dictEn[k] = self.textEn.get()
        self.clear()


    def saveFiles(self):
        files = os.listdir(self.filename)
        with open(self.filename+'/'+files[0],'w', encoding="utf-8") as fileAr:
            json.dump(self.dictAr, fileAr, ensure_ascii=False)
        

        with open(self.filename+'/'+files[1],'w', encoding="utf-8") as fileEn:
            json.dump(self.dictEn, fileEn, ensure_ascii=False)

        messagebox.showinfo("Done", "File Saved Successfully")

    def onselect(self,evt):
        # Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.textKey.set(value)
        self.textAr.set(self.dictAr[value])
        self.textEn.set(self.dictEn[value])


    def read_files(self,folder):
        files = os.listdir(folder);
        fileAr = open(folder+'/'+files[0],'r', encoding="utf-8")
        self.dictAr = json.loads(fileAr.read())

        fileEn = open(folder+'/'+files[1],'r', encoding="utf-8")
        self.dictEn = json.loads(fileEn.read())

        self.keys = list(self.dictAr.keys())
        self.valuesAr = list(self.dictAr.values())
        self.valuesEn = list(self.dictEn.values())

        for i,item in enumerate(self.keys):
            self.lbox.insert(1,item)


    def loadFils(self):
        self.filename = filedialog.askdirectory()
        print(self.filename)
        self.read_files(self.filename)

if __name__ == "__main__":
    I18nEditor().form.mainloop()