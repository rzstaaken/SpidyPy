import os
import tkinter as tk
from JsonIO import JsonIO
import Drag_and_Drop_Listbox as DDListbox


class GetSpidy(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Kopiert Dateien von GitHub ins eigene Verzeichnis ")
        #self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.listboxFiles=DDListbox.Drag_and_Drop_Listbox(self)
        self.listboxFiles.bind('<Button-3>', lambda event: self.doRightMouseClick( self.listboxFiles.get(self.listboxFiles.nearest(event.y))))     
        self.listboxFiles.grid(column=0, columnspan=1, row=0, rowspan=1, sticky='nw')
        self.fillListBox(self.listboxFiles)
        self.pack(padx=100, pady=50, fill="both")



    def fillListBox(self, lBox, path='.'):
        """
           Aus dem Directory posi werden die json-Dateien gelesen und
           in der listbox dargestellt.
        """
        lBox.delete(0, tk.END)
        files = os.listdir(path)
        i=0
        for fileName in files:
            pos = fileName.find(".py")
            if pos != -1:
                fileName = fileName[:pos]
                lBox.insert(i,fileName)
                i=i+1
    def doRightMouseClick(self,posName):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = GetSpidy(root )
    app.mainloop()