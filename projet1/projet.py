#!/usr/bin/env python

#imports
import sys, os.path
from copy import deepcopy

# argument number
argc = len(sys.argv) - 1

# number of thread
threads = 8

# default option is nothing
option = ""
# if no option: take the first argument, else the second. it's where the filename arguments starts
start = 1

# not one or two argument : need a file name
if argc == 0 : exit(0)
elif argc > 1:
    option = sys.argv[1]
    if option != "-s": exit(0)
    start = 2


########################################################################################

# create 2D array by LxL size, filled by 0 or False
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
    if verifyArray(arr): return arr
    else: exit(0)

# print array
def printProgram(listoflists):
    l = len(listoflists)
    # for each row
    for i in range(l):
        # transform each element to string and join them, separated by |
        print("| "+" | ".join(map(str, listoflists[i]))  +" |")
    print("\n")

# transform each 0/False -> * and each 1/True -> <
def afficheRelation(listoflists):
    return [["<" if i[j] and j>0 else "*" for j in range(len(i))] for i in listoflists]



######### 2 ###########

# transform each number to 0, and link the dependencies's ID
def progDep(listoflists):
    l = len(listoflists)
    l2 = len(listoflists[0])
    before = zeros(l)
    for i in range(l):
        # start to second range because we don't need to take the ID and constant value of the row
        for j in range(2, l2-2):
            if listoflists[i][j] != -1:
                for k in range(l):
                    # if the number of the dependency correspond to the ID, then note it as a relation
                    if listoflists[k][0] == listoflists[i][j]:
                        before[k][i] = 1
                        #print("la ligne",i,"est dependante de la ligne",k)
    return before

# transitive closure
def progDepT(listoflists):
    after = deepcopy(listoflists)
    l = len(after)
    for i in range(l):
        for j in range(l):
            for k in range(l):
                # if its 1 or True for both
                if after[i][j] and after[j][k]:
                    # then the relation is weither True or 1 depending the variable type
                    after[i][k] = True if type(after[i][j]) == bool else 1
    return after

# sequential relation
def relationSequentielle(L, R):
    # create a LxL array with the i-1=j diagonal filled by 1 and all others by 0
    # then apply the transitive closure
    arr = R([[True if i==j-1 else False for j in range(L)] for i in range(L)])
    return arr



######### 3 ###########

# return the column n of an array
def getCol(index, array):
    if len(array)>0 and index < len(array):
        return [array[i][index] for i in range(len(array))]

# calcul the minimum of an array, if the number is greater than -1
def min(arr):
    # default minimum (it can be -1)
    j = 0
    m = arr[j]
    for i in range(len(arr)):
        # if the element i is lower than the saved minimum, and if it's not -1 or if the saved (default) minimum is -1
        # update the new minimum
        if arr[i] < m and arr[i] > -1 or m == -1:
            m = arr[i]
            j = i
    # mark the new minimum as read, like that, the next loop it will be another minimum
    arr[j] = -1
    # return the minimum and its index in the array
    return m, j

# /!\ unused function
# change each 0 by True, like that we do not have to check them when we'll execute the program
def verifyUnused(arr, placee):
    l = len(arr)
    for i in range(l):
        for j in range(l):
            if arr[i][j] == 0:
                placee[i][j] = True

# /!\ unused function
# display the Placee array
def affichePlacee(placee):
    for i in range(len(placee)):
        row = "| "
        for j in range(len(placee)):
            row += str(placee[i][j]) + (" "*(6-len(str(placee[i][j])))) + "| "
        print(row)
    print("\n")

# display Placement array
def affichePlacement(placement):
    header = "         | "
    for i in range(len(placement)):
        row = "task "+str(i+1)+(" "*(4 - len(str(i+1))))+"| "
        for j in range(len(placement[i])):
            # place the header of the array
            if i==0:
                header += "Thd "+str(j+1) + " | "
            # then add all values of the row
            row += str(placement[i][j]) + (" "*(6-len(str(placement[i][j])))) + "| "
        if i==0: print(header)
        print(row)
    print("\n")

def findDepCol(placement, dependency_f):
    # find the right dependency's column
    right_col_idx = -1
    for line in range(len(placement)):
        for column in range(len(placement[0])):
            if placement[line][column] == dependency_f and type(placement[line][column]) == int:
                right_col_idx = column
    return right_col_idx

def findPlace(placement, arr, idx_nb, nb_dep):
    # coords to place the executable
    x = 0
    y = -1
    l = len(arr)
    dependency_f = 0 # last dependency (direct)
    for line in range(l):
        if arr[line][idx_nb] == 1:
            dependency_f = line
    
    right_col_idx = findDepCol(placement, dependency_f)
    
    # dependency not even placed: we place it before (recursivity)
    if right_col_idx == -1:
        nb_dep[dependency_f] = -1
        findPlace(placement, arr, dependency_f, nb_dep)
        right_col_idx = findDepCol(placement, dependency_f)

    # find the right line to place executable line
    for line in range(len(placement)):
        if type(placement[line][right_col_idx]) == bool and y==-1:
            x = right_col_idx
            y = line

    # if the iterator reached the limit, then add new line to placement array
    if y == -1:
        placement.append([False for i in range(threads)])
        y = len(placement)-1
    
    placement[y][x] = idx_nb

