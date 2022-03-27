# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 00:21:01 2021

@author: usuario
"""

import geopandas as gpd
import pandas as pd
path2 = 'C:/Users/usuario/Desktop/CODIGO_OFICIAL/Archivos_oficiales_mt/Archivos_oficiales_mt/'
#MOD_1 = gpd.read_file(path2 + 'MOD_1_.shp' )
#MOD_2 = gpd.read_file(path2 + 'MOD_2.shp') # personas o_d == False que se agruparon en familias,
MOD_1 = gpd.read_file(path2 + 'MOD_11_.shp' )
MOD_2 = gpd.read_file(path2 + 'MOD_21.shp')

nodos = gpd.read_file(path2 + 'nodos_con_edificios_total.shp')
#sin asignar a nodos

# MOD_2 corresponde a la población que no se ha movido

MOD_od = MOD_1[MOD_1['o_d']!='0']
MOD_od.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)
MOD_no_od = MOD_2

######################################################################
MOD_colegios = gpd.read_file(path2 + 'MOD_colegios1.shp') # falta agrupar colegios, y modificar filas de trabajo y otros
MOD_colegios.rename(columns={'id_macrozo':'id_macrozona'},inplace=True)

# FALTA AGRUPAR COLEGIOS

columns = ['INDICES', 'ID_ZONA_LO', 'ID_MANZENT', 'NVIV', 'HOMBRES', 'MUJERES',
       'EDAD_0A5', 'EDAD_6A14', 'EDAD_15A64', 'EDAD_65YMA', 'CASA', 'DEPTO','o_d','o',
       'EE','num_personas', 'geometry']
df_2= pd.DataFrame(columns = columns[:-1] )
gdf_2 = gpd.GeoDataFrame( df_2)


colegios = MOD_colegios[MOD_colegios['o_d']=='estudio']




def agrupar_personas(familias = colegios,filtro = 'EE'):
    
  count = 0
  for key,grouped in familias.groupby(filtro):
    
    personas = familias[familias[filtro]==key]

    #INDICES	ID_ZONA_LO	ID_MANZENT	NVIV	HOMBRES	MUJERES	EDAD_0A5	EDAD_6A14	EDAD_15A64	EDAD_65YMA	CASA	DEPTO	geometry
    indices = personas.iloc[0,:].INDICES
    
    
    id_zona = [personas.iloc[0,:].ID_ZONA_LO]
    id_manzent = None
    nviv = [personas.iloc[0,:].NVIV]
    hombres = personas['SEXO'].tolist().count(1)
    mujeres = personas['SEXO'].tolist().count(2)
    edad_0a5 = [len([i for i in personas['EDAD'].tolist() if i <= 5])]
    edad_6a14 = [len([i for i in personas['EDAD'].tolist() if (i > 5) & (i<=15)])]
    edad_15a64 = [len([i for i in personas['EDAD'].tolist() if(i > 15) & (i<=65)])]
    edad_65ymas = [len([i for i in personas['EDAD'].tolist() if i > 65])]
    
    casa = 0
    depto = 0
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
 
    num_personas = hombres + mujeres
    new_id = [personas.iloc[0,:].new_id]
    geometry = personas.iloc[0,:].geometry # verificado que es el mismo para cada persona con el mismo nviv, el cual fue reseteado para que sea único, para cada familia.

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
  return familias_

H_MOD_ = MOD_colegios
colegios_ = agrupar_personas(familias = colegios, filtro = 'EE')
familias_ = MOD_2
#familias_ = agrupar_personas(familias = familias, filtro = 'NVIV')
trabajo = H_MOD_[(H_MOD_['o_d'] == 'trabajo')]
trabajo = trabajo.reset_index(drop=False)
trabajo_ = agrupar_personas(familias = trabajo,filtro = 'index' )
otros = H_MOD_[(H_MOD_['o_d'] == 'otros')]
otros = otros.reset_index(drop=False)
otros_ =  agrupar_personas(familias = otros,filtro = 'index' )

familias_.crs = 'EPSG:5361'
familias_ = familias_.to_crs(nodos.crs)
#familias_.to_file(path2 + 'familias_.shp')
familias_.to_file(path2 + 'familias1_.shp')
colegios_.crs = 'EPSG:5361'
colegios_ = colegios_.to_crs(nodos.crs)
#colegios_.to_file(path2 + 'colegios_.shp')
colegios_.to_file(path2 + 'colegios1_.shp')
trabajo_.crs = 'EPSG:5361'
trabajo_ = trabajo_.to_crs(nodos.crs)
#trabajo_.to_file(path2 + 'trabajo_.shp')
trabajo_.to_file(path2 + 'trabajo1_.shp')
otros_.crs = 'EPSG:5361'
otros_ = otros_.to_crs(nodos.crs)
#otros_.to_file(path2 + 'otros_.shp')
otros_.to_file(path2 + 'otros1_.shp')


'''
MOD_final = pd.concat([familias_,colegios_],axis = 0)
MOD_final = pd.concat([MOD_final,trabajo_],axis = 0)
MOD_final = pd.concat([MOD_final,otros_],axis = 0)
'''