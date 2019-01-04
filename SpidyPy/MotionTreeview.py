'''
https://stackoverflow.com/questions/16746387/tkinter-treeview-widget

Stand:
Positiv:
    Der Baum lässt sich darstellen, aufklappen usw.
Negativ:
    Es wird die Eingabe selektiert, es ist aber noch keine Eingabe möglich.
'''
import json
import os
#import tkinter as tk
#import tkinter.ttk as ttk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

#https://stackoverflow.com/questions/18562123/how-to-make-ttk-treeviews-rows-editable/41991207
class EntryPopup(Entry):

    def __init__(self, parent, text, **kw):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent, **kw)

        self.insert(0, text) 
        self['state'] = 'readonly'
        #self['readonlybackground'] = 'white'
        #self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Control-a>", self.selectAll)
        self.bind("<Escape>", lambda *ignore: self.destroy())

    def selectAll(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'


class MotionTreeview(object):
    def __init__(self, master, inhalt):
        self.nodes = dict()
        frame = Frame(master)
        
        self.tree = ttk.Treeview(frame,height=10)#10 Zeilen hoch
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w' )
        self.tree.grid(row=0,column=0)
        self.tree.column('#0', width=400)

        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        frame.grid()

        self.insert_node('',"Sequence", inhalt)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<Double-1>", self.on_click)

    def insert_node(self, parent, text, myNode):
        node = self.tree.insert(parent, 'end', text=text,open=False)
        if  (myNode is not str) and (myNode is not int):
            self.nodes[node] = myNode
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        selNode = self.nodes.pop(node, None)
        if selNode:
            self.tree.delete(self.tree.get_children(node))
            if type(selNode)!=int:
                for p in selNode:
                    if type(p) is int:
                        self.insert_node(node,str(p)+" Times",p)
                    elif type(p) is str:
                        if len(p)>1:
                            self.insert_node(node,"File: "+p,p)
                    else:
                        self.insert_node(node,p,p)

    def on_click(self,event):

        # close previous popups
        #self.destroyPopups()

        # what row and column was clicked on
        rowid = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # clicked row parent id
        parent = self.tree.parent(rowid)
        # do nothing if item is top-level        
        if parent == '':
            return
        # get column position info
        x,y,width,height = self.tree.bbox(rowid, column)

        # y-axis offset
        pady = height // 2

        # place Entry popup properly         
        url = self.tree.item(rowid, 'text')
        self.entryPopup = EntryPopup(self.tree, url)
        self.entryPopup.place( x=0, y=y+pady, anchor=W, relwidth=1)

        # selitems = self.tree.selection()
        # if selitems:
        #     selitem = selitems[0]
        #     #text = self.tree.item(selitem, "text") # get value in col #0
        #     text = self.tree.getint(selitem)
        #     print( "Es wurde doppel {} geklickt!".format(text))
        #     print(text)
        

    def dummy(self,treeView):
        # First check if a blank space was selected
        entryIndex = self.tree.focus()
        if '' == entryIndex: return

        # Set up window
        win = Toplevel()
        win.title("Edit Entry")
        win.attributes("-toolwindow", True)  

        ####
        # Set up the window's other attributes and geometry
        ####

        # Grab the entry's values
        for child in treeView.get_children():
            if child == entryIndex:
                values = treeView.item(child)["values"]
                break
        print( values)


if __name__ == '__main__':
    li = []  
    # Times, File, ...
    li.append([1,"Name1","Name2"])
    li.append([3,"Name2","Name3","Name4"])

    print(li)
    #with open("test.json",'w') as f:
        #json.dump(li,f,indent=4,separators=(',',':'))

    #with open("test.json",'r') as f:
        #erg = json.load(f)
    #print("Erg:{}".format(erg))
    root = Tk()
    app = MotionTreeview(root, inhalt=li)
    root.mainloop()
