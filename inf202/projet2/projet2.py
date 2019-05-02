# projet 2 inf202
# Dorian THIVOLLE

# imports
import sys, os, datetime
from random import randint, randrange

# vars
argc = len(sys.argv) - 1
args = sys.argv[1:]

# CONSTS
NB_CLAUSES = 20
MAX_NUM_ATOM = 26
MAX_LG_CLAUSE = 10
WRITE_TYPE = 0
NIV_TRACE = 2
LOG = []

# verification of given arguments
def verifyInput():
    if argc != 2:
        print("2 arguments expected.",argc,"given")
        return 1

    if not args[0].endswith('.txt'):
        print("First argument must be file name with .txt extension")
        return 2
    
    if not args[1].isdigit() or args[1] not in ["1","2"]:
        print("Second argument must be 1 or 2 (convention)")
    
    if not os.path.isfile(args[0]):
        print("file not found")

    args[1] = int(args[1])

    return 0


# parse array to conv 1 {1,2,3} | 2D array
def parseConv1(arr):
    arr = arr[:]
    if isinstance(arr[0][0], int): return arr
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            a = arr[i][j].replace('-','')
            if a.isalpha():
                if "-" in arr[i][j]: arr[i][j] = -(ord(a)-96)
                else: arr[i][j] = ord(a)-96
            else: arr[i][j] = int(arr[i][j])
    return arr


# parse array to conv 2 {a,b,c} | 2D array
def parseConv2(arr):
    arr = arr[:]
    if str(arr[0][0]).replace('-','').isalpha(): return arr
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if '-' in str(arr[i][j]): arr[i][j] = '-'+chr(int(str(arr[i][j]).replace('-',''))+96)
            else: arr[i][j] = chr(int(arr[i][j])+96)
    return arr


# print 1D / 2D array
def printArray(arr):
    if len(arr) == 0: return False
    
    if isinstance(arr[0], int):
        print(str(arr).replace(",",""))
    elif isinstance(arr[0], list):
        print("[")
        for i in arr: print("  "+str(i).replace(",",""))
        print("]")


def stringify(arr):
    sArr = '['
    for i in arr:
        sArr += '\n\t'+str(i)
    sArr += '\n]'
    return sArr


def ecrireEnsClauses(ensClauses, convSor):
    if convSor == 0:        clauseSeparator, elementSeparator, brackets = " and ",  " or", ["(",")"]
    elif convSor == 1:      clauseSeparator, elementSeparator, brackets = " ",      " ",    ["[","]"]
    else:                   clauseSeparator, elementSeparator, brackets = " + ",    "",     ["",""]

    ensClauses = clauseSeparator.join(map(str, parseConv2(ensClauses))).replace('[',brackets[0]).replace(']',brackets[1]).replace(',',elementSeparator).replace("'",'')
    if convSor == 1: ensClauses = "[ "+ensClauses+" ]"
    print(ensClauses)


# return atom / -atom
def occurences(arr, el):
    if -abs(el) in arr and not abs(el) in arr: return -1 # -a and not a
    if not abs(el) in arr and not -abs(el) in arr: return 0 # any of both
    if abs(el) in arr and not -abs(el) in arr: return 1 # a and not -a
    return 2 # both

# alphabetical array
def printInternalRepr(matrix):
    print("-"*152)
    for i in range(26):
        if i < 25: print(chr(i+97)+"  |  ", end="")
        else: print(chr(i+97))
    print("-"*152)

    for i in matrix:
        for j in range(len(i)):
            if j < len(i)-1: print(str(i[j])+(" "*(3-len(str(i[j]))))+"|  ", end="")
            else: print(str(i[j]))
    
    print() # blankspace

# read file and extract array then parse it to desired convention
def getArray(fle, convEnt):
    fd = open(fle, "r")
    arr = fd.read()
    fd.close()

    arr = arr.split('\n')
    for i in range(len(arr)): arr[i] = arr[i].split(' ')

    if convEnt == 1: return parseConv1(arr)
    return parseConv2(arr)


# algorithm to know how many occurence of atom/lit there is in clauses
def internalRepr(matrix):
    matrix = parseConv1(matrix)
    internal = [[] for row in matrix]
    for i in range(26):
        for j in range(len(matrix)):
            internal[j].append(occurences(matrix[j], i+1))
    return internal

# return internal representation of file clauses
def lireEnsClauses(fichEntree, convEnt):
    ensClauses = getArray(fichEntree, convEnt)
    #printArray(ensClauses)
    #algoDP(ensClauses, NIV_TRACE)
    return internalRepr(ensClauses)

# random generation of clauses
def genAleaEnsClauses(nbClauses, maxNumAtomes, maxLgClauses):
    matrix = [[randint(1,26) if randrange(-1,2,2) == 1 else -randint(1,26) for j in range(maxLgClauses)] for i in range(nbClauses)]
    return parseConv1(matrix) if args[1] == 1 else parseConv2(matrix)

