
"""
Created on Tue Jan  4 13:10:30 2022

@author: usuario
"""
# ESTE CÓDIGO CORRESPONDE AL SIMULADOR ESCENARIO NOCHE PARA EVACUACIÓN TSUNAMI ANTOFAGASTA\\
# BASADO EN POBLACIÓN
# -*- coding: utf-8 -*-

################# PREPROCESAMIENTO #######################################################################33
import geopandas as gpd
import numpy as np
import pandas as pd
path_ = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

pppp = 'MOD_'
MOD_final_ = gpd.read_file(path_ +  'MOD_final_OF.shp')
MOD_final_['o_d'] =[False if i == '0' else i for i in MOD_final_['o_d'].tolist()]
'''
path = "/content/drive/MyDrive/MT/Código_simulación/Simulador_basico/shapefiles_codigo_oficial/"
nodos = gpd.read_file(path + 'Antofa_nodes_of.shp')
calles = gpd.read_file(path + 'Antofa_edges_of.shp')
'''
nodos = gpd.read_file(path_ + 'nodos_con_edificios_total.shp')
#nodos = gpd.read_file('/content/drive/MyDrive/MT/Código_simulación/Archivos_oficiales_mt/nodos_con_edificios_total.shp')
calles = gpd.read_file(path_ + 'edges_con_edificios_total.shp')
#calles = gpd.read_file('/content/drive/MyDrive/MT/Código_simulación/Archivos_oficiales_mt/edges_con_edificios_total.shp')
#print('CALLES ANTES: ',calles.shape[0])
#calles = calles[(calles['new_id']!=11858) ]
#print('CALLES DESPUES: ',calles.shape[0])
#from shapely.geometry import Point, LineString
#P1 = nodos[nodos['new_id']=='3539'].geometry.tolist()[0]
#P2 = nodos[nodos['new_id']=='4802'].geometry.tolist()[0]
#nueva_linea = LineString([P1,P2])
#calles=calles.append({'u' : 'u' , 'v' : 'v', 'new_u' : 3539,'new_v' : 4802,'new_id':calles.shape[0] ,'geometry' :nueva_linea ,'id' : 'id','backRefere' : 'u','forwardRef' : 'v'} , ignore_index=True)
nodos['depto'] = [int(i) if i == '1' else i for i in nodos['depto'].tolist()]
#print('CALLES DESPUES 2: ',calles.shape[0])

#ADD reverse streets
calles_reverse = calles.copy()

from shapely.geometry import Point, LineString
columns = ['u','v','new_u','new_v','new_id','geometry','id','backRefere','forwardRef']
reverse_columns = ['v','u','new_v','new_u',None,None,None,'forwardRef','backRefere']
for column,reverse in zip(columns,reverse_columns):
  if column == 'new_id':
    calles_reverse[column] = [i for i in range(calles.shape[0], 2*calles.shape[0])]
  elif column == 'geometry':
    calles_reverse[column] = [LineString([Point(list(line.coords)[::-1][0]),Point(list(line.coords)[::-1][1])])  for line in calles_reverse[column].tolist()] 
  elif column == 'id':
    calles_reverse[column] = ['reverse_{}'.format(i) for i in range(calles.shape[0], 2*calles.shape[0])]
  else:
    calles_reverse[column] = calles[reverse].tolist()
    
calles = pd.concat([calles,calles_reverse],axis= 0)
calles['width'] = [4 if calle == 'residential' else 8 if calle == 'primary' else 2 for calle in calles['highway'].tolist()] 



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

escenarios = [1,2,4,5]
for e in [1,2,4,5]:
    nombre = 'scenario_{}_{}_{}'.format(e,1,'flujocalles_con_ids_total')
    pathhh = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Estadisticas'
    valor_estadistica = leer_archivo(name = [nombre],ps = pathhh )[0] 
    #crear diccionario new_ids : flujo
    dict_flujos = {}
    new_ids_in_dict = []
    for a,b,c in valor_estadistica:
        dict_flujos[b] = c
        new_ids_in_dict.append(b)
    
    calles['flujo'] = [dict_flujos[new_id] if new_ids_in_dict.count(new_id)>0 else 0  for new_id in calles.new_id.tolist()]
    calles.to_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt//Archivos_oficiales_mt/calles_con_flujos_{}.shp'.format(e))