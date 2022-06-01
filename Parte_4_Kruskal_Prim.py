# -- coding: utf-8 --
"""
Created on Sat Mar 19 18:08:24 2022
@author: Mayapache
¡PirateⒶ y difunde!
"""

'''
Biblioteca de generación aleatoria de grafos
Parte de la materia de diseño y analisis de algoritmos, CIC-IPN
Clases:
    -Grafo
        -G,V, tipo
        -Exporta Grafo
    -Vertice
        -Nombre, posición x, posición y
        -Agrega +1 a su grado
    -Arista
        -Fuente, Destino, Distancia
Funciones generadoras:
    -Gnm_Erdo_Renyi(n,m,Nom,dirigido=False,auto=False)
    -Gnp_Gilbert(n,p,Nom,dirigido=False,auto=False)
    -Gnr_Geograf_Simple(n,r,Nom,dirigido=False, auto=False)
    -Gnd_Barrbasi_Albert(n,d,Nom,dirigido=False,auto=False)
    -Gmn_Malla(n,m,Nom,dirigido=False)
    -Dorogovtsev_Mendes(n,Nom,dirigido=False)

El trabajo a futuro de cada función y clase están como comentarios
justo antes de que se definan, así como una pequeña descripción de la funcion

'''

import random
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import copy
import time as tm



#---------------------DEFINICION DE CLASES-------------------

class Grafo:
    def __init__(self, nom, tipo="graph",ruta=False):
        self.Nom = nom
        self.Vert = []
        self.Aris = []
        self.Tipo = tipo
        self.Ruta = ruta
        self.Lis_aris=[]
        self.Lis_nod=[]
        self.Lis_pes_nod=[]
    def Agrega_Vertices(self,vec_ver):
        self.Vert.extend(vec_ver)
    def Agrega_Aristas(self,vec_ari):
        self.Aris.extend(vec_ari)
    def Obten_Vertices(self):
        return self.Vert
    def Obten_Aristas(self):
        return self.Aris
    #Opción de agregar más información a los vértices y a los nodos, acorde a la naturaleza del grafo generado
    #Opción de exportar en otros formatos además del .gv
    
    def Exporta_grafo(self,nombre_doc,peso_aleat=False):
        dot_str=self.Tipo+" "+self.Nom+" {\n"
        if self.Ruta:
            for i in range(len(self.Vert)):
                if i in self.Lis_nod:
                    pos_nod=self.Lis_nod.index(i)
                    dot_str+=str(self.Vert[i].Nom)+" [label=nd_"+str(self.Vert[i].Nom)+"("+str(self.Lis_pes_nod[pos_nod])+")];\n"
    #[label="hello world"]            
                else: #Si no está conectado
                    dot_str+=str(self.Vert[i].Nom)+";\n"
        else:
            for i in range(len(self.Vert)):
                dot_str+=str(self.Vert[i].Nom)+";\n"
        #********************
        if self.Tipo=="graph":
            union=" -- "
        else:
            union=" -> "
        #****************************
        if peso_aleat:
            for i in range(len(self.Aris)):
                dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+"[weight=\""+str(round(random.random()*4)+1)+ "\"]"+";\n"
        elif self.Ruta:
            for i in range(len(self.Aris)):
                dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+"[weight=\""+str(self.Aris[i].Pes)+ "\"]"+";\n"
                
        else:
            for i in range(len(self.Aris)):
                dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+" [color=black];\n"
        
        if self.Ruta:
            for i in range(len(self.Lis_aris)):
                dot_str+=str(self.Lis_aris[i][0])+union+str(self.Lis_aris[i][1])+" [color=red,] ;\n"
        dot_str+="}"
        with open('C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Arch_gv_4/'+nombre_doc+'.gv', 'w') as f:
            f.write(dot_str)
        print(dot_str)


        #Agregar características de vértice
        #¿Agregar opción de posición en z? ¿Cambiar a un vector de parámetros?
