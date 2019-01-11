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
from ECom import ECom

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

    def fillListBox(self, sequence=False, path=None):
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
            if len(self.curselection())==0: #Wenn nichts selektiert ist
                self.select_set(0)          #Die erste Zeile selektieren
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
            if sequence:
                if self.get(tk.END) != ECom.End.__str__():
                    self.insert(tk.END, ECom.End.__str__())
                self.form()

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
            sucht das 2. LOOP usw.    
        '''
        listeTup = self.get(0, tk.END)
        lines=[]
        for li in listeTup:
            lines.append(li)
        #Alle Spaces rauswerfen, Positionen von 'LOOP' und 'Repeat' merken
        repeatLines=[]
        loopToLineLines=[]
        loopToLineZiel=[]
        for i in range(0, len(lines) ):
            lines[i] = str(lines[i]).strip()
            if ECom.LoopToLine.__str__() in lines[i]:#:LoopToLine
                loopToLineLines.append(i)
                #sp=str(lines[i]).split()
                #if len(sp)==1:
                #    lines[i]=sp[0]+   Den zugehörigen 'Repeat'  ????
            if ECom.Repeat.__str__() in lines[i]:#:Repeat
                repeatLines.append(i)
        if len(repeatLines)!=len(loopToLineLines):
            return False
        lastRepeatPos = len(lines)
        for i in range(0,len(loopToLineLines)):#Check ob die LoopToLines zu den Repeat passen 
            
            if repeatLines[i] > lastRepeatPos:#<---?
                return False # LoopToLine weist auf falschen Repeat
        for i in range(0,len(loopToLineLines)):
            self.einruecken(lines,repeatLines[len(repeatLines)-i-1]+1,loopToLineLines[i])
        self.delete(0,tk.END)
        for i in range(0,len(lines)):
            self.insert(i,lines[i])
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
            if not  (ECom.End.__str__() in self.get(i)):  # not ':END'
                self.delete(i)
                self.check()

    def check(self):
        if self.form():
            #Alles OK
            self["bg"]='SystemWindow'
        else:
            #Es stimmt mit den Sequenzen etwas nicht
            self["bg"]='red2'

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
            self.check()
        elif i > self.curIndex:
            # Moves down
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i-1, x)
            if selected:
                self.selection_set(i-1)
            self.curIndex = i
            self.check()

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
