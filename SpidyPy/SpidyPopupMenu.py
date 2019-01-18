"""
V0.01 18.01.2019 11:00 SpidyPopup.py 
https://github.com/rzstaaken/SpidyPy
"""
import os
import csv
import re
import time
from threading import Thread
from JsonIO import JsonIO
import tkinter as tk
import tkinter.messagebox as tkmb


class SpidyPopup(tk.Listbox):

    def __init__(self, parent, *args, **kwargs):
        tk.Listbox.__init__(self, parent, *args, **kwargs)

        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Delete", command=self.delete_selected)
        self.popup_menu.add_command(label="Select All", command=self.select_all)

        self.bind("<Button-3>", self.popup) # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        for i in self.curselection()[::-1]:
            self.delete(i)

    def select_all(self):
        self.selection_set(0, 'end')

    def show(self):
        pass

root = tk.Tk()
flb = SpidyPopup(root, selectmode='multiple')
for n in range(10):
    flb.insert('end', n)
flb.pack()
root.mainloop()
