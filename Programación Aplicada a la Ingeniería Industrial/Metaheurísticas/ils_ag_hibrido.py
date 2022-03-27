# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 23:57:36 2021

@author: usuario
"""
#Nombres: Nicolás Araya Vera y Pablo Jerez Agurto
#Asignatura: Programación Aplicada a la Ingeniería Industrial
#Profesor: Carlos Contreras Bolton
#Carrera: Ingeniería Civil Industrial
#Universidad de Concepción, Chile
#Fecha: 5/01/2021


import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion
from operator import itemgetter

import array
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

graficar_ruta = False
coord_x = []
coord_y = []
archivo=open("lectura_instancias.txt","r")
instancias=archivo.readlines()
lineas=[]
for i in instancias:
    lineas.append(i.split())




# distancia entre la ciudad i y j
def distancia(i, j):
    u = i + 1 , j + 1
    return problem.get_weight(*u)
def distancia2(i, j):
    u = i , j 
    return problem.get_weight(*u)
# Costo de la ruta
def costoTotal(ciudad):
    suma = 0
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distancia(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distancia(ciudad[-1], ciudad[0])
    return suma

def VecinoMasCercanoOpt(ciudad):
    n = len(ciudad)
    Minimo = 999999999999999999999999999999
    for i in range(n):
        solucion = vecinoMasCercano(n, i)
        if costoTotal( solucion ) < Minimo:
            Minimo = costoTotal(solucion)
            partida = i
    return partida
# heurística del vecino más cercano
    
def vecinoMasCercano(n, desde):
    actual = desde
    ciudad = []
    ciudad.append(desde)
    seleccionada = [False] * n
    seleccionada[actual] = True

    while len(ciudad) < n:
        min = 9999999
        for candidata in range(n):
            if seleccionada[candidata] == False and candidata != actual:
                costo = distancia(actual, candidata)
                if costo < min:
                    min = costo
                    siguiente = candidata

        ciudad.append(siguiente)
        seleccionada[siguiente] = True
        actual = siguiente

    return ciudad

def DosOptDLB(ciudad):
    n = len( ciudad )
    dontlook = []
    for i in ciudad:
        dontlook.append(False)
    
    for i in range(0, n - 1):
        if dontlook :
            caca= 3
    
# Búsqueda local 2-opt
def DosOpt(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            # nuevoCosto= costo nuevo - costo actual
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < 0:
                min_i, min_j = i, j
                contar = contar + 1
                if contar == 1:
                    flag = False
        if flag == False:
            break


    if contar > 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
def TresOpt1(ciudad):#http://tsp-basics.blogspot.com/2017/03/3-opt-move.html 
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 3):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                minimo = 0
                nuevoCosto1 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[k]) - distancia(ciudad[i+1],ciudad[k+1]) #a'bc (=ac'b')#abc'
                if nuevoCosto1 > minimo:
                    minimo = nuevoCosto1
                nuevoCosto2 = distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[j],ciudad[k]) - distancia(ciudad[j+1],ciudad[k+1])
                if nuevoCosto2 > minimo:
                    minimo = nuevoCosto2
                nuevoCosto3 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) - distancia(ciudad[i],ciudad[j]) - distancia(ciudad[i+1],ciudad[j+1])
                if nuevoCosto3 > minimo:
                    minimo = nuevoCosto3
                nuevoCosto4 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[k],ciudad[i+1]) - distancia(ciudad[i],ciudad[j]) - distancia(ciudad[j+1],ciudad[k+1])
                if nuevoCosto4 > minimo:
                    minimo = nuevoCosto4
                nuevoCosto5 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[k]) - distancia(ciudad[i+1],ciudad[j+1]) - distancia(ciudad[j],ciudad[k+1])
                if nuevoCosto5 > minimo:
                    minimo = nuevoCosto5
                nuevoCosto6 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[j+1]) - distancia(ciudad[i+1],ciudad[k+1]) - distancia(ciudad[j],ciudad[k])
                if nuevoCosto6 > minimo:
                    minimo = nuevoCosto6
                nuevoCosto7 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[j+1]) - distancia(ciudad[i+1],ciudad[k]) - distancia(ciudad[j],ciudad[k+1])
                if nuevoCosto7 > minimo:
                    minimo = nuevoCosto7
                    
                    
                if nuevoCosto1 ==  minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto2 == minimo:
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto3 == minimo:
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto4 == minimo:
                    min_i, min_k = i, j
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_k = j, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto5 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto6 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto7 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
               
        if flag == False:
            break
def TresOpt(ciudad):#http://tsp-basics.blogspot.com/2017/03/3-opt-move.html
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 3):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                
                nuevoCosto1 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[k]) - distancia(ciudad[i+1],ciudad[k+1]) #a'bc (=ac'b')#abc'
                nuevoCosto2 = distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[j],ciudad[k]) - distancia(ciudad[j+1],ciudad[k+1])
                nuevoCosto3 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) - distancia(ciudad[i],ciudad[j]) - distancia(ciudad[i+1],ciudad[j+1])
                nuevoCosto4 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[k],ciudad[i+1]) - distancia(ciudad[i],ciudad[j]) - distancia(ciudad[j+1],ciudad[k+1])
                nuevoCosto5 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[k]) - distancia(ciudad[i+1],ciudad[j+1]) - distancia(ciudad[j],ciudad[k+1])
                nuevoCosto6 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[j+1]) - distancia(ciudad[i+1],ciudad[k+1]) - distancia(ciudad[j],ciudad[k])
                nuevoCosto7 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[j+1]) - distancia(ciudad[i+1],ciudad[k]) - distancia(ciudad[j],ciudad[k+1])
                
                if nuevoCosto1 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto2 > 0:
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto3 > 0:
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto4 > 0:
                    min_i, min_k = i, j
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_k = j, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto5 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto6 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto7 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
        if flag == False:
            break
 

def OrOpt2(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    minimo = 0
   #Or Opt equivale a un cambio del segmento (i+1 al j), es decir, de x2 a y1. j varian hasta maximo 3 ciudades
    for h in range(3,0,-1):
        
        for i in range(0, n - 2):
            j = i + h 
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                
                nuevoCosto7 = distancia(ciudad[i],ciudad[i+1]) + distancia(ciudad[j],ciudad[j+1]) + distancia(ciudad[k],ciudad[k+1]) - distancia(ciudad[i],ciudad[j+1]) - distancia(ciudad[i+1],ciudad[k]) - distancia(ciudad[j],ciudad[k+1])
                if nuevoCosto7 > minimo:
                    minimo = nuevoCosto7
                #minimo = nuevoCosto7
                    contar = contar + 1
                    min_j = j
                    min_i = i
                    min_k = k
                    indz1 = min_k
                    #z1 = ciudad[j]
                    #eliminar segmento [x2 : y1]
                    segmento_x2_y1 = ciudad[min_i + 1 : min_j + 1 ]
             
                    for m in segmento_x2_y1: 
                        
                        indz1= min_k
                        indm = ciudad.index(m)
                        #print(m)
                        valor = ciudad.pop(indm)
                        #indz1= ciudad2.index(z1)
                        ciudad.insert(indz1,valor)

               
                    flag = False    
            if flag == False:
                break  

        
def NodeShift2(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            #value = random.uniform(0,1)
            v0 = i + 2
            nuevoCosto1 = distancia(ciudad[i], ciudad[v0]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[i + 1],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[i + 1],ciudad[v0]) - distancia(ciudad[j],ciudad[j + 1])
            v0 = j - 1
            nuevoCosto2 = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[v0],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[v0],ciudad[j]) - distancia(ciudad[j],ciudad[j + 1])
            
            if (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto1 < nuevoCosto2:
                v0 = i + 2
            
                #nuevoCosto = distancia(ciudad[i], ciudad[v0]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[i + 1],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[i + 1],ciudad[v0]) - distancia(ciudad[j],ciudad[j + 1])
                valor = ciudad.pop(i + 1)
                ciudad.insert(j, valor)
                contar += 1
                if contar == 1:
                    flag = False
            elif (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto2 < nuevoCosto1:
                v0 = j - 1
                valor = ciudad.pop(j)
                ciudad.insert(i + 1, valor)
                contar += 1
                if contar == 1:
                    flag = False
       
        
        if flag == False:
            break

       
def Opt2_5(ciudad):#http://tsp-basics.blogspot.com/2017/03/25-opt.html
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            value = random.uniform(0,1)
        
            # nuevoCosto= costo nuevo - costo actual
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            
            if nuevoCosto < 0:
                min_i, min_j = i, j
                ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                contar += 1
                if contar == 1:
                    flag = False
            else:
                v0 = i + 2
                nuevoCosto1 = distancia(ciudad[i], ciudad[v0]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[i + 1],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[i + 1],ciudad[v0]) - distancia(ciudad[j],ciudad[j + 1])
                v0 = j - 1
                nuevoCosto2 = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[v0],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[v0],ciudad[j]) - distancia(ciudad[j],ciudad[j + 1])
                
                if (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto1 < nuevoCosto2:
                    v0 = i + 2
                
                    #nuevoCosto = distancia(ciudad[i], ciudad[v0]) + distancia(ciudad[j],ciudad[i + 1]) + distancia(ciudad[i + 1],ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[i + 1],ciudad[v0]) - distancia(ciudad[j],ciudad[j + 1])
                    valor = ciudad.pop(i + 1)
                    ciudad.insert(j, valor)
                    contar += 1
                    if contar == 1:
                        flag = False
                elif (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto2 < nuevoCosto1:
                    v0 = j - 1
                    valor = ciudad.pop(j)
                    ciudad.insert(i + 1, valor)
                    contar += 1
                    if contar == 1:
                        flag = False
        if contar > 0:
            break
                            

        if flag == False:
            break

   
def Make_Node_Shift_Move(i, j, ciudad):
    n = len(ciudad)
    shiftSize = j - i  
    left = i
    #print("left: ", left)
    #print(ciudad[left])
    #print(shiftSize)
    valor = ciudad.pop(i)
    ciudad.insert(j, valor)         

    
def NodeShift(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            # nuevoCosto= costo nuevo - costo actual
            v0 = i - 1
            #if v0 != j:
            nuevoCosto = distancia(ciudad[v0], ciudad[i + 1]) + distancia(ciudad[i],ciudad[j + 1]) + distancia(ciudad[i],ciudad[j]) - distancia(ciudad[v0], ciudad[i]) - distancia(ciudad[i],ciudad[i + 1]) - distancia(ciudad[j],ciudad[j + 1])
            if nuevoCosto < 0:
                #print( i , j)
                min_i = i
                min_j = j
              
                contar += 1
                if contar == 1:
                    flag = False
                #break
        if flag == False:
            break


    if contar > 0:
        Make_Node_Shift_Move(min_i, min_j, ciudad)



def serepite(valor, ciudad):
    encontrado = False
    repite = 0
    for i in ciudad:
        if valor == i:
            repite = repite + 1
            if repite == 2:
                encontrado = True
                break
    return encontrado              

def ciclohamiltoniano(ciudad):
    ciclohamiltoniano == "True"
    for valor in ciudad:
        if serepite(valor,ciudad) == True:
            ciclohamiltoniano == "False"
           
            break
    if ciclohamiltoniano == "False":
        return "False"
    else:
        return "True"
            
def costoTotalk(ciudad):
    suma = 0
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distancia2(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distancia2(ciudad[-1], ciudad[0])
    return suma

def VecinoMasCercanoOptk(ciudad):
    n = len(ciudad)
    Minimo = 999999999999999999999999999999
    for i in range(n):
        solucion = vecinoMasCercanok(n, i)
        if costoTotalk( solucion ) < Minimo:
            Minimo = costoTotalk(solucion)
            partida = i
    return partida
# heurística del vecino más cercano
    
def vecinoMasCercanok(n, desde):
    actual = desde
    ciudad = []
    ciudad.append(desde)
    seleccionada = [False] * n
    seleccionada[actual] = True

    while len(ciudad) < n:
        min = 9999999
        for candidata in range(n):
            if seleccionada[candidata] == False and candidata != actual:
                costo = distancia2(actual, candidata)
                if costo < min:
                    min = costo
                    siguiente = candidata

        ciudad.append(siguiente)
        seleccionada[siguiente] = True
        actual = siguiente

    return ciudad

 
def DosOptDLBk(ciudad):
    n = len( ciudad )
    dontlook = []
    for i in ciudad:
        dontlook.append(False)
    
    for i in range(0, n - 1):
        if dontlook :
            caca= 3
        

def DosOptk(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            # nuevoCosto= costo nuevo - costo actual
            nuevoCosto = distancia2(ciudad[i], ciudad[j]) + distancia2(ciudad[i + 1], ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[j], ciudad[j + 1])
            if nuevoCosto < 0:
                min_i, min_j = i, j
                contar = contar + 1
                if contar == 1:
                    flag = False
        if flag == False:
            break


    if contar > 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
def TresOpt1k(ciudad):#http://tsp-basics.blogspot.com/2017/03/3-opt-move.html 
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 3):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                minimo = 0
                nuevoCosto1 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[k]) - distancia2(ciudad[i+1],ciudad[k+1]) #a'bc (=ac'b')#abc'
                if nuevoCosto1 > minimo:
                    minimo = nuevoCosto1
                nuevoCosto2 = distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[j],ciudad[k]) - distancia2(ciudad[j+1],ciudad[k+1])
                if nuevoCosto2 > minimo:
                    minimo = nuevoCosto2
                nuevoCosto3 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) - distancia2(ciudad[i],ciudad[j]) - distancia2(ciudad[i+1],ciudad[j+1])
                if nuevoCosto3 > minimo:
                    minimo = nuevoCosto3
                nuevoCosto4 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[k],ciudad[i+1]) - distancia2(ciudad[i],ciudad[j]) - distancia2(ciudad[j+1],ciudad[k+1])
                if nuevoCosto4 > minimo:
                    minimo = nuevoCosto4
                nuevoCosto5 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[k]) - distancia2(ciudad[i+1],ciudad[j+1]) - distancia2(ciudad[j],ciudad[k+1])
                if nuevoCosto5 > minimo:
                    minimo = nuevoCosto5
                nuevoCosto6 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k+1]) - distancia2(ciudad[j],ciudad[k])
                if nuevoCosto6 > minimo:
                    minimo = nuevoCosto6
                nuevoCosto7 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k]) - distancia2(ciudad[j],ciudad[k+1])
                if nuevoCosto7 > minimo:
                    minimo = nuevoCosto7
                    
                    
                if nuevoCosto1 ==  minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto2 == minimo:
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto3 == minimo:
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto4 == minimo:
                    min_i, min_k = i, j
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_k = j, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto5 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto6 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto7 == minimo:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
               
        if flag == False:
            break
def TresOptk(ciudad):#http://tsp-basics.blogspot.com/2017/03/3-opt-move.html
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 3):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                
                nuevoCosto1 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[k]) - distancia2(ciudad[i+1],ciudad[k+1]) #a'bc (=ac'b')#abc'
                nuevoCosto2 = distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[j],ciudad[k]) - distancia2(ciudad[j+1],ciudad[k+1])
                nuevoCosto3 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) - distancia2(ciudad[i],ciudad[j]) - distancia2(ciudad[i+1],ciudad[j+1])
                nuevoCosto4 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[k],ciudad[i+1]) - distancia2(ciudad[i],ciudad[j]) - distancia2(ciudad[j+1],ciudad[k+1])
                nuevoCosto5 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[k]) - distancia2(ciudad[i+1],ciudad[j+1]) - distancia2(ciudad[j],ciudad[k+1])
                nuevoCosto6 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k+1]) - distancia2(ciudad[j],ciudad[k])
                nuevoCosto7 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k]) - distancia2(ciudad[j],ciudad[k+1])
                
                if nuevoCosto1 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto2 > 0:
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto3 > 0:
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto4 > 0:
                    min_i, min_k = i, j
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_k = j, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto5 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
                elif nuevoCosto6 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    flag = False
                    
                elif nuevoCosto7 > 0:
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    flag = False
                    
        if flag == False:
            break
 

def OrOptk(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    minimo = 0
   #Or Opt equivale a un cambio del segmento (i+1 al j), es decir, de x2 a y1. j varian hasta maximo 3 ciudades
    for h in range(3,1,-1):
        
        for i in range(0, n - 2):
            j = i + h
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                
                nuevoCosto7 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k]) - distancia2(ciudad[j],ciudad[k+1])
                if nuevoCosto7 > minimo:
                    minimo = nuevoCosto7
                    min_i, min_k = i, k
                    ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                    min_j, min_k = j, k
                    ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
                    min_i, min_j = i, j
                    ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                    #flag = False
                    break
                    

def OrOpt2k(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    minimo = 0
   #Or Opt equivale a un cambio del segmento (i+1 al j), es decir, de x2 a y1. j varian hasta maximo 3 ciudades
    for h in range(3,0,-1):
        
        for i in range(0, n - 2):
            j = i + h 
            for k in range(j + 1, n - 1):
                contar = contar + 1
                #print(contar,"---",i,j,k)
                
                nuevoCosto7 = distancia2(ciudad[i],ciudad[i+1]) + distancia2(ciudad[j],ciudad[j+1]) + distancia2(ciudad[k],ciudad[k+1]) - distancia2(ciudad[i],ciudad[j+1]) - distancia2(ciudad[i+1],ciudad[k]) - distancia2(ciudad[j],ciudad[k+1])
                if nuevoCosto7 > minimo:
                    minimo = nuevoCosto7
                #minimo = nuevoCosto7
                    contar = contar + 1
                    min_j = j
                    min_i = i
                    min_k = k
                    indz1 = min_k
                    #z1 = ciudad[j]
                    #eliminar segmento [x2 : y1]
                    segmento_x2_y1 = ciudad[min_i + 1 : min_j + 1 ]
             
                    for m in segmento_x2_y1: 
                        
                        indz1= min_k
                        indm = ciudad.index(m)
                        #print(m)
                        valor = ciudad.pop(indm)
                        #indz1= ciudad2.index(z1)
                        ciudad.insert(indz1,valor)

               
                    flag = False    
            if flag == False:
                break  
 
        
def NodeShift2k(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            #value = random.uniform(0,1)
            v0 = i + 2
            nuevoCosto1 = distancia2(ciudad[i], ciudad[v0]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[i + 1],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[i + 1],ciudad[v0]) - distancia2(ciudad[j],ciudad[j + 1])
            v0 = j - 1
            nuevoCosto2 = distancia2(ciudad[i], ciudad[j]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[v0],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[v0],ciudad[j]) - distancia2(ciudad[j],ciudad[j + 1])
            
            if (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto1 < nuevoCosto2:
                v0 = i + 2
            
                #nuevoCosto = distancia2(ciudad[i], ciudad[v0]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[i + 1],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[i + 1],ciudad[v0]) - distancia2(ciudad[j],ciudad[j + 1])
                valor = ciudad.pop(i + 1)
                ciudad.insert(j, valor)
                contar += 1
                if contar == 1:
                    flag = False
            elif (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto2 < nuevoCosto1:
                v0 = j - 1
                valor = ciudad.pop(j)
                ciudad.insert(i + 1, valor)
                contar += 1
                if contar == 1:
                    flag = False
       
        
        if flag == False:
            break
      
def Opt2_5k(ciudad):#http://tsp-basics.blogspot.com/2017/03/25-opt.html
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            value = random.uniform(0,1)
        
            # nuevoCosto= costo nuevo - costo actual
            nuevoCosto = distancia2(ciudad[i], ciudad[j]) + distancia2(ciudad[i + 1], ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[j], ciudad[j + 1])
            
            if nuevoCosto < 0:
                min_i, min_j = i, j
                ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
                contar += 1
                if contar == 1:
                    flag = False
            else:
                v0 = i + 2
                nuevoCosto1 = distancia2(ciudad[i], ciudad[v0]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[i + 1],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[i + 1],ciudad[v0]) - distancia2(ciudad[j],ciudad[j + 1])
                v0 = j - 1
                nuevoCosto2 = distancia2(ciudad[i], ciudad[j]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[v0],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[v0],ciudad[j]) - distancia2(ciudad[j],ciudad[j + 1])
                
                if (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto1 < nuevoCosto2:
                    v0 = i + 2
                
                    #nuevoCosto = distancia2(ciudad[i], ciudad[v0]) + distancia2(ciudad[j],ciudad[i + 1]) + distancia2(ciudad[i + 1],ciudad[j + 1]) - distancia2(ciudad[i], ciudad[i + 1]) - distancia2(ciudad[i + 1],ciudad[v0]) - distancia2(ciudad[j],ciudad[j + 1])
                    valor = ciudad.pop(i + 1)
                    ciudad.insert(j, valor)
                    contar += 1
                    if contar == 1:
                        flag = False
                elif (nuevoCosto1 < 0 or nuevoCosto2 < 0) and nuevoCosto2 < nuevoCosto1:
                    v0 = j - 1
                    valor = ciudad.pop(j)
                    ciudad.insert(i + 1, valor)
                    contar += 1
                    if contar == 1:
                        flag = False
        if contar > 0:
            break
                            

        if flag == False:
            break
    
def NodeShiftk(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            # nuevoCosto= costo nuevo - costo actual
            v0 = i - 1
            #if v0 != j:
            nuevoCosto = distancia2(ciudad[v0], ciudad[i + 1]) + distancia2(ciudad[i],ciudad[j + 1]) + distancia2(ciudad[i],ciudad[j]) - distancia2(ciudad[v0], ciudad[i]) - distancia2(ciudad[i],ciudad[i + 1]) - distancia2(ciudad[j],ciudad[j + 1])
            if nuevoCosto < 0:
                #print( i , j)
                min_i = i
                min_j = j
              
                contar += 1
                if contar == 1:
                    flag = False
                #break
        if flag == False:
            break


    if contar > 0:
        Make_Node_Shift_Move(min_i, min_j, ciudad)
    
def Optk(ciudad):# PENDIENTE
    n = len(ciudad)
    flag = True
    contar = 0
    minimizar = False
    while minimizar == False or flag == True: #PASO 1, PASO 2 Y PASO 3
        #PASO 1: SELECCIONAR UN NODO
        i = random.randint(0, n - 1)
        n1 = i
        #PASO 2: SELECCIONAR ARISTA X1 = (N1,N2)
        if i == 0:
            sig = i + 1
            ant = n - 1
        elif i == n - 1: 
            sig = 0
            ant = i - 1
        else:
            sig = i + 1
            ant = i - 1
            
        aux1 = distancia2(i, sig)
        aux2 = distancia2(i, ant)
              
        if aux1 >= aux2:
            x1 = aux1
            x1alt = aux2
            n2 = sig
            n2alt = ant
        else:
            x1 = aux2
            x1alt = aux1
            n2 = ant
            n2alt = sig
      
        #PASO 3: ESCOGER ARISTA Y1 = (N2,N3) (y1 no pertenece a la solucion actual, por lo que N3 != N2 + 1)
        #non3 es el nodo siguiente a n2.
        aristas = 0
       # while aristas < ((n*(n-1))/2) and flag == True :
        if n2 == n - 1:
            non3 = 0
        else:
            non3 = n2 + 1
        #y es candidata a ser n3, para encontrar y1=(n2,n3)
        minimizar = False
        for y in range(n):
            if y != non3 and y != n1 and y != n2  and non3 == n - 1:
                valorganado = x1 - distancia2(n2, y)
                if valorganado > 0:
                    minimizar = False
                    n3 = y
                    y1 = valorganado
                    break
       
    if minimizar == False: # no se encontro y1, volver paso 2 y trabajar con la otra arista
        n2 = n2alt
        x1 = x1alt
        if n2 == n - 1:
            non3 = 0
        else:
            non3 = n2 + 1
        #y es candidata a ser n3, para encontrar y1=(n2,n3)
        minimizar = False
        for y in range(n):
            if y != non3 and y != n1 and y != n2  and non3 == n - 1:
                valorganado = x1 - distancia2(n2, y)
                if valorganado > 0:
                    minimizar = False
                    n3 = y
                    y1 = valorganado
                    break
    #if y1 no es encontrado, se vuelve al PASO 1
    aristas = aristas + 1
    #PASO 4, seleccionar arista x2 =(n3,n4)   
    # dos posibilidades para n4
    if n3 == n-1:
        costo1 = distancia2(n3, 0)
        costo2 = distancia2(n3, n3 - 1)
    elif n3 == 0:
        costo1 = distancia2(n3, n3 + 1)
        costo2 = distancia2(n3, n - 1)
    else:
        costo1 = distancia2(n3, n3 + 1)
        costo2 = distancia2(n3, n3 - 1)
        
    if costo1 >= costo2:
        costoMayor = costo1
        costoMenor = costo2
    else:
        costoMayor = costo2
        costoMenor = costo1
    
    value = random.uniform(0, 1)
    if value > 0.3:
        n4 = costoMayor
    else:
        n4 = costoMenor
    
    x2 = distancia2(n3, n4)
    
    #PASO 5, seleccionar aleatoriamente x3 = (n5,n6), x3 != x1 and x3 != x2, x3 pertenece a la solución actual
    #x1 = (n1,n2)
    #x2 = (n3,n4)
    ciudad1 = []
    ciudad1.append(n1)
    ciudad1.append(n2)
    ciudad1.append(n3)
    ciudad1.append(n4)
    
    while flag == True and len(ciudad1) < n:
        n5 = random.randint(0 , n + 1)
        n6 = random.randint(0, n + 1)
        
        for i in ciudad1:
            if (n5 != i and n6 != i) and n5 != n6:
                serepite = False
                ciudad1.append(n5)
                ciudad1.append(n6)
            else: 
                serepite = True
                
        
        while serepite == True:
            n5 = random.randint(0 , n + 1)
            n6 = random.randint(0, n + 1)
            for i in ciudad1:
                if (n5 != i and n6 != i) and n5 != n6:
                    serepite = False
                    ciudad1.append(n5)
                    ciudad1.append(n6)
                else: 
                    serepite = True

           
     
            
        i = n1
        
  
        nuevoCosto5 = distancia2(ciudad[n1],ciudad[n2]) + distancia2(ciudad[n3],ciudad[n4]) + distancia2(ciudad[n5],ciudad[n6]) - distancia2(ciudad[n2],ciudad[n3]) - distancia2(ciudad[n4],ciudad[n6]) - distancia2(ciudad[n5],ciudad[n1])
        nuevoCosto6 = distancia2(ciudad[n1],ciudad[n2]) + distancia2(ciudad[n3],ciudad[n4]) + distancia2(ciudad[n5],ciudad[n6]) - distancia2(ciudad[n2],ciudad[n3]) - distancia2(ciudad[n4],ciudad[n5]) - distancia2(ciudad[n6],ciudad[n1])
        
        
        if nuevoCosto5 > 0:
            min_i, min_k = n1, n2
            ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
            min_i, min_j = n3, n4
            ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
            flag = False
            
        elif nuevoCosto6 > 0:
            min_i, min_k = n3, 4
            ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
            min_j, min_k = n5, n6
            ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
            flag = False
                                    
            
def perturbation(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i == j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

# perturbación: se escoge una ciudad aleatoria y se intercambia con la ciudad siguiente en la ruta
def perturbation3(ciudad):
    j = 0
    n = len(ciudad)
    i = random.randint(0, n - 1)

    if i == n - 1:
        j = 0
    else:
        j = i + 1
    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp


def perturbation2(ciudad):#cambio 2-opt
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    ciudad[i : j] = ciudad[i : j][::-1]
    
def perturbation4(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    ciudad[i : j] = ciudad[i : j][::-1]
def perturbation5(ciudad):
    j = 0
    n = len(ciudad)
    i = random.randint(0, n - 1)

    if i == 0:
        j = n - 1
    #elif i == n-1:
    #    j = 1
    else:
        j = i - 1
    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp
def desplazamiento(ciudad): #quuita un segmento de la lista y lo coloca en otra posicion
    i,j = 0,0
    n=len(ciudad)
    while i>=j:
        i= random.randint(0, n-1)
        j= random.randint(0, n-1)
    #print(i,j)
    temp = ciudad[i : j]
    #print(temp)
    for a in temp:
        ciudad.remove(a)
    #print(ciudad)
    m=len(ciudad)
    l=random.randint(0, m-1)
    #print(l)
    for b in temp:
        ciudad.insert(l,b)
        l+=1
    #print(ciudad)
        
def basada_en_insercion(ciudad):
    i,j = 0,0
    n=len(ciudad)
    i= random.randint(0, n-1)
    temp = ciudad[i]
    ciudad.remove(temp)
    m=len(ciudad)
    l=random.randint(0, m-1)
    ciudad.insert(l,temp)
    
    #print(ciudad)
    # i,j = 0,0
    # n=len(ciudad)
    # f= ciudad
    
    # while costoTotal(ciudad)>= costoTotal(f):
    #     i= random.randint(0, n-1)
    #     #print (i)
    #     temp = ciudad[i]
    #     ciudad.remove(temp)
    #     #print(ciudad)
    #     m=len(ciudad)
    #     l=random.randint(0, m-1)
    #     #print(l)
    #     ciudad.insert(l,temp)
    #     #print(ciudad)
    # #print(costoTotal(f))
    # #print(costoTotal(ciudad))  
    
def invertir_y_insertar(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    temp= ciudad[i:j]    
    temp1 = ciudad[i : j][::-1]
    for a in temp:
        ciudad.remove(a)
    m=len(ciudad)
    l=random.randint(0, m-1)
    for b in temp1:
        ciudad.insert(l,b)
        l+=1
        
def revolver(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    temp=ciudad[i:j]
    for a in temp:
        ciudad.remove(a)
    random.shuffle(temp) 
    for b in temp:
        ciudad.insert(i,b)
        i+=1

def mutSet(ciudad):
    #perturbation2(ciudad)
    #value = random.uniform(0, 1)
    value = 0
    if value < 0.999:
         perturbation2(ciudad)
    # elif value >= 0.3 and value < 0.6:
    #     perturbation2(ciudad)
    # elif value >= 0.6 and value < 0.85:
    #     perturbation3(ciudad)
    else:
         DosOpt(ciudad)
         OrOpt2(ciudad)

    return ciudad,
def _repeated(element, collection):
    c = 0
    for e in collection:
        if e == element:
            c += 1
    return c > 1
 
def _swap(data_a, data_b, cross_points):
    c1, c2 = cross_points
    new_a = data_a[:c1] + data_b[c1:c2] + data_a[c2:]
    new_b = data_b[:c1] + data_a[c1:c2] + data_b[c2:]
    return new_a, new_b
 
 
def _map(swapped, cross_points):
    n = len(swapped[0])
    c1, c2 = cross_points
    s1, s2 = swapped
    map_ = s1[c1:c2], s2[c1:c2]
    for i_chromosome in range(n):
        if not c1 < i_chromosome < c2:
            for i_son in range(2):
                while _repeated(swapped[i_son][i_chromosome], swapped[i_son]):
                    map_index = map_[i_son].index(swapped[i_son][i_chromosome])
                    swapped[i_son][i_chromosome] = map_[1-i_son][map_index]
    return s1, s2
 
 
def pmx(parent_a, parent_b):#https://thortuga.wordpress.com/2013/11/24/pmx-en-python/
    assert(len(parent_a) == len(parent_b))
    n = len(parent_a)
    cross_points = sorted([random.randint(0, n) for _ in range(2)])
    swapped = _swap(parent_a, parent_b, cross_points)
    mapped = _map(swapped, cross_points)
 
    return mapped
def ox2(ciudad1,ciudad2):
    ciudad1_inicial= list(ciudad1)
    ciudad2_inicial= list(ciudad2)
    # padre1= copy.deepcopy(ciudad1)
    # padre2 = copy.deepcopy(ciudad2)
    n = len(ciudad1)
    remover=[]
    lista1=[]
    cont = 0
    i=0
    j=0
    k=8
    #while j<=i:
    while cont < k:
        i= random.randint(0, n-1)
        while i in lista1:
            i= random.randint(0, n-1)
        lista1.append(i)
        cont+=1
        #j= random.randint(0, n-1)
    #lista1= [i,j]
    #print(lista1)
    lista1.sort()    
    #print('ubicacion',lista1)
    for i in lista1:
        remover.append(ciudad2_inicial[i])
    #print('numeroselegidos',remover)    
    for i in remover:
        ciudad1.insert(ciudad1.index(i),'x')
        ciudad1.remove(i)
    #print(ciudad1)
    for i in remover:
        ciudad1.insert(ciudad1.index('x'),i)
        ciudad1.remove('x')
    #print('ciudad final',ciudad1)
    #hijo1 = ciudad1
     
    remover=[]
    
    #print('ubicacion',lista1)
    for i in lista1:
        remover.append(ciudad1_inicial[i])
    #print('numeroselegidos',remover)    
    for i in remover:
        ciudad2.insert(ciudad2.index(i),'x')
        ciudad2.remove(i)
    #print(ciudad2)
    for i in remover:
        ciudad2.insert(ciudad2.index('x'),i)
        ciudad2.remove('x')
    #print('ciudad final',ciudad2)
    #hijo2 = ciudad2
    #print(costoTotal(ciudad1),costoTotal(ciudad1_inicial))
    # if costoTotal(ciudad1) > costoTotal(ciudad1_inicial):
    #     ciudad1 = ciudad1_inicial
    #     #print('hola')
    # if costoTotal(ciudad2) > costoTotal(ciudad2_inicial):
    #     ciudad2 = ciudad2_inicial
def estaenlista(valor,lista):
    for i in lista:
        if i == valor:
            return True
    return False
 
def ILS(fila,ciudad,a, sumas, semillas=10):
    promedios = []
    tiempos=[]
    costos=[]
    suma_costos=0
    suma_tiempos=0
    minimo=99999999999999999
    for i in range(0,semillas):
        #print("SEMILLA: ",i)
        random.seed(i)
        inicioTiempo = time.time()
        n = len(ciudad)
        # Solución inicial
        desde = VecinoMasCercanoOpt(ciudad)
      
        s = vecinoMasCercano(n, desde)#random.randint(0, n))
        #Mejora solución inicial
        #TresOpt(s)
        #Opt(s)
        #Opt2_5(s)
        perturbation2(s)
        #Opt2_5(s)
        DosOpt(s)
        #OrOpt2(s)
        #DosOpt(s)
        #Opt2_5(s)
        #TresOpt(s)
        NodeShift2(s)
        s_mejor = s[:]
        costoMejor = costoTotal(s_mejor)
        lista_soluciones = []
        lista_costos = []
        lista_costosMejores = []
        lista_costos.append(costoMejor)
        lista_costosMejores.append(costoMejor)
        lista_soluciones.append(s_mejor)
        #print("inicial %d" % costoMejor)
        iterMax = 500
        for iter in range(iterMax):
            # Perturbación
            
            #perturbation3(s)
            # Búsqueda local
            value = random.uniform(0,1) #ERP CERCANO A 2%
            #print(value)
            #value = 0
            if value < 0.9 :
                perturbation2(s)
                DosOpt(s)
                OrOpt2(s)
                #NodeShift2(s)
                #if ciclohamiltoniano(s) == False:
                #    print("Solución no factible")
                #DosOpt(s)
                #OrOpt2(s,s2)
                #Opt2_5(s)
                #TresOpt(s)
                crit = 0.05
            else:
                perturbation2(s)
                TresOpt(s)
                #if ciclohamiltoniano(s) == False:
                #    print("Solución no factible")
                crit = 0.05
            
            #TresOpt(s)
            #Local(s)
            costo_candidato = costoTotal(s)
            values = False
            # Actualizar mejor solución
            if costoMejor > costo_candidato:
                s_mejor = s[:]#actualiza mejor solución
                costoMejor = costo_candidato
                #print("%d\t%d" % (iter, costoMejor))
    
            lista_costos.append(costo_candidato)
            lista_costosMejores.append(costoMejor)
            lista_soluciones.append(s)
            # criterio de aceptación de la solución actual
            if abs(costoMejor - costo_candidato) / costoMejor > crit:
                values = True
                s = s_mejor[:]#actualiza solución actual
            #print(a[2])
            if costoTotal(s) == int(a[2]):
                #print("holaaa", iter)
                break
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print("Semilla: ",i," costo",costoMejor, "Tiempo: ", tiempo," Solución factible: ",ciclohamiltoniano(s) )
        #print("Costo  : %d" % costoMejor)
        #print("Tiempo : %f" % tiempo)
       
        #tiempos.append(tiempo)
        #costos.append(costoMejor)
        suma_costos = suma_costos + costoMejor
        suma_tiempos = suma_tiempos + tiempo
        if costoMejor < minimo:
            minimo = costoMejor
    
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i

    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    c3 = int(c3)
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimo#minimo
    c7 = round(((minimo - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    fila.append(cdatos2)
              
def ILS2(fila,ciudad,a, sumas, semillas=10):
    
    tiempos=[]
    costos=[]
    suma_costos=0
    suma_tiempos=0
    minimo=99999999999999999
    for i in range(0,semillas):
        #print("SEMILLA: ",i)
        random.seed(i)
        inicioTiempo = time.time()
        n = len(ciudad)
        # Solución inicial
        desde = VecinoMasCercanoOptk(ciudad)
      
        s = vecinoMasCercanok(n, desde)#random.randint(0, n))
        #Mejora solución inicial
        #TresOpt(s)
        #Opt(s)
        #Opt2_5(s)
        perturbation2(s)
        #Opt2_5(s)
        DosOptk(s)
        #OrOpt2k(s)
        #DosOpt(s)
        #Opt2_5(s)
        #TresOpt(s)
        NodeShift2k(s)
        s_mejor = s[:]
        costoMejor = costoTotalk(s_mejor)
        lista_soluciones = []
        lista_costos = []
        lista_costosMejores = []
        lista_costos.append(costoMejor)
        lista_costosMejores.append(costoMejor)
        lista_soluciones.append(s_mejor)
        #print("inicial %d" % costoMejor)
        iterMax = 500
        for iter in range(iterMax):
            # Perturbación
            
            #perturbation3(s)
            # Búsqueda local
            #value = random.uniform(0,1) #ERP CERCANO A 2%
            #print(value)
            value = 0
            if value < 0.9 :
                perturbation2(s)
                DosOptk(s)
                OrOpt2k(s)
                #NodeShift2k(s)
                #if ciclohamiltoniano(s) == False:
                #    print("Solución no factible")
                #DosOpt(s)
                #OrOpt2(s,s2)
                #Opt2_5(s)
                #TresOpt(s)
                crit = 0.05
            else:
                perturbation2(s)
                TresOptk(s)
                #if ciclohamiltoniano(s) == False:
                #    print("Solución no factible")
                crit = 0.05
            
            #TresOpt(s)
            #Local(s)
            costo_candidato = costoTotalk(s)
            values = False
            # Actualizar mejor solución
            if costoMejor > costo_candidato:
                s_mejor = s[:]#actualiza mejor solución
                costoMejor = costo_candidato
                #print("%d\t%d" % (iter, costoMejor))
    
            lista_costos.append(costo_candidato)
            lista_costosMejores.append(costoMejor)
            lista_soluciones.append(s)
            # criterio de aceptación de la solución actual
            if abs(costoMejor - costo_candidato) / costoMejor > crit:
                values = True
                s = s_mejor[:]#actualiza solución actual
            #print(a[2])
            if costoTotalk(s) == int(a[2]):
                #print("holaaa", iter)
                break
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print("Semilla: ",i," costo",costoMejor, "Tiempo: ", tiempo," Solución factible: ",ciclohamiltoniano(s) )
        #print("Costo  : %d" % costoMejor)
        #print("Tiempo : %f" % tiempo)
       
        #tiempos.append(tiempo)
        #costos.append(costoMejor)
        suma_costos = suma_costos + costoMejor
        suma_tiempos = suma_tiempos + tiempo
        if costoMejor < minimo:
            minimo = costoMejor
    
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i

    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    c3 = int(c3)
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimo#minimo
    c7 = round(((minimo - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    fila.append(cdatos2)
        
def GA4(fila, ciudad, a, sumas, semillas = 10):#va con ILS2
    mejor_semillas = []
    n= len(ciudad)
    g = 0
    suma_costos = 0
    suma_tiempos = 0
    iterMax = 100
    CXPB, MUTPB= 0.9, 0.3
    #crear poblacion de x soluciones iniciales
    k = 100 #tamaño de poblacion
    for h in range(0,semillas):
        random.seed(h)
        inicioTiempo = time.time()
        g = 0
        poblacion= []
        desde = VecinoMasCercanoOptk(ciudad)
        solucion = vecinoMasCercanok(n,desde)
        for i in range(0,k):
            solucion = vecinoMasCercanok(n,desde)
            # perturbation2(solucion)
            # OrOpt2k(solucion)
            b = solucion
            poblacion.append(b)
        mejores_generacion = []
        ####################
    
        lista_costos= []
        for i in poblacion:
            temp=[]
            temp.append(i)
            c = costoTotalk(i)
            temp.append(c)
            lista_costos.append(temp)
        solucion_costos = sorted(lista_costos, key=itemgetter(1))    
        poblacion=[]
        #####################
        #calcular fitness
        while g < iterMax:
            #seleccion
            nueva_poblacion= []
            # if g == 0:
            #     pass
            # else:
            #     lista_costos = []
            
     
            poblacion=[]
            
            for i in solucion_costos:
                poblacion.append(i[0])
                
            #cruzamiento
            for child1, child2 in zip(poblacion[::2], poblacion[1::2]):
                if random.random() < CXPB:
                    #pmx(child1,child2)
                    ox2(child1,child2)
                    #pmx(child1,child2)
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                else:
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                    
            #mutación
            for mutant in nueva_poblacion: #arreglar esto bien, problemas para reemplazar el mutante por el que ya estaba
                    if random.random() < MUTPB:
                        #anterior = copy.deepcopy(mutant)
                        revolver(mutant) 
                        #nueva_poblacion[nueva_poblacion.index(anterior)] = mutant
                        
            #reemplazamiento            
            poblacion = nueva_poblacion
            lista_costos = []
            #Mejor de la generación
            for i in poblacion:
                temp=[]
                temp.append(i)
                d = costoTotalk(i)
                temp.append(d)
                lista_costos.append(temp)
            solucion_costos = sorted(lista_costos, key=itemgetter(1))
            mejor_generacion = solucion_costos[0]
            mejores_generacion.append(mejor_generacion)
            #print(mejores_generacion)
            g = g + 1
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print(len(mejores_generacion))
        #print(mejor_semilla)
        elmejordelasemilla = sorted(mejores_generacion, key = itemgetter(1))[0][1]
        mejor_semilla = elmejordelasemilla
        mejor_semillas.append(mejor_semilla)
        suma_costos = suma_costos + mejor_semilla
        suma_tiempos = suma_tiempos + tiempo
        #print(mejor_semilla)
        #print("semilla: ",h,"costo:  ",mejor_semilla,"tiempo: ",round(tiempo,2))
    #print(a)
    minimos = sorted(mejor_semillas)[0]
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i
    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    #c3 = int(a[2])
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimos#minimo
    c7 = round(((minimos - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    fila.append(cdatos2)
    
def GA3(fila, ciudad, a, sumas, semillas = 10):
    #print(a)
    mejor_semillas = []
    n= len(ciudad)
    g = 0
    l = 0
    iterMax = 100
    CXPB, MUTPB= 0.9, 0.2
    suma_costos = 0
    suma_tiempos = 0
    #crear poblacion de x soluciones iniciales
    k = 100 #tamaño de poblacion
    for h in range(0,semillas):
        random.seed(h)
        inicioTiempo = time.time()
        g = 0
        poblacion= []
        desde = VecinoMasCercanoOpt(ciudad)
        #solucion = vecinoMasCercano(n,desde)
        
        for i in range(0,k):
            #desde = random.randint(0,n-1)
            solucion = vecinoMasCercano(n,desde)
            # perturbation2(solucion)
            # NodeShift2(solucion)
            
            b = solucion
            poblacion.append(b)
        
        # while l < ILS:
        #     i = 0
        #     for solucion in poblacion:
        #         anterior = solucion[:]
        #         CA = costoTotal(anterior)
        #         perturbation2(solucion)
        #         OrOpt2(solucion)
        #         CS = costoTotal(solucion)
        #         if CA < CS:
        #             poblacion[i] = anterior
        #             if CS == int(a[2]):
        #                 break
        #         i = i + 1
        #     l = l + 1
            
                
            
        mejores_generacion = []
        ####################
    
        lista_costos= []
        for i in poblacion: #ordenar segun el costoTotal
            temp=[]
            temp.append(i)
            c = costoTotal(i)
            temp.append(c)
            lista_costos.append(temp)
        solucion_costos = sorted(lista_costos, key=itemgetter(1))    
        poblacion=[]
        #####################
        #calcular fitness
        while g < iterMax:
            #seleccion
            nueva_poblacion= []
            # if g == 0:
            #     #lista_costos = []
            #     pass
            # else:
            #     lista_costos = []
            
     
            poblacion=[]
            
            for i in solucion_costos:
                poblacion.append(i[0])
                
            #cruzamiento
            for child1, child2 in zip(poblacion[::2], poblacion[1::2]):
                if random.random() < CXPB:
                    #pmx(child1,child2)
                    ox2(child1,child2)
                   #pmx(child1,child2)
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                else:
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                    
            #mutación
            for mutant in nueva_poblacion: #arreglar esto bien, problemas para reemplazar el mutante por el que ya estaba
                    if random.random() < MUTPB:
                        #anterior = copy.deepcopy(mutant)
                        revolver(mutant) 
                        #DosOpt(mutant)
                        #OrOpt2(mutant)
                        #nueva_poblacion[nueva_poblacion.index(anterior)] = mutant
                        
                        
            #reemplazamiento            
            poblacion = nueva_poblacion
            lista_costos= []
            #Mejor de la generación
            for i in poblacion:
                temp=[]
                temp.append(i)
                d = costoTotal(i)
                temp.append(d)
                lista_costos.append(temp)
            solucion_costos = sorted(lista_costos, key=itemgetter(1))
            mejor_generacion = solucion_costos[0]
            mejores_generacion.append(mejor_generacion)
            
            #print(mejores_generacion)
            if mejor_generacion[0][1] == a[2]:
                break
            
            g = g + 1
            
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print(mejor_semilla)
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print(mejor_semilla)
        elmejordelasemilla = sorted(mejores_generacion, key = itemgetter(1))[0][1]
        mejor_semilla = elmejordelasemilla
        mejor_semillas.append(mejor_semilla)
        suma_costos = suma_costos + mejor_semilla
        suma_tiempos = suma_tiempos + tiempo
        #print(mejor_semilla)
        #print("semilla: ",h,"costo:  ",mejor_semilla,"tiempo: ",round(tiempo,2))
    #print(a)
    minimos = sorted(mejor_semillas)[0]
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i
    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    #c3 = int(a[2])
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimos#minimo
    c7 = round(((minimos - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    
    fila.append(cdatos2)


def MIXTO2(fila, ciudad, a, sumas, semillas = 10):
#print(a)
    mejor_semillas = []
    n= len(ciudad)
    g = 0
    l = 0
    iterMax = 100
    ILS = 3
    CXPB, MUTPB= 0.9, 0.2
    suma_costos = 0
    suma_tiempos = 0
    #crear poblacion de x soluciones iniciales
    k = 100 #tamaño de poblacion
    for h in range(0,semillas):
        random.seed(h)
        inicioTiempo = time.time()
        g = 0
        poblacion= []
        desde = VecinoMasCercanoOptk(ciudad)
        #solucion = vecinoMasCercano(n,desde)
        
        for i in range(0,k):
            #desde = random.randint(0,n-1)
            solucion = vecinoMasCercanok(n,desde)
            perturbation2(solucion)
            NodeShift2k(solucion)
            
            b = solucion
            poblacion.append(b)
        
        while l < ILS:
            i = 0
            for solucion in poblacion:
                anterior = solucion[:]
                CA = costoTotalk(anterior)
                perturbation2(solucion)
                OrOpt2k(solucion)
                CS = costoTotalk(solucion)
                if CA < CS:
                    poblacion[i] = anterior
                    if CS == int(a[2]):
                        break
                i = i + 1
            l = l + 1
            
                
            
        mejores_generacion = []
        ####################
    
        lista_costos= []
        for i in poblacion: #ordenar segun el costoTotal
            temp=[]
            temp.append(i)
            c = costoTotalk(i)
            temp.append(c)
            lista_costos.append(temp)
        solucion_costos = sorted(lista_costos, key=itemgetter(1))    
        poblacion=[]
        #####################
        #calcular fitness
        while g < iterMax:
            #seleccion
            nueva_poblacion= []
            # if g == 0:
            #     #lista_costos = []
            #     pass
            # else:
            #     lista_costos = []
            
     
            poblacion=[]
            
            for i in solucion_costos:
                poblacion.append(i[0])
                
            #cruzamiento
            for child1, child2 in zip(poblacion[::2], poblacion[1::2]):
                if random.random() < CXPB:
                    #pmx(child1,child2)
                    ox2(child1,child2)
                    #pmx(child1,child2)
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                else:
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                    
            #mutación
            for mutant in nueva_poblacion: #arreglar esto bien, problemas para reemplazar el mutante por el que ya estaba
                    if random.random() < MUTPB:
                        #anterior = copy.deepcopy(mutant)
                        revolver(mutant) 
                        DosOptk(mutant)
                        #OrOpt2k(mutant)
                        #nueva_poblacion[nueva_poblacion.index(anterior)] = mutant
                        
                        
            #reemplazamiento            
            poblacion = nueva_poblacion
            lista_costos= []
            #Mejor de la generación
            for i in poblacion:
                temp=[]
                temp.append(i)
                d = costoTotalk(i)
                temp.append(d)
                lista_costos.append(temp)
            solucion_costos = sorted(lista_costos, key=itemgetter(1))
            mejor_generacion = solucion_costos[0]
            mejores_generacion.append(mejor_generacion)
            #print(mejores_generacion)
            if mejor_generacion[0][1] == a[2]:
                break
            
            g = g + 1
            
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print(mejor_semilla)
        #print(mejor_semilla)
        elmejordelasemilla = sorted(mejores_generacion, key = itemgetter(1))[0][1]
        mejor_semilla = elmejordelasemilla
        mejor_semillas.append(mejor_semilla)
        suma_costos = suma_costos + mejor_semilla
        suma_tiempos = suma_tiempos + tiempo
        #print(mejor_semilla)
        #print("semilla: ",h,"costo:  ",mejor_semilla,"tiempo: ",round(tiempo,2))
    #print(a)
    minimos = sorted(mejor_semillas)[0]
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i
    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    #c3 = int(a[2])
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimos#minimo
    c7 = round(((minimos - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    fila.append(cdatos2)

def MIXTO1(fila, ciudad, a, sumas, semillas = 10):
#print(a)
    mejor_semillas = []
    n= len(ciudad)
    g = 0
    l = 0
    iterMax = 100
    ILS = 3
    CXPB, MUTPB= 0.9, 0.2
    suma_costos = 0
    suma_tiempos = 0
    #crear poblacion de x soluciones iniciales
    k = 100 #tamaño de poblacion
    for h in range(0,semillas):
        random.seed(h)
        inicioTiempo = time.time()
        g = 0
        poblacion= []
        desde = VecinoMasCercanoOpt(ciudad)
        #solucion = vecinoMasCercano(n,desde)
        
        for i in range(0,k):
            #desde = random.randint(0,n-1)
            solucion = vecinoMasCercano(n,desde)
            perturbation2(solucion)
            NodeShift2(solucion)
            
            b = solucion
            poblacion.append(b)
        
        while l < ILS:
            i = 0
            for solucion in poblacion:
                anterior = solucion[:]
                CA = costoTotal(anterior)
                perturbation2(solucion)
                OrOpt2(solucion)
                CS = costoTotal(solucion)
                if CA < CS:
                    poblacion[i] = anterior
                    if CS == int(a[2]):
                        break
                i = i + 1
            l = l + 1
            
                
            
        mejores_generacion = []
        ####################
    
        lista_costos= []
        for i in poblacion: #ordenar segun el costoTotal
            temp=[]
            temp.append(i)
            c = costoTotal(i)
            temp.append(c)
            lista_costos.append(temp)
        solucion_costos = sorted(lista_costos, key=itemgetter(1))    
        poblacion=[]
        #####################
        #calcular fitness
        while g < iterMax:
            #seleccion
            nueva_poblacion= []
            # if g == 0:
            #     #lista_costos = []
            #     pass
            # else:
            #     lista_costos = []
            
     
            poblacion=[]
            
            for i in solucion_costos:
                poblacion.append(i[0])
                
            #cruzamiento
            for child1, child2 in zip(poblacion[::2], poblacion[1::2]):
                if random.random() < CXPB:
                    #pmx(child1,child2)
                    ox2(child1,child2)
                    #pmx(child1,child2)
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                else:
                    nueva_poblacion.append(child1)
                    nueva_poblacion.append(child2)
                    
            #mutación
            for mutant in nueva_poblacion: #arreglar esto bien, problemas para reemplazar el mutante por el que ya estaba
                    if random.random() < MUTPB:
                        #anterior = copy.deepcopy(mutant)
                        revolver(mutant) 
                        DosOpt(mutant)
                        #OrOpt2(mutant)
                        #nueva_poblacion[nueva_poblacion.index(anterior)] = mutant
                        
                        
            #reemplazamiento            
            poblacion = nueva_poblacion
            lista_costos= []
            #Mejor de la generación
            for i in poblacion:
                temp=[]
                temp.append(i)
                d = costoTotal(i)
                temp.append(d)
                lista_costos.append(temp)
            solucion_costos = sorted(lista_costos, key=itemgetter(1))
            mejor_generacion = solucion_costos[0]
            mejores_generacion.append(mejor_generacion)
            #print(mejores_generacion)
            if mejor_generacion[0][1] == a[2]:
                break
            
            g = g + 1
            
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        #print(mejor_semilla)
   
        #print(mejor_semilla)
        elmejordelasemilla = sorted(mejores_generacion, key = itemgetter(1))[0][1]
        mejor_semilla = elmejordelasemilla
        mejor_semillas.append(mejor_semilla)
        suma_costos = suma_costos + mejor_semilla
        suma_tiempos = suma_tiempos + tiempo
        #print(mejor_semilla)
        #print("semilla: ",h,"costo:  ",mejor_semilla,"tiempo: ",round(tiempo,2))
    #print(a)
    minimos = sorted(mejor_semillas)[0]
    c33 = list()
    for numero in range(len(a[1])-1,-1,-1):
        k = a[1][numero]
        if k == '0' or k == '1' or k == '2' or k == '3' or k == '4' or k == '5' or k == '6' or k == '7' or k == '8' or k == '9':
            c33.insert(0,k)
        
    c3 = ''       
    

    for i in c33:
        c3 = c3 + i
    c1 = int(a[0])#numero instancia
    c2 = str(a[1])#nombre instancia
    #c3 = int(a[2])
    c4 = int((n*(n-1))/2) #numero aristas
    c5 = int(a[2])#costo optimo
    c6 = minimos#minimo
    c7 = round(((minimos - int(a[2]))/int(a[2]))*100,2)#error relativo minimo
    c8 = round((suma_costos/semillas),2)#promedio
    c9 = round(((c8 - int(a[2]))/int(a[2]))*100,2)#error relativo promedio
    c10 = round((suma_tiempos/semillas),2)#tiempo promedio
    #print("Numero instancia: ",c1)
    #print("Nombre instancia: ",c2)
    #print("Costo optimo: ",c5)
    #print("Minimo: ",c6)
    #print("ERM: ",c7)
    #print("Promedio: ",c8)
    #print("ERP: ",c9)
    #print("Tiempo: ",c10)
    sumas.append(int(c3))
    sumas.append(int(c4))
    sumas.append(int(c5))
    sumas.append(int(c6))
    sumas.append(c7)
    sumas.append(c8)
    sumas.append(c9)
    sumas.append(c10)
    datos = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
    
    #cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia', 'costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    #salida = [cc1,cc2,cc5,cc6,cc7,cc8,cc9,cc10]
    #p = '       '
    #print(len(p))
    #cfinal = cc1 + p + cc2 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    #print(cfinal)
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print(fila_concatenada)
    #print(cdatos2)
    fila.append(cdatos2)

     
     
def main(fila,ciudad,i,k,algoritmo,sumas):
    #print(i)
    if k == 0:
        if algoritmo == 1:
            ILS(fila, ciudad,i,sumas)
        elif algoritmo == 2:
            GA3(fila, ciudad, i, sumas)
        else:
            MIXTO1(fila, ciudad, i, sumas)
    else: 
        if algoritmo == 1:
            ILS2(fila, ciudad,i, sumas)
        elif algoritmo == 2:
            GA4(fila, ciudad, i, sumas)
        else:
            MIXTO2(fila, ciudad, i, sumas)
     
    
if __name__ == "__main__":
    print("Bienvenido optimiza tu viaje 3.0: ")
    print("A continuación se presentan las alternativas para resolver las instancias de tu viaje: ")
    print(".Ingrese 1 para utilizar método ILS")
    print(".Ingrese 2 para utilizar método GA")
    print(".Ingrese 3 para utilizar método HÍBRIDO")
    while True:
        try:
            algoritmo = int(input("---------------> "))
            break
        except:
            print("Valor no válido! por favor ingrese las opciones disponibles.")
            
    
    
    archivo_salida=open('salidass.txt','w')
    cc1,cc2,cc3,cc4,cc5,cc6,cc7,cc8,cc9,cc10 = '#','instancia','|V|','|A|','costo óptimo', 'mínimo', 'ERM', 'promedio', 'ERP', 'tiempo'
    salida = [cc1,cc2,cc3,cc4,cc5,cc6,cc7,cc8,cc9,cc10]
    p = '       '
    p2 = ','
    #print(len(p))
    cfinal = cc1 + p + cc2 + p + cc3 + p + cc4 + p + cc5 + p + cc6 + p + cc7 + p + cc8 + p + cc9 + p + cc10
    cfinal2 = cc1 + p2 + cc2 + p2 + cc3 + p2 + cc4 + p2 + cc5 + p2 + cc6 + p2 + cc7 + p2 + cc8 + p2 + cc9 + p2 + cc10 
    #for i in cfinal:
    #    print (i)
    print(str(cfinal))
    archivo_salida.write(cfinal2)
    archivo_salida.write('\n')
    tipos_archivos = ['GEO', 'EXPLICIT', 'ATT', 'EUC_2D']
    tipos_archivo = [{'GEO': 0}, {'EXPLICIT': -1}, {'EXPLICIT': 0}, {'ATT': 0}, {'EUC_2D': 0}]
    lala = []
    SUMAS = []
    x = 0
    CONTADOR = 0
    for i in lineas:
        fila = list()
        entrada1 = 'instancias/'
        entrada2 = str(i[1])
        entrada3 = '.tsp'
        entrada = entrada1 + entrada2 + entrada3
        problem = tsplib95.load(str(entrada))
        ciudad = [i - 1   for i in list(problem.get_nodes())]
        #numero = len(list(problem.get_nodes()))
        #ciudad = [ i for i in range(1, numero + 1)]
        k = 0 #usa distancia1
        info = problem.as_keyword_dict()
        #print("instancia :",info['NAME']," primer indice: ",ciudad[0],ciudad[-1],", tipo: ",info['EDGE_WEIGHT_TYPE'])
        x = info['EDGE_WEIGHT_TYPE']
        #if  estaenlista({x:ciudad[0]}, tipos_archivo) == False:
        #    tipos_archivo.append({x:ciudad[0]})
        if {x: ciudad[0]} == {'EXPLICIT': -1}:
            ciudad = [i   for i in list(problem.get_nodes())]
            k = 1 #usa distancia2
        #print("instancia :",info['NAME']," primer indice: ",ciudad[0],ciudad[-1],", tipo: ",info['EDGE_WEIGHT_TYPE'])
        #if int(i[0]) == 3:
        #    break
        #print("--------------------------------------")
        # info = problem.as_keyword_dict()
        #print(ciudad)
        #if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D' and info['NAME'] == 'gr21':
        #if   info['NAME'] == 'st70':# or info['NAME'] == 'rat99':
        if k!=3:    #print("holaaaaaaa")
            #print(ciudad)
            #print(i)
            sumas = []
            main(fila,ciudad,i,k,algoritmo,sumas)#ILS OPCION 1
            #main() GA OPCION 2 #GA OPCION 2
            #main() mixto OPCION 3 #MIX OPCION 3
            #print(fila[0])
            
            lala.append(fila)
            SUMAS.append(sumas)
            #archivo_salida.write(fila[0])
            #archivo_salida.write('\n')
            
            print("--------------------------------------")
        else: 
            pass
        CONTADOR = CONTADOR + 1
        
    #  GUARDAR ARCHIVO CSV CON DATOS
    #print(tipos_archivo)
    #print(len(SUMAS))
    prom = [0,0,0,0,0,0,0,0,0]
    for instancias in SUMAS:
        cont = 0
        for i in instancias:
            prom[cont] = prom[cont] + i
            cont = cont + 1
    #print(prom)
    for i in prom:
        prom[prom.index(i)] = round((prom[prom.index(i)]/len(SUMAS)),2)
    #print(prom)
    datos = [prom[0],prom[1],prom[2],prom[3],prom[4],prom[5],prom[6],prom[7]]
    cdatos2 = ''
    cdatos = []
    cont = 0
    for columna in datos:
        coma = ','
        espacios = 7 - (len(str(columna)) - len(salida[cont]))
        p = ' '
        for i in range(espacios - 1):
            p = p + ' '
        cdatos.append(datos[cont])
        cdatos.append(p)
        if cont < (len(datos)-1):
            cdatos2 = cdatos2 + str(datos[cont]) + coma
        else:
            cdatos2= cdatos2 + str(datos[cont])
        cont = cont + 1
    
        
    #print(cdatos)
    fila_concatenada = ''
    for i in range(0,len(cdatos)):
        fila_concatenada = fila_concatenada + str(cdatos[i]) 
    
    print("Promedio                        ",fila_concatenada)
    for i in lala:
        archivo_salida.write(i[0])
        archivo_salida.write('\n')
    #print(cdatos2)
    cdatos2 = ' '+','+'Promedio'+','+cdatos2
    archivo_salida
    archivo_salida.write(cdatos2)
