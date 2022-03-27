# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 03:11:03 2021

@author: usuario
"""
import geopandas as gpd
import numpy as np
import pandas as pd

path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
#MOD_final= gpd.read_file(path2 + 'MOD_FINAL_OF.shp')
MOD_final= gpd.read_file(path2 + 'MOD_FINAL_OF1.shp')
MOD_final['ubicacion'] = [(i.x,i.y) for i in MOD_final['geometry'].tolist()]
ED = MOD_final[MOD_final['DEPTO']==1]


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
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

gdA = ED
gdB = B
ED_ = ckdnearest(gdA, gdB) 

for key,grouped in ED_.groupby('edificio'):
    cap_ed = B[B['edificio']==key].available_capacity.tolist()[0]
    pos1 = B[B['edificio']==key].ubicacion.tolist()[0]
    pos2 = grouped.ubicacion.tolist()[0]
    ocupacion = sum(grouped.num_person.tolist())
    if (cap_ed<ocupacion ) == True:
    #if cap_ed<ocupacion:
        print(cap_ed,ocupacion, pos1,pos2,key)
    