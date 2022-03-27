# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 23:59:58 2021

@author: usuario
"""
import geopandas as gpd
#MOD_1 = gpd.read_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/MOD_1_.shp')
MOD_1 = gpd.read_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/MOD_11_.shp')
path = "/content/drive/MyDrive/MT/Código_simulación/Simulador_basico/shapefiles_codigo_oficial/"
path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'

nodos = gpd.read_file('C:/Users/usuario/Desktop/Antofagasta/drive-download-20211006T010518Z-001/Shapefiles/Corrected_Road_Network/Antofa_nodes_cut_edges/sin_edificios/Antofa_nodes.shp')
#calles = gpd.read_file('C:/Users/usuario/Desktop/Antofagasta/drive-download-20211006T010518Z-001/Shapefiles/Corrected_Road_Network/Antofa_nodes_cut_edges/sin_edificios/Antofa_edges.shp')
#zonas = zonas = gpd.read_file(path2 + 'macrozonas.shp' )
#zonas = zonas.to_crs(nodos.crs)

viviendas_zona_evacuacion = gpd.read_file(path2 + 'viviendas_zona_evacuacion_.shp')
viviendas_zona_evacuacion['ubicacion'] = [(i.x,i.y) for i in viviendas_zona_evacuacion['geometry'].tolist()]
viviendas_zona_evacuacion.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
viviendas_zona_evacuacion.rename(columns={'num_person':'num_personas'},inplace=True)
viviendas_zona_evacuacion['id_macrozona'] = [int(i) for i in viviendas_zona_evacuacion['id_macrozona'].tolist()]
viviendas_zona_evacuacion = viviendas_zona_evacuacion[viviendas_zona_evacuacion['num_personas']>0]

viviendas_zona_evacuacion_final = gpd.read_file(path2 + 'viviendas_zona_evacuacion.shp')
viviendas_zona_evacuacion_final['ubicacion'] = [(i.x,i.y) for i in viviendas_zona_evacuacion_final['geometry'].tolist()]
viviendas_zona_evacuacion_final.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
viviendas_zona_evacuacion_final.rename(columns={'num_person':'num_personas'},inplace=True)
viviendas_zona_evacuacion_final['id_macrozona'] = [int(i) for i in viviendas_zona_evacuacion_final['id_macrozona'].tolist()]
viviendas_zona_evacuacion_final = viviendas_zona_evacuacion_final[viviendas_zona_evacuacion_final['num_personas']>0]
#viviendas_zona_evacuacion_final = viviendas_zona_evacuacion_final[viviendas_zona_evacuacion_final['DEPTO']!=1]
_INDICES = list(set(viviendas_zona_evacuacion_final.INDICES.tolist()))
viviendas_zona_evacuacion = viviendas_zona_evacuacion[viviendas_zona_evacuacion.INDICES.isin(_INDICES)]
zona_no_segura = gpd.read_file('C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/zona_no_segura.shp')
zona_no_segura = zona_no_segura.to_crs(nodos.crs)
zona_no_segura = zona_no_segura[zona_no_segura['comuna'] == 'Antofagasta' ]
#poblacion['id_macrozona'] = [int(i) for i in poblacion['id_macrozona'].tolist()]
print(viviendas_zona_evacuacion_final.shape[0],viviendas_zona_evacuacion.shape[0])
print(MOD_1.crs==viviendas_zona_evacuacion.crs, MOD_1.crs == nodos.crs)

# HACER MATCH VIVIENDAS ORIGINAL CON MOD_1 (SOLO PARA O_D == FALSE)
print(MOD_1.groupby(['o_d']).size())

import pandas as pd
from shapely.geometry import Point
import shapely
from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString
import numpy as np

def ckdnearest(gdA, gdB):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].reset_index(drop=True)
    gdA = gdA.drop(columns=['geometry','INDICES','ID_ZONA_LO','id_macrozo','is_in'])
    gdB_nearest = gdB_nearest.drop(columns=['NVIV'])
    #gdB_nearest = gdB.iloc[idx].drop(columns=['geometry']).reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

# HACER MATCH DE PERSONAS QUE NO SE HAN MOVIDO, CON VIVIENDAS
gdA = MOD_1[(MOD_1['o_d']=='0') ]
gdB = viviendas_zona_evacuacion
MOD_= ckdnearest(gdA, gdB)
MOD_ = MOD_[MOD_['num_personas']<=10]
print(MOD_.columns)
MOD_ = MOD_.drop(['ubicacion'],axis=1)
MOD_.to_file(path2 + 'MOD_match.shp')
print(MOD_.columns)

# 1. CREAR FAMILIAS PARA CASOS O_D == 0
columns = ['INDICES', 'ID_ZONA_LO', 'ID_MANZENT', 'NVIV', 'HOMBRES', 'MUJERES',
       'EDAD_0A5', 'EDAD_6A14', 'EDAD_15A64', 'EDAD_65YMA', 'CASA', 'DEPTO','o_d','o',
       'EE','num_personas', 'geometry']
df = pd.DataFrame(columns = columns[:-1] )
gdf = gpd.GeoDataFrame( df)

geometryy = ['None' for i in range(viviendas_zona_evacuacion.shape[0])] # ir asignando ubicacion,
#en caso de ser edifcio, hacer match con viviendas_zona_evacuacion_final para
# obtener geometria del edificio
vv = MOD_
vv_final = viviendas_zona_evacuacion_final

def agrupar_personas(familias = vv,filtro = 'ID_MANZENT'):
  count = 0
  lolo = 0
  for key,grouped in familias.groupby(filtro):
    
    personas_ = familias[familias[filtro]==key]
    ff_ = vv_final[vv_final[filtro]==key] 
    
    #is_in_depto = [True if i == 1 else False for i in ff.DEPTO.tolist() ][0]
    
   
    for key_,grouped_ in personas_.groupby('NVIV'):
        
        personas = personas_[personas_['NVIV']==key_]
        ff = ff_[ff_['NVIV']==key_] # PARA ASOCIAR GEOMETRIA CORRECTA, EN EL CASO DE EDFICIOS
        if ff.empty:
            if personas.DEPTO.tolist()[0] == 1:
                casa = 0
                depto = 1
                geometry = ff_[ff_['INDICES'] == personas.INDICES.tolist()[0]].geometry.tolist()[0]
              
            else:
                casa = 1
                depto = 0
                geometry = personas.geometry.tolist()[0]
        else:
            if personas.DEPTO.tolist()[0] == 1:
                casa = 0
                depto = 1
            else:
                casa = 1
                depto = 0
            geometry = ff.geometry.tolist()[0]
            
        #INDICES	ID_ZONA_LO	ID_MANZENT	NVIV	HOMBRES	MUJERES	EDAD_0A5	EDAD_6A14	EDAD_15A64	EDAD_65YMA	CASA	DEPTO	geometry
        indices = personas.iloc[0,:].INDICES
        
        
        id_zona = [personas.iloc[0,:].ID_ZONA_LO]
        id_manzent = key#ff.ID_MANZENT.tolist()[0]
        nviv = [personas.iloc[0,:].NVIV]
        hombres = personas['SEXO'].tolist().count(1)
        mujeres = personas['SEXO'].tolist().count(2)
        edad_0a5 = [len([i for i in personas['EDAD'].tolist() if i <= 5])]
        edad_6a14 = [len([i for i in personas['EDAD'].tolist() if (i > 5) & (i<=15)])]
        edad_15a64 = [len([i for i in personas['EDAD'].tolist() if(i > 15) & (i<=65)])]
        edad_65ymas = [len([i for i in personas['EDAD'].tolist() if i > 65])]
        
        
        
        
        if filtro == 'EE':
          o_d = 'estudio'
          ee = [personas.iloc[0,:].EE]
          o = '12'
        elif filtro == 'index':
          o_d = personas.o_d.tolist()[0]
          #o_d = 'trabajo'
          ee = None
          o = personas.o.tolist()[0]
        
        else:
          o = personas.o.tolist()[0] 
          o_d = False
          ee = None
        
        #new_id = [personas.iloc[0,:].new_id]
        
        #geometry = personas.iloc[0,:].geometry # verificado que es el mismo para cada persona con el mismo nviv, el cual fue reseteado para que sea único, para cada familia.
        
        
        num_personas = hombres + mujeres
       
        if num_personas>10:
            print(key_,num_personas)
            #print(num_personas,geometry.x,geometry.y,ff.DEPTO.tolist()[0])
            lolo +=1
            
        columnas = [indices,id_zona,id_manzent,nviv,hombres,mujeres,edad_0a5,edad_6a14,edad_15a64,edad_65ymas,casa,depto,o_d,o,ee,num_personas,geometry]
        #print(len(columnas),len(columns)) 
        #print(columnas)
        df = pd.DataFrame({i:j for i,j in zip(columns[:-1],columnas[:-1])})
        
        gdf = gpd.GeoDataFrame( df, geometry=[columnas[-1]])
        #if o == 12 and d == 2:
        #  print(gdf.shape[0])
        if count == 0:
          familias_ = gdf
        else:
          familias_ = pd.concat([familias_,gdf],axis = 0)
        count += 1
  familias_ = familias_.reset_index(drop=True)
  print(lolo)
  return familias_

MOD_2 = agrupar_personas(familias = vv, filtro = 'ID_MANZENT')
MOD_2.crs = 'EPSG:5361'
MOD_2 = MOD_2.to_crs(nodos.crs)
#MOD_2.to_file(path2 + 'MOD_2.shp')
MOD_2.to_file(path2 + 'MOD_21.shp')



# MOD_2 corresponde a la población que no se ha movido

MOD_od = MOD_1[MOD_1['o_d']!='0']
MOD_no_od = MOD_2

# FALTA AGRUPAR COLEGIOS

columns = ['INDICES', 'ID_ZONA_LO', 'ID_MANZENT', 'NVIV', 'HOMBRES', 'MUJERES',
       'EDAD_0A5', 'EDAD_6A14', 'EDAD_15A64', 'EDAD_65YMA', 'CASA', 'DEPTO','o_d',
       'EE','num_personas', 'geometry']
df_2= pd.DataFrame(columns = columns[:-1] )
gdf_2 = gpd.GeoDataFrame( df_2)


colegios = MOD_od[MOD_od['o_d']=='estudio']



# MOVER PERSONAS QUE VIVEN EN DEPARTAMENTOS, A EDIFICIOS CORRESPONDIENTES.
# HACER MATCH CON VIVIENDAS_ZONA_EVACUACION PARA ESO

#for i in viviendas_zona_evacuacion.index.tolist():
  #print(viviendas_zona_evacuacion.loc[i,'num_personas'])
#  if viviendas_zona_evacuacion.loc[i,'num_personas']>10:
#    viviendas_zona_evacuacion = viviendas_zona_evacuacion.drop([i],axis=0)

# HACER MATCH CON VIVIENDAS ZONA EVACUACION, PARA O_D == 0 Y DEPTO == 0
# MOD_PERSONAS_NO_DEPTO = MOD_[MOD_['DEPTO']==0]



# CREAR FAMILIAS EN BASE A MATCH CON VIVIENDAS



# MOVER PERSONAS QUE VIVEN EN DEPARTAMENTOS, A EDIFICIOS CORRESPONDIENTES.
# HACER MATCH CON VIVIENDAS_ZONA_EVACUACION PARA ESO.

#MOD_PERSONAS_DEPTO = MOD_[MOD_['DEPTO']==1] # MODIFICAR GEOMETRIA EN ESTOS CASOS, AL EDIFICIO DE VIVIENDAS_ZONA_EVACUACION
#gdA = MOD_PERSONAS_DEPTO
#gdB = viviendas_zona_evacuacion 
#MOD_3= ckdnearest(gdA, gdB)
#print(MOD_3.columns)


