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
import pygame as pg
import os
import imageio


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
    #plt.figure()
    for i in range (n):
        px=random.random()
        vec_x.append(px)
        py=random.random()
        vec_y.append(py)
        Vert.append(Vertice(i,posx=px,posy=py))
    #plt.scatter(vec_x,vec_y)
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
    
    actual=copy.deepcopy(grf)
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

#=======================INICIA CODIGOS DE VISUALIZACION========================
    
class App:
    def __init__(self,grf):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = int(1920*.9), int(1080*.9) #80% de la pantalla
        self.Grf=grf
    def on_init(self):
        pg.init()
        self._display_surf = pg.display.set_mode(self.size, pg.HWSURFACE | pg.DOUBLEBUF)
        self._running = True
        
        
        col_texto=(230,230,230)
        col_fondo=(10,10,10)
        inicio_ancho_text=int(self.weight*.7+70)
        inicio_alto_text=int(self.height*.8+70)
        self.inicio_ancho_text=int(self.weight*.7+70)
        self.col_texto=(230,230,230)
        self.col_fondo=col_fondo
        
        self._display_surf.fill(col_fondo) #fondo
        
        #Creamos fuente, de titulo y de texto:
        self.font_tit = pg.font.Font('C:\\WINDOWS\\Fonts\\segoepr.ttf', 20)
        self.font_nor = pg.font.Font('C:\\WINDOWS\\Fonts\\segoepr.ttf', 17)
        self.font_mini = pg.font.Font('C:\\WINDOWS\\Fonts\\segoepr.ttf', 14)

        #Creamos superficie con el texto, a partir de la fuente :D
        texto = self.font_tit.render('Informacion del grafo:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 40)) #texto
        texto = self.font_nor.render('Numero de nodos:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 77)) #texto
        texto = self.font_nor.render('Numero de aristas:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 100)) #texto
        texto = self.font_nor.render('C1:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 123)) #texto
        texto = self.font_nor.render('C2:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 146)) #texto
        texto = self.font_nor.render('C3:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 169)) #texto
        texto = self.font_nor.render('C4:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 192)) #texto
        
        texto = self.font_nor.render('Variables de Fruchter:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 215)) #texto
        texto = self.font_nor.render('C:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 238)) #texto
        texto = self.font_nor.render('Temp:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 261)) #texto
        texto = self.font_nor.render('Cool:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 284)) #texto
        
        texto = self.font_nor.render('Variables del QuadTree:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 307)) #texto
        texto = self.font_nor.render('Resolucion:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 330)) #texto
        texto = self.font_nor.render('Theta:', True, col_texto)
        self._display_surf.blit(texto, (inicio_ancho_text, 353)) #texto
        #texto = self.font_nor.render(':', True, col_texto)
        #self._display_surf.blit(texto, (inicio_ancho_text, 357)) #texto
        
        texto = self.font_nor.render('Resortitos', True, col_texto)
        self._display_surf.blit(texto, (50, inicio_alto_text)) #texto
        texto = self.font_nor.render('Fruchterman y Reigold', True, col_texto)
        self._display_surf.blit(texto, (250, inicio_alto_text)) #texto
        texto = self.font_nor.render('Q-adtris', True, col_texto)
        self._display_surf.blit(texto, (550, inicio_alto_text)) #texto

        
        self.color_inactivo = pg.Color('lightskyblue3')
        self.color_activo = pg.Color('dodgerblue2')
        self.c1_color=self.color_inactivo
        self.c2_color=self.color_inactivo
        self.c3_color=self.color_inactivo
        self.c4_color=self.color_inactivo
        self.c_color=self.color_inactivo
        self.temp_color=self.color_inactivo
        self.cool_color=self.color_inactivo
        self.resortitos_color=self.color_inactivo
        self.fruch_color=self.color_inactivo
        self.quad_color=self.color_inactivo
        self.res_color=self.color_inactivo
        self.theta_color=self.color_inactivo
        self.c1_activo=False
        self.c2_activo=False
        self.c3_activo=False
        self.c4_activo=False
        self.c_activo=False
        self.temp_activo=False
        self.cool_activo=False
        self.resortitos_activo=False
        self.fruch_activo=False
        self.quad_activo=False
        self.res_activo=False
        self.theta_activo=False

        self.input_c1 = pg.Rect(inicio_ancho_text+35, 130, 120, 20)
        self.text_c1='1'
        pg.draw.rect(self._display_surf,self.c1_color,self.input_c1,width=2)
        self.input_c2 = pg.Rect(inicio_ancho_text+35, 153, 120, 20)
        self.text_c2='1'
        pg.draw.rect(self._display_surf,self.c2_color,self.input_c2,width=2)
        self.input_c3 = pg.Rect(inicio_ancho_text+35, 176, 120, 20)
        self.text_c3='1'
        pg.draw.rect(self._display_surf,self.c3_color,self.input_c3,width=2)
        self.input_c4 = pg.Rect(inicio_ancho_text+35, 199, 120, 20)
        self.text_c4='1'
        pg.draw.rect(self._display_surf,self.c4_color,self.input_c4,width=2)

        self.input_c = pg.Rect(inicio_ancho_text+25, 245, 120, 20)
        self.text_c='.3'
        pg.draw.rect(self._display_surf,self.c_color,self.input_c,width=2)
        self.input_temp = pg.Rect(inicio_ancho_text+55, 268, 120, 20)
        self.text_temp=str(self.weight*.7*.01)
        pg.draw.rect(self._display_surf,self.temp_color,self.input_temp,width=2)
        self.input_cool = pg.Rect(inicio_ancho_text+55, 291, 120, 20)
        self.text_cool='.99'
        pg.draw.rect(self._display_surf,self.cool_color,self.input_cool,width=2)

        self.input_res= pg.Rect(inicio_ancho_text+95, 337, 120, 20)
        self.text_res='1'
        pg.draw.rect(self._display_surf,self.res_color,self.input_res,width=2)
        self.input_theta= pg.Rect(inicio_ancho_text+55, 360, 120, 20)
        self.text_theta='0.3'
        pg.draw.rect(self._display_surf,self.theta_color,self.input_theta,width=2)



        self.input_resortitos = pg.Rect(50, inicio_alto_text+7, 93, 20)
        pg.draw.rect(self._display_surf,self.resortitos_color,self.input_resortitos,width=2)
        self.input_fruch= pg.Rect(250, inicio_alto_text+7, 205, 20)
        pg.draw.rect(self._display_surf,self.fruch_color,self.input_fruch,width=2)
        self.input_quad= pg.Rect(550, inicio_alto_text+7, 80, 20)
        pg.draw.rect(self._display_surf,self.quad_color,self.input_quad,width=2)



        self.c1=1
        self.c2=1
        self.c3=1
        self.c4=1

        self.c=.3
        self.temp=self.weight*.7*self.height*.8*.01
        self.temp=self.weight*.7*.01
        self.cool=.99
        
        self.res=1
        self.theta=0.3


        #Valores de la cantidad de vertices y de aristas
        text_=str(len(self.Grf.Vert))
        texto = self.font_nor.render(text_, True, col_texto,col_fondo)
        self._display_surf.blit(texto, (inicio_ancho_text+180, 77)) #texto
        text_=str(len(self.Grf.Aris))
        texto = self.font_nor.render(text_, True, col_texto,col_fondo)
        self._display_surf.blit(texto, (inicio_ancho_text+180, 100)) #texto

        self.Grf=posiciones_aleat_ini(self.Grf,self.weight*.7,self.height*.8)
        
        self.cuenta_imag=0
        pg.display.set_caption('Gephito')  #nombre ventana
        
    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            #Si fue en la cajita
            if self.input_c1.collidepoint(event.pos):
                self.c1_activo= not self.c1_activo
            else:
                self.c1_activo=False
            self.c1_color=self.color_activo if self.c1_activo else self.color_inactivo            
            if self.input_c2.collidepoint(event.pos):
                self.c2_activo= not self.c2_activo
            else:
                self.c2_activo=False
            self.c2_color=self.color_activo if self.c2_activo else self.color_inactivo
            if self.input_c3.collidepoint(event.pos):
                self.c3_activo= not self.c3_activo
            else:
                self.c3_activo=False
            self.c3_color=self.color_activo if self.c3_activo else self.color_inactivo
            if self.input_c4.collidepoint(event.pos):
                self.c4_activo= not self.c4_activo
            else:
                self.c4_activo=False
            self.c4_color=self.color_activo if self.c4_activo else self.color_inactivo
            if self.input_c.collidepoint(event.pos):
                self.c_activo= not self.c_activo
            else:
                self.c_activo=False
            self.c_color=self.color_activo if self.c_activo else self.color_inactivo
            if self.input_temp.collidepoint(event.pos):
                self.temp_activo= not self.temp_activo
            else:
                self.temp_activo=False
            self.temp_color=self.color_activo if self.temp_activo else self.color_inactivo
            if self.input_cool.collidepoint(event.pos):
                self.cool_activo= not self.cool_activo
            else:
                self.cool_activo=False
            self.cool_color=self.color_activo if self.cool_activo else self.color_inactivo
            
            if self.input_res.collidepoint(event.pos):
                self.res_activo= not self.res_activo
            else:
                self.res_activo=False
            self.res_color=self.color_activo if self.res_activo else self.color_inactivo
            if self.input_theta.collidepoint(event.pos):
                self.theta_activo= not self.theta_activo
            else:
                self.theta_activo=False
            self.theta_color=self.color_activo if self.theta_activo else self.color_inactivo
            
            if self.input_resortitos.collidepoint(event.pos):
                self.resortitos_activo= not self.resortitos_activo
            elif self.input_fruch.collidepoint(event.pos) or self.input_quad.collidepoint(event.pos):
                self.resortitos_activo=False
            self.resortitos_color=self.color_activo if self.resortitos_activo else self.color_inactivo
            if self.input_fruch.collidepoint(event.pos):
                self.fruch_activo= not self.fruch_activo
            elif self.input_resortitos.collidepoint(event.pos) or self.input_quad.collidepoint(event.pos):
                self.fruch_activo=False
            self.fruch_color=self.color_activo if self.fruch_activo else self.color_inactivo
            if self.input_quad.collidepoint(event.pos):
                self.quad_activo= not self.quad_activo
            elif self.input_fruch.collidepoint(event.pos) or self.input_resortitos.collidepoint(event.pos):
                self.quad_activo=False
            self.quad_color=self.color_activo if self.quad_activo else self.color_inactivo

        if event.type == pg.KEYDOWN:
            if self.c1_activo:
                if event.key==pg.K_RETURN:
                    self.c1=float(self.text_c1)
                elif event.key==pg.K_BACKSPACE:
                    self.text_c1=self.text_c1[:-1]
                else:
                    self.text_c1 += event.unicode
            
            if self.c2_activo:
                if event.key==pg.K_RETURN:
                    self.c2=float(self.text_c2)
                elif event.key==pg.K_BACKSPACE:
                    self.text_c2=self.text_c2[:-1]
                else:
                    self.text_c2 += event.unicode
            
            if self.c3_activo:
                if event.key==pg.K_RETURN:
                    self.c3=float(self.text_c3)
                elif event.key==pg.K_BACKSPACE:
                    self.text_c3=self.text_c3[:-1]
                else:
                    self.text_c3 += event.unicode
            
            if self.c4_activo:
                if event.key==pg.K_RETURN:
                    self.c4=float(self.text_c4)
                elif event.key==pg.K_BACKSPACE:
                    self.text_c4=self.text_c4[:-1]
                else:
                    self.text_c4 += event.unicode
            
            if self.c_activo:
                if event.key==pg.K_RETURN:
                    self.c=float(self.text_c)
                elif event.key==pg.K_BACKSPACE:
                    self.text_c=self.text_c[:-1]
                else:
                    self.text_c += event.unicode
            
            if self.temp_activo:
                if event.key==pg.K_RETURN:
                    self.temp=float(self.text_temp)
                elif event.key==pg.K_BACKSPACE:
                    self.text_temp=self.text_temp[:-1]
                else:
                    self.text_temp += event.unicode
            
            if self.cool_activo:
                if event.key==pg.K_RETURN:
                    self.cool=float(self.text_cool)
                elif event.key==pg.K_BACKSPACE:
                    self.text_cool=self.text_cool[:-1]
                else:
                    self.text_cool += event.unicode
            
            if self.res_activo:
                if event.key==pg.K_RETURN:
                    self.res=float(self.text_res)
                elif event.key==pg.K_BACKSPACE:
                    self.text_res=self.text_res[:-1]
                else:
                    self.text_res += event.unicode
            
            if self.theta_activo:
                if event.key==pg.K_RETURN:
                    self.theta=float(self.text_theta)
                elif event.key==pg.K_BACKSPACE:
                    self.text_theta=self.text_theta[:-1]
                else:
                    self.text_theta += event.unicode
            
    def on_loop(self):
        #avanzamos 1 en el tiempo        

        #sig_tiempo()
        #pequeña pausa/delay 
        pg.time.delay(100)
        #actualizamos mapa_pix, 1,2,3 
        #mapa_pix= actualiza_imagen() #Actualizamos la imagen :D

        #surface = pg.surfarray.make_surface(colores[mapa_pix])
        surface= pg.Surface((32,32))
        surface = pg.transform.scale(surface, (int(self.weight*.7), int(self.height*.8)))  # Escalado, al 80%

        #Actualiza posiciones (el algoritmo)
        #self.Grf=posiciones_aleat_ini(self.Grf,self.weight*.7,self.height*.8)
        ini_t=tm.time()
        if self.resortitos_activo:
            self.Grf=resortitos(self.Grf,self.c1,self.c2,self.c3,self.c4,self.weight*.7,self.height*.8)            
            self.cuenta_imag+=1
            pg.image.save(self._display_surf,"C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Imagenes_6/grafito_prueba"+str(self.cuenta_imag)+".jpg")
        elif self.fruch_activo:
            self.Grf,self.temp=Fruchterman_Reigold(self.Grf,self.c,self.temp,self.cool,self.weight*.7,self.height*.8)
            self.cuenta_imag+=1
            pg.image.save(self._display_surf,"C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Imagenes_6/grafito_prueba"+str(self.cuenta_imag)+".jpg")
        elif self.quad_activo:
            self.Grf,self.temp=Fru_quad(self.Grf,self.c,self.temp,self.cool,self.weight*.7,self.height*.8,self.res,self.theta)
            self.cuenta_imag+=1
            pg.image.save(self._display_surf,"C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Imagenes_6/grafito_prueba"+str(self.cuenta_imag)+".jpg")
        fin_t=tm.time()
        t_proces=fin_t-ini_t
        print(t_proces)

        #Dibuja nuevas posiciones en la superficie
        for i in range(len(self.Grf.Vert)):
            pg.draw.circle(surface,(21,230,230),(self.Grf.Vert[i].Posx,self.Grf.Vert[i].Posy),4) #En donde, colores, posición xy, radio
        #Dibujamos las aristas
        for i in range(len(self.Grf.Aris)):
            v1=self.Grf.Aris[i].Fue
            v2=self.Grf.Aris[i].Des
            ps1=(self.Grf.Vert[v1].Posx,self.Grf.Vert[v1].Posy)
            ps2=(self.Grf.Vert[v2].Posx,self.Grf.Vert[v2].Posy)
            pg.draw.line(surface,(200,180,255),ps1,ps2) #En donde, colores, pos inicial, pos final
        
        self._display_surf.blit(surface, (50, 50)) #Superficie
        
        
        #Limpiamos
        texto = self.font_nor.render('          ', True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 123)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 146)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 169)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 192)) #texto
        
        self._display_surf.blit(texto, (self.inicio_ancho_text+25, 238)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 261)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 284)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+95, 330)) #texto
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 353)) #texto
        
        
        texto = self.font_nor.render(self.text_c1, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 123)) #texto
        texto = self.font_nor.render(self.text_c2, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 146)) #texto
        texto = self.font_nor.render(self.text_c3, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 169)) #texto
        texto = self.font_nor.render(self.text_c4, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+35, 192)) #texto
        texto = self.font_nor.render(self.text_c, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+25, 238)) #texto
        texto = self.font_nor.render(self.text_temp, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 261)) #texto
        texto = self.font_nor.render(self.text_cool, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 284)) #texto
        texto = self.font_nor.render(self.text_res, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+95, 330)) #texto
        texto = self.font_nor.render(self.text_theta, True, self.col_texto,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text+55, 353)) #texto
        
        vel_="t (ms): "+str(t_proces)
        texto = self.font_nor.render(vel_, True,self.col_texto ,pg.Color('dodgerblue3'))
        self._display_surf.blit(texto, (self.inicio_ancho_text, 376)) #texto
        
        pg.draw.rect(self._display_surf,self.c1_color,self.input_c1,width=2)
        pg.draw.rect(self._display_surf,self.c2_color,self.input_c2,width=2)
        pg.draw.rect(self._display_surf,self.c3_color,self.input_c3,width=2)
        pg.draw.rect(self._display_surf,self.c4_color,self.input_c4,width=2)
        pg.draw.rect(self._display_surf,self.c_color,self.input_c,width=2)
        pg.draw.rect(self._display_surf,self.temp_color,self.input_temp,width=2)
        pg.draw.rect(self._display_surf,self.cool_color,self.input_cool,width=2)
        pg.draw.rect(self._display_surf,self.res_color,self.input_res,width=2)
        pg.draw.rect(self._display_surf,self.theta_color,self.input_theta,width=2)
        pg.draw.rect(self._display_surf,self.resortitos_color,self.input_resortitos,width=2)
        pg.draw.rect(self._display_surf,self.fruch_color,self.input_fruch,width=2)
        pg.draw.rect(self._display_surf,self.quad_color,self.input_quad,width=2)



                
        pass
    def on_render(self):
        pg.display.flip()
        pass
    def on_cleanup(self):
        pg.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while( self._running ):
            il=0
            for event in pg.event.get():
                self.on_event(event)
                il+=1
            self.on_loop()
            self.on_render()
        
        self.on_cleanup()

