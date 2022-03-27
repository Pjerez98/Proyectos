# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:28:46 2021

@author: usuario
"""

# FILTRAR ESTABLECIMIENTOS EDUCACIONALES Y POBLACION(MOD) POR ZONA DE EVACUACION, Y FILTRAR NODOS POR ZONA ANTOFAGASTA
import geopandas as gpd
import pandas as pd
import numpy as np
#path2 = 'C:/Users/usuario/Desktop/Simulador_basico/codigos_evacuacion/'
path_ = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
#MOD_1 = gpd.read_file('C:/Users/usuario/Desktop/TODO/MOD_1.shp')
MOD_1 = gpd.read_file(path_ + 'MOD_11.shp')
path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

nodos = gpd.read_file('C:/Users/usuario/Desktop/Antofagasta/drive-download-20211006T010518Z-001/Shapefiles/Corrected_Road_Network/Antofa_nodes_cut_edges/sin_edificios/Antofa_nodes.shp')


zona_no_segura = gpd.read_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/zona_no_segura.shp')
zona_no_segura = zona_no_segura.to_crs(nodos.crs)
zona_no_segura = zona_no_segura[zona_no_segura['comuna'] == 'Antofagasta' ]



def filtrar_puntos_en_zona(puntos,zona,num_zona):
    puntos['zona_{}'.format(num_zona)] = puntos.within(zona.iloc[num_zona][-1])
    #puntos = puntos[puntos['is_in']==True]
    return puntos
    #join = gpd.sjoin(puntos,zona, how="left",op = 'within')
    #return join

def filtrar_puntos_en_zona_(puntos,zona,num_zona = 2):
    puntos['is_in'] = puntos.within(zona.iloc[num_zona][-1])
    puntos = puntos[puntos['is_in']==True]
    return puntos
    #join = gpd.sjoin(puntos,zona, how="left",op = 'within')
    #return join
#def filtar_puntos_en_zona(puntos,zona):
#    join = gpd.sjoin(puntos,zona)
#   return join






o = filtrar_puntos_en_zona_(puntos = MOD_1, zona = zona_no_segura,num_zona = 2)
#o.to_file(path2 + 'MOD_1_.shp')
o.to_file(path2 + 'MOD_11_.shp')