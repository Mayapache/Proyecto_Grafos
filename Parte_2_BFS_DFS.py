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
    def __init__(self, nom, tipo="graph"):
        self.Nom = nom
        self.Vert = []
        self.Aris = []
        self.Tipo = tipo
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
        for i in range(len(self.Vert)):
            dot_str+=str(self.Vert[i].Nom)+";\n"
        if self.Tipo=="graph":
            union=" -- "
        else:
            union=" -> "
        if peso_aleat:
            for i in range(len(self.Aris)):
                dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+"[weight=\""+str(round(random.random()*4)+1)+ "\"]"+";\n"
        else:
            for i in range(len(self.Aris)):
                dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+";\n"
            
        dot_str+="}"
        with open('C:/Users/Charlie/Documents/Maestria/1er_Semestre/Diseño y análisis de algoritmos/Proyecto/Parte_2/'+nombre_doc+'.gv', 'w') as f:
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
    def Obten_Nom(self):
        return self.Nom
    def Obten_Deg(self):
        return self.Deg
    def Suma_Deg(self):
        self.Deg+=1
        
        #Agregar/cambiar distancia por peso de la arista
        #¿Agregar característica de dirigida o no dirigida?
class Arista:
    def __init__(self, fue, des, dis=0):
        self.Fue = fue
        self.Des = des
        self.Dis=dis
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
    
    

#def BFS(self,s) #Búsqueda a lo Ancho, s= nodo fuente
#def DFS_R(self,s) #Búsqueda a Profundidad, s= nodo fuente, Recursivo
#def DFS_I(self,s) #Búsqueda a Profundidad, s= nodo fuente, Iterativo



#a=Gnm_Erdo_Renyi(100,150,"Primer_matriiiiz",dirigido=True,auto=True)
#a=Gnp_Gilbert(100,.07,"bb_aleatorio",dirigido=True,auto=True)
#a=Gnr_Geograf_Simple(100,.3,"Espacialigrafo")

#a=Gnr_Geograf_Simple(600,.07,"Espacialigrafo")

#a=Gnd_Barabasi_Albert(200,7,"Grafo_Barbaro")
#a=Gmn_Malla(30,30,"Mallita",dirigido=False,pacman=True)
#a=Dorogovtsev_Mendes(30,"Triangulitos",limite=5)
#a=Gmn_Malla_Hex(30,30,"Mallita_Hex_2",dirigido=False)
#a.Exporta_grafo(a.Nom,peso_aleat=True)

#**** ZONA DE MODIFICACION  *****

#b=BFS(a,0)
#c=DFS_R(a,0)
#d=DFS_I(a,0)

import sys
print(sys.getrecursionlimit())
print(sys.setrecursionlimit(3500))

Grafos=[]
Grafos.append(Gnm_Erdo_Renyi(30,100,"Gnm_Erdo_Renyi_n30_m100")) #420
Grafos.append(Gnm_Erdo_Renyi(100,400,"Gnm_Erdo_Renyi_n100_m400")) #4900
Grafos.append(Gnm_Erdo_Renyi(500,1000,"Gnm_Erdo_Renyi_n500_m1000")) #124500
Grafos.append(Gnp_Gilbert(30,.2,"Gnp_Gilbert_n30_p20"))
Grafos.append(Gnp_Gilbert(100,.07,"Gnp_Gilbert_n100_p07"))
Grafos.append(Gnp_Gilbert(500,.01,"Gnp_Gilbert_n500_p001"))
Grafos.append(Gnr_Geograf_Simple(30,.4,"Gnr_Geograf_Sim_n30_r40"))
Grafos.append(Gnr_Geograf_Simple(100,.2,"Gnr_Geograf_Sim_n100_r30"))
Grafos.append(Gnr_Geograf_Simple(500,.1,"Gnr_Geograf_Sim_n500_r05"))
Grafos.append(Gnd_Barabasi_Albert(30,3,"Gnd_Barabasi_Albert_n30_d3"))
Grafos.append(Gnd_Barabasi_Albert(100,5,"Gnd_Barabasi_Albert_n100_d5"))
Grafos.append(Gnd_Barabasi_Albert(500,10,"Gnd_Barabasi_Albert_n500_d10"))
Grafos.append(Gmn_Malla(7,7,"Gmn_Malla_n7_m7"))
Grafos.append(Gmn_Malla(25,5,"Gmn_Malla_n25_m5"))
Grafos.append(Gmn_Malla(90,10,"Gmn_Malla_n90_m10"))
Grafos.append(Dorogovtsev_Mendes(30,"Dorogovtsev_Mendes_30"))
Grafos.append(Dorogovtsev_Mendes(100,"Dorogovtsev_Mendes_100"))
Grafos.append(Dorogovtsev_Mendes(500,"Dorogovtsev_Mendes_500"))
for i in range(len(Grafos)):
    Grafos[i].Exporta_grafo(Grafos[i].Nom)
    a=BFS(Grafos[i],random.randint(0,len(Grafos[i].Vert)-1))
    a.Exporta_grafo(a.Nom)
    a=DFS_R(Grafos[i],random.randint(0,len(Grafos[i].Vert)-1))
    a.Exporta_grafo(a.Nom)
    a=DFS_I(Grafos[i],random.randint(0,len(Grafos[i].Vert)-1))
    a.Exporta_grafo(a.Nom)