def resortitos(a,c1,c2,c3,c4,anc,alt):
    grf=copy.deepcopy(a)
    
    #calcular fuerzas en cada vértice
    vec_fuerzas=[(0,0)]*len(grf.Vert)
    
    #fuerzas de respulsión, por otros vértices
    for i in range(len(grf.Vert)):
        for j in range(len(grf.Vert)):
            if i!=j:
                #Distancia y angulo
                ps1=(grf.Vert[i].Posx,grf.Vert[i].Posy)
                ps2=(grf.Vert[j].Posx,grf.Vert[j].Posy)
                dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
                #fuerza
                if dis>0:
                    fuerza=c3/mt.sqrt(dis)
                else:
                    fuerza=c3*5
                #agregamos al vec_fuerzas
                fue_f, ang_f=suma_vec(fuerza,ang,vec_fuerzas[i][0],vec_fuerzas[i][1])
                vec_fuerzas[i]=(fue_f,ang_f)

    #fuerzas de atracción, por las aristas
    for i in range(len(grf.Aris)):
        v1=grf.Aris[i].Fue
        v2=grf.Aris[i].Des
        ps1=(grf.Vert[v1].Posx,grf.Vert[v1].Posy)
        ps2=(grf.Vert[v2].Posx,grf.Vert[v2].Posy)
        dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
        if dis>0:
            fuerza=c1*np.log(dis/c2)
        else:
            fuerza=0
        fue_f, ang_f=suma_vec(fuerza,ang+mt.pi,vec_fuerzas[v1][0],vec_fuerzas[v1][1])
        vec_fuerzas[v1]=(fue_f,ang_f)
        fue_f, ang_f=suma_vec(fuerza,ang,vec_fuerzas[v2][0],vec_fuerzas[v2][1])
        vec_fuerzas[v2]=(fue_f,ang_f)
        
    #__________________ Gran atractor
    psx_GA=anc/2
    psy_GA=alt/2
    for i in range(len(grf.Vert)):
        ps1=(grf.Vert[i].Posx,grf.Vert[i].Posy)
        dis, ang = dis_ang(ps1[0],ps1[1],psx_GA,psy_GA)
        if dis>0:
            #fuerza=c1*np.log(dis/c2)
            fuerza=dis*0
        else:
            fuerza=0
        fue_f, ang_f=suma_vec(fuerza,ang+mt.pi,vec_fuerzas[i][0],vec_fuerzas[i][1])
        vec_fuerzas[i]=(fue_f,ang_f)
        
    #Actualizar las posiciones x, y de cada vértice
    for i in range(len(grf.Vert)):
        co_x=c4*vec_fuerzas[i][0]*mt.cos(vec_fuerzas[i][1])
        co_y=c4*vec_fuerzas[i][0]*mt.sin(vec_fuerzas[i][1])
        grf.Vert[i].Posx=grf.Vert[i].Posx+co_x
        grf.Vert[i].Posy=grf.Vert[i].Posy+co_y
        aleat=random.randint(1, 2)
        if grf.Vert[i].Posx>=anc:
            grf.Vert[i].Posx=anc-aleat
        elif grf.Vert[i].Posx<1:
            grf.Vert[i].Posx=aleat
        if grf.Vert[i].Posy>=alt:
            grf.Vert[i].Posy=alt-aleat
        elif grf.Vert[i].Posy<1:
            grf.Vert[i].Posy=aleat
    
    return grf

