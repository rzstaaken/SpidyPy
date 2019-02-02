from enum import IntEnum

class ECom(IntEnum):
    '''Enum Commandos  '''
    End = 0
    LoopToLine = 1
    Repeat = 2
    Wait = 3

    @staticmethod
    def get_min_val(eCom):
        ''' Liefert den minimalen Wert des Commandos
        '''
        if eCom==ECom.End:
            return None
        elif eCom==ECom.LoopToLine:
            return None # Das System bestimmt selber die Rücksprungsadresse
        elif eCom==ECom.Repeat:
            return 1
        elif eCom==ECom.Wait:
            return 0.1
        return None

    @staticmethod
    def getNames():
        return [name for name,member in ECom.__members__.items()]

    @staticmethod
    def getValues():
        return list(map(lambda x:ECom.getNames().index(x),[name for name,member in ECom.__members__.items()]))

    @staticmethod
    def getStr(num):
        return ((ECom)(num)).__str__()

    @staticmethod
    def getCommands():
        return list(map(lambda x:ECom.getStr(x),[v for v in ECom.getValues()]))

    @staticmethod
    def getValue(st):
        '''
        liefert den 1. Zahlen Wert 
        Wenn die Zeile Commando beinhaltet
        '''
        li = ECom.getCommands()
        for i in range(0,len(li)):
            if li[i] in st:
                return ECom.getNumber(st)

    @staticmethod
    def insertNumber(inpStr,number):
        '''
        'number' ist ein int oder ein float
        Schreibt 'number=7.7' in beide Zahlenwerte in 'inpStr' mit
        inpStr sieht z.B. so aus '    :Wait 1.2 (1.2)'
        Das Return dann so       '    :Wait 7.7 (7.7)'
        '''
        dp = inpStr.find(':')#Führende Leerstellen merken
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!=2 and le!= 3:
            raise AttributeError("Der übergebene String hat nicht die nötige Struktur!")
        if le==3:
            if aIn[2][0] != '(' or aIn[2][-1] != ')':
                raise AttributeError("Der übergebene String hat nicht die nötige Struktur! 2.Wert nicht in ( und )")
        ret= ' '*dp+ aIn[0]+' '+str(number)
        if le==2:
            return ret
        return ret + ' ('+str(number)+')'

    @staticmethod
    def findECom(st):
        '''
        Sucht ein Commando im String und liefert die Enum ECom
        '''
        li = ECom.getCommands()
        for i in range(0,len(li)):
            if li[i] in st:
                return ((ECom ) (i))

    @staticmethod
    def getNumber(inpStr):
        '''
        siehe insertNumber()
        Liefert den 1. Zahlenwert als int oder float
        '''
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!=2 and le!= 3:
            raise AttributeError("Der übergebene String hat nicht die Spidy-Anweisungs-Struktur!")
        try:
            return int(aIn[1])
        except ValueError:
            return float(aIn[1])

    @staticmethod
    def getSecondNumber(inpStr):
        '''
        siehe insertNumber()
        Liefert den 2. Zahlenwert als int oder float
        '''
        inpStr=str(inpStr).strip()
        aIn=str(inpStr).split(' ')
        le = len(aIn)
        if le!= 3:
            raise AttributeError("Der übergebene String hat nicht die Spidy-Anweisungs-Struktur mit zweit Zahlenwerte!")
        v= aIn[2][1:-1]
        try:
            return int(v)
        except ValueError:
            return float(v)

    def __str__(self):
        return ':'+self.name
        
if __name__ == "__main__":
    print(ECom.getNames())
    print(ECom.getValues())
    print(ECom.getCommands())

    x=ECom.get_min_val(ECom.Repeat)
    print("ECom.get_min_val(ECom.Repeat) = "+str(x))

    x=ECom.getValue('    :Repeat 5 (3)')
    print("ECom.getValue('    :Repeat 5 (3)') + "+str(x))

    x= ECom.findECom('    :Repeat 5 (3)')
    print("ECom.findECom('    :Repeat 5 (3)')  = "+str(x))
    
    x=ECom.getValue(':Abc')
    print("ECom.getValue(':Abc')="+str(x))

    x= ECom.findECom('In bin nur ein Text' )
    print("ECom.findECom('In bin nur ein Text' ) = "+str(x))

    print("'"+ECom.insertNumber(inpStr='    :Wait 1.2 (1.2)',number=7.7)+"'")
    print(ECom.insertNumber(inpStr='    :Wait 1.2 (1.2)',number=float(7)))
    x= ECom.getNumber(inpStr='    :Wait 1.2 (1.2)' )
    print(str(x))

    x= ECom.getNumber(inpStr='    :Repeat 2 (2)' )
    print(str(x))

    x= ECom.getSecondNumber(inpStr='    :Wait 7.2 (6.2)' )
    print(str(x))