# write new log file
def writeLog(content):
    path = "log"
    if not os.path.isdir(path): os.mkdir(path)
    nFiles = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) + 1
    nameFile = "log_"+str(nFiles)+"_trace_"+str(NIV_TRACE)+".txt"
    print("Log file created : "+path+"/"+nameFile)

    fd = open(path+"/"+nameFile, "w")
    fd.write("\n".join(LOG))
    fd.close()


# append log message in array of log
def log(msg=''):
    LOG.append(msg)

def removeArray(arr, arr2):
    for i in arr2:
        if i in arr: arr.remove(i)

# Davis and Putnam
def sat(ensClauses, verbose):
    F = ensClauses[:]
    log('\n\n'+('-'*50)+' F :\n'+str(F if args[1]==1 else parseConv2(F)))
        
    # 1.
    if len(F) == 0:
        if verbose: log('\nSATISFAISABLE')
        return True
    Lit1, Atomes, U = [], [], []

    # 2.
    i = 0
    for k in range(len(F)):
        if len(F[k-i]) == 0:
            if verbose: log("La clause "+str(k)+" est vide: NON SATISFAISABLE")
            return False
        C = F[k-i][:]
        if len(C) == 1:
            U.extend(C)
            F.remove(C)
            i += 1
            if verbose: log("La clause "+str(k)+" n'a qu'un litteral: ajout du litteral dans U et suppression dans F")
        for j in C:
            if not j in Lit1: Lit1.append(j)
            if not abs(j) in Atomes: Atomes.append(abs(j))
    
    if verbose: log("F apres la premiere etape: "+str(F)+"\nU: "+str(U)+"\nAtomes: "+str(Atomes)+"\nLit1: "+str(Lit1))

    # 3.
    for i in U:
        if -i in U:
            if verbose: log("Opposé de "+str(i)+" trouve dans U: contradiction: NON SATISFAISABLE")
            return False
    
    for k in range(len(F)):
        C = F[k][:]
        if any(lit in U for lit in C):
            if verbose: log("litteral dans la clause C "+str(k)+" trouve dans U: NON SATISFAISABLE")
            return False
    
    removeArray(Lit1, U)
    removeArray(Atomes, [abs(a) for a in U])
    if verbose:
        log("Suppression de tous les litteraux de U dans Lit1: "+str(Lit1))
        log("Suppression de tous les atomes de U dans Atomes: "+str(Atomes))

    # 4.
    if len(Lit1) > 0:
        i = 0
        for k in range(len(F)):
            C = F[k-i][:]
            if any(lit in Lit1 for lit in C):
                if verbose: log("litteral dans la clause C "+str(k)+" trouve dans Lit1: suppression de la clause C dans F")
                F.remove(C)
                i += 1
        removeArray(Atomes, [a for a in Lit1 if a >= 0])
        if verbose: log("Suppression de tous les atomes de Lit1 dans Atomes: "+str(Atomes)+"\nF: "+str(F))

    # 5.
    for i in range(len(F)):
        C = F[:]
        del C[i]
        for j in range(len(C)):
            if set(F[i]).issubset(C[j]): removeArray(C[j], F[i])
    
    if verbose: log('Phase omettable: F: '+str(F))
    

    # 6.
    if F != ensClauses: return sat(F, verbose)

    # 7.
    Fp, Fm = [], []
    if verbose: log('Construction de F+ et F-')
    for a in Atomes:
        i = 0
        for k in range(len(F)):
            C = F[k-i][:]
            if a in C:
                if verbose: log("Atome "+str(a)+" trouve dans C "+str(k)+": suppression de C dans F et ajout de l'atome dans F+")
                F.remove(C)
                Fp.append(C.remove(a))
                i += 1
            if -a in C:
                if verbose: log("inverse de l'Atome "+str(a)+" trouve dans C "+str(k)+": suppression de C dans F et ajout de l'inverse de l'atome dans F-")
                F.remove(C)
                Fm.append(C.remove(a))
                i += 1
    
    resaF = []
    for C in Fp:
        for D in Fm:
            n = C or D
            if not n in resaF: resaF.append(n)

    for i in resaF:
        if not i in F: F.append(i)
    
    if verbose:
        log('resa(F): '+str(resaF)+'\nUnion de resa(F) et F: '+str(F))

    # 8.
    return sat(F, verbose)


# function that init then call sat
def algoDP(ensClauses, nivTraces):
    LOG = []
    log('LOG Davis & Putnam - '+str(datetime.datetime.now())+'\nEnsemble de clauses :\n'+stringify(ensClauses))
    if sat(parseConv1(ensClauses), nivTraces==2): print("satisfaisable")
    else: print("non satisfaisable")
    if(nivTraces): writeLog(LOG)





############
# execution

if verifyInput(): exit(1)

# 2.2 - Lecture
ensClauses = lireEnsClauses(args[0], args[1])
printInternalRepr(ensClauses)

# 2.3 - Génération aléatoire d'ensemble de clauses
ensClauses = genAleaEnsClauses(NB_CLAUSES, MAX_NUM_ATOM, MAX_LG_CLAUSE)

# 2.4 - Ecriture
ecrireEnsClauses(ensClauses, WRITE_TYPE)
algoDP(ensClauses, NIV_TRACE)