def Fruchterman_Reigold(a,c,temp,cool,anc,alt):
    grf=copy.deepcopy(a)
    n_vert=len(grf.Vert)
    area=anc*alt
    k=c*np.sqrt(area/n_vert)
    
    vec_fuerzas=[(0,0)]*len(grf.Vert)
    
    #fuerzas de repulsión, por otros vértices
    for i in range(len(grf.Vert)):
        for j in range(len(grf.Vert)):
            if i!=j:
                #Distancia y angulo
                ps1=(grf.Vert[i].Posx,grf.Vert[i].Posy)
                ps2=(grf.Vert[j].Posx,grf.Vert[j].Posy)
                dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
                #fuerza
                if dis>0:
                    fuerza=k**2/dis
                else:
                    fuerza=k**2
                #agregamos al vec_fuerzas
                fue_f, ang_f=suma_vec(fuerza,ang,vec_fuerzas[i][0],vec_fuerzas[i][1])
                vec_fuerzas[i]=(fue_f,ang_f)

    #fuerzas de atracción, por las aristas
    for i in range(len(grf.Aris)):
        v1=grf.Aris[i].Fue
        v2=grf.Aris[i].Des
        ps1=(grf.Vert[v1].Posx,grf.Vert[v1].Posy)
        ps2=(grf.Vert[v2].Posx,grf.Vert[v2].Posy)
        dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
        if dis>0:
            fuerza=(dis**2)/ k
        else:
            fuerza=0
        fue_f, ang_f=suma_vec(fuerza,ang+mt.pi,vec_fuerzas[v1][0],vec_fuerzas[v1][1])
        vec_fuerzas[v1]=(fue_f,ang_f)
        fue_f, ang_f=suma_vec(fuerza,ang,vec_fuerzas[v2][0],vec_fuerzas[v2][1])
        vec_fuerzas[v2]=(fue_f,ang_f)
    
    #Actualizar las posiciones x, y de cada vértice, imitado por la temperatura :D
    for i in range(len(grf.Vert)):
        co_x=min(vec_fuerzas[i][0],temp)*mt.cos(vec_fuerzas[i][1])
        co_y=min(vec_fuerzas[i][0],temp)*mt.sin(vec_fuerzas[i][1])
        grf.Vert[i].Posx=grf.Vert[i].Posx+co_x
        grf.Vert[i].Posy=grf.Vert[i].Posy+co_y
        aleat=random.randint(1, 2)
        if grf.Vert[i].Posx>=anc:
            grf.Vert[i].Posx=anc-aleat
        elif grf.Vert[i].Posx<1:
            grf.Vert[i].Posx=aleat
        if grf.Vert[i].Posy>=alt:
            grf.Vert[i].Posy=alt-aleat
        elif grf.Vert[i].Posy<1:
            grf.Vert[i].Posy=aleat
    temp= cool*temp
    return grf,temp

        