class Vertice:
    def __init__(self, Nom, posx=0, posy=0, deg=0):
        self.Nom = Nom
        self.Posx = posx
        self.Posy = posy
        self.Deg = deg
        self.Peso_desde = 0
    def Obten_Nom(self):
        return self.Nom
    def Obten_Deg(self):
        return self.Deg
    def Suma_Deg(self):
        self.Deg+=1
        
        #Agregar/cambiar distancia por peso de la arista
        #¿Agregar característica de dirigida o no dirigida?
class Arista:
    def __init__(self, fue, des, dis=0,pes=0):
        self.Fue = fue
        self.Des = des
        self.Dis=dis
        self.Pes=pes
    def Obten_Fue(self):
        return self.Fue
    def Obten_Des(self):
        return self.Des
    def Obten_Fue_Des(self):
        return [self.Fue,self.Des]


#---------------------ALGORITMOS DE GENERACION DE GRAFOS-------------------


     #Función auxiliar para el geográfico
def distancia(ax,ay,bx,by):
    dis=mt.sqrt((ax-bx)**2+(ay-by)**2)
    return dis


    #Agregar limitante de m, acorde a n, auto y dirigido, pa evitar loop infinito
    #Descripción: n vértices, elegir unif al azar m pares de nodos pa unir
def Gnm_Erdo_Renyi(n,m,Nom,dirigido=False,auto=False):
    mat_ady=np.zeros((n,n),dtype=int)    
    Vert=[]
    for i in range(n):
        Vert.append(Vertice(i))
    Aris=[]
    for i in range(m):  
        while True:    
            fue=random.randint(0,n-1)
            des=random.randint(0,n-1)
            if ( (fue!=des) or auto ) and mat_ady[fue][des]==0:
                break
        mat_ady[fue][des]=1
        Aris.append(Arista(fue,des))
        if not dirigido:
            mat_ady[des][fue]=1
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf

    #Falta dirigido=True, doble posibilidad de nodo, ida y de vuelta
    #n nodos, p probabilidad se forme o no arista entre cada par 
def Gnp_Gilbert(n,p,Nom,dirigido=False,auto=False):  
    Vert=[]
    for i in range(n):
        Vert.append(Vertice(i))
    Aris=[]
    lim=n+auto-1
    for i in range(n):
        if not dirigido:
            lim=i+auto
        for j in range(lim):
            if random.random()<=p:
                if auto or (not i==j):
                    Aris.append(Arista(i,j))
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf

    #Dirigido ¿?, uno implica el otro 
    #¿? radios aleatorios en un rango por cada nodo, agregar caracterisitaca al vertice
    #Comentarios sirven para el ploteo
    #Descripción: n nodos, distrbuidis aleatoriamente espacio, arista para nodos a distancia<r 
def Gnr_Geograf_Simple(n,r,Nom,dirigido=False, auto=False):    
    Vert=[]
    vec_x=[]
    vec_y=[]
    Aris=[]
    plt.figure()
    for i in range (n):
        px=random.random()
        vec_x.append(px)
        py=random.random()
        vec_y.append(py)
        Vert.append(Vertice(i,posx=px,posy=py))
    plt.scatter(vec_x,vec_y)
    for i in range(n):
        plt.text(vec_x[i],vec_y[i],i)
    for i in range(n):
        for j in range(n-i-1+auto):
            dist=distancia(vec_x[i],vec_y[i],vec_x[n-j-1],vec_y[n-j-1])
            if dist<r:
                Aris.append(Arista(i,n-j-1,dis=dist))
                plt.plot([vec_x[i],vec_x[n-j-1]],[vec_y[i],vec_y[n-j-1]])
    Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


    #Optimizar el uso del vec_v, ¿es necesario? 
    #Si es dirigido, ¿en qué dirección? (nuevo a viejo, viceversa, aleatorio?)
    #generamos nuevo nodo, probabilidad de conectar con viejos=1-grad(nviejo)/d
    #limitar d
def Gnd_Barabasi_Albert(n,d,Nom,dirigido=False,auto=False):    
    Vert=[]
    vec_v=[]
    Aris=[]
    for i in range(n): #generamos nuevo nodo
        Vert.append(Vertice(i))
        vec_v.append(0)
        for j in range (0,i): #comparamos con los viejos nodos
            p=1-vec_v[j]/d
            if random.random()<p:
                Aris.append(Arista(i,j))
                vec_v[i]+=1
                vec_v[j]+=1
                Vert[i].Suma_Deg()
                Vert[j].Suma_Deg()
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf

    #Opción malla Hexagonal
    #Generamos n*m nodos, nodo i,j, con nodo i+1,j  y  i,j+1
