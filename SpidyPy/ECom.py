from enum import Enum

class ECom(Enum):
    '''Enum Commandos  '''
    END = 0
    Repeat = 1
    LOOP = 2
    T = 3

    def __str__(self):
        return ':'+self.name

class ERunMode(Enum):
    '''Enum Commandos  '''
    IDLE = 0
    SINGLE_STEP = 1
    AUTOMATIC = 2