def dis_ang(ax,ay,bx,by):
    dis=mt.sqrt((ax-bx)**2+(ay-by)**2)
    ang=mt.atan2( ay-by,ax-bx,)    
    return dis,ang

def suma_vec(f1,ang1,f2,ang2):
    co_x_1=f1*mt.cos(ang1)
    co_y_1=f1*mt.sin(ang1)
    co_x_2=f2*mt.cos(ang2)
    co_y_2=f2*mt.sin(ang2)
    co_x=co_x_1+co_x_2
    co_y=co_y_1+co_y_2
    f,ang=dis_ang(co_x,co_y,0,0)
    return f,ang



def posiciones_aleat_ini(a,anc,alt):
    grf=copy.deepcopy(a)
    for i in range(len(grf.Vert)):
        grf.Vert[i].Posx=np.random.randint(0,anc)
        grf.Vert[i].Posy=np.random.randint(0,alt)
    return grf


def por_y(elem):
    return elem[1]

class quadtrito:
    def __init__(self,bor_x,bor_y):
        self.Centro=((bor_x[0]+bor_x[1])/2,(bor_y[0]+bor_y[1])/2)
        self.Centro_masa=0
        self.Cant_masa=0
        self.QAd3=[[],[],[],[]]
        self.Bor_x=bor_x
        self.Bor_y=bor_y
        self.Vec_ver=[]
    def Agrega_Masa(self):
        self.Cant_masa+=1
    def Calcula_cen_mas(self):
        sum_x=0
        sum_y=0
        for i in range(len(self.Vec_ver)):
            sum_x+=self.Vec_ver[i][0]
            sum_y+=self.Vec_ver[i][1]
        if self.Cant_masa>0:
            self.Centro_masa=(sum_x/self.Cant_masa,sum_y/self.Cant_masa)
        else:
            self.Centro_masa=self.Centro


