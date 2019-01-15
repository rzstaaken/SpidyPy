from enum import Enum


class ERunMode(Enum):
    '''Betriebsarten  '''
    IDLE = 0        #Während  Ablauf steht
    STEP = 1        #Während  SingleStep ausgeführt wird
    AUTOMATIC = 2   #Während  Automatik ausgeführt wird

    @staticmethod
    def getNames():
        return [name for name,member in ERunMode.__members__.items()]
    @staticmethod
    def getValues():
        return list(map(lambda x:ERunMode.getNames().index(x),[name for name,member in ERunMode.__members__.items()]))

# class Waehrung ( Enum ):
#     EUR = "EUR"
#     USD = "USD"
#     JPY = "JPY"
#     HUF = "HUF"
#     NOK = "NOK"

#     @staticmethod
#     def getNames ( ):
#         return [ name for name, member in Waehrung.__members__.items ( ) ]



if __name__ == "__main__":
    # print("ERunMode.IDLE.value type={} ERunMode.IDLE.name type={}  ERunMode.IDLE.value={}  ERunMode.IDLE.name={}  "
    #     .format(  type(ERunMode.IDLE.value),type(ERunMode.IDLE.name),ERunMode.IDLE.value,ERunMode.IDLE.name))
    # er = ERunMode()
    print(ERunMode.getNames())
    print(ERunMode.getValues())
    #print(ERunMode.__members__.items())
    # print ( Waehrung.HUF )
    # print ( Waehrung.getNames ( ) )
    # dic={}
    # for erun in ERunMode:
    #     dic.update( {erun.name:erun.value})
    # print( dic )

    # eruList=[] 
    # for erun in ERunMode:eruList.append(erun.name)
    # print( eruList )

    # li=[dic[x] for x in dic ]
    # print(li)

    # print(list(map(lambda x: x ,dic)))

    # names=list(map(lambda x:x[0],ERunMode.__members__.items()))
    # print(names)



    


    