def Gmn_Malla(n,m,Nom,dirigido=False,pacman=False):
    #n es el ancho, m es la altura
    Vert=[]
    Aris=[]    
    #vec_x=[]
    #vec_y=[]
    #plt.figure()
    cont=0
    for j in range(m):
        for i in range(n): #generamos nuevo nodo    
            #vec_x.append(i)
            #vec_y.append(j)
            Vert.append(Vertice(cont, posx=i, posy=j))
            cont+=1
    #plt.scatter(vec_x,vec_y)
    #for i in range(m*n):
     #   plt.text(vec_x[i],vec_y[i],i)
    #Aristas principales
    for j in range(m-1):
        for i in range(n-1):
            #plt.plot([vec_x[i+n*j],vec_x[i+1+j*n]],[vec_y[i+n*j],vec_y[i+1+j*n]])
            #plt.plot([vec_x[i+n*j],vec_x[i+n+j*n]],[vec_y[i+n*j],vec_y[i+n+j*n]])
            Aris.append(Arista(i+n*j,i+1+j*n))
            Aris.append(Arista(i+n*j,i+n+j*n))
    #Hasta la derecha
    for i in range(m-1): #n es el ancho, m es la altura
        Aris.append(Arista(n-1+i*n,2*n-1+i*n)) 
        #plt.plot([vec_x[n-1+i*n],vec_x[2*n-1+i*n]],[vec_y[n-1+i*n],vec_y[2*n-1+i*n]])
    #Hasta arriba
    for i in range(n-1): #n es el ancho, m es la altura
        Aris.append(Arista(n*(m-1)+i,n*(m-1)+i+1))
        #plt.plot([vec_x[n*(m-1)+i],vec_x[n*(m-1)+i+1]],[vec_y[n*(m-1)+i],vec_y[n*(m-1)+i+1]])
    if pacman: #si es un mundo pacman y el final es el inicio :o Ö o.o O_O
        #Conectamos derecha con izquierda
        for i in range(m):
            Aris.append(Arista(n-1+i*n,i*n))
            #plt.plot([vec_x[n-1+i*n],vec_x[i*n]],[vec_y[n-1+i*n],vec_y[i*n]])
        #Conectamos arriba con abajo
        for i in range(n):
            Aris.append(Arista(n*(m-1)+i,i))
            #plt.plot([vec_x[n*(m-1)+i],vec_x[i]],[vec_y[n*(m-1)+i],vec_y[i]])
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


    #Opciones de figuras iniciales
    #Acomodar/pensar si fuera dirigida
    #Descripción: Generamos tres nodos iniciales conectados entre sí, 
    #agregamos nodo y elegimos arista al azar, conectamos el nodo nuevo a 
    #cada extremo  de la arista elegida, opción a limitar el grado de los nodos
def Dorogovtsev_Mendes(n,Nom,dirigido=False,limite=0):
    Vert=[] #Vector de objetos Vertice(nom,deg=0)
    Aris=[] #Vector de objetos Arista(fue,des) # de las posiciones del vector de vertices
    #Primeros tres nodos
    for i in range(3):
        Vert.append(Vertice(i))
    Aris.append(Arista(0,1))
    Aris.append(Arista(1,2))
    Aris.append(Arista(2,0))
    if limite:
        Vert[0].Suma_Deg()
        Vert[1].Suma_Deg()
        Vert[2].Suma_Deg()
        Vert[0].Suma_Deg()
        Vert[1].Suma_Deg()
        Vert[2].Suma_Deg()
    for i in range(n-3):
        Vert.append(Vertice(i+3))
        if limite:
            bandera=True
            while bandera:
                selec=random.randint(0,len(Aris)-1)
                if Vert[Aris[selec].Obten_Fue()].Obten_Deg()<limite and Vert[Aris[selec].Obten_Des()].Obten_Deg()<limite:
                    bandera=False
        else:
            selec=random.randint(0,len(Aris)-1)
        Aris.append(Arista(i+3,Aris[selec].Obten_Fue()))
        Aris.append(Arista(i+3,Aris[selec].Obten_Des()))
        if limite:
            Vert[-1].Suma_Deg()
            Vert[-1].Suma_Deg()
            Vert[Aris[selec].Obten_Fue()].Suma_Deg()
            Vert[Aris[selec].Obten_Des()].Suma_Deg()
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