#Particion a cuadtree
#Orden= NO, NE, SO, SE
# NO NE
# SO SE
def Parte_quad(quad,res):
    quad.QAd3[0]=quadtrito((quad.Bor_x[0],quad.Centro[0]),(quad.Bor_y[0],quad.Centro[1]))
    quad.QAd3[1]=quadtrito((quad.Centro[0],quad.Bor_x[1]),(quad.Bor_y[0],quad.Centro[1]))
    quad.QAd3[2]=quadtrito((quad.Bor_x[0],quad.Centro[0]),(quad.Centro[1],quad.Bor_y[1]))
    quad.QAd3[3]=quadtrito((quad.Centro[0],quad.Bor_x[1]),(quad.Centro[1],quad.Bor_y[1]))
    
    for i in range(len(quad.Vec_ver)):
        if quad.Vec_ver[i][0]<quad.Centro[0]:  #Si está en el Oeste
            if quad.Vec_ver[i][1]>quad.Centro[1]: #Si está en el Norte
                quad.QAd3[0].Agrega_Masa()
                quad.QAd3[0].Vec_ver.append(quad.Vec_ver[i])
            else:           #Si está en el Sur
                quad.QAd3[2].Agrega_Masa()
                quad.QAd3[2].Vec_ver.append(quad.Vec_ver[i])
        else:               #Si está en el Este
            if quad.Vec_ver[i][1]>quad.Centro[1]:  #Si está en el Norte
                quad.QAd3[1].Agrega_Masa()
                quad.QAd3[1].Vec_ver.append(quad.Vec_ver[i])
            else:        #Si está en el Sur
                quad.QAd3[3].Agrega_Masa()
                quad.QAd3[3].Vec_ver.append(quad.Vec_ver[i])
    quad.QAd3[0].Calcula_cen_mas()
    quad.QAd3[1].Calcula_cen_mas()
    quad.QAd3[2].Calcula_cen_mas()
    quad.QAd3[3].Calcula_cen_mas()
    if quad.QAd3[0].Cant_masa>res:
        quad.QAd3[0]=Parte_quad(quad.QAd3[0], res)
    if quad.QAd3[1].Cant_masa>res:
        quad.QAd3[1]=Parte_quad(quad.QAd3[1], res)
    if quad.QAd3[2].Cant_masa>res:
        quad.QAd3[2]=Parte_quad(quad.QAd3[2], res)
    if quad.QAd3[3].Cant_masa>res:
        quad.QAd3[3]=Parte_quad(quad.QAd3[3], res)
    return quad


