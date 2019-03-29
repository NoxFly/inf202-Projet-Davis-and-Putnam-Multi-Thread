#!/usr/bin/env python

#imports
import sys, os.path
from copy import deepcopy

url = "./programs/"+sys.argv[1]+".txt"

# verify whether file exists
if not os.path.isfile(url):
    print("File not found: "+url+"\n")
    exit(0)

# create 2D array filled by 0
def zeroArr(L, l):
    return [[0 for j in range(l)] for i in range(L)]

# transform from string file to int array
def readProgram(filename):
    fd = open(filename,"r")
    arr = []
    
    # for each line
    for row in fd:
        # transform the str line to int line, and split each element to get an array
        row_int = [int(elt) for elt in row.replace("\n","").split(" ")]
        arr.append(row_int)

    fd.close()
    return arr

# print array
def printProgram(listoflists):
    l = len(listoflists)
    for i in range(l):
        print("| "+" | ".join(map(str, listoflists[i]))  +" |")
    print("\n")

# transform each 0 -> * and each 1 -> <
def afficheRelation(listoflists):
    return [["<" if i[j]==1 and j>0 else "*" for j in range(len(i))] for i in listoflists]
        

# transform each number to 0, and link the dependencies's ID
def progDep(listoflists):
    l = len(listoflists)
    l2 = len(listoflists[0])
    arr = zeroArr(l, l)
    for i in range(l):
        for j in range(2, l2-2):
            if listoflists[i][j] != -1:
                for k in range(l):
                    if listoflists[k][0] == listoflists[i][j]:
                        arr[k][i] = 1
                        print("la ligne",i,"est dependante de la ligne",k)
    return arr

# transitive closure
def progDepT(listoflists):
    arr = progDep(listoflists)
    l = len(listoflists)
    l2 = len(listoflists[0])-1

    for i in range(l):
        for j in range(l2):
            if arr[i][j] == 1:
                for k in range(0, i):
                    arr[k][j] = 1
    return arr

# sequential relation
def relationSequentielle(L):
    return [[1 if i<j else 0 for j in range(L)] for i in range(L)]



# OUTPUT #

# create array
arr = readProgram("programs/"+sys.argv[1]+".txt")
# basic array
printProgram(arr)
# progDep
#printProgram(progDep(arr))
# symbolysed array
#printProgram(afficheRelation(progDepT(arr)))
#printProgram(relationSequentielle(6))