def Gmn_Malla_Hex(n,m,Nom,dirigido=False):
    #n es el ancho, m es la altura
    Vert=[]
    Aris=[]
    #vec_x=[]
    #vec_y=[]
    #plt.figure()
    cont=0
    for j in range(m):
        for i in range(n): #generamos nuevo nodo    
            #vec_x.append(i)
            if i%2: #Si es impar
                Vert.append(Vertice(cont, posx=i, posy=j+.5))
                #vec_y.append(j+.5)
            else:
                Vert.append(Vertice(cont, posx=i, posy=j))
                #vec_y.append(j)
            cont+=1
    #plt.scatter(vec_x,vec_y)
    #for i in range(m*n):
        #plt.text(vec_x[i],vec_y[i],i)
    
    #n es el ancho, m es la altura
    #A la derecha
    for j in range(m):
        for i in range(n-1):
            #plt.plot([vec_x[i+n*j],vec_x[i+1+j*n]],[vec_y[i+n*j],vec_y[i+1+j*n]])
            Aris.append(Arista(i+n*j,i+1+j*n))#A la derecha
    #Arriba
    for j in range(m-1):
        for i in range(n):
            #plt.plot([vec_x[i+n*j],vec_x[i+n+j*n]],[vec_y[i+n*j],vec_y[i+n+j*n]])
            Aris.append(Arista(i+n*j,i+n+j*n)) #Arriba
    
    #Los pares, abajo a la derecha
    for j in range(1,m):
        for i in range(0,n-1,2): 
            #plt.plot([vec_x[i+n*j],vec_x[i-n+j*n+1]],[vec_y[i+n*j],vec_y[i-n+j*n+1]])
            Aris.append(Arista(i+n*j,i-n+j*n+1)) #Arriba
    
    #Los impares, arriba a la derecha
    for j in range(m-1):
        for i in range(1,n-1,2): 
            #plt.plot([vec_x[i+n*j],vec_x[i+n+j*n+1]],[vec_y[i+n*j],vec_y[i+n+j*n+1]])
            Aris.append(Arista(i+n*j,i+n+j*n+1)) #Arriba
    
    
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf

#---------------------ALGORITMOS DE ARBOLES-------------------

#optimizar/limitar la búsqueda con: forma matricial de nodos, o, grados de nodos, o lista de aristas en cada vertice
#optimizar por variables usadas
def BFS(a,s): #Búsqueda a lo Ancho, s= nodo fuente
    grf=copy.deepcopy(a)
    Vert=[]
    Aris=[]
    Vert.append(Vertice(s))
    L=[s]
    cambios=1
    agregados=1
    while cambios:
        cambios=0
        rng=range(agregados)
        agregados=0
        xagregar=[]
        for i in rng:
            popear=[]
            for j in range(len(grf.Aris)): #Para todas las aristas
                if (L[-i-1] in grf.Aris[j].Obten_Fue_Des()): #Si está
                    if grf.Aris[j].Obten_Fue_Des().index(L[-i-1]): #Si está en la 2da posición
                        otro_nodo=grf.Aris[j].Obten_Fue_Des()[0]
                    else:
                        otro_nodo=grf.Aris[j].Obten_Fue_Des()[1]
                    if (otro_nodo not in L) and (otro_nodo not in xagregar): #el otro valor no en L
                            xagregar.append(otro_nodo) #lo agregamos a L
                            Aris.append(grf.Aris[j])
                            agregados+=1
                            cambios=1
                    popear.append(j) #Arista ya revisada
            for k in range(len(popear)):
                grf.Aris.pop(popear[-k-1])
        for k in range(len(xagregar)):    
            Vert.append(Vertice(xagregar[k]))
        L.extend(xagregar)
    Nom=grf.Nom+"_BFS"
    Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf

def excava(nodo, L, grf, ari):    
    for j in range(len(grf.Aris)): #Para todas las aristas
        if nodo in grf.Aris[j].Obten_Fue_Des(): #Si está
            if grf.Aris[j].Obten_Fue_Des().index(nodo): #Si está en la 2da posición
                otro_nodo=grf.Aris[j].Obten_Fue_Des()[0]
            else:
                otro_nodo=grf.Aris[j].Obten_Fue_Des()[1]
            if otro_nodo not in L: #el otro valor no en L, nos vamos hacia allá
                ari.append(Arista(nodo,otro_nodo))
                L.append(otro_nodo)
                L,ari=excava(otro_nodo,L,grf,ari) #Nuevo nodo de posición
    return L, ari
def DFS_R(a,s):
    lista=[s]
    grf=copy.deepcopy(a)

    Aris=[]
    Vert=[]
    lista_v,Aris=excava(s,lista,grf,Aris)
    for i in range(len(lista_v)):
        Vert.append(Vertice(lista[i]))
    Nom=grf.Nom+"_DFS_R"
    Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


def DFS_I(a,s):    
    grf=copy.deepcopy(a)
    L=[s]
    Vert=[]
    Vert.append(Vertice(s))
    Aris=[]
    pos=0
    while pos<len(L):
        nodo=L[pos]
        for j in range(len(grf.Aris)): #Para todas las aristas
            if nodo in grf.Aris[j].Obten_Fue_Des(): #Si está
                if grf.Aris[j].Obten_Fue_Des().index(nodo): #Si está en la 2da posición
                    otro_nodo=grf.Aris[j].Obten_Fue_Des()[0]
                else:
                    otro_nodo=grf.Aris[j].Obten_Fue_Des()[1]
                if otro_nodo not in L: #el otro valor no en L, nos vamos hacia allá
                    L=[otro_nodo]+L
                    Aris.append(Arista(nodo,otro_nodo))
                    Vert.append(Vertice(otro_nodo))
                    suma=0
                    pos=0
                    break
        pos+=suma
        suma=1
    Nom=grf.Nom+"_DFS_I"
    Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf
    
