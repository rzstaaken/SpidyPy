from enum import Enum


class ERunMode(Enum):
    '''Betriebsarten  '''
    IDLE = 0        #Während  Ablauf steht
    SINGLE_STEP = 1 #Während  SingleStep ausgeführt wird
    AUTOMATIC = 2   #Während  Automatik ausgeführt wird



if __name__ == "__main__":
    print("ERunMode.IDLE.value type={} ERunMode.IDLE.name type={}  ERunMode.IDLE.value={}  ERunMode.IDLE.name={}  "
        .format(  type(ERunMode.IDLE.value),type(ERunMode.IDLE.name),ERunMode.IDLE.value,ERunMode.IDLE.name))


    liste={}
    for erun in ERunMode:
        liste.update( {erun.name:erun.value})
    print( liste )


    


