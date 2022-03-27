# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:44:51 2020

@author: usuario
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:50:19 2020

@author: usuario
"""


import time
from collections import deque
import docplex.mp #Cplex
from docplex.mp.model import Model
#from arbol_normal2 import Arbol
#from arbol_normal2 import Nodo
from matplotlib import pyplot as plt 
import numpy as np
import copy
import random
import networkx as nx



#FUNCIONES CREADAS PARA FACILITAR LA LECTURA Y TRANSFORMACIÓN DE LOS DATOS
def posicion_lista(valor,lista): 
    posicion=0
    for i in lista:
        #print("valor actual: ",valor, " valor buscado: ",i)
        if valor==i:
            return posicion
        posicion=posicion+1
    return None
def funcion1(Linea_3f,subindices): # ASIGNA VALORES NEGATIVOS O POSITIVOS A LOS PARÁMETROS, 
    j=0                            #Y EN CASO DE QUE EL X_i NO TENGA ACOMPAÑANTE NUMÉRICO,SE INGRESA UN 1 A LA LISTA
    for i in Linea_3f:
        if i==Linea_3f[0] and type(i)!=type(1.5) and j==0: #primer elemento de la lista
            if i=='-' and type(Linea_3f[j+1])!=type(1.5):#que sea signo y el siguiente un x_i
                Linea_3f.insert(j+1,(-1))
            elif i=='-' and type(Linea_3f[1])==type(1.5):#que sea signo y el siguiente un numero 
                Linea_3f[j+1]=Linea_3f[j+1]*(-1)
            elif i!='-' and type(Linea_3f[j+1])!=type(1.5):#que sea x_i(equivale a un coeficiente de 1 positivo)
                Linea_3f.insert(j,1)
            else: 
                pass
            
                #Linea_3f[0]=i
        else:
            if posicion_lista(i, subindices)!=None:
                Linea_3f[j]=posicion_lista(i, subindices)
            if i=='+':
                if type(Linea_3f[j+1])!=type(1.5):
                    Linea_3f.insert(j+1,1)
                   
                else:
                    pass
            elif i=='-':
                if type(Linea_3f[j+1])!=type(1.5):
                    Linea_3f.insert(j+1,-1)
                else:
                    Linea_3f[j+1]=Linea_3f[j+1]*(-1)
                    
        j=j+1
    return Linea_3f


class Archivo:
    def __init__(self):
        #Entrada
        self.numero_variables=None
        self.tiempo_max=None
        self.max_min=None
        self.funcion_objetivo=None
        self.restricciones=None
        self.operadores=None
        #print("numero variables",self.numero_variables)
        
        #Salida
        self.nodos=None
        self.tiempo=None
        self.optimo=None
        self.soluciones_optimo=None
    
        #Tiempo ejecución
        self.tiempo=None
    def leer(self,txt):
        inicio=time.time()
        Archivo=open(str(txt),"r")
        #NUMERO VARIABLES Y TIEMPO MAXIMO                    ---------->LINEA 1
        Linea_1=Archivo.readline().split()
        #Numero_variables=int(Linea_1[0])
        
        #Tiempo_max=int(Linea_1[1])
        #MAXIMIZAR O MINIMIZAR                                -------->LINEA 2
        Linea_2=Archivo.readline()                           
        
        #INICIO TRANSFORMACION DE LOS DATOS(FUNCION OBJETIVO) -------->LINEA 3
        Linea_3=Archivo.readline().split()
        Linea_3f=[Linea_3[i] for i in range(1,len(Linea_3))]
            
        #SUBINDICES DE VARIABLES ORIGINALES, SIN REPETIRSE
        subindices=[]
        m=0
        for i in Linea_3f:
            while True :
                try :
                    i=float(i)
                    #i=int(i)
                    Linea_3f[m]=i
                    interruptor=True 
                    break
                except :
                    interruptor=False
                    break
            #print(interruptor)
            #if i=='+':
             #   Linea_3f[m-1]=Linea_3f[m-1].split()
              #  print(Linea_3f[m-1])
                
            m=m+1
        for i in Linea_3f:
            if type(i)!=type(1.5) and i!='+' and i!='-':
                subindices.append(i)
        #print("SUBINDICES FO: ",subindices)    
        j=0  
        #INICIO TRANSFORMACION DATOS FUNCION OBJETIVO
        Linea_3f=funcion1(Linea_3f,subindices)
        for i in Linea_3f:
            if i=='+' or i=='-':
                Linea_3f.remove(i)
        
        j=0
        for i in Linea_3f:
            if j%2!=0:
                Linea_3f[j]=posicion_lista(i, subindices)
        #FIN TRANSFORMACIÓN A LOS DATOS(FUNCION OBJETIVO)  -------->LINEA 4
        #MAXIMIZAR O MINIMIZAR                             
        Linea_4=Archivo.readline()
        
        #INICIO TRANSFORMACIÓN DE LOS DATOS(RESTRICCIONES) -------->LINEA 5 HACIA ABAJO
        Linea_5=Archivo.readlines()
        Linea_o=[]
        j=0
        for lineas in Linea_5:
            Linea_5[j]=lineas.split()
            Linea_5[j].pop(0)
            Linea_o.append(Linea_5[j].pop(-2))
            j=j+1
        for i in Linea_5:
            m=0
            for linea in i:
                while True :
                    try :
                        linea=float(linea)
                        i[m]=linea
                        interruptor=True 
                        break
                    except :
                        interruptor=False
                        break
                m=m+1       
        #cont=0 
        for linea in Linea_5:
            for i in linea:
                if type(i)!=type(1.5) and i!='+' and i!='-' and posicion_lista(i, subindices)==None:
                    subindices.append(i)
        #print("SUBINDICES FO: ",subindices)
        i=0      
        for lineas in Linea_5:
            Linea_5[i]=funcion1(Linea_5[i],subindices)
            i=i+1   
        for lineas in Linea_5:
            for i in lineas:
                if i=='+' or i=='-':
                    lineas.remove(i)
        for lineas in Linea_5:
            j=0
            for i in lineas:
                if j%2!=0:
                    lineas[j]=posicion_lista(i, subindices)
            
        #FIN TRANSFORMACIÓN DE LOS DATOS(RESTRICCIONES) ------------------>FINAL LINEAS
                    
        #DATOS PARA CPLEX                              ------------------->PARÁMETROS PARA RESOLVER PL
        numero_variables=int(Linea_1[0])
        tiempo_max=int(Linea_1[1])
        max_min=Linea_2
        funcion_objetivo=Linea_3f
        restricciones=Linea_5
        
        final=time.time()
        
        #print(numero_variables)
        #print(tiempo_max)
        #print(max_min)
        #print(funcion_objetivo) 
        #print(restricciones)
        self.numero_variables=numero_variables
        self.tiempo_max=tiempo_max
        self.max_min=max_min
        self.funcion_objetivo=funcion_objetivo
        self.restricciones=restricciones
        self.operadores=Linea_o
        
        self.tiempo=round(final-inicio,5)
    def guardar(self,arbol):
        if arbol.nodo!=None:
            nodos_recorridos=arbol.nodos_recorridos
            cota=arbol.nodo.valorfo
            tiempo=arbol.tiempo
            guardar_archivo=open("salidas.txt","w")
            guardar_archivo.write('Nodos :'+str(nodos_recorridos))
            guardar_archivo.write('\n')
            guardar_archivo.write('Tiempo: '+str(tiempo))
            guardar_archivo.write('\n')
            guardar_archivo.write("Fobjetivo: "+str(int(cota)))
            guardar_archivo.write('\n')
          
            solucion_final=arbol.nodo.soluciones
            n=0
            for i in solucion_final:
                if i==1:
                    
                    guardar_archivo.write("x_"+str(n)+" = "+str(int(i)))
                    guardar_archivo.write('\n')
                    n=n+1
                else:
                    pass
        else:
            nodos_recorridos=arbol.nodos_recorridos
            #cota=arbol.nodo.valorfo
            tiempo=arbol.tiempo
            guardar_archivo=open("salidas.txt","w")
            guardar_archivo.write('Nodos :'+str(nodos_recorridos))
            guardar_archivo.write('\n')
            guardar_archivo.write('Tiempo: '+str(tiempo))
            guardar_archivo.write('\n')
            guardar_archivo.write("Fobjetivo: Infactible")
            guardar_archivo.write('\n')
            
        guardar_archivo.close()
        

class Nodo:
    def __init__(self,archivo,valorbin=None,pos=None):
        
        #Punteros
        self.anterior=None
        self.izquierda=None
        self.derecha=None
        
        #Identificador nodo
        self.id=None
        self.nivel=0
        #Valor binario,junto con su variable asociada(posicion de x, ej x[2]=1)
        self.bin=valorbin
        self.pos=pos
        #Entrada cplex
        
        #self.lista_binaria=lista_bin#Nuevas restricciones
        self.numero_variables=archivo.numero_variables
        self.tiempo_max=archivo.tiempo_max
        self.max_min=archivo.max_min
        self.funcion_objetivo=archivo.funcion_objetivo
        self.restricciones=archivo.restricciones
        self.operadores=archivo.operadores
        
        #Resultados cplex
        self.factibilidad=None
        self.valorfo=None
        self.soluciones=None
        self.estado=None
        self.cplex=None
        self.soluciondisplay=None
        
    def __iter__ ( self ) :
        #print("izquierda")
        if self.izquierda != None :
            for i in self.izquierda :
                yield i

        yield self . info
        #print("derecha")
        if self . derecha != None :
            for elem in self . derecha :
                yield elem
        
        
           
    def resolver_pl(self,lista_binaria=None):
        
        #lista_binaria=self.lista_binaria
        n=self.numero_variables
        tiempo_max=self.tiempo_max
        max_min=(self.max_min).split()[0]
        FO=self.funcion_objetivo
        REST=self.restricciones
        operadores=self.operadores
        #print("MAX MIN: ",len(max_min))        
        modelo=Model('modelo') #nombre del modelo
        
        x = modelo.continuous_var_list(n,name='x')
        
        
        if max_min=='Maximizar':
            modelo.maximize(modelo.sum(x[FO[j+1]]*FO[j] for j in range(0,len(FO)-1,2)))
        else: 
            modelo.minimize(modelo.sum(x[FO[j+1]]*FO[j] for j in range(0,len(FO)-1,2)))
        k=0
        for restricciones in REST:
            if operadores[k]=='<=':
                modelo.add(modelo.sum(x[restricciones[i+1]]*(restricciones[i]) for i in range(0,len(restricciones)-2,2))<=restricciones[-1])
            elif operadores[k]=='>=':
                modelo.add(modelo.sum(x[restricciones[i+1]]*(restricciones[i]) for i in range(0,len(restricciones)-2,2))>=restricciones[-1])
            elif operadores[k]=='<':
                modelo.add(modelo.sum(x[restricciones[i+1]]*(restricciones[i]) for i in range(0,len(restricciones)-2,2))<restricciones[-1])
            elif operadores[k]=='>':
                modelo.add(modelo.sum(x[restricciones[i+1]]*(restricciones[i]) for i in range(0,len(restricciones)-2,2))>restricciones[-1])
            elif operadores[k]=='=' or operadores[k]=='==':
                modelo.add(modelo.sum(x[restricciones[i+1]]*(restricciones[i]) for i in range(0,len(restricciones)-2,2))==restricciones[-1])
            k=k+1  
            
        #if lista_binaria:
            #print("tamaño lista binaria:",len(lista_binaria))
        if lista_binaria:  
            for i in range(0,len(lista_binaria)):
                #print("posicion lista binaria, ",i)
                #print("valor lista binaria: ",lista_binaria[i])
                #print("lista_binaria[i]!='vacio'",lista_binaria[i]!='vacio')
                if lista_binaria[i]!='vacio':
                    modelo.add_constraint(x[i]==lista_binaria[i])
                    #print("x_",str(i),"= ","b_",str(i)," = ",lista_binaria[i])
        
        for i in range(0,n):
            modelo.add_constraint(x[i]<=1)
            modelo.add_constraint(x[i]>=0)
            
            
        #modelo.add(modelo.sum(x[i]*1 for i in range(0,self.m))==1)
        cplex=modelo.export_to_string()
        #print(cplex)

        #modelo.print_information()
        solucion = modelo.solve(log_output=False)
        estado = modelo.get_solve_status()
        if solucion:
            #i=solucion.display()
            fo=solucion.get_objective_value()
            solutions=[x[i].solution_value for i in range(0,n)]
           
           # print("--------------Iteración x---------------")
            #print("Estado: ",estado)
            #print("FO=",fo,end= "")
            #for i in range(0,n):
             #   x='x'+str(i+1)
              #  print(", ",x,"=" ,solutions[i],end= "")
                #print(" binaria: ",solutions[2])
            interruptor=True
            
            self.factibilidad=interruptor
            self.valorfo=fo
            self.soluciones=solutions
            self.estado=estado
            self.lista_binaria=lista_binaria
            self.cplex=cplex
            #self.soluciondisplay=solucion.display()
         
        else: 
            #print("Estado: ",estado)
            interruptor=False
            self.factibilidad=interruptor
            self.estado=estado
        
   

class Arbol1:
    def __init__(self):
        #Raiz del árbol creado
        self.raiz=None
        
        #Información del Nodo con la solución óptima
        self.nodo=None #puntero al nodo óptimo
        self.nodos_recorridos=None
        self.lista_nodosrecorridos=None
        #Tiempo ejecución
        self.tiempo=None
        #self.optimo=self.nodo.valorfo
        #self.solucion=self.nodo.soluciones
        #self.recorrido=None
        #self.cplex=self.nodo.cplex
    def max_coef(self,soluciones,fo): #variable no binaria dentro de las solución con mayor coef en F.O.
        max_valor=None
        pos=-1
        
        
        for i in range(0,int(len(fo)/2)):#Caso en que la variable se encuentra en la F.O.
            if soluciones[i]!=0 and soluciones[i]!=1:#solucion no binaria,se ramifica
                for j in range(1,len(fo),2):#se busca coef en funcion objetivo
                    if i==fo[j]:
                        coef=fo[j-1]
                        #print("coeficiente: ",coef)
                        #print("Maximo valor: ",max_valor)
                        if max_valor==None:
                            max_valor=coef
                            pos=i
                            
                        elif max_valor!=None and coef>max_valor:
                            #print("coeficiente: ",coef,"maximo valor: ",max_valor)
                            max_valor=coef
                            #print("coeficiente: ",coef,"maximo valor: ",max_valor)
                            pos=i
                            break
        for i in range(int(len(fo)/2),len(soluciones)):#Caso en que la variable no se encuentra en la F.O.
            if soluciones[i]!=0 and soluciones[i]!=1:#solucion no binaria, se ramifica
                pos=i
                break
        if pos==-1:
            return None
        else:
            return pos      
    def min_coef(self,soluciones,fo):#variable no binaria dentro de las solución con mayor coef en F.O.
        max_valor=None
        pos=-1
        
        
        for i in range(0,int(len(fo)/2)):#Caso en que la variable se encuentra en la F.O.
            if soluciones[i]!=0 and soluciones[i]!=1:#solucion no binaria,se ramifica
                for j in range(1,len(fo),2):#se busca coef en funcion objetivo
                    if i==fo[j]:
                        coef=fo[j-1]
                        #print("coeficiente: ",coef)
                        #print("Maximo valor: ",max_valor)
                        if max_valor==None:
                            max_valor=coef
                            pos=i
                            
                        elif max_valor!=None and coef<max_valor:
                            #print("coeficiente: ",coef,"maximo valor: ",max_valor)
                            max_valor=coef
                            #print("coeficiente: ",coef,"maximo valor: ",max_valor)
                            pos=i
                            break
        for i in range(int(len(fo)/2),len(soluciones)):#Caso en que la variable no se encuentra en la F.O.
            if soluciones[i]!=0 and soluciones[i]!=1:#solucion no binaria, se ramifica
                pos=i
                break
        if pos==-1:
            return None
        else:
            return pos      
    def primer_coef(self,soluciones):#primera variable no binaria dentro de la solución 
        pos=-1
        for i in range(0,len(soluciones)):
            if soluciones[i]!=0 and soluciones[i]!=1:#primera variable no binaria
                pos=i
        if pos==-1:
            return None
        else:
            return pos
                
    def __agregar_izquierda(self,nodo_padre,nodo_hijo):
        
        nodo_padre.izquierda=nodo_hijo
        nodo_padre.izquierda.anterior=nodo_padre
        nodo_padre.izquierda.nivel=nodo_padre.nivel+1
        nodo_padre.izquierda.lista_binaria=nodo_padre.lista_binaria
        return nodo_hijo
    
    def __agregar_derecha(self,nodo_padre,nodo_hijo):
        
        nodo_padre.derecha=nodo_hijo
        nodo_padre.derecha.anterior=nodo_padre
        nodo_padre.derecha.nivel=nodo_padre.nivel+1
        nodo_padre.derecha.lista_binaria=nodo_padre.lista_binaria
        return nodo_hijo
    def __generarlistabinaria(self,aux,lista_binaria):
        while aux:#Se genera la lista de restricciones con la información de los nodos anteriores(No pude hacer que se guardaran estas lista como atributos en los nodos)
            if aux.bin!=None and aux.pos!=None:#A esta lista le falta la restricción del nodo al se ramificará
                lista_binaria[aux.pos]=aux.bin
            else:
                break
            aux=aux.anterior
        return lista_binaria
    def __generarvacia(self,nodo_actual,lista_binaria):
        for i in range(0,nodo_actual.numero_variables):
                lista_binaria.append('vacio')
        return lista_binaria
    def __guardarencola(self,nodo,cola):
        #print("aloalaolalooooooooooooooooooo")
        if nodo.max_min.split()[0]=='Maximizar':
            for i in range(len(cola)-1,-1,-1):
             #   print("lalalallalla",nodo.valorfo,cola[i].valorfo)
                if nodo.valorfo<cola[i].valorfo:
                    if i==(len(cola)-1):#ultima posicion en la cola
                        cola.append(nodo)
                        break
                    else:
                        cola.insert(i+1,nodo)
                        break
                else:
                    if i==0:
                        cola.insert(i,nodo)
                        break
        else:       
            for i in range(len(cola)-1,-1,-1):
             #   print("lalalallalla",nodo.valorfo,cola[i].valorfo)
                if nodo.valorfo>cola[i].valorfo:
                    if i==(len(cola)-1):#ultima posicion en la cola
                        cola.append(nodo)
                        break
                    else:
                        cola.insert(i+1,nodo)
                        break
                else:
                    if i==0:
                        cola.insert(i,nodo)
                        break
                
    def __maximizar(self,archivo):
        inicio=time.time()
        cola=list()
        nodos_recorridos=list()
        contador_nodos=1
        cola.append(Nodo(archivo))
        nodo_actual=cola[0]
        self.raiz=nodo_actual
        numero_cambioscota=0
        arcos=[]
        idnodos=0
        cota=0
        lista_binaria=[]
        nodo_actual.id=idnodos
        nodos_recorridos.append(nodo_actual)
        nodo_actual.resolver_pl()
        while cola:
            #self.__burbuja(cola)
            self.nodos_recorridos=contador_nodos
        
            nodo_actual=cola[0]
            lista_binaria=[]
            lista_binaria=self.__generarvacia(nodo_actual,lista_binaria)
            aux=nodo_actual
            lista_binaria=self.__generarlistabinaria(aux,lista_binaria)#agregar restricciones de nodos anteriores
            nodo_actual.id=contador_nodos
           
            #nodo_actual.resolver_pl(lista_binaria)
        
            #print("FO ",nodo_actual.valorfo)
            #print("COTA ",cota)
            #print("tamaño cola",len(cola))
            #print("factibilidad ",nodo_actual.factibilidad)
            #print("Nivel ",nodo_actual.nivel)
            if nodo_actual.factibilidad==True:
            
            #for i in nodo_actual.soluciones:
                #print("LISTA BINARIA: ",nodo_actual.lista_binaria)
                #print("SOLUCIONES: ",nodo_actual.soluciones)
                if self.max_coef(nodo_actual.soluciones,nodo_actual.funcion_objetivo)!=None:#Primera solución no binaria, se ramifica su respectiva variable    
                    max_coef=self.max_coef(nodo_actual.soluciones,nodo_actual.funcion_objetivo)
                   
                    if nodo_actual.valorfo>cota or numero_cambioscota==0:
                       
                        if nodo_actual.bin!=None: #se excluye solo el primero caso, es decir, la raiz no incluye restricciones adicionales
                            lista_binaria[nodo_actual.pos]=nodo_actual.bin
                        
                        lista_binaria[max_coef]=1
                        nodo_derecha=self.__agregar_derecha(nodo_actual,Nodo(archivo,1,max_coef))
                        nodo_derecha.resolver_pl(lista_binaria)
                        
                        
                        
                        #lista_binaria=self.__generarvacia(nodo_actual,lista_binaria)
                        #aux=nodo_actual
                        #lista_binaria=self.__generarlistabinaria(aux,lista_binaria)
    
                        
                        lista_binaria[max_coef]=0
                        nodo_izquierda=self.__agregar_izquierda(nodo_actual,Nodo(archivo,0,max_coef))
                        nodo_izquierda.resolver_pl(lista_binaria)
                        #print("")
                        #print("--------------------------------------")
                        #print("VALOR DERECHA, VALOR IZQUIERDA",nodo_derecha.valorfo,nodo_izquierda.valorfo)
                        #print("-----------------------------------------------------")
                        nodo_actual.id=idnodos
                        idnodos=idnodos+1
                        nodo_derecha.id=idnodos
                        nodos_recorridos.append(nodo_derecha)
                        
                        
                        idnodos=idnodos+1
                        nodo_izquierda.id=idnodos
                        
                        arcos.append((nodo_actual.id,nodo_derecha.id))
                        arcos.append((nodo_actual.id,nodo_izquierda.id))
                        nodos_recorridos.append(nodo_izquierda)
                        if nodo_derecha.factibilidad==True and nodo_izquierda.factibilidad==True:
                            if nodo_derecha.valorfo>nodo_izquierda.valorfo:#Se prioriza al nodo con mayor valor de la funcion objetivo
                                self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                                self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                            elif nodo_derecha.valorfo<=nodo_izquierda.valorfo:
                                self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                                self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                            
                        
                        elif nodo_derecha.factibilidad==True and nodo_izquierda.factibilidad==False :
                            self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                           
                        elif nodo_derecha.factibilidad==False and nodo_izquierda.factibilidad==True :
                            self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                            
                            
                            
                        
                    else:
                        #print("SOLUCION NO BINARIA Y VALOR FO NO SIRVE, NO SE RAMIFICA")
                        pass
                        
                else:#Todas las soluciones fueron binarias
                    #print("---------------SOLUCION BINARIA-------------------- ",nodo_actual.soluciones[a]!=1 and nodo_actual.soluciones[a]!=0)
                    #print(" ---------------------------------------------- ")
                    if nodo_actual.valorfo>cota or numero_cambioscota==0: 
                        cota=nodo_actual.valorfo
                        self.nodo=nodo_actual
                        numero_cambioscota=numero_cambioscota+1
                #else:
                    #print("---------------SOLUCION BINARIA--------------------  False")
                    #print(" ---------------------------------------------- ")
                 
            else:
                pass
            contador_nodos=contador_nodos+1
            #print("-----------------------------")
            #print("TAMAÑO COLA: ",len(cola))
            #print("-----------------------------")
            finali=time.time()
            tiempoo=round(finali-inicio,5)
            if tiempoo>=float(archivo.tiempo_max):
                self.tiempo=tiempoo
                self.lista_nodosrecorridos=len(nodos_recorridos)-1
                break
            else:
                pass
            cola.remove(nodo_actual)
        
        
        print("nodos recorridos",len(nodos_recorridos))
        self.nodos_recorridos=len(nodos_recorridos)
        self.lista_nodosrecorridos=len(nodos_recorridos)-1
        self.tiempo= tiempoo
        print("dsafas",arcos)
        self.dibujar(len(nodos_recorridos)-1,arcos)
     
        
        
  
        
        
        
        
        
    def __minimizar(self,archivo):
        inicio=time.time()
        nodos_recorridos=list()
        cola=list()
        arcos=[]
        contador_nodos=1
        cola.append(Nodo(archivo))
        nodo_actual=cola[0]
        nodos_recorridos.append(nodo_actual)
        self.raiz=nodo_actual
        numero_cambioscota=0
        idnodos=0
        cota=0
        lista_binaria=[]
        nodo_actual.resolver_pl()
        while cola:
            self.nodos_recorridos=len(nodos_recorridos)
            nodo_actual=cola[0]
            lista_binaria=[]
            lista_binaria=self.__generarvacia(nodo_actual,lista_binaria)
            aux=nodo_actual
            lista_binaria=self.__generarlistabinaria(aux,lista_binaria)#agregar restricciones de nodos anteriores
            nodo_actual.id=contador_nodos
        
            #nodo_actual.resolver_pl(lista_binaria)
            #print("FO ",nodo_actual.valorfo,",factibilidad: ",nodo_actual.factibilidad)
            #print("COTA ",cota)
            #print("tamaño cola",len(cola))  
            #print("solucion binaria: ",self.primer_coef(nodo_actual.soluciones)==None)
            if nodo_actual.factibilidad==True:
            #a=0
            #for i in nodo_actual.soluciones:
                #print("LISTA BINARIA: ",nodo_actual.lista_binaria)
                #print("SOLUCIONES: ",self.min_coef(nodo_actual.soluciones,nodo_actual.funcion_objetivo))
                if self.primer_coef(nodo_actual.soluciones)!=None:#Primera solución no binaria, se ramifica    
                    min_coef=self.min_coef(nodo_actual.soluciones,nodo_actual.funcion_objetivo)
                    #print("---------------SOLUCION BINARIA-------------------- ",nodo_actual.soluciones[a]!=1 and nodo_actual.soluciones[a]!=0)
                    #print(" ---------------------------------------------- ")
                    if numero_cambioscota==0 or (nodo_actual.valorfo<cota):
                        #for i in range(0,nodo_actual.numero_variables):
                        if nodo_actual.bin!=None: 
                            lista_binaria[nodo_actual.pos]=nodo_actual.bin#restriccion de la variable actual del nodo
                        
                            #print("")
                            #print("lista binaria actual: ",lista_binaria)
                            
                        lista_binaria[min_coef]=1#restriccion de la variable del nodo hijo derecha
                        nodo_derecha=self.__agregar_derecha(nodo_actual,Nodo(archivo,1,min_coef))
                        nodo_derecha.resolver_pl(lista_binaria)
                    
                    
                    
                        #lista_binaria=self.__generarvacia(nodo_actual,lista_binaria)
                        #aux=nodo_actual
                        #lista_binaria=self.__generarlistabinaria(aux,lista_binaria)

                        #print("aloooooooooo")
                        lista_binaria[min_coef]=0#restriccion de la variable del nodo hijo izquierda
                        nodo_izquierda=self.__agregar_izquierda(nodo_actual,Nodo(archivo,0,min_coef))
                        nodo_izquierda.resolver_pl(lista_binaria)
                        #print("lista binaria izquierda: ",lista_binaria)
                        #cola.append(nodo_izquierda)
                        nodo_actual.id=idnodos
                        idnodos=idnodos+1
                        nodo_derecha.id=idnodos
                        nodos_recorridos.append(nodo_derecha)
                        
                        
                        idnodos=idnodos+1
                        nodo_izquierda.id=idnodos
                        
                        arcos.append((nodo_actual.id,nodo_derecha.id))
                        arcos.append((nodo_actual.id,nodo_izquierda.id))
                        nodos_recorridos.append(nodo_izquierda)
                        
                        
                        #print("nodos recorridos",nodos_recorridos)
                        #print("wola",nodo_derecha.factibilidad==True and nodo_izquierda.factibilidad==True)
                        if nodo_derecha.factibilidad==True and nodo_izquierda.factibilidad==True:
                            if nodo_derecha.valorfo<nodo_izquierda.valorfo:#Se prioriza al nodo con mayor valor de la funcion objetivo
                                self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                                self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                                
                                #cola.append(nodo_izquierda)
                                #cola.append(nodo_derecha)
                                #cola.append(nodo_izquierda)
                               # print("tamaño cola",len(cola))
                            elif nodo_derecha.valorfo>=nodo_izquierda.valorfo:
                                self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                                self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                               # print("tamaño cola",len(cola))
                        
                        elif nodo_derecha.factibilidad==True and nodo_izquierda.factibilidad==False :
                            self.__guardarencola(nodo_derecha,cola)#cola.append(nodo_derecha)
                           
                        elif nodo_derecha.factibilidad==False and nodo_izquierda.factibilidad==True :
                            self.__guardarencola(nodo_izquierda,cola)#cola.append(nodo_izquierda)
                            
                        
                    else :
                        #print("SOLUCION NO BINARIA Y VALOR FO NO SIRVE, NO SE RAMIFICA")
                        pass
                        
                else:#Todas las soluciones fueron binarias
                    #print("---------------SOLUCION BINARIA-------------------- ",nodo_actual.soluciones[a]!=1 and nodo_actual.soluciones[a]!=0)
                    #print(" ---------------------------------------------- ")
                    if nodo_actual.valorfo<cota or numero_cambioscota==0: 
                        cota=nodo_actual.valorfo
                        self.nodo=nodo_actual
                        numero_cambioscota=numero_cambioscota+1
                #else:
                    #print("---------------SOLUCION BINARIA--------------------  False")
                    #print(" ---------------------------------------------- ")
                #a=a+1    
            else:
                pass
            contador_nodos=contador_nodos+1
            #print("-----------------------------")
            #print("TAMAÑO COLA: ")
            #print("-----------------------------")
            finali=time.time()
            tiempoo=round(finali-inicio,5)
            if tiempoo>=float(archivo.tiempo_max):
                self.tiempo=tiempoo
                self.lista_nodosrecorridos=len(nodos_recorridos)-1
                
                break
            else:
                pass
            cola.remove(nodo_actual)
      
        
        final=time.time()
        self.tiempo=tiempoo
        self.lista_nodosrecorridos=len(nodos_recorridos)-1
        #lista=self.arbol(self.lista_nodosrecorridos)
        #self.dibujar(nodos_recorridos,len(lista))
        print("dsafas",arcos)
        self.dibujar(len(nodos_recorridos)-1,arcos)
        
    
            
            
            
        
    def dibujar (self,numero,ver):
        G = nx.Graph()
        for i in range (numero):
            G.add_node(i+1)
        G.add_edges_from(ver)
        nx.draw(G, with_labels=1,node_size=1000)
        plt.show()    
    
                
        
    
        
    
    def branch_bound(self,archivo):
        
        #print(archivo.max_min.split()[0]=='Maximizar')
        #print(archivo.max_min.split()[0]=='Minimizar')
        if archivo.max_min.split()[0]=='Maximizar':
            self.__maximizar(archivo)
            #print("alooooooooo MAXIMIZAR")
        elif archivo.max_min.split()[0]=='Minimizar':
            self.__minimizar(archivo)
            #print("alooooooooo MINIMIZAR")
    
        
        
    def recorrer_nivel(self):
        #print("arbol.raiz es distinto de None?: ",self.raiz!=None)
        return self.__recorrer_nivel(self.raiz)
    
    def __recorrer_nivel(self,nodo):
        if nodo is None:
            return

        cola = deque()
        cola.append(nodo)
        #print("arbol.raiz es distinto de None?: ",self.raiz!=None)
        #print("arbol.raiz es distinto de None?: ",cola[0]!=None)
        while cola:
            #print(cola)
            #print(cola[0].info)
            nodo=cola[0]
            if nodo.derecha is not None:
                cola.append(nodo.derecha)
                
            if nodo.izquierda is not None:
                cola.append(nodo.izquierda)
        
            if cola[0].anterior!=None:
                aux=cola[0]
                #print("aux es distinto de None?: ",aux!=None)
                #print("aux es : ",aux.bin)
                print("------------------------")
                print("Restricciones adicionales")
                while aux.bin!=None:
                    
                    print(" x",aux.pos,"= "," ",aux.bin,end=" ,")
                    aux=aux.anterior
                print("")
                
                if cola[0].factibilidad==True:
                    interruptor=True
                    for i in cola[0].soluciones:
                        if i!=1 and i!=0:
                            print("Solución NO binaria")
                            interruptor=False
                            break
                    if interruptor==True:   
                        print("Solución binaria")
                    pos=0
                    for i in cola[0].soluciones:
                        print("x"+str(pos),"= ",i)
                        pos=pos+1
                   
                else:
                    print("No factible")
                
                print("nodo: ",cola[0].id," nivel: ",cola[0].nivel,", valor fo: ",cola[0].valorfo,", nodo anterior: ",cola[0].anterior.id,", valor fo: ",cola[0].anterior.valorfo)
                
                cola.popleft()
            else:
                
                aux=cola[0]
                print("Sin restricciones adicionales")
                if cola[0].factibilidad==True:
                    interruptor=True
                    for i in cola[0].soluciones:
                        if i!=1 and i!=0:
                            print("Solución NO binaria")
                            interruptor=False
                            break
                    if interruptor==True:   
                        print("Solución binaria")
                    pos=0
                    for i in cola[0].soluciones:
                        print("x"+str(pos),"= ",i)
                        pos=pos+1
                else:
                    print("No factible")
                print("nodo raiz: ",cola[0].id," nivel: ",cola[0].nivel,", valor fo : ",cola[0].valorfo,", nodo anterior: ")
                cola.popleft()

#FUNCIONAMIENTO
archivo=Archivo()
archivo.leer("entrada_0.txt")
#print("Numero variables: ",archivo.numero_variables)
#print("Tiempo maximo: ",archivo.tiempo_max)
#print("Maximizar o Minimizar: ",archivo.max_min)
#print("Funcion objetivo: ",archivo.funcion_objetivo)
#print("Restricciones: ",archivo.restricciones)


arbol=Arbol1()
arbol.branch_bound(archivo)
if arbol.nodo==None:
    print("Sin Solución")
else:
    print("solucion",arbol.nodo.cplex)
    print(arbol.nodo.valorfo)
    #print(arbol.nodo.soluciones)

archivo.guardar(arbol)
if arbol.nodo!=None:
    print("-------------------------")
    print("Nodos :",arbol.nodos_recorridos)
    print("Tiempo: ",arbol.tiempo)
    print("Fobjetivo: ",arbol.nodo.valorfo)
    #print(arbol.nodo.soluciondisplay)
    a=0
    for i in arbol.nodo.soluciones:
        print("x"+str(a)+"="+str(i),end="  ")
        a=a+1
else:
    print("-------------------------")
    print("Nodos : ")
    print("Tiempo: ")
    print("Fobjetivo: ")
    
print("-------------------------")
#print("arbol.raiz es distinto de None?: ",arbol.raiz!=None)
print("-------------------------")
#arbol.recorrer_nivel()    
    
print("TIEMPO: ",arbol.tiempo)   