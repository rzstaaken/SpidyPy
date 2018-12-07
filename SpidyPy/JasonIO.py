#!/usr/bin/python
import os
import json

class JasonIO:
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

if __name__ == "__main__":
    j=JasonIO()
    dic = {4:3.6,7:5.3}
    j.WriteP(dic)
    x=j.ReadP()
    print(x)

