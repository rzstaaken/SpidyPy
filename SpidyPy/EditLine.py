import tkinter as tk
from ECom import ECom
from EListbox import EListbox

class EditLine(tk.Widget):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master,elistbox=None,listbox=None,lineNr=0, **kw):
        #super().__init__(self.popup)
        self.master=master
        self.elistbox = elistbox
        self.listbox = listbox
        
        self.lineNr = lineNr
        st = self.listbox.get(self.lineNr)
        tk.Label(master, text="New Line:",width=20,takefocus=1, highlightthickness=2).pack(side="left")

        master.title("Original Line "+str(lineNr)+" :"+st)
        
        self.retStr = st

        self.labelNew = tk.Label(master,text=st)
        self.labelNew.configure(background='gray') 
        self.labelNew.pack(side="left")

        self.vcmd = master.register(self.is_number)
        self.entryText = tk.StringVar()

        self.entryVal = tk.Entry(master,justify='right',textvariable=self.entryText, width=12,takefocus=1, highlightthickness=2)
        self.entryVal.bind("<Return>", self.ok)
        self.entryVal.bind("<Escape>", self.cancel)
        self.entryVal.bind("<Up>", self.specialKey)
        self.entryVal.bind("<Down>", self.specialKey)


        self.entryVal['validate']='key'

        self.entryVal['validatecommand']=(self.vcmd,'%P')
        self.entryVal.pack(side="top")
        self.entryVal.focus_set()

        if elistbox == EListbox.PROCEDURE:
            if listbox:
                self.origStr = listbox.get(lineNr)
                self.origECom = ECom.findECom(self.origStr)
                self.origNumber = ECom.getNumber(inpStr = self.origStr)
                self.data=self.origNumber
                self.entryVal.insert(tk.END,str(self.origNumber))

    def specialKey(self, event=None):
        if event.keysym == 'Up' and event.state == 262152:
            data=float(self.data)+1.0#set Value
        if event.keysym == 'Up' and event.state == 262153:#With Shift
            data=float(self.data)+10.0
        
        if event.keysym == 'Down' and event.state == 262152:
            data=float(self.data)-1.0#set Value
        if event.keysym == 'Down' and event.state == 262153:#With Shift
            data=float(self.data)-10.0
        if data>= ECom.get_min_val(self.origECom):
            self.entryVal.delete(0,tk.END)
            self.entryVal.insert(0,str(round(data,1)))
        #print(event.keysym+"   "+str(event.state))



    def ok(self, event=None):
        self.retStr=self.labelNew['text']
        self.listbox.delete(self.lineNr)
        self.listbox.insert(self.lineNr,self.retStr)
        self.master.destroy()
 
    def cancel(self, event=None):
        self.master.destroy()

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
        self.data=data
        return True

if __name__ == "__main__":
    pass


