import tkinter as tk
import tkinter.messagebox as tkmb
from functools import partial

class CheckButtonLegs(tk.Checkbutton):
    def __init__(self, master,nr, **kw):

        tk.Checkbutton.__init__(self, master, kw)
        self.nr=nr
        self.var = tk.IntVar()
        self.config(variable=self.var,offvalue=0,onvalue=1)
        #self.bind("<Shift-ButtonPress-1>",partial( self.my_callback,name='Anton'),add=True)

    def get(self):
        return self.var.get()

    def my_callback(self,event,name):
        print('Hallo')

if __name__ == "__main__":
    root = tk.Tk()

    def dein_callback(event):
        print(event.widget.var.get())
        #print('Hi')

    boxes = []
    for i in range(0,12):
        boxes.append( CheckButtonLegs( master = root,nr=i, height = 5) )
        boxes[i].grid(column=i, row=0)
    #root.widget.bind("<Shift-ButtonPress-1>", callback)
    root.bind_all("<ButtonPress-1>", dein_callback,add=True)

    root.mainloop()