def Dijikstra(a):
    grf=copy.deepcopy(a)
    #dijikstra
    Nu_vert=len(grf.Vert)
    origen=round(random.random()*(Nu_vert-1))
            #Empieza árbol de expansión mínima
    #Creamos matriz de vertices
    mat_vert=np.zeros((Nu_vert,Nu_vert),dtype=int)
    for i in range(len(a.Aris)):
        mat_vert[a.Aris[i].Fue][a.Aris[i].Des]=a.Aris[i].Pes
        mat_vert[a.Aris[i].Des][a.Aris[i].Fue]=a.Aris[i].Pes
    #inicializamos :D
    lis_nod_rec=[origen] #Lista de nodos ya reconocidos
    lis_nod_rec_pes=[0] # Lista de los pesos de los nodos ya reconocidos
    lis_ari_rec=[] #Lista de Aristas reconocidas
    lis_nod_ady=np.asarray(np.where(mat_vert[origen]>0)[0])     #Lista de nodos adyacentes a los ya reconocidos
    lis_ari_ady=[]  #Lista de aristas adyacentes
    for i in range(len(lis_nod_ady)):
        lis_ari_ady.append([origen,lis_nod_ady[i]])
    lis_pes_ari_ady=mat_vert[origen][lis_nod_ady]   #Lista de los pesos de las aristas adyacentes
    lis_pes_nod_ady=mat_vert[origen][lis_nod_ady]   #Lista de los pesos de los nodos adyacentes
    
    #Quitamos los pesos que dan a lo que hay en la lsita de aristas recorridas :D
    for i in range(Nu_vert):
        mat_vert[origen][i]=0
        mat_vert[i][origen]=0    

    while len(lis_nod_ady): #Mientras hayan nodos por explorar
        selec=np.where(lis_pes_nod_ady==min(lis_pes_nod_ady))[0] #encontramos el de menor peso :DD
        selec=selec[0]
        #Actualizamos los recorridos al agregar el de menor peso
        lis_ari_rec.append(lis_ari_ady[selec])
        lis_nod_rec.append(lis_nod_ady[selec])
        lis_nod_rec_pes.append(lis_pes_nod_ady[selec])
        
        #Actualizamos adyacencias,nodos, aristas, peso aristas, peso nodos
        #primero vemos lo nuevo
        nod_selec=lis_nod_ady[selec]
        lis_nod_nue=np.where(mat_vert[nod_selec]>0)[0]
        lis_ari_nue=[]
        for i in range(len(lis_nod_nue)):
            lis_ari_nue.append([nod_selec,lis_nod_nue[i]])
        lis_pes_ari_nue=mat_vert[nod_selec][lis_nod_nue]
        lis_pes_nod_nue=lis_pes_ari_nue+lis_pes_nod_ady[selec]
        #Ahora sí actualizamos listas :D con el menoooor    
        for i in range(len(lis_nod_nue)):
            if lis_nod_nue[i] not in lis_nod_ady: #si son nodos completamente nuevos...
                lis_nod_ady=np.append(lis_nod_ady,lis_nod_nue[i])
                lis_ari_ady.append(lis_ari_nue[i])
                lis_pes_ari_ady=np.append(lis_pes_ari_ady,lis_pes_ari_nue[i])
                lis_pes_nod_ady=np.append(lis_pes_nod_ady,lis_pes_nod_nue[i])
            else:       #si el nodo ya estaba conectado por otro lado
                disputa=np.where(lis_nod_ady==lis_nod_nue[i])[0] #encontramos la posición de disputa
                disputa=disputa[0]
                if lis_pes_nod_ady[disputa]>lis_pes_nod_nue[i]: #si el peso por el nuevo camino es menor...
                    lis_ari_ady[disputa]=lis_ari_nue[i]
                    lis_pes_nod_ady[disputa]=lis_pes_nod_nue[i]
                    lis_pes_ari_ady[disputa]=lis_pes_ari_nue[i]
        #Quitamos de la matriz pa no repetirts
        for i in range(Nu_vert):
            mat_vert[nod_selec][i]=0
            mat_vert[i][nod_selec]=0

        #Quitamos de las adyecencias lo seleccionado :D
        lis_nod_ady=np.delete(lis_nod_ady,selec)
        lis_ari_ady.pop(selec)
        lis_pes_nod_ady=np.delete(lis_pes_nod_ady,selec)
        lis_pes_ari_ady=np.delete(lis_pes_ari_ady,selec)    
    #Encontramos ahora el camino, marcando las aristas  y vertices, empezando por el final
    #y para atrás, buscando el de menor costo :D    
    #rut_ari=[]
    #inicializamos ruta de las aristas
    '''
    for i in range(len(lis_ari_rec)):
        if lis_ari_rec[i][1]==destino:
            rut_ari.append(lis_ari_rec[i])    
    while rut_ari[-1][0]!=origen:
        for i in range(len(lis_ari_rec)):
            if lis_ari_rec[i][1]==rut_ari[-1][0]:
                rut_ari.append(lis_ari_rec[i])    
                '''
    #Colocamos los datos en el grafo
    grf.Nom=grf.Nom+"_"+str(origen)
    grf.Ruta=True
    grf.Lis_aris=lis_ari_rec
    grf.Lis_nod=lis_nod_rec
    grf.Lis_pes_nod=lis_nod_rec_pes
    return grf

    #Optimizar el doble for >:0, ver kruskal_I
