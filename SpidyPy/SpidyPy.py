"""
V0.19 18.01.2019 8:45 SpidyPy.py 
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
import tkinter.messagebox as tkmb
import SpiderDefaults
from time import sleep
import threading
import Drag_and_Drop_Listbox as DDListbox
from enum import Enum
from ECom import ECom
from ERunMode import ERunMode
from LoopRepeat import LoopRepeat

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
        self.entryName.grid(column=i+1, row=2,sticky='w')
        self.entryNum = tk.Entry(root, width=5)
        self.entryNum.grid(column=i+2, row=2,sticky='w')
        self.setEntryNum(0)

        self.btnReset = tk.Button(root, text='Reset')
        self.btnReset["command"] = self.onReset
        self.btnReset.grid(column=i+1, columnspan=1, row=3, sticky='nw')

        self.btnSave = tk.Button(root)
        self.btnSave["text"] = "Save"
        self.btnSave["command"] = self.onSave
        self.btnSave.grid(column=i+1, columnspan=1, row=3, sticky='ne')

        #TODO:Die Scrollbar funktioniert noch nicht
        #self.scrollbar = tk.Scrollbar(self, orient='vertical')
        #self.scrollbar.grid(column=i+3,columnspan=3, row=4, rowspan=11)
        self.labelBew = tk.Label(root,text="Movings:")  #Bewegungen
        self.labelBew.grid(column=i+1, columnspan=3, row=4, sticky='nw')

        #Moving-Abschnitt
        self.createOptionMenueOpRun(column=i+4,row=3)

        self.labelProcedure = tk.Label(root,text="Procedure:")# Sequenz jetzt Procedure (Ablauf)
        self.labelProcedure.grid(column=i+4, row=4)

        self.listboxMoves=DDListbox.Drag_and_Drop_Listbox(root,lbname='listboxMoves',height=20)
        self.listboxMoves.bind('<Button-3>', lambda event: self.move( self.listboxMoves.get(self.listboxMoves.nearest(event.y))))     
        self.listboxMoves.bind('<Double-Button-1>', lambda event: self.delMove( self.listboxMoves.get(self.listboxMoves.nearest(event.y))))  
        self.listboxMoves.grid(column=i+1, row=5,rowspan=10)
        
        self.listboxMoves.fillListBox(path='posi')

        #
        self.labelTimes= tk.Label(root, text = "Times:")
        self.labelTimes.grid(column=i+1, columnspan=1, row=17, sticky='nw')

        #Times Textfeld für die Anzahl der Wiederholungen
        entryTextTimes = tk.StringVar()
        self.entryTimes = tk.Entry(root,textvariable=entryTextTimes, width=5)
        entryTextTimes.set(1)
        self.entryTimes.grid(column=i+1, columnspan=1, row=17, sticky='ne')

        self.btnStart = tk.Button(root)
        self.btnStart["text"] = "Start"
        self.btnStart.bind('<ButtonPress-1>', self.onStart)
        self.btnStart.grid(column=i+1, columnspan=3, row=18, sticky='nw')

        #Procedure-Box
        self.listboxProcedure=DDListbox.Drag_and_Drop_Listbox(root,lbname='listboxProcedure',height=20,width=33,exportselection=False)
        self.listboxProcedure.bind('<Button-3>', lambda event: self.listboxProcedure.myDelete(self.listboxProcedure.nearest(event.y)))     
        self.listboxProcedure['selectmode'] = tk.SINGLE  #kw['selectmode'] = tk.MULTIPLE
        self.listboxProcedure.grid(column=i+4, row=5,rowspan=10)       
        self.listboxProcedure.fillListBox(procedure=True)

        self.btnToSeq = tk.Button(root,width=10)
        self.btnToSeq["text"] = "---->"
        self.btnToSeq.bind('<ButtonPress-1>', self.onToSeq)
        self.btnToSeq.grid(column=i+2, row=5)

        #+1
        self.btnInc = tk.Button(root,width=10)
        self.btnInc["text"] = "  +1   "
        self.btnInc.bind('<ButtonPress-1>', self.onInc)
        self.btnInc.grid(column=i+2, columnspan=1, row=7, sticky='nw')

        #Repeat
        self.btnRep = tk.Button(root,width=10)
        self.btnRep["text"] = ECom.Repeat.__str__() +" 1"
        self.btnRep.bind('<ButtonPress-1>', self.onInsertRepeat)
        self.btnRep.grid(column=i+2, columnspan=1, row=8, sticky='nw')

        #-1
        self.btnDec = tk.Button(root,width=10)
        self.btnDec["text"] = "  -1   "
        self.btnDec.bind('<ButtonPress-1>', self.onDec)
        self.btnDec.grid(column=i+2, columnspan=1, row=9, sticky='nw')

        #LOOP
        self.btnLOOP = tk.Button(root,width=10)
        self.btnLOOP["text"] = ECom.LoopToLine.__str__()
        self.btnLOOP.bind('<ButtonPress-1>', self.onLOOP)
        self.btnLOOP.grid(column=i+2, columnspan=1, row=10, sticky='nw')

        #Wait
        self.btnWait = tk.Button(root,width=10)
        self.btnWait["text"] = ECom.Wait.__str__()+' 3.0'
        self.btnWait.bind('<ButtonPress-1>', self.onInsertWait)
        self.btnWait.grid(column=i+2, columnspan=1, row=11, sticky='nw')

        #Wait Textfeld (float) für die Sekunden
        self.vcmd = root.register(self.is_number)
        self.entryTextWaitSec = tk.StringVar()
        self.entryWaitSec = tk.Entry(root,justify='right',textvariable=self.entryTextWaitSec, width=12)
        self.entryTextWaitSec.set(2.5)
        self.entryWaitSec.grid(column=i+2, columnspan=1, row=13, sticky='nw')
        self.entryWaitSec['validate']='key'
        self.entryWaitSec['validatecommand']=(self.vcmd,'%P')
        #self.result.bind('<<UpdateNeeded>>', self.do_update)

        #Wait
        self.btnDelSequLine = tk.Button(root,width=10)
        self.btnDelSequLine["text"] = "Delete Line"
        self.btnDelSequLine.bind('<ButtonPress-1>', self.onDelSequLine)
        self.btnDelSequLine.grid(column=i+2, columnspan=1, row=14, sticky='nw')

        self.master.protocol(name="WM_DELETE_WINDOW", func=self.windowDelHandler) 
        self.runMode=ERunMode.IDLE
        self.th_runner = Thread(target=self.runner,args=(0,))
        self.th_runner.setDaemon(True) #Damit lässt sich die Anwendung ohne Fehler beenden
        self.th_runner.start()

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

    def do_update(self,event):
        w = event.widget
        number = float(self.entryWaitSec.get())
        w['text'] = '{}'.format(number)

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

            # if self.varRunMode.get() == ERunMode.IDLE.value:
            #     break
            # if self.varRunMode.get() == ERunMode.STEP.value:
            #     break
            self.update()
            self.update_idletasks()#Wichtig!  ohne diese Zeile wird nur die letzte Position ausgegeben. 
            
        #widget = self.listboxSequenz
        #widget.configure(state = tk.DISABLED)

    def doStep(self):
        self.varRunMode.set(self.runModelst[ERunMode.STEP.value])
        self.step()
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
            self.move(str(command).strip())
        if ECom.Wait.__str__() in command:
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
                        return 
                    ist=ist-0.1
                    x=spaces + ECom.Wait.__str__() +' '+str(start)+' ('+ "%.1f"%(ist) +')'
                    self.listboxProcedure.delete(n)
                    self.listboxProcedure.insert(n,x)
                    self.listboxProcedure.select_set(n)
                    return

        n=self.nextStep()
        #print("nextStep={}".format(n))
        self.listboxProcedure.select_set(n)

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


    def windowDelHandler(self):
        self.is_mw = False 
        self.saveListboxes()
        self.master.quit() 
        self.master.destroy()

    def saveListboxes(self):
        self.listboxMoves.save()
        self.listboxProcedure.save()

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
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            st=self.listboxProcedure.get(p)
            st=st.strip()
            a = st.split(' ')
            st = a[0]+' '+a[1]
            if p >= 0 and 'Repeat' in st:
                s=self.increment(st)
                self.listboxProcedure.delete(p)
                self.listboxProcedure.insert(p,s)
                self.listboxProcedure.check()
                self.listboxProcedure.select_set(p)
                return
        self.btnRep["text"] = self.increment(self.btnRep["text"])

    def onDec(self,event):
        #-1
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            st=self.listboxProcedure.get(p)
            st=st.strip()
            a = st.split(' ')
            st = a[0]+' '+a[1]
            if p >= 0 and ECom.Repeat.__str__() in st:
                s=self.decrement(st)
                self.listboxProcedure.delete(p)
                self.listboxProcedure.insert(p,s)
                self.listboxProcedure.check()
                self.listboxProcedure.select_set(p)
                return
        self.btnRep["text"] = self.decrement(self.btnRep["text"])

    def onInsertRepeat(self,event):
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxProcedure.selection_clear(p)
            self.listboxProcedure.insert(p,self.btnRep["text"])
            self.listboxProcedure.check()
            self.listboxProcedure.select_set(p)


    def onInsertWait(self,event):
        wert=self.entryWaitSec.get()
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxProcedure.selection_clear(p)
            self.listboxProcedure.insert(p,ECom.Wait.__str__()+' '+wert+ ' ('+wert+')')# TODO
            self.listboxProcedure.check()
            self.listboxProcedure.select_set(p)

    def onDelSequLine(self,event):
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxProcedure.delete(p)
            self.listboxProcedure.check()
            self.listboxProcedure.select_set(p)
            
    def onLOOP(self,event):
        #LOOP X
        cur=self.listboxProcedure.curselection()
        if len(cur)==1:
            p=cur[0]
            self.listboxProcedure.selection_clear(p)
            self.listboxProcedure.insert(p,self.btnLOOP["text"])
            self.onInsertWait(None)

    def onToSeq(self,event):
        #---->
        sz= self.listboxMoves.curselection()#liefert die Indexe der selektierten Zeilen
        items=[]
        for i in sz:
            items.append(self.listboxMoves.get(i))
        self.einfuegen(listbox=self.listboxProcedure,items=items)

    def einfuegen(self,listbox,items):
        cur=self.listboxProcedure.curselection()
        if len(cur)!=1:
            return
        p=cur[0]
        p2 = p
        for a in items:
            listbox.insert(p2,a)
        self.onInsertWait(None)     
        
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

    def onSave(self):
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

    def delMove(self,posName):
        filename= os.path.join( 'posi', "{0}{1}".format(posName,JsonIO.Ext()))
        print(posName)
        if tkmb.askyesno(title="Delete", message="Should the file \""+posName +"\" really be deleted?"):
            pass

    def move(self,posName):
        #selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', f"{posName}{JsonIO.Ext()}"))
        selLegs=SpiderDefaults.ReadDefLegs(filename= os.path.join( 'posi', "{0}{1}".format(posName,JsonIO.Ext())))
        dicBewegungen=self.getMotionsDictionaryList(selLegs) 
        #print(dicBewegungen)
        self.animiereSliderAsync(dicBewegungen)#----Überspringe Async 

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
