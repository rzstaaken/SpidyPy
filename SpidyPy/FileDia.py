#!/usr/bin/python3

import tkinter as tk
import tkinter.tix as tix
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.colorchooser as tkcc
import tkinter.filedialog as tkfd
import tkinter.simpledialog as tksd


def ausgeben():
    print("Wurde geklickt")

root = tk.Tk()

menu = tk.Menu(root)
root.config(menu = menu)

dateiMenu = tk.Menu(menu)
menu.add_cascade(label="Datei", menu = dateiMenu)
dateiMenu.add_command(label = "Neues Projekt anlegen", command = ausgeben)
dateiMenu.add_command(label = "Projekt öffnen", command = ausgeben)
dateiMenu.add_command(label = "Speichern", command = ausgeben)
dateiMenu.add_separator()
dateiMenu.add_command(label = "Schließen", command = exit)

einstellungenMenu = tk.Menu(menu)
menu.add_cascade(label= "Einstellungen", menu = einstellungenMenu)
einstellungenMenu.add_command(label="Aussehen", command = ausgeben)
einstellungenMenu.add_command(label="Grundeinstellungen", command = ausgeben)

root.mainloop()