# place all executable rows in the correct order, depending of their dependencies
def Placement(arr):
    # need the transitive closure
    arr = progDepT(progDep(arr))
    arr_len = len(arr)

    # /!\ unused
    #placee = zeros(arr_len, False)
    #verifyUnused(arr, placee)

    # create the first row filled by False : placed not used yet
    # --> we don't need to create a huge array in one time.
    #     we'll create new rows if we need it
    placement = [[False for i in range(threads)]]
    
    # variables
    idx_nb = 0
    row = 0
    col = -1

    # the goal is to place the column that have the minimum of dependencies in first

    # get the number of dependencies of all column
    nb_dep = [sum(getCol(i, arr)) for i in range(arr_len)]
    # copy the array. we'll change this one when we will used the column that have the
    # minimum if dependencues
    rest = deepcopy(nb_dep)
    #print("Tableau des dépendances:",nb_dep)
    

    for each_line in range(arr_len):
        # get the row to execute in first
        nb, idx_nb = min(rest)

        # if 0 dependency --> then it can be placed on new thread
        if nb == 0:
            # next thread
            col += 1

            # if max thread = 8 and the current thread is 8, then reset to 0 and go to next row
            # --> array index : 8-1 = 7, so if col = 8, exceeds 1
            if col == threads:
                col = 0
                row += 1

                # if the Placement array have not longer any place, we create a new row
                if row+1 > len(placement):
                    placement.append([False for i in range(threads)])
            placement[row][col] = idx_nb
        else:
            # if one dependency or more
            findPlace(placement, arr, idx_nb, nb_dep)

    return placement


######### 4 ###########

def calculMemoire(arr):
    placement = Placement(arr)
    V = len(arr)            # number of variables
    l = len(placement)+1    # number of executed lines on placement array + 1 (initialization)
    
    #we could use one 2D array but to make it more understandable
    ID = getCol(0, arr)     # all ID on 1D array
    const = getCol(1, arr)  # all const on 1D array
    memoire = []

    for i in range(l):
        row = []
        # each variable need 3 element : (id, bvalue, value) * number of variable
        for j in range(V*3):
            # force the int() else it's 4.0 and not 4 (for example)
            idx = int(j/3)
            # if it's the ID column
            if j%3 == 0:
                row.append(ID[idx])
            # else if it's the bvalue column
            elif j%3 == 1:
                row.append(1 if i-1>=idx else 0)
            # else if it's the value column
            elif j%3 == 2:
                row.append(const[idx] + (0 if i<=0 or j<=2 else memoire[i-1][j-3]) if i>=j/3 else 0)
        memoire.append(row)
    return memoire

# display the memory array
def afficheMemoire(M):
    # -1 because it's the initialization row
    exec_line = -1
    l = len(M)
    l2 = int(len(M[0])/3)

    print("Memoire:")
    for line in range(l):
        text_line = "{}{}:  ".format(exec_line, " "*(3-len(str(exec_line))))
        for j in range(l2):
            txt = "x{}: {}".format(M[line][j*3], M[line][j*3+2])
            # if it's the current time to change this one, [[ x ]]
            if exec_line > -1 and j == exec_line:
                txt = "[[ "+txt+" ]]"
            text_line += txt
            # add spaces to be clearest
            text_line += " "*(15-len(txt))
        print(text_line)
        exec_line += 1


###### BONUS : verify array correspond to some criteria

def verifyArray(arr):
    # first: verify the array has the correct number of elements:
    # ID | CST | nb of dependencies according to number of rows -1 (itself)
    # second: verify the dependencies of a row is well linked to an existing row
    l = len(arr)

    for i in range(l):
        if len(arr[i]) != l + 1:
            print("Array doesn't have correct number of elements line",i+1,"\n")
            return False
        if l > 1:
            for j in range(2, len(arr[i])):
                if arr[i][j] != -1:
                    exists = False
                    for k in range(l):
                        if arr[k][0] == arr[i][j]:
                            exists = True
                    if not exists:
                        print("The dependency number",j-1,"of the line",i+1,"which reffered to the line",arr[i][j],"does not exists\n")
                        return False
    return True


# OUTPUT #

# for each filname's argument, execute this function that show
# the initial array,
# the before array,
# the after array,
# sequential or parallel array
# and then the memory array
def printAllArrays(program):
    print("\n########### "+program+" ###########")

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
    
    afficheMemoire(calculMemoire(arr))

# for all given arguments
for i in range(start,len(sys.argv)):
    url = "./programs/"+sys.argv[i]+".txt"

    # verify whether file exists
    if not os.path.isfile(url):
        print("File not found: "+url+"\n")
        exit(0)

    printAllArrays(sys.argv[i])