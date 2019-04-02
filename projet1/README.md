# PROJET 1 - transitivité

commande : `python projet.py (-s) program1 [ program2 program3... ]`

utilise 2 méthodes:
* sequentielle
* parallèle

par défaut: parallèle

avec l'option `-s`: sequentielle

pour chaque fichier mit en argument, affiche (exemple avec **program2**):

### **Array:**

/  |   ID    | constante    | dependance 1    | dependance 2 | dependance 3
-- | ------- | ------------ | --------------- | ------------ | -------------
0  |   3     | 1            | -1              | -1           | -1
1  |   7     | 3            | 3               | -1           | -1
2  |   5     | 0            | 7               | -1           | -1
3  |   0     | 11           | 5               | -1           | -1

### **Before:**

/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | 0 | 1 | 0 | 0
1  | 0 | 0 | 1 | 0
2  | 0 | 0 | 0 | 1
3  | 0 | 0 | 0 | 0

### **After:**

/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | 0 | 1 | 1 | 1
1  | 0 | 0 | 1 | 1
2  | 0 | 0 | 0 | 1
3  | 0 | 0 | 0 | 0

et suivant l'option mit en argument:

### **Execution séquentielle:**

/  | 0     | 1     | 2     | 3
---|-------|-------|-------|-------
0  | False | True  | True  | True
1  | False | False | True  | True
2  | False | False | False | True
3  | False | False | False | False

(toutes les case en dessus de la dioganole sont **True** sinon **False**)

### **Execution parallèle:**

Si le processeur a 4 coeurs (pour simplifier l'affichage)

Thd = Thread, chaque coeur/thread pouvant executer une tâche

Chaque executable étant dépendant d'un seul ou plusieurs autre(s) executable(s) se retrouve dans le même Thread, et s'executera après sa dépendance

/      | Thd 1  | Thd2  | Thd3  | Thd4
-------|--------|-------|-------|-------
task 1 | 0      | False | False | False
task 2 | 1      | False | False | False
task 3 | 2      | False | False | False
task 4 | 3      | False | False | False



les Tableaux **after**, **before** et **execution sequentielle** appliqués à la fonction **afficheRelation** sont affiché comme suit (les `0` sont remplacés par des `*` et les `1` par des `<`) :

/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | * | < | < | <
1  | * | * | < | <
2  | * | * | * | <
3  | * | * | * | *

### Memoire

affiche chaque ligne d'execution de façon séparé avec l'id de la ligne et sa constante.

si c'est son tour d'execution, alors sa constante devient const(id(n)) + const(id(n-1)) (const affichée)

donc pour:
* x3: 0 + 1 = 1
* x7: 3 + const(x3) = 3 + 1 = 4
* x5: 0 + const(x7) = 0 + 4 = 4
* x0: 11 + const(x5) = 11 + 4 = 15

**Résultat:**

tache | id1 + const1 | id2 + const2 | id3 + const3 | id4 + const4
------|--------------|--------------|--------------|-------------
-1    | x3: 0        | x7: 0        | x5: 0        | x0: 0
0     | [[ x3: 1 ]]  | x7: 0        | x5: 0        | x0: 0
1     | x3: 1        | [[ x7: 4 ]]  | x5: 0        | x0: 0
2     | x3: 1        | x7: 4        | [[ x5: 4 ]]  | x0: 0
3     | x3: 1        | x7: 4        | x5: 4        | x0: 15
