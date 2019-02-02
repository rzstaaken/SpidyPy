#!/usr/bin/python
import os
import json
fNameMinMax = "LegsMinMax.json" 

posiPath = 'posi'
ROWSPAN =20
PADX=PADY=5

#Achtung: Es werden andere Werte aus der Datei gelesen!
#Diese Daten werden nur gelesen wenn die Datei 'LegsMinMax.json' nicht existiert
LegsMinMax = [
    {"No":0 ,"Min":9.5,"Max":2.5,"Start":7.5},
    {"No":1 ,"Min":2.5,"Max":9.5,"Start":4.0},
    {"No":2 ,"Min":2.5,"Max":8.0,"Start":4.0},
    {"No":3 ,"Min":2.5,"Max":9.5,"Start":4.0},
    {"No":4 ,"Min":9.5,"Max":2.5,"Start":7.5},
    {"No":5 ,"Min":9.5,"Max":3.3,"Start":7.7},
    {"No":6 ,"Min":9.5,"Max":2.5,"Start":7.5},
    {"No":7 ,"Min":2.5,"Max":9.5,"Start":4.0},
    {"No":8 ,"Min":2.5,"Max":9.5,"Start":4.0},
    {"No":9 ,"Min":2.5,"Max":9.5,"Start":4.0},
    {"No":10,"Min":9.5,"Max":2.5,"Start":7.6},
    {"No":11,"Min":9.5,"Max":3.0,"Start":7.6}]

def ReadDefLegsIf(filename=fNameMinMax):
    """
    Lesen, wenn das File mit den Default-Werten existiert.
    Sonst das File mit den Default-Werten anlegen
    """
    if os.path.exists('SpidyPy'):
        os.chdir('SpidyPy')   #Bei Visual Studio Code wird das gebraucht

    if os.path.exists('Spider'):
        os.chdir('Spider')
    #p=os.path.curdir
    #r=os.getcwd()
    #p=os.path.realpath('.')
    #print(p)
    #print(r)
    #z=os.chdir('Spider')
    #z=os.getcwd()
    #print(z)
    if os.path.exists(fNameMinMax):
        return ReadDefLegs()
    else:
        return WriteDefLegs()
def ReadDefLegs(filename=fNameMinMax):
    """
    DefLegs lesen
    Testen ob das File existiert wird nicht geprüft!
    """
    try:
        with open(filename,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise

def WriteDefLegs(filename=fNameMinMax):
    with open(filename,'w') as f:
        #json.dump(LegsMinMax,f,indent=4,separators=(',',':'))
        json.dump(LegsMinMax,f,indent=None,separators=(',',':'))
        #print(LegsMinMax)
    return LegsMinMax

if __name__ == "__main__":
    LegsMinMax = ReadDefLegsIf()
    print(LegsMinMax)