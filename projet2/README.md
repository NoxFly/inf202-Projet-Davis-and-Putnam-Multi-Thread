# PROJET 2 - Davis et Putnam

binôme : non

Etudiant : Dorian Thivolle

commande : `python projet2.py path/to/file.txt convention`

`convention` doit être compris entre 1 et 2.

Lit le fichier mit en paramètre, génère le tableau et le convertit sous la convention voulue.

Créer et renvoie un tableau de représentation interne de l'ensemble de clauses, puis l'affiche.

Ensuite, génère aléatoirement un ensemble de clauses suivant des constantes déclarée en début du fichier, puis l'affiche suivant le type de forme voulue (et/ou | [[][]] | .+).

## EXEMPLE :

Si la commande est `python projet2.py data.txt 2`
Pour un fichier data.txt ayant pour contenu :
```
3 7 -2 -5 -6
1 5 7 -3 -4 -5
```

Créé un tableau comme suit :
```
[
    [ 3, 7, -2, -5, -6 ],
    [ 1, 5, 7, -3, -4, -5 ]
]
```

puis le convertit sous la seconde convention :
```
[
    [ c, g, -b, -e, -f ],
    [ a, e, g, -c, -d, -e ]
]
```

Enfin, créé et retourne le tableau de représentation interne, et l'affiche avec comme en-tête l'alphabet :

| a   |  b  |  c  |  d  |  e  |  f  |  g  | ... |  z
| --- | --- | --- | --- | --- | --- | --- | ... | ---
| 0   | -1  | 1   | 0   | -1  | -1  | 1   | ... | 0
| 1   | 0   | -1  | -1  | 2   | 0   | 1   | ... | 0

Génère un ensemble de clauses aléatoire, par exemple avec comme paramètres :

* nbClauses : 2
* maxNumAtome : 22
* maxLgClause : 5

```
[
    [ c, -q, -t, -o, v ],
    [ i, n, s, j, -k ]
]
```

puis l'affiche :

* pour la forme `convSor = 0` :

`(c or -q or -t or -o or v) and (i or n or s or j or -k)`

* pour la forme `convSor = 1` :

`[ [c -q -t -o v] [i n s j -j] ]`

* et pour la forme `convSor = 2` :

`c-q-t-ov + insj-k`