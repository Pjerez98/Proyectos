# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 01:15:22 2021

@author: usuario
"""
import copy
import numpy as np
from math import sqrt
from scipy.cluster.vq import vq
from scipy.cluster.vq import kmeans
import random
import matplotlib.pyplot as plt
#from sklearn.datasets import make_blobsfrom
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import IncrementalPCA as sk_pca
from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm


def distEuclidiana(punto1, punto2):
    distancia = sqrt(sum([(a - b) ** 2 for a, b in zip(punto1, punto2)]))  
    return distancia

# Se ocupa un metodo parecido al del codo, pero se llama metodo de la rodilla
def calcularEpsilon(x, nombre):
    dist_matriz = np.zeros((len(x), len(x)))
    neighbors_index = np.zeros((len(x), len(x)))
    
    # Para calcular un epsilon aproximado para el DBSCAN
    for i in range(len(x)):
        for j in range(len(x)):
            dist = distEuclidiana(x[i], x[j])
            dist_matriz[i][j] = dist
    
    neighbors_index[:] = dist_matriz
        
    for i in range(len(x)):
        dist_matriz[i].sort()
    
    neighbors_matriz = dist_matriz[:] # Matriz de distancia ordenadas del vecino mas cercano
    neighbors_index = neighbors_index.argsort() # Matriz que guarda los indices de la matriz de distancia 
    
    dist_matriz = dist_matriz[:,:4] # Solo ocupo los k vecinos mas cercanos
    dist_matriz = np.sort(dist_matriz, axis=0)
    dist_matriz = dist_matriz[:,3]
    plt.title("Técnica de la rodilla para encontrar epsilon óptimo - "+nombre)
    plt.plot(dist_matriz)
    
    return neighbors_matriz, neighbors_index

# El algoritmo DBSCAN se baso en parte en el pseudocodigo de https://es.wikipedia.org/wiki/DBSCAN
    # Entrega exactamente los mismo resultados del algoritmo DBSCAN implementado en scikit learn
def DBSCAN(data, eps, minPts, neighbors_matriz, neighbors_index):
    n_cluster = 1
    n = len(data)
    clasificacion = [False] * n 
    for p in range(n):
        if clasificacion[p] == False:
            clasificacion[p] = True # punto clasificado general, se tiene que clasificar en core, border or noise point
            neighborPts = regionQuery(p, eps, neighbors_matriz, neighbors_index)
            if len(neighborPts) < minPts:
                clasificacion[p] = -1 # punto noise; Que pasa si se clasifico un border como noise?
            else:
                clasificacion[p] = n_cluster # punto core
                expandCluster(p, clasificacion, neighborPts, n_cluster, eps, minPts, neighbors_matriz, neighbors_index) # Desarrollo del punto core en su respectivo cluster
                n_cluster += 1
            
    return clasificacion
                  
def expandCluster(p, clasificacion, neighborPts, n_cluster, eps, minPts, neighbors_matriz, neighbors_index):
    for neighbors in neighborPts:
        if clasificacion[neighbors] == False or clasificacion[neighbors] == -1:
            clasificacion[neighbors] = True # Es un punto border point hasta el momento; Puede pasar a ser core point
            expand_neighbor = regionQuery(neighbors, eps, neighbors_matriz, neighbors_index)
            # En esta parte el punto solamente puede ser core o border point
            if len(expand_neighbor) >= minPts: 
                for i in expand_neighbor:
                    neighborPts.append(i) 
        if clasificacion[neighbors] == True:
            clasificacion[neighbors] = n_cluster
                
def regionQuery(p, eps, neighbors_matriz, neighbors_index):
    ptos_region = []
    for j in range(len(neighbors_matriz[p])):
        if neighbors_matriz[p][j] <= eps and p != j:
            ptos_region.append(neighbors_index[p][j])
    return ptos_region   

def distancia(centroide, punto):
    num_coord = len(punto)
    coord_cent = 0
    coord_punto = 0
    distancia = 0
    #resta cada coordenada de los puntos y la eleva al cuadrado
    for i in range(0, num_coord):
        x1 = centroide[coord_cent]
        x2 = punto[coord_punto]
        coord_cent = coord_cent + 1
        coord_punto = coord_punto + 1
        dif_al_cuadrado = (x1 - x2)**2
        distancia = distancia + dif_al_cuadrado
    distancia = distancia**(0.5)
    return distancia


def asignar_datos_a_centroides(data, clust_centers, asig_cent):
    pos_punto = 0
    for punto in data:
        minimo = 999999999999999999999999
        asig = 0
      
        for centroide in clust_centers:
            d = distancia(centroide, punto)
            
            #print(d)
            if d < minimo:
            #    print(asig)
                minimo = d
                k = asig
                
                
            asig = asig + 1
    
        asig_cent[pos_punto] = k
        pos_punto = pos_punto + 1

def recalcular_centroides(data, clust_centers, asig_cent):
    
    num_centroides = len(clust_centers)
    num_columnas = len(data[0])
    nuevos_centroides = [0 for _ in range(0,len(clust_centers))]
    #print(nuevos_centroides)
    num_puntos = len(data)
    pos_punto = 0
    centroide = 0
    ind_centroide = 0
    interruptor = False
    nuevos_centroides = [[] for _ in range(0, num_centroides)]
    #ir agrupando cada punto para obtener nuevos centroides
    for i in range(0, num_puntos):
        j = asig_cent[i] #centroide asignado
    #     nuevos_centroides[j].append(data[i])
    # print("--------------------")
    # print(len(nuevos_centroides))
    # print("--------------------")
    # nuevos_centroides = np.array(nuevos_centroides).mean(axis=0)
    # # for g in range(len(nuevos_centroides)):
    # #     nuevos_centroides[g] = np.array(nuevos_centroides[g]).mean(axis=0)
    # #     break

    # print(nuevos_centroides)
    
        for k in range(0, num_columnas):
            nuevos_centroides[j].append(data[i][k])
            #print(data[i][k])
            # if nuevos_centroides[j] != type(2.5):
            #     print("ERROR")
            #     interruptor = True
            #     break
   
    for j in range(0, num_centroides):
        nuevos_centroides[j] = np.array(nuevos_centroides[j]).reshape(int(len(nuevos_centroides[j])/num_columnas),num_columnas)
    
    #print("HOLAAAAAAAAAAAAAAAAAAAA")
    #print(len(nuevos_centroides))
    #print(asig_cent)
    #print(nuevos_centroides)

    for j in range(0, num_centroides):
        #print(nuevos_centroides[j])
      
        nuevos_centroides[j] = nuevos_centroides[j].mean(axis = 0)
    #print(nuevos_centroides)    
        #print(nuevos_centroides[j])
        #print(nuevos_centroides[j])
    clust_centerss = list(nuevos_centroides)
    j = 0
 
    for i in clust_centerss:
        
     
        clust_centers[j] = i
        j = j + 1
                
def kmeanss(data, clust_centers, asig_cent):
    finalizar = False
    contador = 0
    a = 0
    while finalizar == False:
  
        copia = list(asig_cent)
        asignar_datos_a_centroides(data, clust_centers, asig_cent)
        a = a + 1
        if asig_cent == copia: #significa que no hubo reasignación a los centroides
          
            finalizar = True
        else: #si es que hubo reasignación
            #print("HOLAAAAAAAAA34343")
            recalcular_centroides(data, clust_centers, asig_cent)
        contador = contador + 1
    
def metodo_codo(X, nombre):
    max_k = 10## maximo número de clusters que vamos a crear
    K = range(1,max_k)
    ssw = []
    cmap = cm.get_cmap("Spectral")
    color_palette = [cmap(float(i)/max_k) for i in K]
    centroid = [sum(X)/len(X) for i in K]
    sst = sum(np.min(cdist(X, centroid, "euclidean"), axis = 1))
    #print(X)
    #print(centroid)
    data = X.copy()
    
    for k in K:
        clust_centers, labels = pd.DataFrame(kmeanof(k , data)[0]), kmeanof(k , data)[1]
        #kmeanModel = KMeans(n_clusters=k).fit(X)
        #print(X)
        #centers = pd.DataFrame(kmeanModel.cluster_centers_)
        #labels = kmeanModel.labels_
        #print(labels)
        #print(centers)
        ssw_k = sum(np.min(cdist(X, kmeanof(k , data)[0], "euclidean"), axis = 1))#distancias al cuadrado del cada punto con su centroide respectivo
        #ssw_k = sum(np.min(cdist(X, kmeanModel.cluster_centers_, "euclidean"), axis = 1))#distancias al cuadrado del cada punto con su centroide respectivo
        #print(kmeanModel.cluster_centers_)
        #print(cdist(X, kmeanModel.cluster_centers_, "euclidean"))
        #break
        # if ssw_k <= 0:
        #     break
        ssw.append(ssw_k)
    #Representación del codo
    #print(ssw)
    plt.plot(K, ssw, "bx-")
    plt.xlabel("k")
    plt.ylabel("SSw(k)")
    plt.title("La técnica del codo para encontrar el k óptimo - "+nombre)
    plt.show()       

#-------------------------------------------------------------------

#Analisis de componentes principales (usando librerías) . Objetivo: Reducir dimensionalidad de los datos previo a clusterización.
#seeds, statlog, haberman, bs(1), breat_cw, cmc, wine(1)    
def PCAs(df, dataset):
    if dataset == 'wine' or dataset == 'bs': #target 1
        X = df.iloc[:,1:].values
        #y = df.iloc[:,-1].values
        X_std = StandardScaler().fit_transform(X)
        acp = sk_pca(n_components = 2)
        Y = acp.fit_transform(X_std)
    
    else:
        X = df.iloc[:,0:-1].values
        #y = df.iloc[:,-1].values
        X_std = StandardScaler().fit_transform(X)
        acp = sk_pca(n_components = 2)
        Y = acp.fit_transform(X_std)
    
    return Y


def kmeanof( k , data, pts = None):
    #k   = 7
    pts = np.random.random((k,2))
    #print(pts)
    clust_centers = pts
    #print(len(clust_centers))
    numero_cluster = k     
    asig_cent = [None for _ in range(0,len(data))]
    #print("hola")
    
    asignar_datos_a_centroides(data, clust_centers, asig_cent)
    
    recalcular_centroides(data, clust_centers, asig_cent)
    
    kmeanss(data, clust_centers, asig_cent)
    # plt.figure(figsize = (10,5))
    # plt.scatter(data[:,0], data[:,1],10, c = asig_cent, cmap = "prism")
    # plt.show()
    #print(asig_cent)
    #clust_centers = centroides de los clusters
    #asig_cent = etiquetas de clusters de los datos 
    #k = número clusters
    
    return clust_centers,asig_cent,k
    
  
def partida_optima(k, data, n):
    random.seed(8)
    pto = np.random.random((k,2))
    a = 0
    best = sum(np.min(cdist(data, kmeanof(k , data, pto)[0], "euclidean"), axis = 1))
    puntos = []
    for i in range(n):
        pts = np.random.random((k,2))
        puntos.append(pts)
    
    for t in range(n):
        c = sum(np.min(cdist(data, kmeanof(k , data, puntos[t])[0], "euclidean"), axis = 1))
        if c < best:
            best = c
            pto = puntos[t]
            a = 1
    
    return pto
    
def graficar(x, target, nombre): #DBSCAN
    # Para graficar en 2D, con dos dimensiones
    plt.figure(figsize = (10,5))
    plt.title("DBSCAN - "+nombre)
    plt.scatter(x[:,0], x[:,1], 10, c = target)
    plt.show()  

def graficar_kmeans(data, clust_centers, centros, asig_cent, nombre): #Kmeans
    plt.figure(figsize = (10,5))
    plt.title("Kmeans - "+nombre)
    plt.scatter(data[:,0], data[:,1],10, c = asig_cent )
    plt.scatter(clust_centers[:,0], clust_centers[:,1],marker = '*',c = centros, s=1000 )
    plt.show()
    
# Para salir de la ejecución del programa
def salir():
    print("")
    print('Has salido de la ejecución del programa')
    print("")

# Las opciones de menu que tendra el usuario para ingresar
def menu():
    k = 0
    print("")
    if k == 0:
        print("Bienvenido a CLUSTER 3.4 !")
    print("Métodos: ")
    print("1. K-MEANS")
    print("2. DBSCAN")  
    print("3. Salir")
    k += 1
    return            
    
def menu1():
    print("")
    print("Métodos: ")
    print("1. K-MEANS")
    print("2. DBSCAN")
    print("3. Salir") 

def main():
    op = 0
    contador = 0
    aux = 0
    menu()  
    while op != 3:
        while True:
            try:
                if contador > 0:
                    menu1()
                op = int(input("Elige una opción: "))
                print("")
                if op == 1 or op == 2 or op == 3:
                    break
                else: 
                    if contador > 0:
                        print("Valor ingresado no es valido, intente nuevamente")
                    if aux == 0:
                        print("")
                        print("Valor ingresado no es valido, intente nuevamente")    
                        menu1()
                        
            except ValueError:
                if contador > 0:
                    print("")
                    print("Valor ingresado no es valido, intente nuevamente")    
                if aux == 0:
                    print("")
                    print("Valor ingresado no es valido, intente nuevamente")    
                    menu1()
                    
        aux += 1
        contador += 1        
        random.seed(35)
        #Lectura de datos
        #seeds, statlog, haberman, bs(1), breat_cw, cmc, wine(1)
        p0 = 'iris'
        p1 = "seeds"
        p2 = "statlog"
        p3 = "haberman"
        p4 = 'bs' 
        p5 = 'breat_cw'
        p6 = 'cmc'
        p7 = 'wine' 
        nombres = [p0,p1,p2,p3,p4,p5,p6,p7]
        
        if op == 1:
            print("########## Algoritmo K-MEANS ##########")
        elif op == 2:
            print("########## Algoritmo DBSCAN ##########")      
        
        j = 0
        for i in nombres:
            print("Ingrese ",j," para leer :","",i,"")
            j += 1
                
        df00 = pd.read_csv("iris.data", header = None)
        df0 = pd.read_csv("seeds_dataset.txt", sep = "\t+", header = None)
        df1 = pd.read_csv("heart.dat", sep = " ", header = None)
        df2 = pd.read_csv("haberman.data", header = None)
        df3 = pd.read_csv("balance-scale.data", header = None)
        df4 = pd.read_csv("breast-cancer-wisconsin.data", header = None)
        df4 = df4.replace('?', np.NaN)
        df4 = df4.dropna()
        df5 = pd.read_csv("cmc.data", header = None)
        df6 = pd.read_csv("wine.data", header = None)
        
        #print(df)
        entradas = [df00,df0,df1,df2,df3,df4,df5,df6]
        if op != 3:
            while True:
                try:
                    r = int(input("Escoga dataset de entrada: "))
                    if r < 0 or r > 7:
                        print("Valor ingresado no es valido, intente nuevamente")
                    else:
                        break
                except ValueError:
                    print("Valor ingresado no es valido, intente nuevamente")
              
            df = entradas[r]
          
            nombre = nombres[r]
            #Se utilizó la libreria sklearn para realizar PCA 
            Y = PCAs(df,nombre)
            data = Y              
            
            if op == 1: 
                k_optimos = [2,3,3,3,4,2,3,3]
                v = nombres.index(nombre)
                #Eleccion del k optimo
                #iris k = 2
                #seeds k = 3 #no mostrar
                #statlog k = 3
                #haberman k = 3
                #bs k = 4 # no mostrar
                #breat_cw k = 2 ##
                #cmc k = 3
                #wine k = 3
                
                metodo_codo(data, nombre)
                k = k_optimos[v]
                # while True:
                #     try:
                #         k = int(input("Ingrese k óptimo según gráfico técnica de codo: "))
                #         if 0 < k < 10:
                #             break
                #     except:
                #         print("Error, por favor ingrese k válido")       
                        
                #Elección punto de partida
                punto_optimo = partida_optima(k, data, 6)
             
                #Ejecucion del k-means
                clust_centers, asig_cent = kmeanof(k , data, punto_optimo)[0], kmeanof(k , data, punto_optimo)[1]
                recalcular_centroides(data, clust_centers, asig_cent)
                centros = []
                for i in range(0,len(clust_centers)):
                    centros.append(i)
                print(asig_cent)
                print(clust_centers)
                graficar_kmeans(data, clust_centers, centros, asig_cent, nombre)
                
            elif op == 2:
                if nombre == 'iris':
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.6, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)
                    
                elif nombre == "seeds":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.5, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)
                    
                elif nombre == "statlog":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.45, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)
                                    
                elif nombre == "haberman":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.3, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)                  
                    
                elif nombre == "bs":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.2, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)
                    
                elif nombre == "breat_cw":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.25, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)   
                    
                elif nombre == "cmc":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.25, 4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)               
                    
                elif nombre == "wine":
                    neighbors_matriz, neighbors_index = calcularEpsilon(data, nombre)
                    target = DBSCAN(data, 0.53,  4, neighbors_matriz, neighbors_index)
                    print(target)
                    graficar(data, target, nombre)        
                                
        elif op == 3:
            salir()
        
        else:
            print("")
            print('Has ingresado un valor fuera de rango. Por favor intentalo nuevamente')  
                
if __name__ == "__main__":               
    main()







#clust_centers = [data[c1],data[c2]]
#print(vq(data,clust_centers))
#print(kmeans(data,clust_centers))
#print(kmeans(data,2))

