import tkinter as tk
from math import *



class EditLine(tk.Widget):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master,parent=None,elistbox=None,listbox=None,lineNr=0, **kw):
        #super().__init__(self.popup)
        self.elistbox = elistbox
        self.listbox = listbox
        
        self.lineNr = lineNr
        st = self.listbox.get(self.lineNr)
        tk.Label(master, text="Neuer Ganzahliger Wert:",width=20).pack(side="left")

        self.textGanzeZeile = tk.Text(master,text=st)
        # self.entry = tk.Entry(master)
        # self.entry.bind("<Return>", self.evaluate)
        # self.entry.pack()
        # self.res = tk.Label(master)

        tk.Label(master, text="Ausgewählte Zeile:",width=20).pack(side="left")
        
        tk.Label(master, text="Neuer Ganzahliger Wert:",width=20).pack(side="left")

        self.vcmd = root.register(self.is_number)
        self.entryTextWaitSec = tk.StringVar()
        self.entryWaitSec = tk.Entry(root,justify='right',textvariable=self.entryTextWaitSec, width=12)
        #self.entryWaitSec.grid(column=i+2, columnspan=1, row=13, sticky='nw')
        self.entryWaitSec['validate']='key'
        self.entryWaitSec['validatecommand']=(self.vcmd,'%P')
        self.entryWaitSec.pack(side="top")
        #self.entryTextWaitSec.set(2.5)

        self.res.pack()

    def evaluate(self,event):
        self.res.configure(text = "Ergebnis: " + str(eval(self.entry.get())))

    # Callback functions
    def is_number(self,data):
        if data == '':
            return True
        try:
            float(data)
            #print('value:', data)
        except ValueError:
            return False
        self.btnWait['text']=ECom.Wait.__str__()+' '+data
        return True

if __name__ == "__main__":
    root = tk.Tk()
    popup = tk.Toplevel(root)
    popup.wm_title("Input")
    popup.tkraise(popup)
    le=EditLine(root)
    root.mainloop()
