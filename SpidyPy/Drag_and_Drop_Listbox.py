# Version 0.4
# Aus 'stackoverflow.com' 'tkinter listbox drag and drop with python'
# https://stackoverflow.com/questions/14459993/tkinter-listbox-drag-and-drop-with-python/39300853#39300853
# Danke 'Moshe'
# Vielen Dank 'Jarad' für die auf Selectmode 'MULTIPLE' umgeschriebene Fassung

# Wenn 'name' angegeben wird, wird die Reihenfolge und der Inhalt als CSV gespeichert.
#   Filename ist dann name.csv
import sys
import os
import tkinter as tk
import tkinter.messagebox as tkmb
import csv
from JsonIO import JsonIO
import SpiderDefaults
from ECom import ECom
from LoopRepeat import LoopRepeat
from EListbox import EListbox
from EditLine import EditLine


class Drag_and_Drop_Listbox(tk.Listbox):
    """ A tk listbox with drag'n'drop reordering of entries. """

    def __init__(self, master,myParent=None, lbname=None,elistbox=None, **kw):
        kw['selectmode'] = tk.MULTIPLE
        kw['activestyle'] = 'none'
        tk.Listbox.__init__(self, master, kw)
        self.master=master
        self.myParent=myParent
        self.curIndex = None
        self.curIndex3 = None
        self.curState = None
        self.lbname = lbname
        self.elistbox = elistbox
        self.is_mw = True
        self.bind('<Button-1>', self.getState, add='+')
        self.bind('<Button-1>', self.setCurrent, add='+')
        self.bind('<B1-Motion>', self.shiftSelection)

        self.insertStr = "Insert"
        #self.bind('<<ListboxSelect>>', self.save)
        self.popup_menu = tk.Menu(self, tearoff=0)
        if self.elistbox!=None:
            self.popup_menu.add_command(label="------", command=self.doNothing,state="disabled")
            if self.elistbox == EListbox.MOVES:
                self.popup_menu.add_command(label="Do Move", command=self.doMove)

            self.popup_menu.add_command(label="Delete", command= self.delete_line)
            if self.elistbox == EListbox.PROCEDURE:
                self.popup_menu.add_command(label="Edit", command= self.edit_line)
                self.popup_menu.add_command(label=self.insertStr +' '+ECom.getStr(ECom.LoopToLine)    , command= self.insertLoopToLine)
                self.popup_menu.add_command(label=self.insertStr +' '+ECom.getStr(ECom.Repeat)    , command= self.insertRepeat)
                self.popup_menu.add_command(label=self.insertStr +' '+ECom.getStr(ECom.Wait)    , command= self.insertWait)

            self.bind("<Button-3>", self.popup,add='+' ) 

