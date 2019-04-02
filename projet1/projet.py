#!/usr/bin/env python

#imports
import sys, os.path
from copy import deepcopy

# arguments number
argc = len(sys.argv) - 1

threads = 4
filename = ""
option = ""
start = 1

# not one or two argument : need a file name
if argc == 0 : exit(0)
elif argc > 1:
    option = sys.argv[1]
    start = 2


########################################################################################

# create 2D array filled by 0
def zeros(L, zero=True):
    return [[0 if zero else False for j in range(L)] for i in range(L)]

######### 1 ###########

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



######### 2 ###########

# transform each number to 0, and link the dependencies's ID
def progDep(listoflists):
    l = len(listoflists)
    l2 = len(listoflists[0])
    arr = zeros(l)
    for i in range(l):
        for j in range(2, l2-2):
            if listoflists[i][j] != -1:
                for k in range(l):
                    if listoflists[k][0] == listoflists[i][j]:
                        arr[k][i] = 1
                        #print("la ligne",i,"est dependante de la ligne",k)
    return arr

# transitive closure
def progDepT(listoflists):
    L_return = deepcopy(listoflists)
    l = len(L_return)
    for i in range(l):
        for j in range(l):
            for k in range(l):
                if L_return[i][j] == 1 and L_return[j][k] == 1:
                    L_return[i][k] = 1
    return L_return

# sequential relation
def relationSequentielle(L, R):
    arr = R([[1 if i==j-1 else 0 for j in range(L)] for i in range(L)])
    return arr

######### 3 ###########

def getCol(index, array):
    if len(array)>0 and index < len(array):
        return [array[i][index] for i in range(len(array))]

def sum(arr):
    n = 0
    for i in arr: n += i 
    return n

def min(arr):
    j = 0
    m = arr[j]
    for i in range(len(arr)):
        if arr[i] < m and arr[i] > -1 or m == -1:
            m = arr[i]
            j = i
    arr[j] = -1
    return m, j

def verifyUnused(arr, placee):
    l = len(arr)
    for i in range(l):
        for j in range(l):
            if arr[i][j] == 0:
                placee[i][j] = True

def affichePlacee(placee):
    for i in range(len(placee)):
        row = "| "
        for j in range(len(placee)):
            row += str(placee[i][j]) + (" "*(6-len(str(placee[i][j])))) + "| "
        print(row)
    print("\n")

def affichePlacement(placement):
    header = "       | "
    for i in range(len(placement)):
        row = "task "+str(i+1)+" | "
        for j in range(len(placement[i])):
            if i==0:
                header += "Thd "+str(j+1) + " | "
            row += str(placement[i][j]) + (" "*(6-len(str(placement[i][j])))) + "| "
        if i==0: print(header)
        print(row)
    print("\n")


def Placement(arr):
    arr = progDepT(progDep(arr))
    L = len(arr)
    placee = zeros(L, False)
    verifyUnused(arr, placee)
    placement = [[False for i in range(threads)]]
    
    idx_nb = 0
    i = 0
    j = -1

    nb_dep = [sum(getCol(i, arr)) for i in range(L)]
    a = deepcopy(nb_dep)
    #print("Tableau des dépendances:",nb_dep)

    for k in range(L):
        j += 1

        if i+2 > len(placement) and j == threads:
            placement.append([False for j in range(threads)])

        if j == threads:
            j = 0
            i += 1

        nb, idx_nb = min(a)

        placement[i][j] = idx_nb
    return placement






# OUTPUT #

def printAllArrays(program):
    print("########### "+program+" ###########")

    arr = readProgram("programs/"+program+".txt")

    # --- basic array
    print("Array:")
    printProgram(arr)

    print("Before:")
    printProgram(afficheRelation(progDep(arr)))

    print("After:")
    printProgram(afficheRelation(progDepT(progDep(arr))))

    if option == "-s":
        print("Execution sequentielle:")
        printProgram(afficheRelation(relationSequentielle(4, progDepT)))
    else:
        print("Execution parallèle:")
        affichePlacement(Placement(arr))

# for all given arguments
for i in range(start,len(sys.argv)):
    url = "./programs/"+sys.argv[i]+".txt"

    # verify whether file exists
    if not os.path.isfile(url):
        print("File not found: "+url+"\n")
        exit(0)

    printAllArrays(sys.argv[i])