def zoom(theta_lim,k,ps1,cuad,val_f):
    if cuad.Cant_masa==0:
        return val_f
    ps2=(cuad.Centro_masa[0],cuad.Centro_masa[1])
    dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
    if dis>0:
        theta=(cuad.Bor_x[1]-cuad.Bor_x[0])/dis
    else:
        return val_f 
    
    if theta<theta_lim:   #Si suficienteimente lejos :D
        fuerza=cuad.Cant_masa*k**2/dis
        #agregamos al vec_fuerzas
        fue_f, ang_f=suma_vec(fuerza,ang,val_f[0],val_f[1])
        val_f=(fue_f,ang_f)
    else:   #Si està muy cerca D:
        if cuad.QAd3[0] != []:
            val_f=zoom(theta_lim,k,ps1,cuad.QAd3[0],val_f)
        if cuad.QAd3[1] != []:
            val_f=zoom(theta_lim,k,ps1,cuad.QAd3[1],val_f)        
        if cuad.QAd3[2] != []:
            val_f=zoom(theta_lim,k,ps1,cuad.QAd3[2],val_f)    
        if cuad.QAd3[3] != []:
            val_f=zoom(theta_lim,k,ps1,cuad.QAd3[3],val_f)    
    return val_f

def Fru_quad(a,c,temp,cool,anc,alt, res,theta_lim):
    grf=copy.deepcopy(a)
    #Generamos primer quad, que abarca todo
    cuad=quadtrito((0,anc),(0,alt))
    #Le agregamos su masa
    for i in range(len(grf.Vert)):
        cuad.Vec_ver.append([grf.Vert[i].Posx,grf.Vert[i].Posy])
        cuad.Agrega_Masa()
    cuad.Calcula_cen_mas()
    #Primer quadtrito listoooo
    if cuad.Cant_masa>res: #¿Partimos?
        #Partimooosss
        cuad=Parte_quad(cuad,res)
    n_vert=len(grf.Vert)
    area=anc*alt
    k=c*np.sqrt(area/n_vert)
    vec_fuerzas=[(0,0)]*len(grf.Vert)

    #fuerzas de repulsión, por otros vértices, por quad
    for i in range(len(grf.Vert)):
        ps1=(grf.Vert[i].Posx,grf.Vert[i].Posy)
        val_f=(0,0)
        val_f=zoom(theta_lim,k,ps1,cuad,val_f)
        vec_fuerzas[i]=val_f
    
    #fuerzas de atracción, por las aristas
    for i in range(len(grf.Aris)):
        v1=grf.Aris[i].Fue
        v2=grf.Aris[i].Des
        ps1=(grf.Vert[v1].Posx,grf.Vert[v1].Posy)
        ps2=(grf.Vert[v2].Posx,grf.Vert[v2].Posy)
        dis, ang = dis_ang(ps1[0],ps1[1],ps2[0],ps2[1])
        if dis>0:
            fuerza=(dis**2)/ k
        else:
            fuerza=0
        fue_f, ang_f=suma_vec(fuerza,ang+mt.pi,vec_fuerzas[v1][0],vec_fuerzas[v1][1])
        vec_fuerzas[v1]=(fue_f,ang_f)
        fue_f, ang_f=suma_vec(fuerza,ang,vec_fuerzas[v2][0],vec_fuerzas[v2][1])
        vec_fuerzas[v2]=(fue_f,ang_f)
    
    
    #Actualizar las posiciones x, y de cada vértice, limitado por la temperatura :D
    for i in range(len(grf.Vert)):
        co_x=min(vec_fuerzas[i][0],temp)*mt.cos(vec_fuerzas[i][1])
        co_y=min(vec_fuerzas[i][0],temp)*mt.sin(vec_fuerzas[i][1])
        grf.Vert[i].Posx=grf.Vert[i].Posx+co_x
        grf.Vert[i].Posy=grf.Vert[i].Posy+co_y
        aleat=random.randint(1, 2)
        if grf.Vert[i].Posx>=anc:
            grf.Vert[i].Posx=anc-aleat
        elif grf.Vert[i].Posx<1:
            grf.Vert[i].Posx=aleat
        if grf.Vert[i].Posy>=alt:
            grf.Vert[i].Posy=alt-aleat
        elif grf.Vert[i].Posy<1:
            grf.Vert[i].Posy=aleat
    temp= cool*temp
    return grf,temp


