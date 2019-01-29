from enum import IntEnum

class ECom(IntEnum):
    '''Enum Commandos  '''
    End = 0
    LoopToLine = 1
    Repeat = 2
    Wait = 3

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
        li = ECom.getCommands()
        for i in range(0,len(li)):
            if li[i] == st:
                return i

    def __str__(self):
        return ':'+self.name
        
if __name__ == "__main__":
    print(ECom.getNames())
    print(ECom.getValues())
    print(ECom.getCommands())

    x=ECom.getValue(':Repeat')
    print(str(x))

    x=ECom.getValue(':Abc')
    print(str(x))

