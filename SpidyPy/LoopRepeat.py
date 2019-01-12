from ECom import ECom

class LoopRepeat():
    # def __init__(self,lines):
    #     ''' Um die LoopRepeat Zeilen und die zugehörigen Zähler zu speichern  '''
    #     self.lines = lines

    def checkLines(self,lines):
        ''' Check und Rücksprungsadresse eintragen '''
        stack=[]
        for i in range(0, len(lines) ):
            lines[i] = str(lines[i]).strip() #Leerstellen rausnehmen
            if ECom.Repeat.__str__() in lines[i]:#:Repeat
                stack.append(i)
            if ECom.LoopToLine.__str__() in lines[i]:#:LoopToLine
                if len(stack)<=0:
                    return None
                pop=stack.pop()
                lines[i]= ECom.LoopToLine.__str__()+' '+str(pop)
                repLi=lines[pop].split(' ')
                if len(repLi)==1:
                    return None # Fehler es ist kein Laufwert angegeben
                if len(repLi)>=2:
                    lines[pop]=repLi[0]+' '+repLi[1]+' ('+repLi[1]+')'

        if len(stack)==0:
            return lines
        return None 

    def einruecken(self,lines):
        for i in range(0, len(lines) ):
            if ECom.LoopToLine.__str__() in lines[i]:#:LoopToLine
                a=lines[i].split(ECom.LoopToLine.__str__())
                start=int(a[len(a)-1])
                self.doEinruecken(lines,start+1,i)
        return True

    
    def doEinruecken(self,liste,von,bis):
        for i in range(von,bis):
            liste[i]='  '+liste[i]
        
if __name__ == "__main__":
    zeilen=[
        ":Repeat 3 (1)",
        "  :Repeat 10 (5)",
        "    :Wait 4.8",
        "    :Wait 0.2",
        "  :LoopToLine 3",
        ":LoopToLine",
        ":Wait 0.2",
        ":Repeat 6 (2)",
        "  :Wait",
        ":LoopToLine",
        ":End",
    ]
    lp=LoopRepeat()
    z=lp.checkLines(zeilen)
    if z==None:
        print("Fehler checkLines")
    else:
        lp.einruecken(z)
        for i in range(0, len(z) ):
            print(z[i])
                