#a=Gnm_Erdo_Renyi(100,150,"Primer_matriiiiz",dirigido=True,auto=True)
#a=Gnp_Gilbert(100,.07,"bb_aleatorio",dirigido=True,auto=True)
#a=Gnr_Geograf_Simple(100,.2,"Espacialigrafo")

#a=Gnr_Geograf_Simple(600,.07,"Espacialigrafo")

#a=Gnd_Barabasi_Albert(100,3,"Grafo_Barbaro")
#b=Pesos_aleat(a, 60)

#c=Prim(b)
#d=Kruskal_I(b)
#e=Kruskal_D(b)

#a=Gmn_Malla(10,10,"Mallita",dirigido=False,pacman=True)

#a=Gmn_Malla(10,10,"Mallita",dirigido=False)

#a=Dorogovtsev_Mendes(30,"Triangulitos",limite=5)
#a=Gmn_Malla_Hex(30,30,"Mallita_Hex_2",dirigido=False)
#a.Exporta_grafo(a.Nom,peso_aleat=True)

#a=Gmn_Malla(20,20,"Mallita",dirigido=False)



'''
a=Gnm_Erdo_Renyi(100,400,"Gnm_Erdo_Renyi_n100_m400")
a=Gnm_Erdo_Renyi(500,1000,"Gnm_Erdo_Renyi_n500_m1000")

a=Gnp_Gilbert(100,.07,"Gnp_Gilbert_n100_p07")
a=Gnp_Gilbert(500,.01,"Gnp_Gilbert_n500_p01")

a=Gnr_Geograf_Simple(100,.2,"Gnr_Geograf_Sim_n100_r20")
a=Gnr_Geograf_Simple(500,.07,"Gnr_Geograf_Sim_n500_r07")

a=Gnd_Barabasi_Albert(100,5,"Gnd_Barabasi_Albert_n100_d5")
a=Gnd_Barabasi_Albert(500,7,"Gnd_Barabasi_Albert_n500_d7")

a=Gmn_Malla(10,10,"Gmn_Malla_n10_m10")
a=Gmn_Malla(23,22,"Gmn_Malla_n23_m22")

a=Dorogovtsev_Mendes(100,"Dorogovtsev_Mendes_100")
a=Dorogovtsev_Mendes(500,"Dorogovtsev_Mendes_500")

'''




