#!/usr/bin/python3
"""
V0.22 05.02.2019 20:00 SpidyPy.py 
https://github.com/rzstaaken/SpidyPy
"""
import getpass
import os
import csv
import re
import time
from threading import Thread
from JsonIO import JsonIO
import tkinter as tk
import SpiderDefaults
from SpidyMenu import SpidyMenu
from time import sleep
import threading
import Drag_and_Drop_Listbox as DD_Listbox #Muss ein Fehler in VS-Code sein, anders geht es nicht!
from ECom import ECom
from ERunMode import ERunMode
from EListbox import EListbox
import datetime

if __name__ == "__main__":
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
        if withRPi:
            root.geometry("1700x600")
        else:
            root.geometry("1500x650")

        root.title("Spidy Moving Application ")
        self.lockMe=threading.Lock()
        self.tr=None
        if withRPi:
            self.tr=TrialPCA01.Trial()

        SpidyMenu(root,parent=self)
        self.createWidgets()

    def createOptionMenueOpRun(self,column=0,row=0):
        self.runModelst=[name for name,member in ERunMode.__members__.items()]#Schreibt die Name des Enums in eine Liste
        self.varRunMode=tk.StringVar()
        self.varRunMode.set(self.runModelst[0])
        self.opRunMode = tk.OptionMenu(root,self.varRunMode,*self.runModelst,command=self.opRunModeHandler)
        self.opRunMode['width']=20
        self.opRunMode.grid(column=column,row=row, ipadx=20)

    def opRunModeHandler(self, text):
        #print(text, self.varRunMode.get())
        print(text)
        self.runMode=self.runModelst.index(text)
        if self.runMode==ERunMode.IDLE.value:
            print("idle wurde gedrückt!")
        elif self.runMode==ERunMode.STEP.value:
            print("step wurde gedrückt!")
        elif self.runMode==ERunMode.SEQUENCE.value:
            print("sequenz wurde gedrückt!")
        elif self.runMode==ERunMode.AUTOMATIC.value:
            print("automatic wurde gedrückt!")

    def createWidgets(self):
        self.legScale=[]
        self.legCheckbutton=[]
        for i in range(0, len(self.legsMinMax)):
            breit=(i+1)%3==0           
            self.legScale.append(tk.Scale(root ,width=9,  from_= self.legsMinMax[i]["Min"], to=self.legsMinMax[i]["Max"], length=400, label="S" + str(i), resolution=0.01))  
            if "Start" in self.legsMinMax[i]:
                self.legScale[i].set(self.legsMinMax[i]["Start"])
            self.legScale[i].grid(row=0, column=i, rowspan=SpiderDefaults.ROWSPAN,sticky='w')
            self.legScale[i].Nummer = i
            self.legScale[i]['command'] = self.onCallbackAction(self.legScale[i])
            self.legScale[i]['bg'] = backgroundGray 
            
            # self.legCheckbutton.append(tk.Checkbutton(root))
            # self.legCheckbutton[i].Number = i
            # self.legCheckbutton[i].grid(row=15, column=i, rowspan=SpiderDefaults.ROWSPAN,padx=22, sticky='w')

            if breit:
                l=tk.Label(root, width=12)
                l.grid(row=19, column=i, rowspan=SpiderDefaults.ROWSPAN,sticky='w')

        self.outText = tk.Text(root, height=10, width=120)
        self.outText.grid(row=25, column=0, columnspan=12)
        self.outText.insert(tk.END,str(datetime.datetime.now())+" Started!")
        self.scrollbarOutText = tk.Scrollbar(root, orient='vertical',command=self.outText.yview)
        self.scrollbarOutText.grid(column=0, row=25,columnspan=12,sticky='nes')

        # self.name.set("Pos")
        # self.entryName = tk.Entry(root,width=32)
        # self.entryName["textvariable"] = self.name
        # self.entryName.grid(column=i+1, row=2, sticky='w')
        # self.entryNum = tk.Entry(root, width=5)
        # self.entryNum.grid(column=i+2, row=2,sticky='w')
        # self.setEntryNum(0)

        # self.btnReset = tk.Button(root, text='Reset',width=10)
        # self.btnReset["command"] = self.onReset
        # self.btnReset.grid(column=i+1, columnspan=1, row=3, sticky='w')

        # self.btnSave = tk.Button(root)
        # self.btnSave["text"] = "Save"
        # self.btnSave["command"] = self.onSaveAxis
        # self.btnSave.grid(column=i+1, columnspan=1, row=3)

        # self.btnSaveAllAxis = tk.Button(root)
        # self.btnSaveAllAxis["text"] = "Save All Axis"
        # self.btnSaveAllAxis["command"] = self.onSaveAllAxis
        # self.btnSaveAllAxis.grid(column=i+1, columnspan=1, row=3, sticky='e')

        #TODO:Die Scrollbar funktioniert noch nicht
        #self.scrollbar = tk.Scrollbar(self, orient='vertical')
        #self.scrollbar.grid(column=i+3,columnspan=3, row=4, rowspan=11)
        self.labelBew = tk.Label(root,text="Movings:")  #Bewegungen
        self.labelBew.grid(column=i+1, columnspan=3, row=4, sticky='nw')

        #Moving-Abschnitt
        self.listboxMoves=DD_Listbox.Drag_and_Drop_Listbox(root,myParent=self,lbname='listboxMoves',elistbox=EListbox.MOVES,height=20,width=30)
        self.listboxMoves.bind('<Button-2>', lambda event: self.move( self.listboxMoves.get(self.listboxMoves.nearest(event.y))))     
        #self.listboxMoves.bind('<Double-Button-1>', lambda event: self.delMove( self.listboxMoves.get(self.listboxMoves.nearest(event.y))))  
        self.listboxMoves.grid(column=i+1, row=5,rowspan=10)

        self.scrollbarMoves = tk.Scrollbar(root, orient='vertical',command=self.listboxMoves.yview)
        self.scrollbarMoves.grid(column=i+1, row=5,rowspan=10,sticky='nes')
        
        self.listboxMoves.fillListBox(path='posi')
        
        self.createOptionMenueOpRun(column=i+5,row=3)

        self.labelProcedure = tk.Label(root,text="Procedure:")# Sequenz jetzt Procedure (Ablauf)
        self.labelProcedure.grid(column=i+5, row=4)

        self.labelTimes= tk.Label(root, text = "Times:")
        self.labelTimes.grid(column=i+1, columnspan=1, row=17, sticky='nw')

        #Times Textfeld für die Anzahl der Wiederholungen
        entryTextTimes = tk.StringVar()
        self.entryTimes = tk.Entry(root,textvariable=entryTextTimes, width=5)
        entryTextTimes.set(1)
        self.entryTimes.grid(column=i+1, columnspan=1, row=17, sticky='ne')

        self.btnStart = tk.Button(root,width=10)
        self.btnStart["text"] = "Start"
        self.btnStart.bind('<ButtonPress-1>', self.onStart)
        self.btnStart.grid(column=i+1, columnspan=1, row=18, sticky='nw')

        # self.btnDelMovesLine = tk.Button(root,width=10)
        # self.btnDelMovesLine["text"] = "Delete Line"
        # self.btnDelMovesLine.bind('<ButtonPress-1>', self.onDelMovesLine)
        # self.btnDelMovesLine.grid(column=i+1, columnspan=1, row=18, sticky='ne')

        #Procedure-Box
        self.listboxProcedure=DD_Listbox.Drag_and_Drop_Listbox(root,myParent=self,lbname='listboxProcedure',elistbox=EListbox.PROCEDURE,height=20,width=33,exportselection=False)
        #self.listboxProcedure.bind('<Button-3>', lambda event: self.listboxProcedure.myDelete(self.listboxProcedure.nearest(event.y)))     
        self.listboxProcedure['selectmode'] = tk.SINGLE  #kw['selectmode'] = tk.MULTIPLE
        self.listboxProcedure.grid(column=i+5, row=5,rowspan=10)       
        self.listboxProcedure.fillListBox(procedure=True)

        self.scrollbarProcedure= tk.Scrollbar(root, orient='vertical',command=self.listboxProcedure.yview)
        self.scrollbarProcedure.grid(column=i+6, row=5,rowspan=10,sticky='nes')

        #Do Step
        self.btnDoStep = tk.Button(root,width=10)
        self.btnDoStep["text"] = "Do Step"
        self.btnDoStep.bind('<ButtonPress-1>', lambda event: self.varRunMode.set(self.runModelst[ERunMode.STEP.value]))
        self.btnDoStep.grid(column=i+5, columnspan=1, row=18, sticky='nw')

        #Do Sequence
        self.btnDoStep = tk.Button(root,width=10)
        self.btnDoStep["text"] = "Do Sequence"
        self.btnDoStep.bind('<ButtonPress-1>', lambda event: self.varRunMode.set(self.runModelst[ERunMode.SEQUENCE.value]))
        self.btnDoStep.grid(column=i+5, columnspan=1, row=18, sticky='ne')

        #Do Automatic
        self.btnDoAutomatic = tk.Button(root,width=10)
        self.btnDoAutomatic["text"] = "Do Automatic"
        self.btnDoAutomatic.bind('<ButtonPress-1>', lambda event: self.varRunMode.set(self.runModelst[ERunMode.AUTOMATIC.value]))
        self.btnDoAutomatic.grid(column=i+5, columnspan=1, row=19, sticky='nw')

        #Do Stop
        self.btnDoStop = tk.Button(root,width=10)
        self.btnDoStop["text"] = "Do Stop"
        self.btnDoStop.bind('<ButtonPress-1>', lambda event: self.varRunMode.set(self.runModelst[ERunMode.IDLE.value]))
        self.btnDoStop.grid(column=i+5, columnspan=1, row=19, sticky='ne')

        # #---->
        # self.btnToSeq = tk.Button(root,width=10)
        # self.btnToSeq["text"] = "---->"
        # self.btnToSeq.bind('<ButtonPress-1>', self.onToSeq)
        # self.btnToSeq.grid(column=i+3, row=5)

        self.master.protocol(name="WM_DELETE_WINDOW", func=self.spidy_exit) # Exit
        self.runMode=ERunMode.IDLE
        self.th_runner = Thread(target=self.runner,args=(0,))
        self.th_runner.setDaemon(True) #Damit lässt sich die Anwendung ohne Fehler beenden
        self.th_runner.start()

    def runner(self,a):
        global thread_started
        #lock.acquire()
        thread_started=True
        while True:
            #time.sleep(1)
            self.runMode=self.runModelst.index(self.varRunMode.get())
            #print("runner")
            if self.runMode==ERunMode.IDLE.value:
                #print("idle")
                pass
            elif self.runMode==ERunMode.STEP.value:
                #print("step")
                self.doStep()
            elif self.runMode==ERunMode.SEQUENCE.value:
                #print("sequenz")
                self.step()                     #Ohne die Betriebsart zu wechseln
                if self.getCurCommand()==ECom.End.__str__():  #':End'
                    self.doStep()           #Mach einen Schritt zur ersten Zeile und gehe in Idle
            elif self.runMode==ERunMode.AUTOMATIC.value:
                #print("automatic")
                self.step()                     #Ohne die Betriebsart zu wechseln
        thread_started=False
        #lock.release()
        
    def startSeq(self,mode=ERunMode.STEP): 
        self.varRunMode.set(self.runModelst[mode.value])
        while True:
            self.step()
            if self.varRunMode.get() != ERunMode.AUTOMATIC.value:
                break
            self.update()
            self.update_idletasks()#Wichtig!  ohne diese Zeile wird nur die letzte Position ausgegeben. 

    def doStep(self):
        self.varRunMode.set(self.runModelst[ERunMode.STEP.value])
        ret=self.step()
        if ret!= 0:
            self.varRunMode.set(self.runModelst[ERunMode.IDLE.value])
    
    def getCurCommand(self):
        cur=self.listboxProcedure.curselection()
        posName = self.listboxProcedure.get(cur)
        striped=posName.strip()
        return striped

    def getCurSpaces(self):
        cur=self.listboxProcedure.curselection()
        posName = self.listboxProcedure.get(cur)
        striped=posName.strip()
        spacesNr=len(posName) - len(striped)
        return ' ' * spacesNr #Liefert  x spaces

    def step(self):
        command= self.getCurCommand()
        if command[0:1]!=':':
            try:
                com=str(command).strip()
                self.move(com)
            except FileNotFoundError:
                self.outText.insert(tk.END,str("\nError: kann JSon-Datei nicht finden :"+com+JsonIO.Ext()))
                self.varRunMode.set(self.runModelst[ERunMode.IDLE.value])
                return -1 #Fehler
        if ECom.Wait.__str__() in command:   #:Wait
            cur=self.listboxProcedure.curselection()
            if len(cur)==1:
                n=cur[0]
                a=command.split(' ')
                start=float(a[1])
                klammerpos=str(a[2]).find("(")
                if(klammerpos>=0):
                    time.sleep(0.1)
                    ist=float(a[2][klammerpos+1:-1])
                    #start=int(p[initpos+len(ECom.Wait.__str__())+1:intposEnde+2])
                    spaces=self.getCurSpaces()
                    if ist<=0.1:#Sollwert erreicht -> ist = start
                        x=spaces + ECom.Wait.__str__() +' '+str(start)+' ('+"%.1f"%(start) +')'
                        self.listboxProcedure.delete(n)
                        self.listboxProcedure.insert(n,x)
                        n=n+1
                        self.listboxProcedure.select_set(n)
                        return 1 #Nächster Schritt melden
                    ist=ist-0.1
                    x=spaces + ECom.Wait.__str__() +' '+str(start)+' ('+ "%.1f"%(ist) +')'
                    self.listboxProcedure.delete(n)
                    self.listboxProcedure.insert(n,x)
                    self.listboxProcedure.select_set(n)
                    return 0 #Es wurde sich nicht bewegt
        n=self.nextStep()
        #print("nextStep={}".format(n))
        self.listboxProcedure.select_set(n)
        return 1 #Nächster Schritt melden

    def nextStep(self):
        cur=self.listboxProcedure.curselection()
        if len(cur)<1:#Keiner selektiert
            self.listboxProcedure.select_set(0)
            cur=self.listboxProcedure.curselection()
        if len(cur)>1:#Mehr als einer selektiert
            self.listboxProcedure.selection_clear(0,tk.END)
            self.listboxProcedure.select_set(cur[0])
            cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxProcedure.selection_clear(p)
            if ECom.End.__str__() in self.listboxProcedure.get(p):  # ':End'
                n=0
            elif ECom.LoopToLine.__str__()in self.listboxProcedure.get(p): 
                line = str(self.listboxProcedure.get(p)).strip() #Leerstellen rausnehmen
                a=line.split(' ')
                nr=int(a[1])
                ziel = self.listboxProcedure.get(nr)
                links=str(ziel).find("(")
                rep=ECom.Repeat.__str__()
                initpos=str(ziel).find(rep)
                intposEnde=str(ziel).find(" ",initpos+1)
                if(links>=0):
                    ist=int(ziel[links+1:-1])
                    start=int(ziel[initpos+len(rep)+1:intposEnde+2])
                    if ist<=1:#Sollwert erreicht -> ist = start
                        x=ziel[0:intposEnde+2]+' ('+str(start)+')'
                        self.listboxProcedure.delete(nr)
                        self.listboxProcedure.insert(nr,x)
                        n=p+1
                        return n
                    #Den Wert in Klammern um 1 vermindern
                    x=ziel[0:intposEnde+2]+' ('+str(ist-1)+')'
                    self.listboxProcedure.delete(nr)
                    self.listboxProcedure.insert(nr,x)
                n=nr
            else:
                n=p+1
            return n
        return 0

    def spidy_exit(self):
        self.is_mw = False 
        self.saveListboxes()
        self.master.quit() 
        self.master.destroy()

    def saveListboxes(self):
        self.listboxMoves.save()
        self.listboxProcedure.save()
        
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
            sleep(0.02)
        #self.lockMe.release()

    def xSteps(self,start,ziel,steps=10):
        """Liefert eine List von einer beliebigen Anzahl Steps zwischen Start und Ziel
        """
        erg=[]
        wert=(ziel-start)/(steps)
        for i in range(1, steps+1):
            erg.append(round(start+wert*i,2))
        return erg

    def getMotionsDictionaryList(self, selLegs,steps=40):
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

    # def setEntryNum(self, n):
    #     """
    #     Die Laufnummer in das Entry schreiben
    #     """
    #     self.num = tk.IntVar()
    #     self.num.set(n)
    #     self.entryNum["textvariable"] = self.num

    # def onExit(self):
    #     self.destroy()

    def onSaveAxis(self, all=False, fname=None):
        """
        Die Scale-Positionen in eine Datei schreiben
        """
        if fname == None:
            raise Exception('filename==None')
        self.listboxMoves.save()  # Erst mal csv-Datei schreiben falls sich die Positionen der Einträge geändert hat
        
        #fname=self.entryName.get()
        #nummer=self.entryNum.get()
        dic = {}
        for i in range(len(self.legScale)):
            if all==True:
                dic.update({i: self.legScale[i].get()})
            else:
                if self.legScale[i]['bg'] != backgroundGray:
                    dic.update({i: self.legScale[i].get()})
        #print(dic) 
        if not SpiderDefaults.os.path.exists(SpiderDefaults.posiPath):
            SpiderDefaults.os.mkdir(SpiderDefaults.posiPath)
        j=JsonIO()

        if str(fname).endswith(JsonIO.Ext()):
            j.WriteP(dic, os.path.join(SpiderDefaults.posiPath,"{0}".format(fname)))
        else:
            j.WriteP(dic, os.path.join(SpiderDefaults.posiPath,"{0}{1}".format(fname,JsonIO.Ext())))
        self.onReset()   
        #self.listboxMoves.delete(0, 'end')
        self.listboxMoves.fillListBox(path=SpiderDefaults.posiPath) #Die Listbox aktualisieren

    # def onSaveAllAxis(self):
    #     self.onSaveAxis(all=True)

    def onStart(self,event):
        self.btnStart.configure(state = tk.DISABLED)
        fileNamesIndxList = []
        fileNamesIndxList = self.listboxMoves.curselection()
        times=int(self.entryTimes.get())
        try:
            for i in range(times):
                for f in fileNamesIndxList:
                    fn = self.listboxMoves.get(f)
                    #print(f"({str(i)}) Es wird {fn} ausgeführt.")
                    #print("({0}) Es wird {1} ausgeführt.".format(str(i),fn))
                    self.move(fn)
                    i=i
        except:
            self.outText.insert(tk.END,str("Error: kann JSon-Datei nicht finden :"+fn+JsonIO.Ext()))
        finally:

            self.onReset()
            self.btnStart.configure(state = tk.NORMAL)

    def move(self,posName):
        try:
            #selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', f"{posName}{JsonIO.Ext()}"))
            selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', "{0}{1}".format(posName,JsonIO.Ext())))

            dicBewegungen=self.getMotionsDictionaryList(selLegs) 
            self.animiereSliderAsync(dicBewegungen)#----Überspringe Async 
        except FileNotFoundError:
            raise

    def selectLeg(self,num,select=True):
        if type(num) is int:
            if num < len(self.legScale): 
                if not select:
                    self.legScale[num]['bg'] = backgroundGray

    def onReset(self,event=None):
        for i in range(0, len(self.legScale)):
            self.selectLeg(i,False)

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
