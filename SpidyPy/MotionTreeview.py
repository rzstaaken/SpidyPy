'''
https://stackoverflow.com/questions/16746387/tkinter-treeview-widget
'''
import json
import os
import tkinter as tk
import tkinter.ttk as ttk

class MotionTreeview(object):
    def __init__(self, master, path):
        self.nodes = dict()
        frame = tk.Frame(master)
        
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

        #abspath = os.path.abspath(path)
        abspath = path
        self.insert_node('',"Sequence", abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind("<Double-1>", self.on_click)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        #if os.path.isdir(abspath):
        if  (abspath is not str) and (abspath is not int):  #<---------------
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            #for p in os.listdir(abspath):
                #self.insert_node(node, p, os.path.join(abspath, p))
            for p in abspath:
                if type(p) is int:
                    self.insert_node(node,str(p)+" Times",p)
                elif type(p) is str:
                    if len(p)>1:
                        self.insert_node(node,"File: "+p,p)
                else:
                    self.insert_node(node,p,p)
    def on_click(self,event):
        print("Es wurde doppel geklickt!")


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
    root = tk.Tk()
    app = MotionTreeview(root, path=li)
    root.mainloop()
