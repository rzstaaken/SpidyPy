#!/usr/bin/python3

import tkinter as tk
import tkinter.tix as tix
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.colorchooser as tkcc
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd


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
        self.movingsMenu.add_command(label="Load", state="disabled", command = self.movLoadFileDialog)              #Control L

        # Sichert Movings im Ordner 'moves'
        self.movingsMenu.add_command(label="Save As", state="disabled", command = self.ausgeben)                    #Control shift S
        self.movingsMenu.add_separator()
        self.movingsMenu.add_command(label="Save Selected Axis", state="disabled", command = self.ausgeben)         #Control A
        self.movingsMenu.add_command(label="Save All Axis", state="disabled", command = self.ausgeben)              #Control S
        if self.parent:
            self.movingsMenu.add_separator()
            #self.movingsMenu.add_command(label="Reset Slider", command =( (SpidyPy) self.parent).onReset))
            self.movingsMenu.add_command(label="Reset Slider", command = self.parent.onReset,accelerator="Ctrl+R")  #Control R
            self.bind_all("<Control-r>", self.parent.onReset)

            self.movingsMenu.add_separator()

        self.movingsMenu.add_command(label = "Exit", command = self.exit,accelerator="Ctrl+E")                      #Control E
        self.bind_all("<Control-e>", self.exit)

        self.sequenceMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Sequence", menu = self.sequenceMenu)
        #self.fileMenu.add_command(label = "Neues Projekt anlegen", command = self.ausgeben)
        self.sequenceMenu.add_command(label = "Load", state="disabled", command = self.ausgeben)                   #alt L
        self.sequenceMenu.add_command(label = "Save As", state="disabled", command = self.ausgeben)                #Alt S

    def movLoadFileDialog(self):
        #    self.parent.listboxMoves.fillListBox(path='posi')
        pass


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