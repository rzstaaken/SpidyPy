#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog


class SpidyMenu(tk.Frame):
    def __init__(self, master=None, parent=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.parent = parent

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.movingsMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Movings", menu=self.movingsMenu)                                      
        self.movingsMenu.add_separator()
        if self.parent:
            self.movingsMenu.add_command(label="Save Selected Axis", state="normal"
                , command=self.movings_save_sel, accelerator="Ctrl+S")                             # Control S
            self.bind_all("<Control-s>", self.movings_save_sel)

            self.movingsMenu.add_command(label="Save All Axis", state="normal"
                , command=self.movings_save_all, accelerator="Ctrl+A")                             # Control A
            self.bind_all("<Control-a>", self.movings_save_all)

            self.movingsMenu.add_separator()
            # self.movingsMenu.add_command(label="Reset Slider", command =( (SpidyPy) self.parent).onReset))
            self.movingsMenu.add_command(label="Reset Slider", command=self.parent.onReset,
                                         accelerator="Ctrl+R")                                      # Control R
            self.bind_all("<Control-r>", self.parent.onReset)

            self.movingsMenu.add_separator()
        self.movingsMenu.add_command(label="Exit", command=self.exit, accelerator="Ctrl+X")         # Control X
        self.bind_all("<Control-x>", self.exit)

        self.procedureMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Procedure", menu=self.procedureMenu)
        # self.fileMenu.add_command(label = "Neues Projekt anlegen", command = self.ausgeben)

        self.procedureMenu.add_command(label="Load", state="normal"
            , command=self.procedureLoadFileDialog, accelerator="Alt+L")                            # alt L
        self.bind_all("<Alt-l>", self.procedureLoadFileDialog)

        self.procedureMenu.add_command(label="Save As", state="normal"
            , command=self.procedureSaveAsFileDialog, accelerator="Alt+S")                          # Alt S
        self.bind_all("<Alt-s>", self.procedureSaveAsFileDialog)
        

    def procedureLoadFileDialog(self, event=None):
        filename = filedialog.askopenfilename(
            title='Procedure Load',
            initialdir="procedure/",
            filetypes=(("Procedure File", "*.csv"),))
        if filename:
            print(filename)
            self.parent.listboxProcedure.fillListBox(procedure=True, filename=filename)
        else:
            self.parent.outText.insert(tk.END, str("\nError: moveLoadFileDialog() kann Datei nicht finden:" + filename))

    def procedureSaveAsFileDialog(self, event=None):
        filename = filedialog.asksaveasfilename(
            title='Procedure Save',
            defaultextension=".csv",
            initialdir="procedure/",
            filetypes=(("Procedure File", "*.csv"),))
        if filename:
            print(filename)
            self.parent.listboxProcedure.save(filename=filename)
        else:
            self.parent.outText.insert(tk.END
                , str("\nError: procedureSaveAsFileDialog() es wurde kein filename angegeben:" + filename))

    def movings_save_sel(self, event=None):
        print("movings_save_sel Wurde geklickt")
        fname = filedialog.asksaveasfilename(
            title='Save Selected Slider Positions',
            defaultextension=".json",
            initialdir="posi/",
            filetypes=(("Moving File", "*.json"),))
        if fname:
            print(fname)      
            self.parent.onSaveAxis( all=False, fname=fname)

    def movings_save_all(self, event=None):
        print("movings_save_all Wurde geklickt")
        fname = filedialog.asksaveasfilename(
            title='Save All Slider Positions',
            defaultextension=".json",
            initialdir="posi/",
            filetypes=(("Moving File", "*.json"),))
        if fname:
            print(fname)  
            self.parent.onSaveAxis( all=True, fname=fname)

    def exit(self, event=None):
        print("Exit geklickt")
        if self.parent:
            # print(isinstance(self.parent,SpidyPy)) #SpidyPy kennt man hier nicht, 'import SpidyPy' gibt ein ERROR ???
            self.parent.spidy_exit()
        else:
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    SpidyMenu(root)
    root.mainloop()
