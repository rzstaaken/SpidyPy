"""
V0.18 09.01.2019 15:00 SpidyPy.py 
https://github.com/rzstaaken/SpidyPy
"""

import getpass
import os
import csv
import re
from JsonIO import JsonIO
import tkinter as tk
import SpiderDefaults
from time import sleep
import threading
import Drag_and_Drop_Listbox as DDListbox
from enum import Enum
from ECom import ECom

lastNum = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')
backgroundGray = 'gray93' #Anders geht es beim RPi nicht 85
withRPi = False # Keine Hardware angeschlossen
if getpass.getuser() == 'pi':
    import TrialPCA01
    withRPi = True # Das Prg. läuft auf dem RPi
    print('Das Prg. läuft auf dem RPi!')
else:
    print('Das Prg. läuft NICHT auf dem RPi!')


class SpidyPy(tk.Frame):

    def __init__(self, root=None,legsMinMax=None):
        super().__init__(root)
        self.name = tk.StringVar()
        self.legsMinMax=legsMinMax
        self.master=root
        #self.pack(padx=SpiderDefaults.PADX, pady=SpiderDefaults.PADX, fill="both")
        root.geometry("1500x500") 
        root.title("Spidy Moving Application ")
        self.lockMe=threading.Lock()
        self.tr=None
        if withRPi:
            self.tr=TrialPCA01.Trial()
        self.createWidgets()

    def createWidgets(self):
        self.legScale=[]
        for i in range(0, len(self.legsMinMax)):
            self.legScale.append(tk.Scale(root ,  from_= self.legsMinMax[i]["Min"], to=self.legsMinMax[i]["Max"], length=400, label="S" + str(i), resolution=0.01))  
            if "Start" in self.legsMinMax[i]:
                self.legScale[i].set(self.legsMinMax[i]["Start"])
            self.legScale[i].grid(row=0, column=i, rowspan=SpiderDefaults.ROWSPAN)
            self.legScale[i].Nummer = i
            self.legScale[i]['command'] = self.onCallbackAction(self.legScale[i])
            self.legScale[i]['bg'] = backgroundGray #Neu
            if (i+1)%3==0: #Um Zwischenräume einzufügen
                self.legScale[i].grid(ipadx=20)

        self.name.set("Pos")
        self.entryName = tk.Entry(root)
        self.entryName["textvariable"] = self.name
        self.entryName.grid(column=i+1, row=0,sticky='w')
        self.entryNum = tk.Entry(root, width=5)
        self.entryNum.grid(column=i+2, row=0,sticky='w')
        self.setEntryNum(0)

        self.btnReset = tk.Button(root, text='Reset')
        self.btnReset["command"] = self.onReset
        self.btnReset.grid(column=i+1, columnspan=3, row=1, sticky='nw')
        self.btnEnter = tk.Button(root)
        self.btnEnter["text"] = "Save"
        self.btnEnter["command"] = self.onEnter
        self.btnEnter.grid(column=i+1, columnspan=3, row=1, sticky='ne')

        self.labelTimes= tk.Label(root, text = "Times:")
        self.labelTimes.grid(column=i+1, columnspan=3, row=2, sticky='nw')
        #Times Textfeld für die Anzahl der wiederholungen
        entryTextTimes = tk.StringVar()
        self.entryTimes = tk.Entry(root,textvariable=entryTextTimes, width=5)
        entryTextTimes.set(1)
        self.entryTimes.grid(column=i+1, columnspan=3, row=2, sticky='ne')

        self.btnStart = tk.Button(root)
        self.btnStart["text"] = "Start"
        self.btnStart.bind('<ButtonPress-1>', self.onStart)
        self.btnStart.grid(column=i+1, columnspan=3, row=3, sticky='nw')

        #TODO:Die Scrollbar funktioniert noch nicht
        #self.scrollbar = tk.Scrollbar(self, orient='vertical')
        #self.scrollbar.grid(column=i+3,columnspan=3, row=4, rowspan=11)
        self.labelBew = tk.Label(root,text="Bewegungen:")
        self.labelBew.grid(column=i+1, columnspan=3, row=4, sticky='nw')

        self.labelSeq = tk.Label(root,text="Sequenzen:")
        self.labelSeq.grid(column=i+4, columnspan=3, row=4, sticky='nw')

        self.listboxMoves=DDListbox.Drag_and_Drop_Listbox(root,lbname='listboxMoves',height=20)
        self.listboxMoves.bind('<Button-3>', lambda event: self.move( self.listboxMoves.get(self.listboxMoves.nearest(event.y))))     
        self.listboxMoves.grid(column=i+1, columnspan=3, row=5, rowspan=11, sticky='nw')
        self.listboxMoves.fillListBox(path='posi')

        #Sequenz-Box
        self.listboxSequenz=DDListbox.Drag_and_Drop_Listbox(root,lbname='listboxSequenz',height=20,exportselection=False)
        self.listboxSequenz.bind('<Button-3>', lambda event: self.listboxSequenz.myDelete(self.listboxSequenz.nearest(event.y)))     
        self.listboxSequenz['selectmode'] = tk.SINGLE  #kw['selectmode'] = tk.MULTIPLE
        self.listboxSequenz.grid(column=i+4, columnspan=3, row=5, rowspan=11, sticky='nw')
        self.listboxSequenz.fillListBox(insertEND=True)

        self.btnStartSeq = tk.Button(root)
        self.btnStartSeq["text"] = "Start Seq."
        self.btnStartSeq.bind('<ButtonPress-1>', self.onStartSeq)
        self.btnStartSeq.grid(column=i+4, row=17, sticky='nw')

        self.btnStopSeq = tk.Button(root)
        self.btnStopSeq["text"] = "Stop Seq."
        self.btnStopSeq.bind('<ButtonPress-1>', self.onStopSeq)
        self.btnStopSeq.grid(column=i+5, row=17, sticky='nw')

        self.btnToSeq = tk.Button(root)
        self.btnToSeq["text"] = "---->"
        self.btnToSeq.bind('<ButtonPress-1>', self.onToSeq)
        self.btnToSeq.grid(column=i+2, columnspan=1, row=5, sticky='nw')

        #+1
        self.btnInc = tk.Button(root)
        self.btnInc["text"] = "  +1   "
        self.btnInc.bind('<ButtonPress-1>', self.onInc)
        self.btnInc.grid(column=i+2, columnspan=1, row=7, sticky='nw')

        #Repeats
        self.btnRep = tk.Button(root)
        self.btnRep["text"] = ECom.Repeat.__str__() +" 1"
        self.btnRep.bind('<ButtonPress-1>', self.onInsertRepeat)
        self.btnRep.grid(column=i+2, columnspan=1, row=8, sticky='nw')

        #-1
        self.btnDec = tk.Button(root)
        self.btnDec["text"] = "  -1   "
        self.btnDec.bind('<ButtonPress-1>', self.onDec)
        self.btnDec.grid(column=i+2, columnspan=1, row=9, sticky='nw')

        #LOOP
        self.btnLOOP = tk.Button(root)
        self.btnLOOP["text"] = ECom.LOOP.__str__()
        self.btnLOOP.bind('<ButtonPress-1>', self.onLOOP)
        self.btnLOOP.grid(column=i+2, columnspan=1, row=10, sticky='nw')

        #check
        self.btnCheck = tk.Button(root)
        self.btnCheck["text"] = " Check "
        self.btnCheck.bind('<ButtonPress-1>', self.onCheck)
        self.btnCheck.grid(column=i+2, columnspan=1, row=11, sticky='nw')

        self.master.protocol(name="WM_DELETE_WINDOW", func=self.windowDelHandler) 

    def onStartSeq(self,event):
        event.widget.configure(state = tk.DISABLED)
        fileNamesIndxList = []
        fileNamesIndxList = self.listboxSequenz.get(0,tk.END)
        for i in range(0,len( fileNamesIndxList)):
            sequenz = fileNamesIndxList[i]
            #self.listboxSequenz.cur
            self.listboxSequenz.selection_clear(0,tk.END)
            self.listboxSequenz.select_set(i)
            self.update_idletasks()#Wichtig!  ohne diese Zeile wird nur die letzte Position ausgegeben. 
            #sleep(0.5)
            print("{}:Es wird \'{}\' ausgeführt.".format(i,sequenz))
            if ECom.LOOP.__str__() in sequenz:
                continue
            if ECom.Repeat.__str__() in sequenz:
                continue
            if ECom.END.__str__() in sequenz:
                continue
            self.move(str(sequenz).strip())
        self.onReset()
        event.widget.configure(state = tk.NORMAL)

    def onStopSeq(self,event):
        pass

    def onCheck(self,event):
        self.listboxSequenz.check()

    def windowDelHandler(self): 
        self.is_mw = False 
        self.saveListboxes()
        self.master.quit() 
        self.master.destroy()

    def saveListboxes(self):
        self.listboxMoves.save()
        self.listboxSequenz.save()

    def increment(self,s):
        """ look for the last sequence of number(s) in a string and increment """
        m = lastNum.search(s)
        if m:
            next = str(int(m.group(1))+1)
            start, end = m.span(1)
            s = s[:max(end-len(next), start)] + next + s[end:]
        return s

    def decrement(self,s,min=1):
        """ look for the last sequence of number(s) in a string and decrement """
        m = lastNum.search(s)
        if m:
            if int(m.group(1)) < min+1:
                return s
            next = str(int(m.group(1))-1)
            start, end = m.span(1)
            s = s[:max(end-len(next), start)] + next + s[end:]
        return s

    def onInc(self,event):
        #+1
        #Testen ob die Sequenzen selektiert sind und ein Repeat ausgewählt ist
        cur=self.listboxSequenz.curselection()
        if len(cur)==1:
            p=cur[0]
            st=self.listboxSequenz.get(p)
            if p >= 0 and 'Repeat' in st:
                s=self.increment(st)
                self.listboxSequenz.delete(p)
                self.listboxSequenz.insert(p,s)
                self.listboxSequenz.select_set(p)
                return
        self.btnRep["text"] = self.increment(self.btnRep["text"])

    def onDec(self,event):
        #-1
        cur=self.listboxSequenz.curselection()
        if len(cur)==1:
            p=cur[0]
            st=self.listboxSequenz.get(p)
            if p >= 0 and ECom.Repeat.__str__() in st:
                s=self.decrement(st)
                self.listboxSequenz.delete(p)
                self.listboxSequenz.insert(p,s)
                self.listboxSequenz.select_set(p)
                return
        self.btnRep["text"] = self.decrement(self.btnRep["text"])

    def onInsertRepeat(self,event):
        #
        cur=self.listboxSequenz.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxSequenz.selection_clear(p)
            self.listboxSequenz.insert(p,self.btnRep["text"])
            self.onCheck(None)

    def onLOOP(self,event):
        #LOOP X
        cur=self.listboxSequenz.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxSequenz.selection_clear(p)
            self.listboxSequenz.insert(p,self.btnLOOP["text"])
            self.onCheck(None)

    def onToSeq(self,event):
        #---->
        sz= self.listboxMoves.curselection()#liefert die Indexe der selektierten Zeilen
        items=[]
        for i in sz:
            items.append(self.listboxMoves.get(i))
        self.einfuegen(listbox=self.listboxSequenz,items=items)

    def einfuegen(self,listbox,items):
        cur=self.listboxSequenz.curselection()
        if len(cur)!=1:
            return
        p=cur[0]
        p2 = p
        for a in items:
            listbox.insert(p2,a)
        self.onCheck(None)     
        
    def animiereSliderStart(self,dicBewegungen):
        self.Fred = threading.Thread(target=self.animiereSliderAsync,args =(  dicBewegungen,))
        self.Fred.daemon=True
        self.Fred.start()

    def animiereSliderAsync(self, dicBewegungen):
        if len(dicBewegungen)==0:
            return
        moveList = [] #Eine Liste der Bewegungen
        legNrList = []
        for key in dicBewegungen:
            moveList.append(dicBewegungen[key])
            legNrList.append(int(key))      
        for i in range(0,len(moveList[0])):
            for indx in range(0,len(moveList)):
                #print("i={0};{1} ,".format(i,indx))
                self.legScale[legNrList[indx]].set(moveList[indx][i])
            self.update_idletasks()#Wichtig!  ohne diese Zeile wird nur die letzte Position ausgegeben. 
            sleep(0.5)
        #self.lockMe.release()

    def xSteps(self,start,ziel,steps=10):
        """Liefert eine List von einer beliebigen Anzahl Steps zwischen Start und Ziel
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

    def setEntryNum(self, n):
        """
        Die Laufnummer in das Entry schreiben
        """
        self.num = tk.IntVar()
        self.num.set(n)
        self.entryNum["textvariable"] = self.num

    def onExit(self):
        self.destroy()

    def onEnter(self):
        """
        Die Scale-Positionen in eine Datei schreiben
        """
        fname=self.entryName.get()
        nummer=self.entryNum.get()
        dic = {}
        for i in range(len(self.legScale)):
            if self.legScale[i]['bg'] != backgroundGray:
                dic.update({i: self.legScale[i].get()})
        print(dic) 
        if not SpiderDefaults.os.path.exists(SpiderDefaults.posiPath):
            SpiderDefaults.os.mkdir(SpiderDefaults.posiPath)
        j=JsonIO()
        #j.WriteP(dic, os.path.join(SpiderDefaults.posiPath,f"{fname}{nummer}{JsonIO.Ext()}"))
        j.WriteP(dic, os.path.join(SpiderDefaults.posiPath,"{0}{1}{2}".format(fname,nummer,JsonIO.Ext())))
        self.setEntryNum(int(nummer) + 1)
        self.onReset()      
        self.listboxMoves.fillListBox() #Die Listbox aktualisieren

    def move(self,posName):
        #selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', f"{posName}{JsonIO.Ext()}"))
        selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', "{0}{1}".format(posName,JsonIO.Ext())))
        dicBewegungen=self.getMotionsDictionaryList(selLegs) 
        #print(dicBewegungen)
        self.animiereSliderAsync(dicBewegungen)#----Überspringe Async 

    def onStart(self,event):
        self.btnStart.configure(state = tk.DISABLED)
        fileNamesIndxList = []
        fileNamesIndxList = self.listboxMoves.curselection()
        times=int(self.entryTimes.get())
        for i in range(times):
            for f in fileNamesIndxList:
                fn = self.listboxMoves.get(f)
                #print(f"({str(i)}) Es wird {fn} ausgeführt.")
                print("({0}) Es wird {1} ausgeführt.".format(str(i),fn))
                self.move(fn)
        self.onReset()
        self.btnStart.configure(state = tk.NORMAL)

    def scaleGray(self,num):
        if type(num) is int:
            if num < len(self.legScale): 
                self.legScale[num]['bg'] = backgroundGray

    def onReset(self):
        for i in range(0, len(self.legScale)):
            self.scaleGray(i)

    def onAction(self, scale):
        scale['bg'] = 'lemon chiffon'#'plum1'
        x=scale.get()
        #Nur mit RPi Schritt ausführen
        if self.tr != None:
            self.tr.schritt(pos=x,channel=scale.Nummer)

    def onCallbackAction(self, scale):
        return lambda xxx: self.onAction(scale)

if __name__ == "__main__":
    _LegsMinMax = SpiderDefaults.ReadDefLegsIf()
    root = tk.Tk()
    app = SpidyPy(root=root, legsMinMax= _LegsMinMax)
    app.mainloop()