# Popup
    def popup(self, event):
        try:
            self.myevent=event  # nicht schön aber selten
            #self.popup_menu.config()
            #Die aktuelle Zeile merken, weil sich der Mauszeiger verschiebt 
            self.popup_line_nr = self.nearest(self.myevent.y)
            self.puLineStr = self.get(self.nearest(self.myevent.y))
            eCom = ECom.findECom(self.puLineStr)
            if self.elistbox==EListbox.PROCEDURE:
                if eCom == None or eCom == ECom.LoopToLine:
                    self.popup_menu.entryconfig("Edit", state="disabled")
                else:
                    print("Commando zum editieren gefunden")
                    self.popup_menu.entryconfig("Edit", state="normal")

                
                #insert
                #self.popup_menu.entryconfig( "Insert ", state="normal")

            #nnn

            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
            #self.popup_menu.
        finally:
            self.popup_menu.grab_release()
    
    def doNothing(self):
        pass

    def insertLoopToLine(self):
        self.insertCom(ECom.LoopToLine)

    def insertRepeat(self):
        self.insertCom(ECom.Repeat)

    def insertWait(self):
        self.insertCom(ECom.Wait)

    def insertCom(self,com):
        sel_set=False
        line=self.popup_line_nr 
        cur=self.curselection()
        if len(cur)==1 and cur[0]==line:
            sel_set=True# Die Zeile war selektiert
        self.selection_clear(line)
        s="" 
        if com==ECom.LoopToLine:
            pass        
        if com==ECom.Repeat:
            s=' 1 (1)'
        if com==ECom.Wait:
            s=' 1.0 (1.0)' 
        self.insert(line,ECom.getStr(com)+s)
        self.check()
        if sel_set:
            self.selection_set(line) #Wenn die selektierte Zeile war, dann die Zeile wieder selektieren

    # def onInsertRepeat(self,event):
    #     cur=self.listboxProcedure.curselection()
    #     if len(cur)==1:
    #         p=cur[0]
    #         self.listboxProcedure.selection_clear(p)
    #         self.listboxProcedure.insert(p,self.btnRep["text"])
    #         self.listboxProcedure.check()
    #         self.listboxProcedure.select_set(p)


    # def onInsertWait(self,event):
    #     wert=self.entryWaitSec.get()
    #     cur=self.listboxProcedure.curselection()
    #     if len(cur)==1:
    #         p=cur[0]
    #         self.listboxProcedure.selection_clear(p)
    #         self.listboxProcedure.insert(p,ECom.Wait.__str__()+' '+wert+ ' ('+wert+')')# TODO
    #         self.listboxProcedure.check()
    #         self.listboxProcedure.select_set(p)

    # def onLOOP(self,event):
    #     #LOOP X
    #     cur=self.listboxProcedure.curselection()
    #     if len(cur)==1:
    #         p=cur[0]
    #         self.listboxProcedure.selection_clear(p)
    #         self.listboxProcedure.insert(p,self.btnLOOP["text"])
    #         self.onInsertWait(None)

    def delete_line(self):
        sel_set=False
        line=self.popup_line_nr #self.nearest(self.myevent.y)
        if self.elistbox == EListbox.MOVES:
            file=self.get(line)
            if not self.delMove(file):  # Zeigt Messagebox, bei ja wird gelöscht
                return
        elif self.elistbox == EListbox.PROCEDURE:
            if ECom.End.__str__() in self.get(line):  # bei ':END' 
                return  # nichts nachen
        cur = self.curselection()
        if len(cur)==1 and cur[0]==line:
            sel_set=True
        self.delete(line)
        self.check()
        if sel_set:
            self.selection_set(line) #Wenn die selektierte Zeile gelöscht wurde, dann die Zeile wieder selektieren

    def doMove(self):
        line=self.popup_line_nr  #self.nearest(self.myevent.y)
        if self.myParent:
            file=self.get(line)
            self.myParent.move(file)  # nicht schön!

    def delMove(self,posName):
        filename= os.path.join( 'posi', "{0}{1}".format(posName,JsonIO.Ext()))
        print(posName)
        if tkmb.askyesno(title="Delete", message="Should the file \""+filename +"\" really be deleted?"):
            #os.rename(src=filename,dst=filename+".bak")
            os.remove(src=filename,dst=filename)
            return True
        return False

    def edit_line(self):
        self.my_top = tk.Toplevel(self)       
        self.my_top.transient(self)
        self.my_top.grab_set()
        EditLine(self.my_top,myParent2=self.myParent, opa=self.master, elistbox = self.elistbox, listbox = self, popup_line_nr = self.popup_line_nr)
        self.master.wait_window(self.my_top)
    

