# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 20:51:00 2021

@author: usuario
"""
import geopandas as gpd
import pandas as pd
path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
#MOD_1 = gpd.read_file(path2 + 'MOD_1_.shp' )
#MOD_2 = gpd.read_file(path2 + 'MOD_2.shp')
MOD_1 = gpd.read_file(path2 + 'MOD_11_.shp' )
MOD_2 = gpd.read_file(path2 + 'MOD_21.shp')

# MOD_2 corresponde a la población que no se ha movido

MOD_od = MOD_1[MOD_1['o_d']!='0']
MOD_od.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
MOD_no_od = MOD_2

##################################
# FILTRAR ESTABLECIMIENTOS EDUCACIONALES Y POBLACION(MOD) POR ZONA DE EVACUACION, Y FILTRAR NODOS POR ZONA ANTOFAGASTA
import geopandas as gpd
import pandas as pd
import numpy as np
#path2 = 'C:/Users/usuario/Desktop/Simulador_basico/codigos_evacuacion/'

nodos = gpd.read_file(path2 + 'nodos_con_edificios_total.shp')
MOD_od = MOD_od.to_crs(nodos.crs)
MOD_no_od = MOD_no_od.to_crs(nodos.crs)
#nodos.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
# Hay que filtrar colegios, por zona de evacuación
establecimientos_educacionales = gpd.read_file(path2 + 'colegios_zona_evacuacion.shp')
establecimientos_educacionales = establecimientos_educacionales.to_crs(nodos.crs)

##################################
# ASOCIAR NODOS A ESTABLECIMIENTOS Y PERSONAS MOD
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
gdA = MOD_od
gdB = nodos[nodos['depto']!='1'] 
MOD_od_2 = ckdnearest(gdA, gdB) # Asignacion solo aplica a personas o_d == False, los otros, el punto corresponde al origen y no al destino, por lo que se tiene que asignar dps
gdA = establecimientos_educacionales
gdB = nodos[nodos['depto']!='1'] # Descarto que se asocie directamente a un nodo edificio.
#EE_ = ckdnearest(gdA, gdB)
EE_ = establecimientos_educacionales
MOD_od_2.to_file(path2 + 'MOD_od_2.shp')
print('STOP')

##################################
# ASIGNAR COLEGIOS A POBLACION, RESPETANDO CAPACIDADES
import random
H_MOD = MOD_od_2
H_MOD_ =  H_MOD.copy(deep = True)
H_MOD_['EE'] = None
zonas_ee = list(set(EE_['ZONA'].tolist()))
num_ee_x_zona = EE_.groupby(['ZONA']).size().tolist()
capacidades_establecimientos = {int(zona):{i:EE_.iloc[i,:].MAT_TOTAL for i in EE_[EE_['ZONA'] == zona].index.tolist() if EE_.iloc[i,:].MAT_TOTAL>0 } for zona in zonas_ee} 
estado_establecimientos = {int(index_zona):{i:0 for i in capacidades_establecimientos[int(index_zona)]} for index_zona in zonas_ee }
indices_ee = {int(index_zona) :[i for i in capacidades_establecimientos[int(index_zona)]] for index_zona in zonas_ee}
random.seed(1)
columna_ee = []
columna_new_id = []
for i in H_MOD_.index.tolist():#.shape[0]):
  flag = False
  estudiante = H_MOD_.loc[i,H_MOD_.columns]
  index_zona = int(estudiante.id_macrozona) - 1
  if zonas_ee.count(index_zona) != 1:
    index_zona = 1
    flag == True

  if estudiante.o_d == 'estudio' and len(indices_ee[index_zona])>0 and flag == False:
    
    #Asignar colegio según capacidad establecimientos
    
    index_ee =  random.choice(indices_ee[index_zona])
    
    # Preguntar por capacidad colegio
    while estado_establecimientos[index_zona][index_ee] == capacidades_establecimientos[index_zona][index_ee]:
      # Eliminar establecimiento
      del estado_establecimientos[index_zona][index_ee]
      del capacidades_establecimientos[index_zona][index_ee]
      indices_ee[index_zona].remove(index_ee)
      if len(indices_ee[index_zona]) == 0:
        break
      else:
        index_ee =  random.choice(indices_ee[index_zona])
      
    if len(indices_ee[index_zona]) > 0:
      EE_.iloc[index_ee,:].new_id
      H_MOD_.loc[i,'new_id'] = EE_.iloc[index_ee,:].new_id
      H_MOD_.loc[i,'EE'] = EE_.iloc[index_ee,:].NOMBRE_RBD
      H_MOD_.loc[i,'geometry'] = EE_.iloc[index_ee,:].geometry
      #columna_new_id.append(EE_.iloc[index_ee,:].new_id)
      #columna_ee.append(EE_.iloc[index_ee,:].NOMBRE_RBD)
      #print(H_MOD_.iloc[i,:].EE )
      #Actualizar capacidad establecimiento
      estado_establecimientos[index_zona][index_ee] += 1
    else:
      #columna_new_id.append(None)
      #columna_ee.append(None)
      pass
    
  else:
    #columna_new_id.append(None)
    #columna_ee.append(None)
    pass
#H_MOD_['new_id'] = columna_new_id
#H_MOD_['EE'] = columna_ee

#H_MOD_.to_file(path2 + 'MOD_colegios.shp')
H_MOD_.to_file(path2 + 'MOD_colegios1.shp')

##################################