def Prim(a):
    grf=copy.deepcopy(a)
    
    #Creamos vector de aristas
    aris_p=[]
    for i in range(len(grf.Aris)):
        aris_p.append([grf.Aris[i].Fue,grf.Aris[i].Des,grf.Aris[i].Pes])
    aris_p.sort(key=elige_peso)
    
    # Agregamos a menos de que se genere un ciclo ¿?
    #vector de conjunto unido :D
    T=[]
    vec_ari_n=[]
    #Inicializamos :D
    T.append(aris_p[0][0])
    T.append(aris_p[0][1])
    vec_ari_n.append([aris_p[0][0],aris_p[0][1]])
    pes_exp=aris_p[0][2]
    aris_p.pop(0)
    
    for i in range(len(grf.Aris)):
        for j in range(len(aris_p)):
            p_T=aris_p[j][0] in T
            s_T=aris_p[j][1] in T
            if p_T and s_T:
                aris_p.pop(j)
                break
            elif p_T and not s_T:
                T.append(aris_p[j][1])
                vec_ari_n.append([aris_p[j][0],aris_p[j][1]])
                pes_exp+=aris_p[j][2]
                aris_p.pop(j)
                break
            elif not p_T and s_T:
                T.append(aris_p[j][0])
                vec_ari_n.append([aris_p[j][0],aris_p[j][1]])
                pes_exp+=aris_p[j][2]
                aris_p.pop(j)
                break
    
    grf.Nom=grf.Nom+"_Prim_"+str(pes_exp)
    grf.Ruta=True
    grf.Lis_aris=vec_ari_n
    return grf


# Kruskal Directo
def Kruskal_D(a):
    grf=copy.deepcopy(a)
    
    #Creamos vector de aristas
    aris_p=[]
    for i in range(len(grf.Aris)):
        aris_p.append([grf.Aris[i].Fue,grf.Aris[i].Des,grf.Aris[i].Pes])
    aris_p.sort(key=elige_peso)
    # Agregamos a menos de que se genere un ciclo ¿?
    #vector de conjunto unido :D
    T=[]
    vec_ari_n=[]
    #Inicializamos :D
    T.append([aris_p[0][0],aris_p[0][1]]) #El primer conjunto
    
    vec_ari_n.append([aris_p[0][0],aris_p[0][1]])
    pes_exp=aris_p[0][2]
    aris_p.pop(0)
    for i in range(len(grf.Aris)):
        for j in range(len(aris_p)):
            igual=False
            p_T=False
            s_T=False
            ind_p=0
            ind_s=0
            for k in range(len(T)):        
                p_T=(aris_p[j][0] in T[k]) or p_T
                if aris_p[j][0] in T[k]:
                    ind_p=k
                if aris_p[j][1] in T[k]:
                    ind_s=k
                s_T=(aris_p[j][1] in T[k]) or s_T
                igual=((aris_p[j][0] in T[k]) and (aris_p[j][1] in T[k])) or igual
    
            if p_T and s_T and igual: #Si están en el mismo conjunto...
                aris_p.pop(j)   #pa fuera
                break
            elif p_T and s_T and not igual: #Si estan en dif. conjuntos
                T[ind_p].extend(T[ind_s])   #Juntamos los conjuntos
                T.pop(ind_s)
                vec_ari_n.append([aris_p[j][0],aris_p[j][1]])
                pes_exp+=aris_p[j][2]
                aris_p.pop(j)
                break
            elif p_T and not s_T:   #Si primero ya en conjunto
                T[ind_p].extend([aris_p[j][1]])
                vec_ari_n.append([aris_p[j][0],aris_p[j][1]])
                pes_exp+=aris_p[j][2]
                aris_p.pop(j)
                break
            elif not p_T and s_T:   #Si segundo ya en conjunto
                T[ind_p].extend([aris_p[j][0]]) 
                vec_ari_n.append([aris_p[j][0],aris_p[j][1]])
                pes_exp+=aris_p[j][2]
                aris_p.pop(j)
                break
    grf.Nom=grf.Nom+"_KrD_"+str(pes_exp)
    grf.Ruta=True
    grf.Lis_aris=vec_ari_n
    return grf

