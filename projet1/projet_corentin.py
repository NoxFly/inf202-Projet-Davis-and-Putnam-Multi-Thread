import copy

def readProgram(filename):
    compt = 0
    Dprog = []
    f = open(filename, "r+") #ouvre le fichier en lecture
	
    for line in f: #compte le nombre de ligne
        compt += 1

    f.seek(0) #revien au depart du fichier
    for i in range(compt):
        line = f.readline() #lecture de la ligne
        line_str = line.split() #coupe les caractere
        line_int = []
        
        for charact in line_str: #transforme les char en int
            line_int.append(int(charact))
			
        Dprog.append(line_int) #stock le tableau de la ligne dans le tableau final

    f.close()
    return Dprog	

def	printProgram(listoflists):
	print("\n")
	for tab in listoflists:
		print(tab)

def progDep(listoflists):
	#Before
	Before = []
	for i in range(len(listoflists)): #chiffre correspondant au nombre de sous tableau
		minibefore = [0]*len(listoflists)
		for tab in listoflists[i][2:]: #tout les variable utiliser pour les sous tableau
			if tab != -1:
				for j in range(i):
					if (tab == listoflists[j][0]):
						minibefore[j] = 1	
				
		Before.append(minibefore)
	
	return Before
	
def clotureTrasitive(listbefore):	
	#After
	After = listbefore[:]
	After_pre = After[:]
	
	for l in range(len(After)^2):
		for i in range(len(After)):
			for j in range(len(After)):
				if After_pre[i][j] == 1:
					for k in range(len(After)):
						if After_pre[j][k] == 1:
							After_pre[i][k] = 1
		
		if After_pre == After:
			break
		else:
			After = After_pre

	return After
	
def afficheRelation(R):
	
	print("   |",end='')
	for i in range(len(R)):
		if i<10:
			print(" "+str(i)+" |",end='')
		elif i<100:
			print(" "+str(i)+"|",end='')
		else:
			print(str(i)+"|",end='')
	
	print("")
	
	for i in range(len(R)):
		if i<10:
			print(" "+str(i)+" |",end='')
		elif i<100:
			print(" "+str(i)+"|",end='')
		else:
			print(str(i)+"|",end='')
		
		for j in range(len(R)):
			if R[j][i] == 1:
				print(" < |",end='')
			else:
				print(" * |",end='')
	
		print("")

def relationSequentielle(L,R):
	tab = []
	for i in range(L):
		tab2 = []
		for j in range(L):
			if i==j-1:
				tab2.append(1)
			else:
				tab2.append(0)
		tab.append(tab2)
	tab = R(tab)
	return tab
	
def RemplitPlacement(After):
	N = len(After)
	Placee = [False]*N
	etape = 0
	Placement = []
	
	while Placee.count(False) != 0:
		tmp = []
		for element in range(N):
			if Placee[element] == False:
				variable_calculer = True
				for i in range(N):
					if After[element][i] == 1 and Placee[i] == False:
						variable_calculer = False
				
				
				if variable_calculer == True:
					tmp.append(element)
		
		for i in tmp:
			Placee[i] = True
		
		Placement.append(tmp)
		etape += 1

	return Placement

def affichePlacee(Placee):
	
	print("[",end='')
	for i in range(len(Placee)):
		if Placee[i] == True:
			print("1",end='')
		else:
			print("0",end='')
		
		if i != len(Placee)-1:
			print(",",end='')
			
	print("]")

def calculMemoire(Placement,Program):
	V=0
	Memoire = []
	Memoire_ligne = []
	for i in Placement:
		for j in i:
			V+=1
	
	for i in Program:
		Memoire_ligne = Memoire_ligne+[i[0],0,0]
	Memoire.append(Memoire_ligne.copy())
	
	for i in Placement:
		for j in i:
			if Memoire_ligne[j*3+1] == 0:
				somme = Program[j][1]
				for k in range(3):
					if Program[j][k+2] != -1:
						somme_tmp = 0
						for x in range(0, len(Memoire_ligne), 3):
							if Memoire_ligne[x] == Program[j][k+2] and Memoire_ligne[x+1] != 0:
								somme_tmp = Memoire_ligne[x+2]
						somme+= somme_tmp
								
			
				Memoire_ligne[j*3+1] = 1
				Memoire_ligne[j*3+2] = somme
		Memoire.append(Memoire_ligne.copy())
	
	return Memoire

def afficheMemoire(M):
	for i in range(len(M)):
		for j in range(0,len(M[i]),3):
			if j==0:
				print(str(i-1)+": ",end='')
			if M[i][j+1] == 0: 1
				#print("x"+str(M[i][j])+":? ",end='')
			elif i==0 or (i != 0 and M[i-1][j+1] == 0):
				print("[[x"+str(M[i][j])+":"+str(M[i][j+2])+"]] ",end='')
			else: 1
				#print("x"+str(M[i][j])+":"+str(M[i][j+2])+" ",end='')
		print("")
			
def affichePlacement(Placement):
	for i in Placement:
		for j in i:
			print(str(j)+" ",end='')
		print("")
	print("\n")

p = readProgram("programs/program4.txt")
print("\n")
t = progDep(p)
c = clotureTrasitive(t)
print("")
a = RemplitPlacement(c)
a = RemplitPlacement(c)
affichePlacement(a)
FIN = calculMemoire(a,p)
afficheMemoire(FIN)
