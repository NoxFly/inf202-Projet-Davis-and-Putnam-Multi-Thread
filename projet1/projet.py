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
    arr = deepcopy(listoflists)
    l = len(arr)
    for i in range(l):
        for j in range(l):
            for k in range(l):
                if arr[i][j] and arr[j][k]:
                    arr[i][k] = True if type(arr[i][j]) == bool else 1
    return arr

# sequential relation
def relationSequentielle(L, R):
    arr = R([[True if i==j-1 else False for j in range(L)] for i in range(L)])
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
    header = "         | "
    for i in range(len(placement)):
        row = "task "+str(i+1)+(" "*(4 - len(str(i+1))))+"| "
        for j in range(len(placement[i])):
            if i==0:
                header += "Thd "+str(j+1) + " | "
            row += str(placement[i][j]) + (" "*(6-len(str(placement[i][j])))) + "| "
        if i==0: print(header)
        print(row)
    print("\n")


def Placement(arr):
    arr = progDepT(progDep(arr))
    arr_len = len(arr)

    # unused
    #placee = zeros(arr_len, False)
    #verifyUnused(arr, placee)

    placement = [[False for i in range(threads)]]
    
    idx_nb = 0
    row = 0
    col = -1

    nb_dep = [sum(getCol(i, arr)) for i in range(arr_len)]
    rest = deepcopy(nb_dep)
    #print("Tableau des dépendances:",nb_dep)
    

    for each_line in range(arr_len):
        x = 0
        y = -1
        nb, idx_nb = min(rest)

        # if 0 dependency
        if nb == 0:
            col += 1

            if col == threads:
                col = 0
                row += 1

                if row+1 > len(placement):
                    placement.append([False for i in range(threads)])
            x = col
            y = row
        else:
            # if one dependency or more
            dependency_i = 0 # first dependency (can be indirect)
            dependency_f = 0 # last dependency (direct)
            for line in range(arr_len):
                if arr[line][idx_nb] == 1:
                    dependency_f = line
                if arr[arr_len-line-1][idx_nb] == 1:
                    dependency_i = arr_len-line-1

            # find the right dependency's column
            right_col_idx = -1
            for line in range(len(placement)):
                for column in range(len(placement[0])):
                    if placement[line][column] == dependency_f and type(placement[line][column]) == int:
                        right_col_idx = column
            
            # find the right line to place executable line
            for line in range(len(placement)):
                if right_col_idx != -1:
                    if type(placement[line][right_col_idx]) == bool and y==-1:
                        x = right_col_idx
                        y = line

            # if the iterator reached the limit, then add new line to placement array
            if y == -1:
                placement.append([False for i in range(threads)])
                y = len(placement)-1

        placement[y][x] = idx_nb
    return placement


######### 4 ###########

def calculMemoire(arr):
    placement = Placement(arr)
    #affichePlacement(placement)
    V = len(arr) # nombre de variables
    l = len(placement)+1 # number of executed lines on placement array + 1 (initialization)
    
    ID = getCol(0, arr)
    const = getCol(1, arr)
    memoire = []

    for i in range(l):
        row = []
        for j in range(V*3):
            idx = int(j/3)
            if j%3 == 0:
                row.append(ID[idx])
            elif j%3 == 1:
                row.append(1 if i-1>=idx else 0)
            elif j%3 == 2:
                row.append(const[idx] + (0 if i<=0 or j<=2 else memoire[i-1][j-3]) if i>=j/3 else 0)
        memoire.append(row)
    printProgram(memoire)
    return memoire

def afficheMemoire(M):
    exec_line = -1
    l = len(M)
    l2 = int(len(M[0])/3)

    print("Memoire:")
    for line in range(l):
        text_line = "{}{}:  ".format(exec_line, " "*(3-len(str(exec_line))))
        for j in range(l2):
            txt = "x{}: {}".format(M[line][j*3], M[line][j*3+2])
            if exec_line > -1 and j == exec_line:
                txt = "[[ "+txt+" ]]"
            text_line += txt
            text_line += " "*(15-len(txt))
        print(text_line)
        exec_line += 1




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
        printProgram(relationSequentielle(4, progDepT))
    else:
        print("Execution parallèle:")
        affichePlacement(Placement(arr))
"""
# for all given arguments
for i in range(start,len(sys.argv)):
    url = "./programs/"+sys.argv[i]+".txt"

    # verify whether file exists
    if not os.path.isfile(url):
        print("File not found: "+url+"\n")
        exit(0)

    printAllArrays(sys.argv[i])
"""
afficheMemoire(calculMemoire(readProgram("./programs/"+sys.argv[1]+".txt")))