def Kruskal_I(a):
    grf=copy.deepcopy(a)
    #Creamos vector de aristas
    aris_p=[]
    for i in range(len(grf.Aris)):
        aris_p.append([grf.Aris[i].Fue,grf.Aris[i].Des,grf.Aris[i].Pes,i])
    aris_p.sort(reverse=True,key=elige_peso)
    
    actual=copy.deepcopy(b)
    g_aux=DFS_I(actual,0)
    vert_conec=len(g_aux.Vert)
    j=0
    while len(aris_p)!=(vert_conec-1) :
        prueba=copy.deepcopy(actual)
        prueba.Aris.pop(aris_p[j][3])
        g_aux=DFS_R(prueba,0)
        if len(g_aux.Vert)==vert_conec: # si no se altera el valor
            actual=copy.deepcopy(prueba)
            #Actualizar aris_p
            for k in range(len(aris_p)):
                if aris_p[k][3]>aris_p[j][3]:
                    aris_p[k][3]=aris_p[k][3]-1
            aris_p.pop(j)
        else:
            j+=1
    pes_exp=0
    vec_ari_n=[]
    for i in range(len(aris_p)):
        pes_exp+=aris_p[i][2]
        vec_ari_n.append([aris_p[i][0],aris_p[i][1]])
    grf.Nom=grf.Nom+"_KrI_"+str(pes_exp)
    grf.Ruta=True
    grf.Lis_aris=vec_ari_n
    return grf

def elige_peso(elem):
    return elem[2]
def Pesos_aleat(a,pes_max):    
    grf=copy.deepcopy(a)
    for i in range(len(grf.Aris)):
        grf.Aris[i].Pes=int(round(random.random()*(pes_max-1))+1)
    return grf
    


#a=Gnm_Erdo_Renyi(100,150,"Primer_matriiiiz",dirigido=True,auto=True)
#a=Gnp_Gilbert(100,.07,"bb_aleatorio",dirigido=True,auto=True)
#a=Gnr_Geograf_Simple(100,.3,"Espacialigrafo")

#a=Gnr_Geograf_Simple(600,.07,"Espacialigrafo")

#a=Gnd_Barabasi_Albert(200,7,"Grafo_Barbaro")
#b=Pesos_aleat(a, 60)

#c=Prim(b)
#d=Kruskal_I(b)
#e=Kruskal_D(b)

#a=Gmn_Malla(30,30,"Mallita",dirigido=False,pacman=True)

#a=Gmn_Malla(5,5,"Mallita",dirigido=False)

#a=Dorogovtsev_Mendes(30,"Triangulitos",limite=5)
#a=Gmn_Malla_Hex(30,30,"Mallita_Hex_2",dirigido=False)
#a.Exporta_grafo(a.Nom,peso_aleat=True)


#**** ZONA DE MODIFICACION  *****


#a=Dijikstra(a)
#a.Exporta_grafo(a.Nom)



Grafos=[]
Grafos.append(Gnm_Erdo_Renyi(30,100,"Gnm_Erdo_Renyi_n30_m100")) #420
Grafos.append(Gnm_Erdo_Renyi(100,400,"Gnm_Erdo_Renyi_n100_m400")) #4900

Grafos.append(Gnp_Gilbert(30,.2,"Gnp_Gilbert_n30_p20"))
Grafos.append(Gnp_Gilbert(100,.07,"Gnp_Gilbert_n100_p07"))

Grafos.append(Gnr_Geograf_Simple(30,.4,"Gnr_Geograf_Sim_n30_r40"))
Grafos.append(Gnr_Geograf_Simple(100,.2,"Gnr_Geograf_Sim_n100_r30"))

Grafos.append(Gnd_Barabasi_Albert(30,3,"Gnd_Barabasi_Albert_n30_d3"))
Grafos.append(Gnd_Barabasi_Albert(100,5,"Gnd_Barabasi_Albert_n100_d5"))

Grafos.append(Gmn_Malla(7,7,"Gmn_Malla_n7_m7"))
Grafos.append(Gmn_Malla(25,5,"Gmn_Malla_n25_m5"))

Grafos.append(Dorogovtsev_Mendes(30,"Dorogovtsev_Mendes_30"))
Grafos.append(Dorogovtsev_Mendes(100,"Dorogovtsev_Mendes_100"))

for i in range(len(Grafos)):
    Grafos[i]=Pesos_aleat(Grafos[i],100)
    Grafos[i].Exporta_grafo(Grafos[i].Nom)
    a=Prim(Grafos[i])
    b=Kruskal_D(Grafos[i])
    c=Kruskal_I(Grafos[i])
    a.Exporta_grafo(a.Nom)
    b.Exporta_grafo(b.Nom)
    c.Exporta_grafo(c.Nom)
    




#https://www.programiz.com/python-programming/methods/list/sort 




