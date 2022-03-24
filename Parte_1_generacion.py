# -*- coding: utf-8 -*-
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
    def Exporta_grafo(self,nombre_doc):
        dot_str=self.Tipo+" "+self.Nom+" {\n"
        for i in range(len(self.Vert)):
            dot_str+=str(self.Vert[i].Nom)+";\n"
        if self.Tipo=="graph":
            union=" -- "
        else:
            union=" -> "
        for i in range(len(self.Aris)):
            dot_str+=str(self.Aris[i].Fue)+union+str(self.Aris[i].Des)+";\n"
        dot_str+="}"
        with open('C:/Users/Charlie/Documents/Maestria/1er_Semestre/Diseño y análisis de algoritmos/Proyecto/Grafos_gv/'+nombre_doc+'.gv', 'w') as f:
            f.write(dot_str)

        #Agregar características de vértice
        #¿Agregar opción de posición en z? ¿Cambiar a un vector de parámetros?
class Vertice:
    def __init__(self, Nom,posx=0,posy=0,deg=0):
        self.Nom = Nom
        self.Posx = posx
        self.Posy = posy
        self.Deg = deg
    def Obten_Nom(self):
        return self.Nom
    def Obten_Deg(self):
        return self.Nom
    def Suma_Deg(self):
        self.Deg=self.Deg +1
        
        #Agregar/cambiar distancia por peso de la arista
        #¿Agregar característica de dirigida o no dirigida?
class Arista:
    def __init__(self, fue, des, dis=0):
        self.Fue = fue
        self.Des = des
        self.Dis=dis
    def Obten_Fue(self):
        return self.Fue.Obten_Nom()
    def Obten_Des(self):
        return self.Des.Obten_Nom()
    def Obten_Fue_Des(self):
        return [self.Fue,self.Des]


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
    #for i in range(n):
        #plt.text(vec_x[i],vec_y[i],i)
    for i in range(n):
        for j in range(n-i-1+auto):
            dist=distancia(vec_x[i],vec_y[i],vec_x[n-j-1],vec_y[n-j-1])
            if dist<r:
                Aris.append(Arista(i,n-j-1,dis=dist))
                #plt.plot([vec_x[i],vec_x[n-j-1]],[vec_y[i],vec_y[n-j-1]])
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

    #Opción de Ciclar (como si fuera el mundo de pacman) extremo con inicio
    #Opción malla Hexagonal 
    #Generamos n*m nodos, nodo i,j, con nodo i+1,j  y  i,j+1
def Gmn_Malla(n,m,Nom,dirigido=False):
    Vert=[]
    Aris=[]
    #vec_x=[]
    #vec_y=[]
    #plt.figure()
    for j in range(m):
        for i in range(n): #generamos nuevo nodo    
            #vec_x.append(i)
            #vec_y.append(j)
            Vert.append(Vertice(i, posx=i, posy=j))
    #plt.scatter(vec_x,vec_y)
    #for i in range(m*n):
    #    plt.text(vec_x[i],vec_y[i],i)
    for j in range(m-1):
        for i in range(n-1):
            #plt.plot([vec_x[i+n*j],vec_x[i+1+j*n]],[vec_y[i+n*j],vec_y[i+1+j*n]])
            #plt.plot([vec_x[i+n*j],vec_x[i+n+j*n]],[vec_y[i+n*j],vec_y[i+n+j*n]])
            Aris.append(Arista(i+n*j,i+1+j*n))
            Aris.append(Arista(i+n*j,i+n+j*n))
    #Hasta la derecha
    for i in range(m-1):
        Aris.append(Arista(n-1+i*n,2*n-1+i*n))
        #plt.plot([vec_x[n-1+i*n],vec_x[2*n-1+i*n]],[vec_y[n-1+i*n],vec_y[2*n-1+i*n]])
    #Hasta arriba
    for i in range(n-1):
        Aris.append(Arista(n*(m-1)+i,n*(m-1)+i+1))
        #plt.plot([vec_x[n*(m-1)+i],vec_x[n*(m-1)+i+1]],[vec_y[n*(m-1)+i],vec_y[n*(m-1)+i+1]])
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


    #Deshacerse del uso de vec_ver y vec_ari
    #Opciones de figuras iniciales
    #Opción de limitar grado máximo de nodo (bloqueando que la arista sea elegible) (¿Genera formas constantes?)
    #Descripción: Generamos tres nodos conectados entre sí, agregamos nodo y 
    #elegimos arista al azar, conectamos el nodo nuevo a cada extremo  de la 
    #arista elegida    
