# projet 2 inf202
# Dorian THIVOLLE

# imports
import sys, os, re
from random import randint, randrange

# vars
argc = len(sys.argv) - 1
args = sys.argv[1:]

# CONSTS
NB_CLAUSES = 2
MAX_NUM_ATOM = 6
MAX_LG_CLAUSE = 5
WRITE_TYPE = 0


# verification of given arguments
def verifyInput():
    if argc != 2:
        print("2 arguments expected.",argc,"given")
        return 1

    pattern = re.compile("[\w\/\\\_\-]+\.txt")
    if not pattern.match(args[0]):
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


def lireEnsClauses(fichEntree, convEnt):
    return internalRepr(getArray(fichEntree, convEnt))


def genAleaEnsClauses(nbClauses, maxNumAtomes, maxLgClauses):
    matrix = [[randint(1,27) if randrange(-1,2,2) == 1 else -randint(1,27) for j in range(maxLgClauses)] for i in range(nbClauses)]
    return parseConv1(matrix) if args[1] == 1 else parseConv2(matrix)

def ecrireEnsClauses(ensClauses, convSor):
    # and / or
    if convSor == 0: clauseSeparator, elementSeparator, brackets = " and ", " or ", ["(",")"]
    # [[][]]
    elif convSor == 1: clauseSeparator, elementSeparator, brackets = " ", " ", ["[","]"]
    # +- | default
    else: clauseSeparator, elementSeparator, brackets = " + ", "", ["",""]

    ensClauses = clauseSeparator.join(map(str, parseConv2(ensClauses))).replace('[',brackets[0]).replace(']',brackets[1]).replace(',',elementSeparator)
    if convSor == 1: ensClauses = "[ "+ensClauses+" ]"
    print(ensClauses)

# execution

if verifyInput(): exit(1)

# 2.2 - Lecture
ensClauses = lireEnsClauses(args[0], args[1])
printInternalRepr(ensClauses)

# 2.3 - Génération aléatoire d'ensemble de clauses
ensClauses = genAleaEnsClauses(NB_CLAUSES, MAX_NUM_ATOM, MAX_LG_CLAUSE)
print(ensClauses)
# 2.4 - Ecriture
#ecrireEnsClauses(ensClauses, WRITE_TYPE)