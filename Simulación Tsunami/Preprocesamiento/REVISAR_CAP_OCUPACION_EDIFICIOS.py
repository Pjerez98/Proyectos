#REVISAR CAPACIDADES EDIFICIOS

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 03:11:03 2021

@author: usuario
"""
import geopandas as gpd
import numpy as np
import pandas as pd
path_ = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
###################################################
# Households to evacuate
#Poblacion sintetica: hogares a evacuar --> filtrar con zona segura y con mujeres y hombres>0 (sacar viviendas vacías). LISTO
#H = gpd.read_file('/content/drive/MyDrive/MT/Código_simulación/drive-download-20211006T010518Z-001/Shapefiles/Tsunami/viviendas_zona_evacuacion.shp')
viviendas_zona_evacuacion = gpd.read_file(path_ + 'viviendas_zona_evacuacion.shp')
viviendas_zona_evacuacion['ubicacion'] = [(i.x,i.y) for i in viviendas_zona_evacuacion['geometry'].tolist()]
viviendas_zona_evacuacion.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
viviendas_zona_evacuacion.rename(columns={'num_person':'num_personas'},inplace=True)
viviendas_zona_evacuacion['id_macrozona'] = [int(i) for i in viviendas_zona_evacuacion['id_macrozona'].tolist()]
viviendas_zona_evacuacion = viviendas_zona_evacuacion[viviendas_zona_evacuacion['num_personas']>0]
for i in viviendas_zona_evacuacion.index.tolist():
  #print(viviendas_zona_evacuacion.loc[i,'num_personas'])
  if viviendas_zona_evacuacion.loc[i,'num_personas']>10:
    viviendas_zona_evacuacion = viviendas_zona_evacuacion.drop([i],axis=0)
#####################


buildings = gpd.read_file(path2 + 'edificios_zona_evacuacion_total.shp')
#buildings = gpd.read_file('/content/drive/MyDrive/MT/Código_simulación/Archivos_oficiales_mt/edificios_zona_evacuacion_total.shp')
buildings.rename(columns={'available_':'available_capacity'},inplace = True)
buildings['available_capacity'] = [int(int(i)*1.3) - int(j) for i,j in zip(buildings['ocupacion'].tolist(),buildings['16_aleat'].tolist())]
buildings['available_capacity'] = [int(i) if int(i)>=int(j) else int(j) for i,j in zip(buildings['available_capacity'].tolist(),buildings['ocupacion'].tolist())]
buildings['ubicacion'] = [(i.x,i.y) for i in buildings['geometry'].tolist()]
B = buildings


import shapely
from scipy.spatial import cKDTree
from shapely.geometry import Point

punto = shapely.geometry.point.Point
multipunto = shapely.geometry.multipoint.MultiPoint

def ckdnearest(gdA, gdB):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y) if type(x) == punto else (x[0].x, x[0].y) )))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].reset_index(drop=True)
    #gdA 
    gdB_nearest = gdB_nearest.drop(columns = ['available_capacity', 'ocupacion', 'num_dep', '16_aleat',
       'is_in', 'new_id', 'geometry', 'ubicacion'])
    #gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdA = gdA.drop(columns = ['edificio'])
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

gdA = viviendas_zona_evacuacion[viviendas_zona_evacuacion['DEPTO']==1]
gdB = B
ED_ = ckdnearest(gdA, gdB) 

capacidad_final = 0
ocupacion_final = 0
for key,grouped in ED_.groupby('edificio'):
    cap_ed = B[B['edificio']==key].available_capacity.tolist()[0]
    pos1 = B[B['edificio']==key].ubicacion.tolist()[0]
    pos2 = grouped.ubicacion.tolist()[0]
    ocupacion = sum(grouped.num_personas.tolist())
    #if (cap_ed<ocupacion ) == True:
    #if pos1 == pos2 :
    #    print(pos1,pos2)
    capacidad_final += cap_ed
    ocupacion_final += ocupacion
    #if cap_ed<ocupacion:
    #print(cap_ed,ocupacion, pos1,pos2,key)

print(ocupacion_final/capacidad_final,(capacidad_final - ocupacion_final)/ sum(viviendas_zona_evacuacion[viviendas_zona_evacuacion['DEPTO']==0].num_personas.tolist()))
    