#ende popup

    def fillListBox(self, procedure=False, path=None):
        """
            Aus dem Directory path werden die json-Dateien gelesen und
            in der listbox dargestellt.
        """
        try:
            self.delete(0, tk.END)            
            index=0
            # Wenn die CSV-Datei existiert wird sie benutzt, Eventuell gibt es diese Dateien nicht mehr oder einige sind hinzugekommen
            with open(self.lbname+'.csv', "r")as f:
                reader = csv.DictReader(f)
                for row in reader:
                    index = row['Index']
                    Name = row['Name']
                    Selected = row['Selected'] == 'True'
                    self.insert(index, Name)
                    if Selected:
                        self.select_set(index)
            
        except:
            #Das Einlesen der Datei mit der Reihenfolge hat nicht funktioniert.
            #Dann einfach das Directory -> listbox
            self.delete(0, tk.END)
            if path:
                #files = SpiderDefaults.os.listdir(path)
                fnames=self.getAllFileExt(path=path,ext=JsonIO.Ext())
                i = 0
                for fileName in fnames:
                    self.insert(i, fileName)
                    i = i+1
        finally:
            if procedure:
                if self.get(tk.END) != ECom.End.__str__():
                    self.insert(tk.END, ECom.End.__str__())
                self.form()
                if len(self.curselection())==0: #Wenn nichts selektiert ist
                    self.select_set(0)          #Die erste Zeile selektieren
            if path:
                self.nichtExistenteFilesEntfernen(path)
                self.save()


    def nichtExistenteFilesEntfernen(self,path):
        fnames=self.getAllFileExt(path=path,ext=JsonIO.Ext())
        li = self.get(0,tk.END)

        for i in reversed( range(len(li))): #Schleife rückwärts um fehlende Files zu löschen
            if not (self.get(i) in fnames):
                self.delete(i)
                
        li = self.get(0,tk.END)
        #Neue Files eintragen
        for fileName in fnames:
            if not fileName in li:
                self.insert(tk.END,fileName)
                print(fileName+" eingetragen!")
        

    def getAllFileExt(self,path,ext):
        names=[]
        files = SpiderDefaults.os.listdir(path)
        for fileName in files:
            pos = fileName.find(ext)
            if pos != -1:
                names.append(fileName[:pos]) # Extention weg und einordnen
        return names

    def save(self):
        if(self.lbname):
            #print("Save Reihenfolge {}".format(self.lbname))
            fieldnames = ['Index', 'Name', 'Selected']
            with open(self.lbname+'.csv', "w") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                li = self.get(0, tk.END)
                for i, name in enumerate(li):
                    writer.writerow(
                        {'Index': i, 'Name': name, 'Selected': self.selection_includes(i)})

    def form(self):
        '''
        Formatiert die Liste der Listbox und macht Einrückungen vor den Bewegungstexten
            sucht das 1. LOOP
                rückt rückwärts alle Zeilen bis zum 'Repeat' ein
            sucht das 2. LOOP usw.    
        '''
        try:
            cursel=self.curselection()
            listeTup = self.get(0, tk.END)
            lines=[]
            for li in listeTup:
                lines.append(li)

            lp=LoopRepeat()
            lines=lp.checkLines(lines)
            if lines==None:
                return False
            lp.einruecken(lines)

            self.delete(0,tk.END)
            for i in range(0,len(lines)):
                self.insert(i,lines[i])
            if len(cursel)==1:
                self.select_set(cursel[0])
        except:
            print("exeption in form():",sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2])
        
        return True

    def check(self):
        if self.form():
            #Alles OK
            self["bg"]='SystemWindow'
        else:
            #Es stimmt mit den Sequenzen etwas nicht
            self["bg"]='red2'

    def setCurrent(self, event):
        ''' gets the current index of the clicked item in the listbox '''
        self.curIndex = self.nearest(event.y)

    def getState(self, event):
        ''' checks if the clicked item in listbox is selected '''
        i = self.nearest(event.y)
        self.curState = self.selection_includes(i)

    def shiftSelection(self, event):
        ''' shifts item up or down in listbox '''
        i = self.nearest(event.y)
        if self.curState == 1:
            self.selection_set(self.curIndex)
        else:
            self.selection_clear(self.curIndex)
        if i < self.curIndex:
            # Moves up
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i+1, x)
            if selected:
                self.selection_set(i+1)
            self.curIndex = i
            self.check()
        elif i > self.curIndex:
            # Moves down
            x = self.get(i)
            selected = self.selection_includes(i)
            self.delete(i)
            self.insert(i-1, x)
            if selected:
                self.selection_set(i-1)
            self.curIndex = i
            self.check()

if __name__ == "__main__":
        # def printRightClickItem( event):
        #   ''' RK 14.12.18: gets the current text of the with the right button clicked item in the listbox '''
        #   curIndex = myListbox.nearest(event.y)
        #   print(f"Ausgewählt wurde: {myListbox.get(curIndex)}")
    root = tk.Tk()
    root.wm_title("Test Pullup")
    #myListbox = Drag_and_Drop_Listbox(root,name="myListbox")
    myListbox = Drag_and_Drop_Listbox(master=root,height=20,elistbox=EListbox.PROCEDURE,width=40)
    #for i, name in enumerate(['name'+str(i) for i in range(10)]):
    myListbox.insert(tk.END, ECom.Wait.__str__()+" 1.7 (1.7)")
    myListbox.insert(tk.END, ""+ECom.Repeat.__str__()+" 5 (3)")
    myListbox.insert(tk.END, "   Spidy Platz")
    myListbox.insert(tk.END, "   "+ECom.Wait.__str__()+" 1.7 (1.7)")
    myListbox.insert(tk.END, "   Spidy Sitz")
    myListbox.insert(tk.END, "   "+ECom.Wait.__str__()+" 3.2 (3.2)")
    myListbox.insert(tk.END, ""+ECom.LoopToLine.__str__()+" 1")
    myListbox.insert(tk.END, ECom.End.__str__()+"")



        # if i % 2 == 0:
        #     myListbox.selection_set(i)
    myListbox.grid()
    scrollbar = tk.Scrollbar(root, orient='vertical')
    scrollbar.config(command=myListbox.yview)
    scrollbar.grid(column=1, row=0)
    root.mainloop()
