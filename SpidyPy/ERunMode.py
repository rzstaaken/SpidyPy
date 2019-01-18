from enum import Enum


class ERunMode(Enum):
    '''Betriebsarten  '''
    IDLE = 0        #Wenn das System steht
    STEP = 1        #Während  SingleStep (Einzelschritt) ausgeführt wird
    SEQUENCE = 2    #Fährt die Sequenz bis END und geht dann in IDLE
    AUTOMATIC = 3   #Automatiklauf startet bei END wieder in der ersten Zeile

    @staticmethod
    def getNames():
        return [name for name,member in ERunMode.__members__.items()]
    @staticmethod
    def getValues():
        return list(map(lambda x:ERunMode.getNames().index(x),[name for name,member in ERunMode.__members__.items()]))

if __name__ == "__main__":
    # print("ERunMode.IDLE.value type={} ERunMode.IDLE.name type={}  ERunMode.IDLE.value={}  ERunMode.IDLE.name={}  "
    #     .format(  type(ERunMode.IDLE.value),type(ERunMode.IDLE.name),ERunMode.IDLE.value,ERunMode.IDLE.name))
    # er = ERunMode()
    print(ERunMode.getNames())
    print(ERunMode.getValues())

    run = ERunMode.SEQUENCE.__str__()
    print(run)





    


    


