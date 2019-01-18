from enum import Enum

class EListbox(Enum):
    '''Verwendete Listboxen  '''
    MOVES = 0       
    PROCEDURE = 1

    @staticmethod
    def getNames():
        return [name for name,member in EListbox.__members__.items()]
    @staticmethod
    def getValues():
        return list(map(lambda x:EListbox.getNames().index(x),[name for name,member in EListbox.__members__.items()]))

if __name__ == "__main__":
    print(EListbox.getNames())
    print(EListbox.getValues())

    run = EListbox.MOVES.__str__()
    print(run)