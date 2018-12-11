#!/usr/bin/python
import os
import json
fNameMinMax = "LegsMinMax.json" 

posiPath = 'posi'
ROWSPAN =20
PADX=PADY=5

#Achtung: Es werden andere Werte aus der Datei gelesen!
LegsMinMax = [	
    {'Min': 2.0, 'Max': 9.5}, 
    {'Min': 2.0, 'Max': 8.0},
    {'Min': 2.0, 'Max': 9.5},
    {'Min': 2.0, 'Max': 8.5},
    {'Min': 2.0, 'Max': 9.0},
    {'Min': 2.0, 'Max': 9.5},
    {'Min': 2.0, 'Max': 9.0},
    {'Min': 2.0, 'Max': 9.5},
    {'Min': 2.0, 'Max': 9.0},
    {'Min': 2.0, 'Max': 9.5},
    {'Min': 2.0, 'Max': 9.5},
    {'Min': 2.0, 'Max': 9.5},]

def ReadDefLegsIf(filename=fNameMinMax):
    """
    Lesen, wenn das File mit den Default-Werten existiert.
    Sonst das File mit den Default-Werten anlegen
    """
    if os.path.exists('SpidyPy'):
        os.chdir('SpidyPi')   #Bei Visual Studio Code wird das gebraucht

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
    with open(filename,'r') as f:
        return json.load(f)

def WriteDefLegs(filename=fNameMinMax):
    with open(filename,'w') as f:
        json.dump(LegsMinMax,f,indent=4,separators=(',',':'))
        #print(LegsMinMax)
        return LegsMinMax

if __name__ == "__main__":
    LegsMinMax = ReadDefLegsIf()
    print(LegsMinMax)