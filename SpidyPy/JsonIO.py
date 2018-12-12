#!/usr/bin/python
import os
import json

class JsonIO:
    def __init__(self):
        pass
    def WriteP(self,ob,filename='dic.json'):
        with open(filename,'w') as f:
            json.dump(ob,f,indent=4,separators=(',',':'))
        #print(ob)

    def ReadP(self,filename='dic.json'):
        """
        Es soll ein Dictionary gelesen werden, in Form {1:4.5,7:6.2}
        Also den key nicht als String sondern als integer liefern. 
        """
        with open(filename,'r') as f:
            obj=json.load(f)
            res={}
            for key in obj:
                res.update({int(key):obj[key]})
            #print(res)
            return res

    @staticmethod
    def Extension(dot=True): 
        if dot:   
            return ".json"
        return "json"

    @staticmethod
    def Ext(dot=True):
        return JsonIO.Extension(dot=dot)


if __name__ == "__main__":
    j=JsonIO()
    dic = {4:3.6,7:5.3}
    j.WriteP(dic)
    print(j.ReadP())
    print(f"Extension with dot:{JsonIO.Extension()}" )
    print(f"Extension without dot:{JsonIO.Ext(False)}")



