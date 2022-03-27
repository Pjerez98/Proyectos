# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:52:53 2022

@author: usuario
"""
import math
import matplotlib.pyplot as plt




def leer_archivo(name,ps):
  import pickle
  solutions = []
  #ps = '/content/drive/MyDrive/MT/Código_simulación/Resultados_simulacion'
  #name = ['B','MP']
  for nam in name:
        with open(ps + "/{}.pickle".format(nam), "rb") as f:
            obj = pickle.load(f)
            solutions.append(obj)
  return solutions

n_replicas = 1
from tqdm import tqdm
def calcular_personas_sistema(X,Y,string):

          num_prom = []

          def get_indexes(ls,index):
            return [i for i in range(len(ls)) if ls[i] == index]

          for y in tqdm(list(set(Y))):
              
            tpo = 0
            indices = get_indexes(Y,y)
            for i in indices:
 
              if X[i] != X[-1]:

                tpo += X[i+1] - X[i]
                #if tpo == 0:
                #  print(X[i+1],X[i])
            vv = (y,tpo/X[-1])
            num_prom.append(vv)

          #print(num_prom)
          num_prom = sum([a*b for a,b in num_prom])
          #print("Ultimo numero {} {}".format(string,Y[-1]))
          print("Número promedio {} en el sistema: {}".format(string,num_prom))
          return num_prom

def calcular_tiempo_promedio_y_acumulado(string,lista_tiempos):
  tiempos = list(set(lista_tiempos))# cada tiempo se repite el numero de personas que evacuaron en dicho tiempo
  if len(lista_tiempos) > 0:    
      mean = round(sum(lista_tiempos)/len(lista_tiempos),2)
      var = sum([(t - mean)**2 for t in lista_tiempos])/len(lista_tiempos)
      std = round(var**0.5,2)
  else:
      mean = 0
      var = 0
      std = 0
      
  
  print('Tiempo promedio {} : {}, Desviacion estándar: {}'.format(string,mean,std))
  tiempos.sort()
  evacuados = [lista_tiempos.count(tiempo) for tiempo in tiempos]

  cum = []
  summ = 0
  for tiempo,evac in zip(tiempos,evacuados):
    summ += evac
    cum.append(summ)
  x = tiempos
  y = cum
  plt.plot(x,y)#, bins=intervalos)
  plt.show()
  return mean

import pickle

replicass = [0]#[1,2,3,4,5,6,7,8,9]

for i in replicass: 
    

  C = leer_archivo(name = ['calles_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  B = leer_archivo(name = ['edificios_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  MP = leer_archivo(name = ['mp_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  
  k = leer_archivo(name = ['kids_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  y = leer_archivo(name = ['youngs_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  a = leer_archivo(name = ['adults_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  e = leer_archivo(name = ['elders_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  m = leer_archivo(name = ['mujeres_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  h = leer_archivo(name = ['hombres_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  t = leer_archivo(name = ['total_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  
  x = leer_archivo(name = ['instantes_{}'.format(i)],ps = 'C:/Users/usuario/Desktop/Proyectos CV/Memoria de título/Código/personasprom_flujocalles' )[0]
  
  print('Calculando personas en sistema...')
  def reducir_listas(xx,tt):
      aux = []
      inst = []
      aux.append(tt[0])
      inst.append(xx[0])
      for i,v in enumerate(t[:-1]):
        if t[i+1] != t[i]:
            aux.append(t[i+1])
            inst.append(x[i+1])
        else:
            pass
      return inst,aux 
  
  calcular_personas_sistema(x,t,'total')
  
  calcular_personas_sistema(x,k,'kids')
  calcular_personas_sistema(x,y,'youngs')
  calcular_personas_sistema(x,a,'adults')
  calcular_personas_sistema(x,e,'elders')
  calcular_personas_sistema(x,m,'mujeres')
  calcular_personas_sistema(x,h,'hombres')
  