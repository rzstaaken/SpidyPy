from enum import IntEnum

class ECom(IntEnum):
    '''Enum Commandos  '''
    End = 0
    Repeat = 1
    LoopToLine = 2
    Wait = 3

    def __str__(self):
        return ':'+self.name
        


