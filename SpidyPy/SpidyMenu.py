#!/usr/bin/python3

import tkinter as tk
import tkinter.tix as tix
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.colorchooser as tkcc
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd
from tkinter import filedialog

class SpidyMenu(tk.Frame):
    def __init__(self, master=None, parent=None):
        # parameters that you want to send through the Frame class. 
        tk.Frame.__init__(self, master)                 
        self.master = master
        self.parent=parent

        self.menu = tk.Menu(self.master)
        self.master.config(menu = self.menu)

        self.movingsMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label= "Movings", menu = self.movingsMenu)                                            #Control M
        self.movingsMenu.add_command(label="Load", state="disabled", command = self.procedureLoadFileDialog)              #Control L

        # Sichert Movings im Ordner 'moves'
        self.movingsMenu.add_command(label="Save As", state="disabled", command = self.ausgeben)                    #Control shift S
        self.movingsMenu.add_separator()
        self.movingsMenu.add_command(label="Save Selected Axis", state="disabled", command = self.ausgeben)         #Control A
        self.movingsMenu.add_command(label="Save All Axis", state="disabled", command = self.ausgeben)              #Control S
        if self.parent:
            self.movingsMenu.add_separator()
            # self.movingsMenu.add_command(label="Reset Slider", command =( (SpidyPy) self.parent).onReset))
            self.movingsMenu.add_command(label="Reset Slider", command = self.parent.onReset,accelerator="Ctrl+R")  #Control R
            self.bind_all("<Control-r>", self.parent.onReset)

            self.movingsMenu.add_separator()

        self.movingsMenu.add_command(label = "Exit", command = self.exit,accelerator="Ctrl+E")                      #Control E
        self.bind_all("<Control-e>", self.exit)

        self.procedureMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Procedure", menu = self.procedureMenu)
        # self.fileMenu.add_command(label = "Neues Projekt anlegen", command = self.ausgeben)
        self.procedureMenu.add_command(label = "Load", state="normal", command = self.procedureLoadFileDialog)      #alt L
        self.procedureMenu.add_command(label = "Save As", state="normal", command = self.procedureSaveAsFileDialog)  #Alt S

    def procedureLoadFileDialog(self):
        filename = filedialog.askopenfilename(
            title='Select image source',
            initialdir="procedure/",
            filetypes=(("Procedure File","*.csv"),)) 
        if filename:
            print(filename)   
            self.parent.listboxProcedure.fillListBox(procedure=True, filename=filename)
        else:
            self.parent.outText.insert(tk.END,str("\nError: moveLoadFileDialog() kann Datei nicht finden:"+filename))

    def procedureSaveAsFileDialog(self):
        
        filename = filedialog.asksaveasfilename(
            title='Choose File',
            defaultextension=".csv",
            initialdir="procedure/",
            filetypes=(("Procedure File","*.csv"),))     
        if filename:
            print(filename)   
            self.parent.listboxProcedure.save(filename=filename)
        else:
            self.parent.outText.insert(tk.END,str("\nError: procedureSaveAsFileDialog() es wurde kein filename angegeben:"+filename))

    def ausgeben(self):
        print("Wurde geklickt")

    def exit(self,event=None):
        print("Exit geklickt")
        if self.parent:
            #print(isinstance(self.parent,SpidyPy)) #SpidyPy kennt man hier nicht, 'import SpidyPy' gibt ein ERROR ???
            self.parent.spidy_exit()
        else:
            self.master.destroy()



if __name__ == "__main__":
    root = tk.Tk()

    SpidyMenu(root)
    root.mainloop()