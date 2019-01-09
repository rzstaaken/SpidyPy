# Version 0.2
# Aus 'stackoverflow.com' 'tkinter listbox drag and drop with python'
# https://stackoverflow.com/questions/14459993/tkinter-listbox-drag-and-drop-with-python/39300853#39300853
# Danke 'Moshe'
# Vielen Dank 'Jarad' für die auf Selectmode 'MULTIPLE' umgeschriebene Fassung

# Wenn 'name' angegeben wird, wird die Reihenfolge und der Inhalt als CSV gespeichert.
#   Filename ist dann name.csv
import tkinter as tk
import csv
from JsonIO import JsonIO
import SpiderDefaults


class Drag_and_Drop_Listbox(tk.Listbox):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, lbname=None, **kw):
        kw['selectmode'] = tk.MULTIPLE
        kw['activestyle'] = 'none'
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.getState, add='+')
        self.bind('<Button-1>', self.setCurrent, add='+')
        self.bind('<B1-Motion>', self.shiftSelection)
        #self.bind('<<ListboxSelect>>', self.save)
        self.curIndex = None
        self.curIndex3 = None
        self.curState = None
        self.lbname = lbname
        self.is_mw = True

    def fillListBox(self, insertEND=False, path=None):
        """
            Aus dem Directory path werden die json-Dateien gelesen und
            in der listbox dargestellt.
        """
        try:
            # Wenn die Datei existiert werden die gesicherten Daten geladen
            with open(self.lbname+'.csv', "r")as f:
                reader = csv.DictReader(f)
                for row in reader:
                    index = row['Index']
                    Name = row['Name']
                    Selected = row['Selected'] == 'True'
                    self.insert(index, Name)
                    if Selected:
                        self.select_set(index)
        except:
            self.delete(0, tk.END)
            if path:
                files = SpiderDefaults.os.listdir(path)
                i = 0
                for fileName in files:
                    pos = fileName.find(JsonIO.Ext())
                    if pos != -1:
                        fileName = fileName[:pos]
                        self.insert(i, fileName)
                        i = i+1
        finally:
            if insertEND:
                if self.get(tk.END) != 'END':
                    self.insert(tk.END, 'END')

    def save(self):
        if(self.lbname):
            print("Save Reihenfolge {}".format(self.lbname))
            fieldnames = ['Index', 'Name', 'Selected']
            with open(self.lbname+'.csv', "w") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                li = self.get(0, tk.END)
                for i, name in enumerate(li):
                    writer.writerow(
                        {'Index': i, 'Name': name, 'Selected': self.selection_includes(i)})

    def form(self):
        '''
        Formatiert die Liste der Listbox und macht Einrückungen vor den Bewegungstexten
            sucht das 1. LOOP
                rückt rückwärts alle Zeilen bis zum 'Repeat' ein
            sucht das 2. LOPP usw.    
        '''
        listeTup = self.get(0, tk.END)
        liste=[]
        for li in listeTup:
            liste.append(li)
        #Alle Spaces rauswerfen, Positionen von 'LOOP' und 'Repeat' merken
        repeats=[]
        loops=[]
        x=len(liste)
        for i in range(0, len(liste) ):
            liste[i] = str(liste[i]).strip()
            if str(liste[i]).startswith('LOOP'):
                loops.append(i)
            if str(liste[i]).startswith('Repeat'):
                repeats.append(i)
        if len(repeats)>len(loops):
            return False
        for i in range(0,len(loops)):
            self.einruecken(liste,repeats[len(repeats)-i-1]+1,loops[i])
        self.delete(0,tk.END)
        for i in range(0,len(liste)):
            self.insert(i,liste[i])
        return True
        
    def einruecken(self,liste,von,bis):
        for i in range(von,bis):
            liste[i]='  '+liste[i]


    def myDelete(self, first, last=None):
        if first > self.size():
            first = self.size()
        if not last:
            last = first
        for i in range(first, last+1):
            if self.get(i) != 'END':
                self.delete(i)

    def setCurrent(self, event):
        ''' gets the current index of the clicked item in the listbox '''
        self.curIndex = self.nearest(event.y)

    def getState(self, event):
        ''' checks if the clicked item in listbox is selected '''
        i = self.nearest(event.y)
        self.curState = self.selection_includes(i)

    def shiftSelection(self, event):
        ''' shifts item up or down in listbox '''
        i = self.nearest(event.y)
        if self.curState == 1:
            self.selection_set(self.curIndex)
        else:
            self.selection_clear(self.curIndex)
        if i < self.curIndex:
            # Moves up
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i+1, x)
            if selected:
                self.selection_set(i+1)
            self.curIndex = i
        elif i > self.curIndex:
            # Moves down
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i-1, x)
            if selected:
                self.selection_set(i-1)
            self.curIndex = i


if __name__ == "__main__":
        # def printRightClickItem( event):
        #   ''' RK 14.12.18: gets the current text of the with the right button clicked item in the listbox '''
        #   curIndex = myListbox.nearest(event.y)
        #   print(f"Ausgewählt wurde: {myListbox.get(curIndex)}")
    root = tk.Tk()
    #myListbox = Drag_and_Drop_Listbox(root,name="myListbox")
    myListbox = Drag_and_Drop_Listbox(master=root)
    for i, name in enumerate(['name'+str(i) for i in range(10)]):
        myListbox.insert(tk.END, name)
        if i % 2 == 0:
            myListbox.selection_set(i)
    myListbox.pack(fill=tk.BOTH, expand=True)
    #listbox.bind('<Button-3>', printRightClickItem)
    myListbox.bind('<Button-3>', lambda event: print(
        "Ausgewählt wurde: {0}".format(myListbox.get(myListbox.nearest(event.y)))))
    root.mainloop()
