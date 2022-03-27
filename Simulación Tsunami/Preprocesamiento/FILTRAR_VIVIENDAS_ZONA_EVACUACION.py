# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:53:14 2021

@author: usuario
"""
import geopandas as gpd

path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

nodos = gpd.read_file('C:/Users/usuario/Desktop/Antofagasta/drive-download-20211006T010518Z-001/Shapefiles/Corrected_Road_Network/Antofa_nodes_cut_edges/sin_edificios/Antofa_nodes.shp')
viviendas = gpd.read_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/viviendas_zonas_antofagasta.shp')
viviendas = viviendas.to_crs(nodos.crs)

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

o = filtrar_puntos_en_zona_(puntos = viviendas, zona = zona_no_segura,num_zona = 2)
o.to_file(path2 + 'viviendas_zona_evacuacion_.shp')
'''
viviendas['ubicacion'] = [(i.x,i.y) for i in viviendas['geometry'].tolist()]
#poblacion = gpd.read_file('/content/drive/MyDrive/MT/Código_simulación/Archivos_oficiales_mt/personas_zonas_antofagasta.shp')
#poblacion.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
viviendas.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
viviendas.rename(columns={'num_person':'num_personas'},inplace=True)
viviendas['id_macrozona'] = [int(i) for i in viviendas['id_macrozona'].tolist()]
'''

