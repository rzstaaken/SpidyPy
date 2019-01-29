import tkinter as tk
from ECom import ECom
from EListbox import EListbox


class EditLine(tk.Widget):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master,parent=None,elistbox=None,listbox=None,lineNr=0, **kw):
        #super().__init__(self.popup)

        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()


        self.elistbox = elistbox
        self.listbox = listbox
        
        self.lineNr = lineNr
        st = self.listbox.get(self.lineNr)
        tk.Label(master, text="Neuer Float Wert:",width=40).pack(side="left")

        master.title("Ausgewählte Zeile:"+st)
        
        self.retStr = st

        self.labelNew = tk.Label(master,text=st)
        self.labelNew.configure(background='gray') 
        self.labelNew.pack(side="left")

        self.vcmd = master.register(self.is_number)
        self.entryText = tk.StringVar()
        #self.entryText.set("Hello")
        self.entryVal = tk.Entry(master,justify='right',textvariable=self.entryText, width=12)
        self.entryVal.bind("<Return>", self.ok)
        self.entryVal.bind("<Escape>", self.cancel)
        self.entryVal['validate']='key'

        self.entryVal['validatecommand']=(self.vcmd,'%P')
        self.entryVal.pack(side="top")

        if elistbox == EListbox.PROCEDURE:
            if listbox:
                self.origStr = listbox.get(lineNr)
                self.origECom = ECom.findECom(self.origStr)
                self.origNumber = ECom.getNumber(inpStr = self.origStr)
                self.entryVal.insert(tk.END,str(self.origNumber))

    def ok(self, event=None):
        #print "Has escrito ...", self.e.get()
        #self.valor.set(self.e.get())
        self.retStr=self.labelNew['text']
        self.top.destroy()
 
    def cancel(self, event=None):
        self.top.destroy()

    # Callback functions
    def is_number(self,data):
        if data == '':
            return True
        try:
            float(data)
            #print('value:', data)
        except ValueError:
            return False
        #self.btnWait['text']=ECom.Wait.__str__()+' '+data
        self.labelNew['text']=ECom.insertNumber(inpStr= self.origStr,number=data)
        return True

if __name__ == "__main__":
    pass


