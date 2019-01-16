# Hilfsfunktion bubbleSort(arr):
def bubbleSort(arr):
    n = len(arr) 
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Einganswerte:
#original="Pferde fressen keinen Gurkensalat und Marco quatscht mit Nicole wegen Rechner Linux und Apple"
original="ABRAKADABRA"
ausgabe=True

# Schritt 1: Matrix bilden mit eins nach links ge-shift-eten Buchstaben
mat=[]
for i in range(0,len(original)):
    r=original[i:]+original[ :i]
    mat.append(r)
if ausgabe:
    print("Matrix:")
    for t in range(0,len(mat)):
        print(mat[t])

# Schritt 2: Festellen ab wieviel Buchstaben die horizontalen Werte eindeutig sind!
eindeutig=-1
strlen=len(mat[0])
for i in range(1,strlen):# 2...strlen-1  Anzahl der Buchstaben
    di={}
    for t in range(0,strlen):
        di.update( { mat[t][0:i]:t})
    if len(di) == strlen: # Die Anzahl im Dictionary unterscheidet sich nicht. Das heißt EINDEUTIG
        eindeutig = i #
        break
print("Eindeutig ab "+str(eindeutig)+" Zeichen"  ) 
print(len(di))

#Das Dictionary ist von Hause schon sortiert! ??? oder nur im Debugger???
reihe=[]
keys=[]
keys =di.keys()

di2=di.copy()
keys2=di2.keys()
for k in keys:
    reihe.append(di[k])

#Wenn man sich di ansieht, sind die keys schon sortiert!

#Hilfsarray ausgeben
#for k in di.keys():
    #print(k+str(v))
    #reihe.append(di[k])

#for i in range(0,len(di)):
#    reihe.append(di[i])


# Schritt 3: Neue Reihenfolge nach der Sortierung bestimmen



s1 =""
pfeil="<-- Index"
index=-1
mat_s=sorted(mat)
for t in range(0,len(mat_s)):
    si=""
    if mat_s[t]==original:
        index=t
    if t==index:
        si=pfeil
    #print(mat_s[t]+si)
    s1+=mat_s[t][-1]
print()
print("Index ="+str(index) )
print("Ergebnis:")
print(s1)
#Aus dem Ergebnis eine liste mit Tupel (Zeichen,Index)
s2L =[]
for i in range(0,len(s1)):
    s2L.append((s1[i],i))
#print(s2L)
#Die Tupel-Liste sortieren
s3L=s2L.copy()
bubbleSort(s3L)
#print(s3L)
#Ab index von s3L beginnen Index aus Tupel führt zum nächsten Buchstaben  
ergStr=""
ix=index
for i in range(0,len(s3L)):
    b,ixn=s3L[ix]
    ergStr+=b
    ix=ixn
print(ergStr)