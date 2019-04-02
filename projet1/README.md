# PROJET 1 - transitivité

commande : `python projet.py (-s) program1 [ program2 program3... ]`

utilise 2 méthodes:
    * sequentielle
    * parallèle

par défaut: parallèle
avec l'option `-s`: sequentielle

pour chaque fichier mit en argument, affiche (exemple avec **program2**):

Array:
/  |   ID    | constante    | dependance 1    | dependance 2 | dependance 3
-- | ------- | ------------ | --------------- | ------------ | -------------
0  |   3     | 1            | -1              | -1           | -1
1  |   7     | 3            | 3               | -1           | -1
2  |   5     | 0            | 7               | -1           | -1
3  |   0     | 11           | 5               | -1           | -1

Before:
/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | 0 | 1 | 0 | 0
1  | 0 | 0 | 1 | 0
2  | 0 | 0 | 0 | 1
3  | 0 | 0 | 0 | 0

After:
/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | 0 | 1 | 1 | 1
1  | 0 | 0 | 1 | 1
2  | 0 | 0 | 0 | 1
3  | 0 | 0 | 0 | 0

et suivant l'option mit en argument:

Execution séquentielle:
/  | 0 | 1 | 2 | 3
---|---|---|---|---
0  | 0 | 1 | 1 | 1
1  | 0 | 0 | 1 | 1
2  | 0 | 0 | 0 | 1
3  | 0 | 0 | 0 | 0

(toutes les case en dessus de la dioganole sont **True** sinon **False**)

Execution parallèle
/      | Thd 1 | Thd2 | Thd3 | Thd4
-------|-------|------|------|------
task 1 | 0     | 1    | 2    | 3

les Tableaux **after**, **before** et **execution sequentielle** appliqués à la fonction __afficheRelation__ sont affiché comme suit (les `0` sont remplacés par des `*` et les `1` par des `<`) :
/ | 0 | 1 | 2 | 3
---|---|---|---|-
0  | * | < | < | <
1  | * | * | < | <
2  | * | * | * | <
3  | * | * | * | *
