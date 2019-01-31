import tkinter as tk
from ECom import ECom
from EListbox import EListbox

class EditLine(tk.Widget):

    def __init__(self, master,opa,myParent2,elistbox=None,listbox=None,popup_line_nr=0, **kw):
        #super().__init__(self.popup)
        self.master=master
        self.opa=opa
        self.myParent2=myParent2
        self.elistbox = elistbox
        self.listbox = listbox
        
        self.popup_line_nr = popup_line_nr

        self.line_is_selected=False
        if  self.popup_line_nr in listbox.curselection():
            self.line_is_selected=True

        st = self.listbox.get(self.popup_line_nr)
        #tk.Label(master, text="New Line:",width=20,takefocus=1, highlightthickness=2).pack(side="left")

        master.title("Original Line "+str(popup_line_nr)+" :"+st)
        
        self.retStr = st

        self.labelNew = tk.Label(master,text=st)
        #self.labelNew.configure(background='gray') 
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
                self.origStr = listbox.get(popup_line_nr)
                self.origECom = ECom.findECom(self.origStr)
                self.origNumber = ECom.getNumber(inpStr = self.origStr)
                self.data=self.origNumber
                self.entryVal.insert(tk.END,str(self.origNumber))

        x = self.opa.winfo_x()
        y = self.opa.winfo_y()
        w = 250#  self.opa.winfo_width()
        #h = self.master.winfo_height()  
        h=20
        dx=self.opa.winfo_width()-w
        dy=0
        self.master.geometry("{}x{}+{}+{}".format(w, h, x + dx, y + dy))

        #overrideredirect(True) 

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
        self.listbox.delete(self.popup_line_nr)
        self.listbox.insert(self.popup_line_nr,self.retStr)

        if self.line_is_selected:
            self.listbox.selection_set(self.popup_line_nr) #Wenn die popup Zeile selektiert war, dann die Zeile wieder selektieren

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


