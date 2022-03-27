# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 01:06:49 2021

@author: usuario
"""
import geopandas as gpd
import numpy as np
import pandas as pd

path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
nodos = gpd.read_file(path2 + 'nodos_con_edificios_total.shp')
#familias_ = gpd.read_file(path2 + 'familias_.shp')
familias_ = gpd.read_file(path2 + 'familias1_.shp')
#MOD_2 = gpd.read_file(path2 + 'MOD_2.shp') 
familias_.rename(columns={'num_person':'num_personas'},inplace=True)
familias_ = familias_[familias_['num_personas']<=10]
#colegios_ = gpd.read_file(path2 + 'colegios_.shp')
colegios_ = gpd.read_file(path2 + 'colegios1_.shp')
colegios_.rename(columns={'num_person':'num_personas'},inplace=True)
#trabajo_ = gpd.read_file(path2 + 'trabajo_.shp')
trabajo_ = gpd.read_file(path2 + 'trabajo1_.shp')
trabajo_.rename(columns={'num_person':'num_personas'},inplace=True)
#otros_ = gpd.read_file(path2 + 'otros_.shp')
otros_ = gpd.read_file(path2 + 'otros1_.shp')
otros_.rename(columns={'num_person':'num_personas'},inplace=True)

'''
#familias_.crs = 'EPSG:5361'
familias_ = familias_.to_crs(nodos.crs)
familias_.to_file(path2 + 'familias_.shp')
#familias__ = familias_[familias_['num_personas']<=10]
#colegios_.crs = 'EPSG:5361'
colegios_ = colegios_.to_crs(nodos.crs)
colegios_.to_file(path2 + 'colegios_.shp')
#trabajo_.crs = 'EPSG:5361'
trabajo_ = trabajo_.to_crs(nodos.crs)
trabajo_.to_file(path2 + 'trabajo_.shp')
#otros_.crs = 'EPSG:5361'
otros_ = otros_.to_crs(nodos.crs)
otros_.to_file(path2 + 'otros_.shp')
'''
#######################################
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
    gdA = gdA.drop(columns = "geometry")
    gdB_nearest = gdB_nearest.drop(columns = ['id', 'nodeId', 'ocupacion', 'depto'])
    #gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf
# una vez filtrados por zona de evacuacion, se asocian a nodos de la red
columns_viviendas = ['INDICES', 'ID_ZONA_LO', 'ID_MANZENT', 'NVIV', 'HOMBRES', 'MUJERES',
       'EDAD_0A5', 'EDAD_6A14', 'EDAD_15A64', 'EDAD_65YMA', 'CASA', 'DEPTO',
       'id_macrozona', 'num_personas', 'is_in', 'seleccion_', 'edificio',
       'geometry', 'ubicacion']

columns_actual= ['INDICES', 'ID_ZONA_LO', 'ID_MANZENT', 'NVIV', 'HOMBRES', 'MUJERES',
       'EDAD_0A5', 'EDAD_6A14', 'EDAD_15A64', 'EDAD_65YMA', 'CASA', 'DEPTO',
       'o_d','o', 'EE', 'num_personas', 'geometry']




gdA = familias_
gdB = nodos
familias = ckdnearest(gdA, gdB) 

gdA = colegios_
gdB = nodos[nodos['depto']!='1'] 
colegios = ckdnearest(gdA, gdB) 

gdA = trabajo_
gdB = nodos[nodos['depto']!='1'] 
trabajo = ckdnearest(gdA, gdB) 

gdA = otros_
gdB = nodos[nodos['depto']!='1'] 
otros = ckdnearest(gdA, gdB) 



# ANTES DE UNIR DATAFRAMES, PRIMERO ASOCIAR A NODOS POR SEPARADO
MOD_final = pd.concat([familias,colegios],axis = 0)
MOD_final = pd.concat([MOD_final,trabajo],axis = 0)
MOD_final = pd.concat([MOD_final,otros],axis = 0)
#MOD_final.to_file(path2 + 'MOD_FINAL_OF1.shp')
MOD_final.to_file(path2 + 'MOD_FINAL_OF1.shp')