def Dorogovtsev_Mendes(n,Nom,dirigido=False):
    Vert=[]
    Aris=[]
    #Primeros tres nodos    
    for i in range(3):
        Vert.append(Vertice(i))
    vec_ver=[0,1,2]
    Aris.append(Arista(0,1))
    Aris.append(Arista(1,2))
    Aris.append(Arista(2,0))
    vec_ari=[[0,1],[1,2],[2,0]]
    
    for i in range(n-3):
        Vert.append(Vertice(i+3))
        vec_ver.append(i+3)
        selec=random.randint(0,len(vec_ari)-1)
        vec_ari.append([i+3,vec_ari[selec][0]])
        vec_ari.append([i+3,vec_ari[selec][1]])
        Aris.append(Arista(i+3,vec_ari[selec][0]))
        Aris.append(Arista(i+3,vec_ari[selec][1]))
    
    if dirigido:
        Graf= Grafo(Nom,tipo="digraph")
    else:
        Graf= Grafo(Nom)
    Graf.Agrega_Vertices(Vert)
    Graf.Agrega_Aristas(Aris)
    return Graf


#a=Gnm_Erdo_Renyi(100,150,"Primer_matriiiiz",dirigido=True,auto=True)
#a=Gnp_Gilbert(100,.07,"bb_aleatorio",dirigido=True,auto=True)
#a=Gnr_Geograf_Simple(100,.3,"Espacialigrafo")
#a=Gnd_Barabasi_Albert(200,7,"Grafo_Barbaro")
#a=Gmn_Malla(30,30,"Mallita",dirigido=False)
#a=Dorogovtsev_Mendes(30,"Triangulitos")


#30, 100 y 500 nodos


Grafos=[]
Grafos.append(Gnm_Erdo_Renyi(30,100,"Gnm_Erdo_Renyi_n30_m100")) #420
Grafos.append(Gnm_Erdo_Renyi(100,400,"Gnm_Erdo_Renyi_n100_m400")) #4900
Grafos.append(Gnm_Erdo_Renyi(500,1000,"Gnm_Erdo_Renyi_n500_m1000")) #124500
Grafos.append(Gnp_Gilbert(30,.2,"Gnp_Gilbert_n30_p20"))
Grafos.append(Gnp_Gilbert(100,.07,"Gnp_Gilbert_n100_p07"))
Grafos.append(Gnp_Gilbert(500,.01,"Gnp_Gilbert_n500_p001"))
Grafos.append(Gnr_Geograf_Simple(30,.4,"Gnr_Geograf_Sim_n30_r40"))
Grafos.append(Gnr_Geograf_Simple(100,.1,"Gnr_Geograf_Sim_n100_r10"))
Grafos.append(Gnr_Geograf_Simple(500,.05,"Gnr_Geograf_Sim_n500_r05"))
Grafos.append(Gnd_Barabasi_Albert(30,3,"Gnd_Barabasi_Albert_n30_d3"))
Grafos.append(Gnd_Barabasi_Albert(100,5,"Gnd_Barabasi_Albert_n100_d5"))
Grafos.append(Gnd_Barabasi_Albert(500,10,"Gnd_Barabasi_Albert_n500_d10"))
Grafos.append(Gmn_Malla(30,30,"Gmn_Malla_n30_m30"))
Grafos.append(Gmn_Malla(100,140,"Gmn_Malla_n100_m140"))
Grafos.append(Gmn_Malla(500,450,"Gmn_Malla_n500_m450"))
Grafos.append(Dorogovtsev_Mendes(30,"Dorogovtsev_Mendes_30"))
Grafos.append(Dorogovtsev_Mendes(100,"Dorogovtsev_Mendes_100"))
Grafos.append(Dorogovtsev_Mendes(500,"Dorogovtsev_Mendes_500"))
Grafos.append(Gmn_Malla(500,40,"Gmn_Malla_n500_m40"))

for i in range(len(Grafos)):
    Grafos[i].Exporta_grafo(Grafos[i].Nom)

