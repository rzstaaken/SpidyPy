class LoopRepeat(object):
    def __init__(self,lineloop,lineRepeat,loopInitVal):
        ''' Um die LoopRepeat Zeilen und die zugehörigen Zähler zu speichern  '''

        self.lineLoop = lineloop
        self.lineRepeat = lineRepeat
        self.loopInitVal = loopInitVal
        self.loopCount = loopInitVal
