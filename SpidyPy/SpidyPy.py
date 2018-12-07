"""
SpidyPy.py 
https://github.com/rzstaaken/SpidyPy
"""


import tkinter
from JasonIO import *
import SpiderDefaults
from time import sleep
import threading
###import TrialPCA01

class ShowScale1(tkinter.Frame):

    def __init__(self, master=None,legsMinMax=None):
        super().__init__(master)
        self.name = tkinter.StringVar()
        self.legsMinMax=legsMinMax
        self.pack(padx=SpiderDefaults.PADX, pady=SpiderDefaults.PADX, fill="both")
        master.title("Spidy Move Application ")
        self.lockMe=threading.Lock()
        self.tr=None
        ###self.tr=TrialPCA01.Trial()
        self.createWidgets()

    def createWidgets(self):
        self.legScale=[]
        for i in range(0, len(self.legsMinMax)):
            #self.legScale.append(tkinter.Scale(self, relief='solid', from_=self.legsMinMax[i]["Min"], to=self.legsMinMax[i]["Max"], length=600, label="S" + str(i), resolution=0.01))
            self.legScale.append(tkinter.Scale(self, from_=self.legsMinMax[i]["Min"], to=self.legsMinMax[i]["Max"], length=600, label="S" + str(i), resolution=0.01))
            
            self.legScale[i].grid(row=0, column=i, rowspan=SpiderDefaults.ROWSPAN)
            self.legScale[i].Nummer = i
            self.legScale[i]['command'] = self.onCallbackAction(self.legScale[i])
            #self.legScale[i].config(from_ =3.0)    #So kann man nachträglich noch etwas ändern
            #self.legScale[i]['from_']=3.0          #So geht es ja auch!
            if (i+1)%3==0: #Um Zwischenräume einzufügen
                self.legScale[i].grid(ipadx=20)

        #self.frameName = tkinter.Frame(self)
        #self.frameName.grid(column=i+1,row=0)
        self.name.set("Pos")
        self.entryName = tkinter.Entry(self)
        #self.entryName.pack(side="left",padx=self.PadX,pady=self.PadY,fill="x")
        self.entryName["textvariable"] = self.name
        #self.entryName['width']=20
        self.entryName.grid(column=i+1, row=0,sticky='w')
        self.entryNum = tkinter.Entry(self, width=5)
        self.entryNum.grid(column=i+2, row=0,sticky='w')
        self.setNum(0)

        self.btnReset = tkinter.Button(self, text='Reset')
        self.btnReset["command"] = self.onReset
        self.btnReset.grid(column=i+1, columnspan=3, row=1, sticky='nw')
        self.btnEnter = tkinter.Button(self)
        self.btnEnter["text"] = "Übernehmen"
        self.btnEnter["command"] = self.onEnter
        self.btnEnter.grid(column=i+1, columnspan=3, row=1, sticky='ne')

        self.btnRep = tkinter.Button(self)
        self.btnRep["text"] = "Wiederholen"
        self.btnRep["command"] = self.onRep
        self.btnRep.grid(column=i+1, columnspan=3, row=2, sticky='ne')

        #Die Scrollbar funktioniert noch nicht
        self.scrollbar = tkinter.Scrollbar(self, orient='vertical')
        self.listboxMoves= tkinter.Listbox(self, yscrollcommand=self.scrollbar.set, selectmode='extended')
        #self.lbMoves['command']=onLbMovesTouch

        self.listboxMoves.grid(column=i+1, columnspan=3, row=3, rowspan=4, sticky='nw')
        self.fillListBox(self.listboxMoves)
        self.listboxMoves.bind('<<ListboxSelect>>', self.onSelectListbox)

        #lb = Listbox(frame, name='lb')
        #lb.bind('<<ListboxSelect>>', onselect)

    def onSelectListbox(self, evt):
        #self.lockMe.acquire()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        selLegs=SpiderDefaults.ReadDefLegs(filename='posi/' + value + '.json')
        dicBewegungen=self.getMotionsDictionaryList(selLegs) 
        #print(dicBewegungen)
        #self.animiereSliderStart(dicBewegungen)
        self.animiereSliderAsync(dicBewegungen)#----Überspringe Async 

    def animiereSliderStart(self, dicBewegungen):
        self.Fred = threading.Thread(target=self.animiereSliderAsync,args =(  dicBewegungen,))
        #self.Fred.target=self.animiereSliderAsync
        #self.Fred.args=dicBewegungen
        self.Fred.daemon=True
        self.Fred.start()
        #self.animiereSliderAsync(dicBewegungen)

    def animiereSliderAsync(self, dicBewegungen):
        #self.lockMe.acquire()
        moveList = []#Eine Liste der Bewegungen
        legNrList = []
        for key in dicBewegungen:
            moveList.append(dicBewegungen[key])
            legNrList.append(int(key))
        
        for i in range(0,len(moveList[0])):
            for indx in range(0,len(moveList)):
                #print("i={0};{1} ,".format(i,indx))
                self.legScale[legNrList[indx]].set(moveList[indx][i])
                self.update_idletasks()#Wichtig!!!!!!
            sleep(0.1)
        #self.lockMe.release()

    def xSteps(self,start,ziel,steps=10):
        """Liefert eine List von beliebigen Steps zwischen Start und Ziel
        """
        erg=[]
        wert=(ziel-start)/(steps)
        for i in range(1, steps+1):
            erg.append(round(start+wert*i,2))
        return erg

    def getMotionsDictionaryList(self, selLegs,steps=6):
        """Liefert ein Dictionary von Listen.
           In jeder Liste werden x Bewegungen, vom Start bis Ziel gespeichert.
           Der Startwert wird vom Slider (Scale) abgelesen
        """
        digBewegungen={}
        for i, wert in selLegs.items():
            start= self.legScale[int(i)].get()
            ziel = float(wert)
            digBewegungen[i] = self.xSteps(start,ziel,steps=steps)
        return digBewegungen

    def fillListBox(self, lBox, path='posi'):
        """
           Aus dem Directory posi werden die json-Dateien gelesen und
           in der listbox dargestellt.
        """
        lBox.delete(0, tkinter.END)
        files = SpiderDefaults.os.listdir(path)
        i=0
        for fileName in files:
            pos = fileName.find('.json')
            if pos != -1:
                fileName = fileName[:pos]
                lBox.insert(i,fileName)
                i=i+1

    def setNum(self, n):
        self.num = tkinter.IntVar()
        self.num.set(n)
        self.entryNum["textvariable"] = self.num

    def onExit(self):
        self.destroy()

    def onEnter(self):
        """
        Die Scale-Position in eine Datei schreiben
        """
        fname=self.entryName.get()
        nummer=self.entryNum.get()
        dic = {}
        for i in range(len(self.legScale)):
            if self.legScale[i]['bg'] != 'gray85':
                dic.update({i: self.legScale[i].get()})
        print(dic) 
        if not SpiderDefaults.os.path.exists(SpiderDefaults.posiPath):
            SpiderDefaults.os.mkdir(SpiderDefaults.posiPath)
        j=JasonIO()
        j.WriteP(dic, SpiderDefaults.posiPath + "/" + fname + nummer + ".json")
        self.setNum(int(nummer) + 1)
        self.onReset()      
        self.fillListBox(self.listboxMoves) #Die Listbox aktualisieren

    def move(self,posName):
        selLegs=SpiderDefaults.ReadDefLegs(filename='posi/' + x + '.json')
        dicBewegungen=self.getMotionsDictionaryList(selLegs) 
        #print(dicBewegungen)
        self.animiereSliderAsync(dicBewegungen)#----Überspringe Async 

    def onRep(self):
        x="oben0"
        print("Hallo")
        self.move(x)
        print(x)
        sleep(1.1)
        x="unten0"
        self.move(x)
        sleep(1.1)
        print(x)

    def onReset(self):
        for i in range(0, len(self.legScale)):
            self.legScale[i]['bg'] = 'gray85'

    def onAction(self, scale):
        #scale['bg']='#fff00f00f'    #'#000fff000'
        scale['bg'] = 'lemon chiffon'#'plum1'

        #print(scale.Nummer,scale.get())
        x=scale.get()
        #Nur mit RPi schritt ausführen
        if self.tr != None:
            self.tr.schritt(pos=x,channel=scale.Nummer)

    def onCallbackAction(self, scale):
        return lambda xxx: self.onAction(scale)

if __name__ == "__main__":
    _LegsMinMax = SpiderDefaults.ReadDefLegsIf()
    root = tkinter.Tk()
    app = ShowScale1(root, _LegsMinMax)
    #app = ShowScale(root)
    app.mainloop()