a=Dorogovtsev_Mendes(500,"Dorogovtsev_Mendes_500")





if __name__ == "__main__" :
    theApp = App(a)
    theApp.on_execute()

#antes de cerrarse:
path="C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Imagenes_6/"
archivos= sorted(os.listdir(path),key=len)
img_array=[]

for x in range(0, len(archivos)):
    nomArchivo = archivos[x]
    dirArchivo = path + str(nomArchivo)

    #Asignar a variable leer_imagen, el nombre de cada imagen
    leer_imagen = imageio.imread(dirArchivo)

    # añadir imágenes al arreglo img_array
    img_array.append(leer_imagen)


#Guardar Gif
imageio.mimwrite('C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Gif_6/'+a.Nom+'.gif', img_array, 'GIF', duration=.07)

#Guardar Imagen
imageio.imwrite('C:/Users/chris/Documents/Mayapachin/Primer_Sem/Algoritmos/Imagenes_graf_6/'+a.Nom+'.png', leer_imagen)


#**** ZONA DE MODIFICACION  *****
'''
Grafos=[]
Grafos.append(Gnm_Erdo_Renyi(30,100,"Gnm_Erdo_Renyi_n30_m100")) #420
Grafos.append(Gnm_Erdo_Renyi(100,400,"Gnm_Erdo_Renyi_n100_m400")) #4900

Grafos.append(Gnp_Gilbert(30,.2,"Gnp_Gilbert_n30_p20"))
Grafos.append(Gnp_Gilbert(100,.07,"Gnp_Gilbert_n100_p07"))

Grafos.append(Gnr_Geograf_Simple(30,.4,"Gnr_Geograf_Sim_n30_r40"))
Grafos.append(Gnr_Geograf_Simple(100,.2,"Gnr_Geograf_Sim_n100_r20"))

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

# import package pygame
import pygame

# initialize pygame
pygame.init()

# Form screen
screen = pygame.display.set_mode()

# get the default size
x, y = screen.get_size()

# quit pygame
pygame.display.quit()

# view size (width x height)
print(x, y)

'''
#https://www.programiz.com/python-programming/methods/list/sort 
