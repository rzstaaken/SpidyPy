import tkinter as tk
#from math import *
from ECom import ECom


class EditLine(tk.Widget):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master,parent=None,elistbox=None,listbox=None,lineNr=0, **kw):
        #super().__init__(self.popup)
        self.elistbox = elistbox
        self.listbox = listbox
        
        self.lineNr = lineNr
        st = self.listbox.get(self.lineNr)
        tk.Label(master, text="Neuer Float Wert:",width=20).pack(side="left")

        # self.entry = tk.Entry(master)
        # self.entry.bind("<Return>", self.evaluate)
        # self.entry.pack()
        # self.res = tk.Label(master)

        master.title("Ausgewählte Zeile:"+st)

        #tk.Label(master, text="Ausgewählte Zeile:",width=20).pack(side="left")
        
        self.labelOriginal = tk.Label(master,text=st)
        self.labelOriginal.configure(background='gray') 
        self.labelOriginal.pack(side="left")

        self.vcmd = master.register(self.is_number)
        self.entryTextWaitSec = tk.StringVar()
        self.entryWaitSec = tk.Entry(master,justify='right',textvariable=self.entryTextWaitSec, width=12)
        #self.entryWaitSec.grid(column=i+2, columnspan=1, row=13, sticky='nw')
        self.entryWaitSec['validate']='key'
        self.entryWaitSec['validatecommand']=(self.vcmd,'%P')
        self.entryWaitSec.pack(side="top")
        #self.entryTextWaitSec.set(2.5)

        #self.res.pack()

    def evaluate(self,event):
        print('Hier')
        #self.res.configure(text = "Ergebnis: " + str(eval(self.entry.get())))

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
        return True

    @staticmethod
    def insertNumber(self,inpStr,number):
        '''
        'number' ist ein int oder ein float
        Schreibt 'number=7.7' in beide Zahlenwerte in 'inpStr' mit
        inpStr sieht z.B. so aus '    :Wait 1.2 (1.2)'
        Das Return dann so       '    :Wait 7.7 (7.7)'
        '''
        dp = inpStr.find(':')#Führende Leerstellen merken
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!=2 and le!= 3:
            raise AttributeError("Der übergebene String hat nicht die nötige Struktur!")
        if le==3:
            if aIn[2][0] != '(' or aIn[2][-1] != ')':
                raise AttributeError("Der übergebene String hat nicht die nötige Struktur! 2.Wert nicht in ( und )")
        ret= ' '*dp+ aIn[0]+' '+str(number)
        if le==2:
            return ret
        return ret + ' ('+str(number)+')'

    @staticmethod
    def getNumber(self,inpStr):
        '''
        siehe insertNumber()
        Liefert den 1. Zahlenwert als int oder float
        '''
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!=2 and le!= 3:
            raise AttributeError("Der übergebene String hat nicht die Spidy-Anweisungs-Struktur!")
        try:
            return int(aIn[1])
        except ValueError:
            return float(aIn[1])

    @staticmethod
    def getSecondNumber(self,inpStr):
        '''
        siehe insertNumber()
        Liefert den 2. Zahlenwert als int oder float
        '''
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!= 3:
            raise AttributeError("Der übergebene String hat nicht die Spidy-Anweisungs-Struktur mit zweit Zahlenwerte!")
        v= aIn[2][1:-1]
        try:
            return int(v)
        except ValueError:
            return float(v)


if __name__ == "__main__":
    print("'"+EditLine.insertNumber(None,inpStr='    :Wait 1.2 (1.2)',number=7.7)+"'")
    print(EditLine.insertNumber(None,inpStr='    :Wait 1.2 (1.2)',number=float(7)))
    x= EditLine.getNumber(None,inpStr='    :Wait 1.2 (1.2)' )
    print(str(x))

    x= EditLine.getNumber(None,inpStr='    :Repeat 2 (2)' )
    print(str(x))

    x= EditLine.getSecondNumber(None,inpStr='    :Wait 7.2 (6.2)' )
    print(str(x))
    # root = tk.Tk()
    # popup = tk.Toplevel(root)
    # popup.wm_title("Input")
    # popup.tkraise(popup)
    # le=EditLine(root)
    # root.mainloop()
